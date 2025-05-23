# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import re
from typing import (
    Any, Dict, Optional, Tuple, Union,
    TYPE_CHECKING
)
from urllib.parse import quote, urlparse

from ._serialize import (
    add_metadata_headers,
    convert_datetime_to_rfc1123,
    get_access_conditions,
    get_cpk_info,
    get_lease_id,
    get_mod_conditions,
    get_path_http_headers,
    get_source_mod_conditions
)
from ._shared.response_handlers import return_headers_and_deserialized, return_response_headers

if TYPE_CHECKING:
    from urllib.parse import ParseResult
    from azure.core.credentials import AzureNamedKeyCredential, AzureSasCredential, TokenCredential
    from azure.core.credentials_async import AsyncTokenCredential
    from azure.core.pipeline import Pipeline
    from ._models import ContentSettings


def _parse_url(account_url: str) -> "ParseResult":
    try:
        if not account_url.lower().startswith('http'):
            account_url = "https://" + account_url
    except AttributeError as exc:
        raise ValueError("Account URL must be a string.") from exc
    parsed_url = urlparse(account_url.rstrip('/'))
    if not parsed_url.netloc:
        raise ValueError(f"Invalid URL: {account_url}")
    return parsed_url


def _format_url(scheme: str, hostname: str, file_system_name: Union[str, bytes], path_name: str, query_str: str) -> str:
    if isinstance(file_system_name, str):
        file_system_name = file_system_name.encode('UTF-8')
    return f"{scheme}://{hostname}/{quote(file_system_name)}/{quote(path_name, safe='~/')}{query_str}"


