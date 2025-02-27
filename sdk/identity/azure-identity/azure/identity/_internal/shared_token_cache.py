# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import abc
import platform
import time
from typing import Any, Iterable, List, Mapping, Optional, cast, Dict
from urllib.parse import urlparse
import msal

from azure.core.credentials import AccessTokenInfo
from .. import CredentialUnavailableError
from .._constants import KnownAuthorities
from .._internal import get_default_authority, normalize_authority, wrap_exceptions
from .._persistent_cache import _load_persistent_cache, TokenCachePersistenceOptions
from .._internal import AadClientBase

ABC = abc.ABC
CacheItem = Mapping[str, str]

MULTIPLE_ACCOUNTS = """SharedTokenCacheCredential authentication unavailable. Multiple accounts
were found in the cache. Use username and tenant id to disambiguate."""

MULTIPLE_MATCHING_ACCOUNTS = """SharedTokenCacheCredential authentication unavailable. Multiple accounts
matching the specified{}{} were found in the cache."""

NO_ACCOUNTS = """SharedTokenCacheCredential authentication unavailable. No accounts were found in the cache."""

NO_MATCHING_ACCOUNTS = """SharedTokenCacheCredential authentication unavailable. No account
matching the specified{}{} was found in the cache."""

NO_TOKEN = """Token acquisition failed for user '{}'. To fix, re-authenticate
through developer tooling supporting Azure single sign on"""

# build a dictionary {authority: {its known aliases}}, aliases taken from MSAL.NET's KnownMetadataProvider
KNOWN_ALIASES = {
    alias: aliases  # N.B. aliases includes alias itself
    for aliases in (
        frozenset((KnownAuthorities.AZURE_CHINA, "login.partner.microsoftonline.cn")),
        frozenset((KnownAuthorities.AZURE_PUBLIC_CLOUD, "login.windows.net", "login.microsoft.com", "sts.windows.net")),
        frozenset((KnownAuthorities.AZURE_GOVERNMENT, "login.usgovcloudapi.net")),
    )
    for alias in aliases
}


def _account_to_string(account):
    username = account.get("username")
    home_account_id = account.get("home_account_id", "").split(".")
    tenant_id = home_account_id[-1] if len(home_account_id) == 2 else ""
    return "(username: {}, tenant: {})".format(username, tenant_id)


def _filtered_accounts(
    accounts: Iterable[CacheItem], username: Optional[str] = None, tenant_id: Optional[str] = None
) -> List[CacheItem]:
    """Return accounts matching username and/or tenant_id.

    :param accounts: accounts from the MSAL cache
    :type accounts: Iterable[CacheItem]
    :param str username: an account's username
    :param str tenant_id: an account's tenant ID
    :return: accounts matching username and/or tenant_id
    :rtype: list[CacheItem]
    """

    filtered_accounts = []
    for account in accounts:
        if username and account.get("username") != username:
            continue
        if tenant_id:
            try:
                _, tenant = account["home_account_id"].split(".")
                if tenant_id != tenant:
                    continue
            except Exception:  # pylint:disable=broad-except
                continue
        filtered_accounts.append(account)
    return filtered_accounts


