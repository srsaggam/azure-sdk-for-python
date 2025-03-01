# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, Callable, Dict, Optional, TypeVar, Union

from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._net_app_resource_operations import (
    build_check_file_path_availability_request,
    build_check_name_availability_request,
    build_check_quota_availability_request,
    build_query_region_info_request,
)

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class NetAppResourceOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.netapp.aio.NetAppManagementClient`'s
        :attr:`net_app_resource` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def check_name_availability(
        self,
        location: str,
        name: str,
        type: Union[str, _models.CheckNameResourceTypes],
        resource_group: str,
        **kwargs: Any
    ) -> _models.CheckAvailabilityResponse:
        """Check resource name availability.

        Check if a resource name is available.

        :param location: The location. Required.
        :type location: str
        :param name: Resource name to verify. Required.
        :type name: str
        :param type: Resource type used for verification. Known values are:
         "Microsoft.NetApp/netAppAccounts", "Microsoft.NetApp/netAppAccounts/capacityPools",
         "Microsoft.NetApp/netAppAccounts/capacityPools/volumes", and
         "Microsoft.NetApp/netAppAccounts/capacityPools/volumes/snapshots". Required.
        :type type: str or ~azure.mgmt.netapp.models.CheckNameResourceTypes
        :param resource_group: Resource group name. Required.
        :type resource_group: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.netapp.models.CheckAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        content_type = kwargs.pop("content_type", _headers.pop("Content-Type", "application/json"))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.CheckAvailabilityResponse]

        _body = _models.ResourceNameAvailabilityRequest(name=name, resource_group=resource_group, type=type)
        _json = self._serialize.body(_body, "ResourceNameAvailabilityRequest")

        request = build_check_name_availability_request(
            location=location,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.check_name_availability.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("CheckAvailabilityResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    check_name_availability.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.NetApp/locations/{location}/checkNameAvailability"}  # type: ignore

    @distributed_trace_async
    async def check_file_path_availability(
        self, location: str, name: str, subnet_id: str, **kwargs: Any
    ) -> _models.CheckAvailabilityResponse:
        """Check file path availability.

        Check if a file path is available.

        :param location: The location. Required.
        :type location: str
        :param name: File path to verify. Required.
        :type name: str
        :param subnet_id: The Azure Resource URI for a delegated subnet. Must have the delegation
         Microsoft.NetApp/volumes. Required.
        :type subnet_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.netapp.models.CheckAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        content_type = kwargs.pop("content_type", _headers.pop("Content-Type", "application/json"))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.CheckAvailabilityResponse]

        _body = _models.FilePathAvailabilityRequest(name=name, subnet_id=subnet_id)
        _json = self._serialize.body(_body, "FilePathAvailabilityRequest")

        request = build_check_file_path_availability_request(
            location=location,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.check_file_path_availability.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("CheckAvailabilityResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    check_file_path_availability.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.NetApp/locations/{location}/checkFilePathAvailability"}  # type: ignore

    @distributed_trace_async
    async def check_quota_availability(
        self,
        location: str,
        name: str,
        type: Union[str, _models.CheckQuotaNameResourceTypes],
        resource_group: str,
        **kwargs: Any
    ) -> _models.CheckAvailabilityResponse:
        """Check quota availability.

        Check if a quota is available.

        :param location: The location. Required.
        :type location: str
        :param name: Name of the resource to verify. Required.
        :type name: str
        :param type: Resource type used for verification. Known values are:
         "Microsoft.NetApp/netAppAccounts", "Microsoft.NetApp/netAppAccounts/capacityPools",
         "Microsoft.NetApp/netAppAccounts/capacityPools/volumes", and
         "Microsoft.NetApp/netAppAccounts/capacityPools/volumes/snapshots". Required.
        :type type: str or ~azure.mgmt.netapp.models.CheckQuotaNameResourceTypes
        :param resource_group: Resource group name. Required.
        :type resource_group: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: CheckAvailabilityResponse or the result of cls(response)
        :rtype: ~azure.mgmt.netapp.models.CheckAvailabilityResponse
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        content_type = kwargs.pop("content_type", _headers.pop("Content-Type", "application/json"))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.CheckAvailabilityResponse]

        _body = _models.QuotaAvailabilityRequest(name=name, resource_group=resource_group, type=type)
        _json = self._serialize.body(_body, "QuotaAvailabilityRequest")

        request = build_check_quota_availability_request(
            location=location,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            template_url=self.check_quota_availability.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("CheckAvailabilityResponse", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    check_quota_availability.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.NetApp/locations/{location}/checkQuotaAvailability"}  # type: ignore

    @distributed_trace_async
    async def query_region_info(self, location: str, **kwargs: Any) -> _models.RegionInfo:
        """Describes region specific information.

        Provides storage to network proximity and logical zone mapping information.

        :param location: The location. Required.
        :type location: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: RegionInfo or the result of cls(response)
        :rtype: ~azure.mgmt.netapp.models.RegionInfo
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.RegionInfo]

        request = build_query_region_info_request(
            location=location,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.query_region_info.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize("RegionInfo", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    query_region_info.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.NetApp/locations/{location}/regionInfo"}  # type: ignore