def _create_path_options(
    resource_type: str,
    scheme: str,
    content_settings: Optional["ContentSettings"] = None,
    metadata: Optional[Dict[str, str]] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    access_conditions = get_access_conditions(kwargs.pop('lease', None))
    mod_conditions = get_mod_conditions(kwargs)

    path_http_headers = None
    if content_settings:
        path_http_headers = get_path_http_headers(content_settings)

    cpk_info = get_cpk_info(scheme, kwargs)

    expires_on = kwargs.pop('expires_on', None)
    if expires_on:
        try:
            expires_on = convert_datetime_to_rfc1123(expires_on)
            kwargs['expiry_options'] = 'Absolute'
        except AttributeError:
            expires_on = str(expires_on)
            kwargs['expiry_options'] = 'RelativeToNow'

    options = {
        'resource': resource_type,
        'properties': add_metadata_headers(metadata),
        'permissions': kwargs.pop('permissions', None),
        'umask': kwargs.pop('umask', None),
        'owner': kwargs.pop('owner', None),
        'group': kwargs.pop('group', None),
        'acl': kwargs.pop('acl', None),
        'proposed_lease_id': kwargs.pop('lease_id', None),
        'lease_duration': kwargs.pop('lease_duration', None),
        'expiry_options': kwargs.pop('expiry_options', None),
        'expires_on': expires_on,
        'path_http_headers': path_http_headers,
        'lease_access_conditions': access_conditions,
        'modified_access_conditions': mod_conditions,
        'cpk_info': cpk_info,
        'timeout': kwargs.pop('timeout', None),
        'encryption_context': kwargs.pop('encryption_context', None),
        'cls': return_response_headers
    }
    options.update(kwargs)
    return options


def _delete_path_options(paginated: Optional[bool], **kwargs) -> Dict[str, Any]:
    access_conditions = get_access_conditions(kwargs.pop('lease', None))
    mod_conditions = get_mod_conditions(kwargs)

    options = {
        'paginated': paginated,
        'lease_access_conditions': access_conditions,
        'modified_access_conditions': mod_conditions,
        'cls': return_response_headers,
        'timeout': kwargs.pop('timeout', None)
    }
    options.update(kwargs)
    return options


def _set_access_control_options(
    owner: Optional[str] = None,
    group: Optional[str] = None,
    permissions: Optional[str] = None,
    acl: Optional[str] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    access_conditions = get_access_conditions(kwargs.pop('lease', None))
    mod_conditions = get_mod_conditions(kwargs)

    options = {
        'owner': owner,
        'group': group,
        'permissions': permissions,
        'acl': acl,
        'lease_access_conditions': access_conditions,
        'modified_access_conditions': mod_conditions,
        'timeout': kwargs.pop('timeout', None),
        'cls': return_response_headers
    }
    options.update(kwargs)
    return options


def _get_access_control_options(upn: Optional[bool] = None, **kwargs: Any) -> Dict[str, Any]:
    access_conditions = get_access_conditions(kwargs.pop('lease', None))
    mod_conditions = get_mod_conditions(kwargs)

    options = {
        'action': 'getAccessControl',
        'upn': upn if upn else False,
        'lease_access_conditions': access_conditions,
        'modified_access_conditions': mod_conditions,
        'timeout': kwargs.pop('timeout', None),
        'cls': return_response_headers
    }
    options.update(kwargs)
    return options


def _set_access_control_recursive_options(mode: str, acl: str, **kwargs: Any) -> Dict[str, Any]:
    options = {
        'mode': mode,
        'force_flag': kwargs.pop('continue_on_failure', None),
        'timeout': kwargs.pop('timeout', None),
        'continuation': kwargs.pop('continuation_token', None),
        'max_records': kwargs.pop('batch_size', None),
        'acl': acl,
        'cls': return_headers_and_deserialized
    }
    options.update(kwargs)
    return options


def _rename_path_options(
    rename_source: str,
    content_settings: Optional["ContentSettings"] = None,
    metadata: Optional[Dict[str, str]] = None,
    **kwargs: Any
) -> Dict[str, Any]:
    if metadata or kwargs.pop('permissions', None) or kwargs.pop('umask', None):
        raise ValueError("metadata, permissions, umask is not supported for this operation")

    access_conditions = get_access_conditions(kwargs.pop('lease', None))
    source_lease_id = get_lease_id(kwargs.pop('source_lease', None))
    mod_conditions = get_mod_conditions(kwargs)
    source_mod_conditions = get_source_mod_conditions(kwargs)

    path_http_headers = None
    if content_settings:
        path_http_headers = get_path_http_headers(content_settings)

    options = {
        'rename_source': rename_source,
        'path_http_headers': path_http_headers,
        'lease_access_conditions': access_conditions,
        'source_lease_id': source_lease_id,
        'modified_access_conditions': mod_conditions,
        'source_modified_access_conditions': source_mod_conditions,
        'timeout': kwargs.pop('timeout', None),
        'mode': 'legacy',
        'cls': return_response_headers
    }
    options.update(kwargs)
    return options


def _parse_rename_path(
    new_name: str,
    file_system_name: str,
    query_str: str,
    raw_credential: Optional[Union[str, Dict[str, str], "AzureNamedKeyCredential", "AzureSasCredential", "TokenCredential", "AsyncTokenCredential"]]  # pylint: disable=line-too-long
) -> Tuple[str, str, Optional[str]]:
    new_name = new_name.strip('/')
    new_file_system = new_name.split('/')[0]
    new_path = new_name[len(new_file_system):].strip('/')

    new_sas = None
    sas_split = new_path.split('?')
    # If there is a ?, there could be a SAS token
    if len(sas_split) > 0:
        # Check last element for SAS by looking for sv= and sig=
        potential_sas = sas_split[-1]
        if re.search(r'sv=\d{4}-\d{2}-\d{2}', potential_sas) and 'sig=' in potential_sas:
            new_sas = potential_sas
            # Remove SAS from new path
            new_path = new_path[:-(len(new_sas) + 1)]

    if not new_sas:
        if not raw_credential and new_file_system != file_system_name:
            raise ValueError("please provide the sas token for the new file")
        if not raw_credential and new_file_system == file_system_name:
            new_sas = query_str.strip('?')

    return new_file_system, new_path, new_sas
