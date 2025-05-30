# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from typing import cast, Optional, Any

from azure.core.credentials import AccessToken, AccessTokenInfo, TokenRequestOptions
from azure.core.exceptions import ClientAuthenticationError
from ..._exceptions import CredentialUnavailableError
from .._internal import AsyncContextManager
from .._internal.aad_client import AadClient
from .._internal.get_token_mixin import GetTokenMixin
from .._internal.decorators import log_get_token_async
from ..._credentials.vscode import _VSCodeCredentialBase
from ..._internal import within_dac


class VisualStudioCodeCredential(_VSCodeCredentialBase, AsyncContextManager, GetTokenMixin):
    """Authenticates as the Azure user signed in to Visual Studio Code via the 'Azure Account' extension.

    **Deprecated**: This credential is deprecated because the Azure Account extension for Visual Studio Code, which
    this credential relies on, has been deprecated. See the Azure Account extension deprecation notice here:
    https://github.com/microsoft/vscode-azure-account/issues/964. Consider using other developer credentials such as
    AzureCliCredential, AzureDeveloperCliCredential, or AzurePowerShellCredential.

    :keyword str authority: Authority of a Microsoft Entra endpoint, for example "login.microsoftonline.com".
        This argument is required for a custom cloud and usually unnecessary otherwise. Defaults to the authority
        matching the "Azure: Cloud" setting in VS Code's user settings or, when that setting has no value, the
        authority for Azure Public Cloud.
    :keyword str tenant_id: ID of the tenant the credential should authenticate in. Defaults to the "Azure: Tenant"
        setting in VS Code's user settings or, when that setting has no value, the "organizations" tenant, which
        supports only Microsoft Entra work or school accounts.
    :keyword List[str] additionally_allowed_tenants: Specifies tenants in addition to the specified "tenant_id"
        for which the credential may acquire tokens. Add the wildcard value "*" to allow the credential to
        acquire tokens for any tenant the application can access.
    """

    async def __aenter__(self) -> "VisualStudioCodeCredential":
        if self._client:
            await self._client.__aenter__()
        return self

    async def close(self) -> None:
        """Close the credential's transport session."""

        if self._client:
            await self._client.__aexit__()

    @log_get_token_async
    async def get_token(
        self, *scopes: str, claims: Optional[str] = None, tenant_id: Optional[str] = None, **kwargs: Any
    ) -> AccessToken:
        """Request an access token for `scopes` as the user currently signed in to Visual Studio Code.

        This method is called automatically by Azure SDK clients.

        :param str scopes: desired scopes for the access token. This method requires at least one scope.
            For more information about scopes, see
            https://learn.microsoft.com/entra/identity-platform/scopes-oidc.
        :keyword str claims: additional claims required in the token, such as those returned in a resource provider's
            claims challenge following an authorization failure.
        :keyword str tenant_id: optional tenant to include in the token request.

        :return: An access token with the desired scopes.
        :rtype: ~azure.core.credentials.AccessToken
        :raises ~azure.identity.CredentialUnavailableError: the credential cannot retrieve user details from Visual
            Studio Code
        """
        if self._unavailable_reason:
            error_message = (
                self._unavailable_reason + "\n"
                "Visit https://aka.ms/azsdk/python/identity/vscodecredential/troubleshoot"
                " to troubleshoot this issue."
            )
            raise CredentialUnavailableError(message=error_message)
        if not self._client:
            raise CredentialUnavailableError("Initialization failed")
        if within_dac.get():
            try:
                token = await super().get_token(*scopes, claims=claims, tenant_id=tenant_id, **kwargs)
                return token
            except ClientAuthenticationError as ex:
                raise CredentialUnavailableError(message=ex.message) from ex
        return await super().get_token(*scopes, claims=claims, tenant_id=tenant_id, **kwargs)

    async def get_token_info(self, *scopes: str, options: Optional[TokenRequestOptions] = None) -> AccessTokenInfo:
        """Request an access token for `scopes` as the user currently signed in to Visual Studio Code.

        This is an alternative to `get_token` to enable certain scenarios that require additional properties
        on the token. This method is called automatically by Azure SDK clients.

        :param str scopes: desired scopes for the access token. This method requires at least one scope.
            For more information about scopes, see https://learn.microsoft.com/entra/identity-platform/scopes-oidc.
        :keyword options: A dictionary of options for the token request. Unknown options will be ignored. Optional.
        :paramtype options: ~azure.core.credentials.TokenRequestOptions

        :rtype: ~azure.core.credentials.AccessTokenInfo
        :return: An AccessTokenInfo instance containing information about the token.
        :raises ~azure.identity.CredentialUnavailableError: the credential cannot retrieve user details from Visual
          Studio Code.
        """
        if self._unavailable_reason:
            error_message = (
                self._unavailable_reason + "\n"
                "Visit https://aka.ms/azsdk/python/identity/vscodecredential/troubleshoot"
                " to troubleshoot this issue."
            )
            raise CredentialUnavailableError(message=error_message)
        if within_dac.get():
            try:
                token = await super().get_token_info(*scopes, options=options)
                return token
            except ClientAuthenticationError as ex:
                raise CredentialUnavailableError(message=ex.message) from ex
        return await super().get_token_info(*scopes, options=options)

    async def _acquire_token_silently(self, *scopes: str, **kwargs: Any) -> Optional[AccessTokenInfo]:
        self._client = cast(AadClient, self._client)
        return self._client.get_cached_access_token(scopes, **kwargs)

    async def _request_token(self, *scopes: str, **kwargs: Any) -> AccessTokenInfo:
        refresh_token = self._get_refresh_token()
        self._client = cast(AadClient, self._client)
        return await self._client.obtain_token_by_refresh_token(scopes, refresh_token, **kwargs)

    def _get_client(self, **kwargs: Any) -> AadClient:
        return AadClient(**kwargs)
