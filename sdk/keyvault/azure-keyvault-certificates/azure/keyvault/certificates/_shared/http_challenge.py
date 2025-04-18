# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import base64
from typing import Dict, MutableMapping, Optional
from urllib import parse


class HttpChallenge(object):
    """An object representing the content of a Key Vault authentication challenge.

    :param str request_uri: The URI of the HTTP request that prompted this challenge.
    :param str challenge: The WWW-Authenticate header of the challenge response.
    :param response_headers: Optional. The headers attached to the challenge response.
    :type response_headers: MutableMapping[str, str] or None
    """

    def __init__(
        self, request_uri: str, challenge: str, response_headers: "Optional[MutableMapping[str, str]]" = None
    ) -> None:
        """Parses an HTTP WWW-Authentication Bearer challenge from a server.

        Example challenge with claims:
            Bearer authorization="https://login.windows-ppe.net/", error="invalid_token",
            error_description="User session has been revoked",
            claims="eyJhY2Nlc3NfdG9rZW4iOnsibmJmIjp7ImVzc2VudGlhbCI6dHJ1ZSwgInZhbHVlIjoiMTYwMzc0MjgwMCJ9fX0="
        """
        self.source_authority = self._validate_request_uri(request_uri)
        self.source_uri = request_uri
        self._parameters: "Dict[str, str]" = {}

        # get the scheme of the challenge and remove from the challenge string
        trimmed_challenge = self._validate_challenge(challenge)
        split_challenge = trimmed_challenge.split(" ", 1)
        self.scheme = split_challenge[0]
        trimmed_challenge = split_challenge[1]

        self.claims = None
        # split trimmed challenge into comma-separated name=value pairs. Values are expected
        # to be surrounded by quotes which are stripped here.
        for item in trimmed_challenge.split(","):
            # Special case for claims, which can contain = symbols as padding. Assume at most one claim per challenge
            if "claims=" in item:
                encoded_claims = item[item.index("=") + 1 :].strip(" \"'")
                padding_needed = -len(encoded_claims) % 4
                try:
                    decoded_claims = base64.urlsafe_b64decode(encoded_claims + "=" * padding_needed).decode()
                    self.claims = decoded_claims
                except Exception:  # pylint:disable=broad-except
                    continue
            # process name=value pairs
            else:
                comps = item.split("=")
                if len(comps) == 2:
                    key = comps[0].strip(' "')
                    value = comps[1].strip(' "')
                    if key:
                        self._parameters[key] = value

        # minimum set of parameters
        if not self._parameters:
            raise ValueError("Invalid challenge parameters")

        # must specify authorization or authorization_uri
        if "authorization" not in self._parameters and "authorization_uri" not in self._parameters:
            raise ValueError("Invalid challenge parameters")

        authorization_uri = self.get_authorization_server()
        # the authorization server URI should look something like https://login.windows.net/tenant-id
        raw_uri_path = str(parse.urlparse(authorization_uri).path)
        uri_path = raw_uri_path.lstrip("/")
        self.tenant_id = uri_path.split("/", maxsplit=1)[0] or None

        # if the response headers were supplied
        if response_headers:
            # get the message signing key and message key encryption key from the headers
            self.server_signature_key = response_headers.get("x-ms-message-signing-key", None)
            self.server_encryption_key = response_headers.get("x-ms-message-encryption-key", None)

    def is_bearer_challenge(self) -> bool:
        """Tests whether the HttpChallenge is a Bearer challenge.

        :returns: True if the challenge is a Bearer challenge; False otherwise.
        :rtype: bool
        """
        if not self.scheme:
            return False

        return self.scheme.lower() == "bearer"

    def is_pop_challenge(self) -> bool:
        """Tests whether the HttpChallenge is a proof of possession challenge.

        :returns: True if the challenge is a proof of possession challenge; False otherwise.
        :rtype: bool
        """
        if not self.scheme:
            return False

        return self.scheme.lower() == "pop"

    def get_value(self, key: str) -> "Optional[str]":
        return self._parameters.get(key)

    def get_authorization_server(self) -> str:
        """Returns the URI for the authorization server if present, otherwise an empty string.

        :returns: The URI for the authorization server if present, otherwise an empty string.
        :rtype: str
        """
        value = ""
        for key in ["authorization_uri", "authorization"]:
            value = self.get_value(key) or ""
            if value:
                break
        return value

    def get_resource(self) -> str:
        """Returns the resource if present, otherwise an empty string.

        :returns: The challenge resource if present, otherwise an empty string.
        :rtype: str
        """
        return self.get_value("resource") or ""

    def get_scope(self) -> str:
        """Returns the scope if present, otherwise an empty string.

        :returns: The challenge scope if present, otherwise an empty string.
        :rtype: str
        """
        return self.get_value("scope") or ""

    def supports_pop(self) -> bool:
        """Returns True if the challenge supports proof of possession token auth; False otherwise.

        :returns: True if the challenge supports proof of possession token auth; False otherwise.
        :rtype: bool
        """
        return self._parameters.get("supportspop", "").lower() == "true"

    def supports_message_protection(self) -> bool:
        """Returns True if the challenge vault supports message protection; False otherwise.

        :returns: True if the challenge vault supports message protection; False otherwise.
        :rtype: bool
        """
        return self.supports_pop() and self.server_encryption_key and self.server_signature_key  # type: ignore

    def _validate_challenge(
        self, challenge: str
    ) -> str:  # pylint:disable=bad-option-value,useless-option-value,no-self-use
        """Verifies that the challenge is a valid auth challenge and returns the key=value pairs.

        :param str challenge: The WWW-Authenticate header of the challenge response.

        :returns: The challenge key/value pairs, with whitespace removed, as a string.
        :rtype: str
        """
        if not challenge:
            raise ValueError("Challenge cannot be empty")

        return challenge.strip()

    def _validate_request_uri(
        self, uri: str
    ) -> str:  # pylint:disable=bad-option-value,useless-option-value,no-self-use
        """Extracts the host authority from the given URI.

        :param str uri: The URI of the HTTP request that prompted the challenge.

        :returns: The challenge host authority.
        :rtype: str
        """
        if not uri:
            raise ValueError("request_uri cannot be empty")

        parsed = parse.urlparse(uri)
        if not parsed.netloc:
            raise ValueError("request_uri must be an absolute URI")

        if parsed.scheme.lower() not in ["http", "https"]:
            raise ValueError("request_uri must be HTTP or HTTPS")

        return parsed.netloc