class SharedTokenCacheBase(ABC):  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        username: Optional[str] = None,
        *,
        authority: Optional[str] = None,
        tenant_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        self._authority = normalize_authority(authority) if authority else get_default_authority()
        environment = urlparse(self._authority).netloc
        self._environment_aliases = KNOWN_ALIASES.get(environment) or frozenset((environment,))
        self._username = username
        self._tenant_id = tenant_id
        self._cache = kwargs.pop("_cache", None)
        self._cae_cache = kwargs.pop("_cae_cache", None)
        if self._cache or self._cae_cache:
            self._custom_cache = True
        else:
            self._custom_cache = False
        self._cache_persistence_options = kwargs.pop("cache_persistence_options", None)
        self._client_kwargs = kwargs
        self._client_kwargs["tenant_id"] = "organizations"
        self._client = cast(AadClientBase, None)
        self._client_initialized = False

    def _initialize_client(self) -> None:
        if self._client_initialized:
            return

        self._client = self._get_auth_client(
            authority=self._authority, cache=self._cache, cae_cache=self._cae_cache, **self._client_kwargs
        )
        self._client_initialized = True

    def _initialize_cache(self, is_cae: bool = False) -> Optional[msal.TokenCache]:

        # If no cache options were provided, the default cache will be used. This credential accepts the
        # user's default cache regardless of whether it's encrypted. It doesn't create a new cache. If the
        # default cache exists, the user must have created it earlier. If it's unencrypted, the user must
        # have allowed that.
        cache_options = self._cache_persistence_options or TokenCachePersistenceOptions(allow_unencrypted_storage=True)
        if not self.supported():
            raise CredentialUnavailableError(message="Shared token cache is not supported on this platform.")

        if not self._cache and not is_cae:
            try:
                self._cache = _load_persistent_cache(cache_options, is_cae)
                self._client._cache = self._cache  # pylint:disable=protected-access
            except Exception:  # pylint:disable=broad-except
                return None

        if not self._cae_cache and is_cae:
            try:
                self._cae_cache = _load_persistent_cache(cache_options, is_cae)
                self._client._cae_cache = self._cae_cache  # pylint:disable=protected-access
            except Exception:  # pylint:disable=broad-except
                return None

        return self._cae_cache if is_cae else self._cache

    @abc.abstractmethod
    def _get_auth_client(self, **kwargs) -> AadClientBase:
        pass

    def _get_cache_items_for_authority(
        self, credential_type: msal.TokenCache.CredentialType, is_cae: bool = False
    ) -> List[CacheItem]:
        """Return cache items matching this credential's authority or one of its aliases.

        :param credential_type: the type of credential to look for in the cache
        :param bool is_cae: whether to look in the CAE cache
        :type credential_type: msal.TokenCache.CredentialType
        :return: a list of cache items
        :rtype: list[CacheItem]
        """

        cache = cast(msal.TokenCache, self._cae_cache if is_cae else self._cache)
        items = []
        for item in cache.search(credential_type):
            environment = item.get("environment")
            if environment in self._environment_aliases:
                items.append(item)
        return items

    def _get_accounts_having_matching_refresh_tokens(self, is_cae: bool = False) -> Iterable[CacheItem]:
        """Returns an iterable of cached accounts which have a matching refresh token.

        :param bool is_cae: whether to look in the CAE cache
        :return: an iterable of cached accounts
        :rtype: Iterable[CacheItem]
        """

        refresh_tokens = self._get_cache_items_for_authority(msal.TokenCache.CredentialType.REFRESH_TOKEN, is_cae)
        all_accounts = self._get_cache_items_for_authority(msal.TokenCache.CredentialType.ACCOUNT, is_cae)

        accounts = {}
        for refresh_token in refresh_tokens:
            home_account_id = refresh_token.get("home_account_id")
            if not home_account_id:
                continue
            for account in all_accounts:
                # When the token has no family, msal.net falls back to matching client_id,
                # which won't work for the shared cache because we don't know the IDs of
                # all contributing apps. It should be unnecessary anyway because the
                # apps should all belong to the family.
                if home_account_id == account.get("home_account_id") and "family_id" in refresh_token:
                    accounts[account["home_account_id"]] = account
        return accounts.values()

    @wrap_exceptions
    def _get_account(
        self, username: Optional[str] = None, tenant_id: Optional[str] = None, is_cae: bool = False
    ) -> CacheItem:
        """Returns exactly one account which has a refresh token and matches username and/or tenant_id.

        :param str username: an account's username
        :param str tenant_id: an account's tenant ID
        :param bool is_cae: whether to use the CAE cache
        :return: an account
        :rtype: CacheItem
        """

        accounts = self._get_accounts_having_matching_refresh_tokens(is_cae)
        if not accounts:
            # cache is empty or contains no refresh token -> user needs to sign in
            raise CredentialUnavailableError(message=NO_ACCOUNTS)

        filtered_accounts = _filtered_accounts(accounts, username, tenant_id)
        if len(filtered_accounts) == 1:
            return filtered_accounts[0]

        # no, or multiple, accounts after filtering -> choose the best error message
        cached_accounts = ", ".join(_account_to_string(account) for account in accounts)
        if username or tenant_id:
            username_string = " username: {}".format(username) if username else ""
            tenant_string = " tenant: {}".format(tenant_id) if tenant_id else ""
            if filtered_accounts:
                message = MULTIPLE_MATCHING_ACCOUNTS.format(username_string, tenant_string)
            else:
                message = NO_MATCHING_ACCOUNTS.format(username_string, tenant_string)
        else:
            message = MULTIPLE_ACCOUNTS.format(cached_accounts)

        raise CredentialUnavailableError(message=message)

    def _get_cached_access_token(
        self, scopes: Iterable[str], account: CacheItem, is_cae: bool = False
    ) -> Optional[AccessTokenInfo]:
        if "home_account_id" not in account:
            return None

        cache = cast(msal.TokenCache, self._cae_cache if is_cae else self._cache)
        try:
            cache_entries = cache.search(
                msal.TokenCache.CredentialType.ACCESS_TOKEN,
                target=list(scopes),
                query={"home_account_id": account["home_account_id"]},
            )
            for token in cache_entries:
                expires_on = int(token["expires_on"])
                refresh_on = int(token["refresh_on"]) if "refresh_on" in token else None
                if expires_on - 300 > int(time.time()):
                    return AccessTokenInfo(
                        token["secret"], expires_on, token_type=token.get("token_type", "Bearer"), refresh_on=refresh_on
                    )
        except Exception as ex:
            message = "Error accessing cached data: {}".format(ex)
            raise CredentialUnavailableError(message=message) from ex

        return None

    def _get_refresh_tokens(self, account, is_cae: bool = False) -> List[str]:
        if "home_account_id" not in account:
            return []

        cache = cast(msal.TokenCache, self._cae_cache if is_cae else self._cache)
        try:
            cache_entries = cache.search(
                msal.TokenCache.CredentialType.REFRESH_TOKEN, query={"home_account_id": account["home_account_id"]}
            )
            return [token["secret"] for token in cache_entries if "secret" in token]
        except Exception as ex:
            message = "Error accessing cached data: {}".format(ex)
            raise CredentialUnavailableError(message=message) from ex

    @staticmethod
    def supported() -> bool:
        """Whether the shared token cache is supported on the current platform.

        :return: True if the shared token cache is supported on the current platform.
        :rtype: bool
        """
        return platform.system() in {"Darwin", "Linux", "Windows"}

    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        # Remove the non-picklable entries
        if not self._custom_cache:
            del state["_cache"]
            del state["_cae_cache"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        # Re-create the unpickable entries
        if not self._custom_cache:
            self._cache = None
            self._cae_cache = None
