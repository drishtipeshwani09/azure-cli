# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "network vnet-gateway revoked-cert create",
)
class Create(AAZCommand):
    """Revoke a certificate.

    :example: Revoke a certificate.
        az network vnet-gateway revoked-cert create -g MyResourceGroup -n MyRootCertificate --gateway-name MyVnetGateway --thumbprint abc123
    """

    _aaz_info = {
        "version": "2022-01-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.network/virtualnetworkgateways/{}", "2022-01-01", "properties.vpnClientConfiguration.vpnClientRevokedCertificates[]"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        self.SubresourceSelector(ctx=self.ctx, name="subresource")
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.gateway_name = AAZStrArg(
            options=["--gateway-name"],
            help="Virtual network gateway name.",
            required=True,
        )
        _args_schema.name = AAZStrArg(
            options=["-n", "--name"],
            help="Root certificate name.",
            required=True,
        )
        _args_schema.thumbprint = AAZStrArg(
            options=["--thumbprint"],
            help="Certificate thumbprint.",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.VirtualNetworkGatewaysGet(ctx=self.ctx)()
        self.pre_instance_create()
        self.InstanceCreateByJson(ctx=self.ctx)()
        self.post_instance_create(self.ctx.selectors.subresource.required())
        yield self.VirtualNetworkGatewaysCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    @register_callback
    def pre_instance_create(self):
        pass

    @register_callback
    def post_instance_create(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.selectors.subresource.required(), client_flatten=True)
        return result

    class SubresourceSelector(AAZJsonSelector):

        def _get(self):
            result = self.ctx.vars.instance
            result = result.properties.vpnClientConfiguration.vpnClientRevokedCertificates
            filters = enumerate(result)
            filters = filter(
                lambda e: e[1].name == self.ctx.args.name,
                filters
            )
            idx = next(filters)[0]
            return result[idx]

        def _set(self, value):
            result = self.ctx.vars.instance
            result = result.properties.vpnClientConfiguration.vpnClientRevokedCertificates
            filters = enumerate(result)
            filters = filter(
                lambda e: e[1].name == self.ctx.args.name,
                filters
            )
            idx = next(filters, [len(result)])[0]
            result[idx] = value
            return

    class VirtualNetworkGatewaysGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworkGateways/{virtualNetworkGatewayName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "virtualNetworkGatewayName", self.ctx.args.gateway_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2022-01-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _CreateHelper._build_schema_virtual_network_gateway_read(cls._schema_on_200)

            return cls._schema_on_200

    class VirtualNetworkGatewaysCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworkGateways/{virtualNetworkGatewayName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "virtualNetworkGatewayName", self.ctx.args.gateway_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2022-01-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=self.ctx.vars.instance,
            )

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _CreateHelper._build_schema_virtual_network_gateway_read(cls._schema_on_200_201)

            return cls._schema_on_200_201

    class InstanceCreateByJson(AAZJsonInstanceCreateOperation):

        def __call__(self, *args, **kwargs):
            self.ctx.selectors.subresource.set(self._create_instance())

        def _create_instance(self):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType
            )
            _builder.set_prop("name", AAZStrType, ".name")
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("thumbprint", AAZStrType, ".thumbprint")

            return _instance_value


class _CreateHelper:
    """Helper class for Create"""

    _schema_address_space_read = None

    @classmethod
    def _build_schema_address_space_read(cls, _schema):
        if cls._schema_address_space_read is not None:
            _schema.address_prefixes = cls._schema_address_space_read.address_prefixes
            return

        cls._schema_address_space_read = _schema_address_space_read = AAZObjectType()

        address_space_read = _schema_address_space_read
        address_space_read.address_prefixes = AAZListType(
            serialized_name="addressPrefixes",
        )

        address_prefixes = _schema_address_space_read.address_prefixes
        address_prefixes.Element = AAZStrType()

        _schema.address_prefixes = cls._schema_address_space_read.address_prefixes

    _schema_sub_resource_read = None

    @classmethod
    def _build_schema_sub_resource_read(cls, _schema):
        if cls._schema_sub_resource_read is not None:
            _schema.id = cls._schema_sub_resource_read.id
            return

        cls._schema_sub_resource_read = _schema_sub_resource_read = AAZObjectType()

        sub_resource_read = _schema_sub_resource_read
        sub_resource_read.id = AAZStrType()

        _schema.id = cls._schema_sub_resource_read.id

    _schema_virtual_network_gateway_read = None

    @classmethod
    def _build_schema_virtual_network_gateway_read(cls, _schema):
        if cls._schema_virtual_network_gateway_read is not None:
            _schema.etag = cls._schema_virtual_network_gateway_read.etag
            _schema.extended_location = cls._schema_virtual_network_gateway_read.extended_location
            _schema.id = cls._schema_virtual_network_gateway_read.id
            _schema.location = cls._schema_virtual_network_gateway_read.location
            _schema.name = cls._schema_virtual_network_gateway_read.name
            _schema.properties = cls._schema_virtual_network_gateway_read.properties
            _schema.tags = cls._schema_virtual_network_gateway_read.tags
            _schema.type = cls._schema_virtual_network_gateway_read.type
            return

        cls._schema_virtual_network_gateway_read = _schema_virtual_network_gateway_read = AAZObjectType()

        virtual_network_gateway_read = _schema_virtual_network_gateway_read
        virtual_network_gateway_read.etag = AAZStrType(
            flags={"read_only": True},
        )
        virtual_network_gateway_read.extended_location = AAZObjectType(
            serialized_name="extendedLocation",
        )
        virtual_network_gateway_read.id = AAZStrType()
        virtual_network_gateway_read.location = AAZStrType()
        virtual_network_gateway_read.name = AAZStrType(
            flags={"read_only": True},
        )
        virtual_network_gateway_read.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )
        virtual_network_gateway_read.tags = AAZDictType()
        virtual_network_gateway_read.type = AAZStrType(
            flags={"read_only": True},
        )

        extended_location = _schema_virtual_network_gateway_read.extended_location
        extended_location.name = AAZStrType()
        extended_location.type = AAZStrType()

        properties = _schema_virtual_network_gateway_read.properties
        properties.active_active = AAZBoolType(
            serialized_name="activeActive",
        )
        properties.bgp_settings = AAZObjectType(
            serialized_name="bgpSettings",
        )
        properties.custom_routes = AAZObjectType(
            serialized_name="customRoutes",
        )
        cls._build_schema_address_space_read(properties.custom_routes)
        properties.disable_ip_sec_replay_protection = AAZBoolType(
            serialized_name="disableIPSecReplayProtection",
        )
        properties.enable_bgp = AAZBoolType(
            serialized_name="enableBgp",
        )
        properties.enable_bgp_route_translation_for_nat = AAZBoolType(
            serialized_name="enableBgpRouteTranslationForNat",
        )
        properties.enable_dns_forwarding = AAZBoolType(
            serialized_name="enableDnsForwarding",
        )
        properties.enable_private_ip_address = AAZBoolType(
            serialized_name="enablePrivateIpAddress",
        )
        properties.gateway_default_site = AAZObjectType(
            serialized_name="gatewayDefaultSite",
        )
        cls._build_schema_sub_resource_read(properties.gateway_default_site)
        properties.gateway_type = AAZStrType(
            serialized_name="gatewayType",
        )
        properties.inbound_dns_forwarding_endpoint = AAZStrType(
            serialized_name="inboundDnsForwardingEndpoint",
            flags={"read_only": True},
        )
        properties.ip_configurations = AAZListType(
            serialized_name="ipConfigurations",
        )
        properties.nat_rules = AAZListType(
            serialized_name="natRules",
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.resource_guid = AAZStrType(
            serialized_name="resourceGuid",
            flags={"read_only": True},
        )
        properties.sku = AAZObjectType()
        properties.v_net_extended_location_resource_id = AAZStrType(
            serialized_name="vNetExtendedLocationResourceId",
        )
        properties.vpn_client_configuration = AAZObjectType(
            serialized_name="vpnClientConfiguration",
        )
        properties.vpn_gateway_generation = AAZStrType(
            serialized_name="vpnGatewayGeneration",
        )
        properties.vpn_type = AAZStrType(
            serialized_name="vpnType",
        )

        bgp_settings = _schema_virtual_network_gateway_read.properties.bgp_settings
        bgp_settings.asn = AAZIntType()
        bgp_settings.bgp_peering_address = AAZStrType(
            serialized_name="bgpPeeringAddress",
        )
        bgp_settings.bgp_peering_addresses = AAZListType(
            serialized_name="bgpPeeringAddresses",
        )
        bgp_settings.peer_weight = AAZIntType(
            serialized_name="peerWeight",
        )

        bgp_peering_addresses = _schema_virtual_network_gateway_read.properties.bgp_settings.bgp_peering_addresses
        bgp_peering_addresses.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.bgp_settings.bgp_peering_addresses.Element
        _element.custom_bgp_ip_addresses = AAZListType(
            serialized_name="customBgpIpAddresses",
        )
        _element.default_bgp_ip_addresses = AAZListType(
            serialized_name="defaultBgpIpAddresses",
            flags={"read_only": True},
        )
        _element.ipconfiguration_id = AAZStrType(
            serialized_name="ipconfigurationId",
        )
        _element.tunnel_ip_addresses = AAZListType(
            serialized_name="tunnelIpAddresses",
            flags={"read_only": True},
        )

        custom_bgp_ip_addresses = _schema_virtual_network_gateway_read.properties.bgp_settings.bgp_peering_addresses.Element.custom_bgp_ip_addresses
        custom_bgp_ip_addresses.Element = AAZStrType()

        default_bgp_ip_addresses = _schema_virtual_network_gateway_read.properties.bgp_settings.bgp_peering_addresses.Element.default_bgp_ip_addresses
        default_bgp_ip_addresses.Element = AAZStrType()

        tunnel_ip_addresses = _schema_virtual_network_gateway_read.properties.bgp_settings.bgp_peering_addresses.Element.tunnel_ip_addresses
        tunnel_ip_addresses.Element = AAZStrType()

        ip_configurations = _schema_virtual_network_gateway_read.properties.ip_configurations
        ip_configurations.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.ip_configurations.Element
        _element.etag = AAZStrType(
            flags={"read_only": True},
        )
        _element.id = AAZStrType()
        _element.name = AAZStrType()
        _element.properties = AAZObjectType(
            flags={"client_flatten": True},
        )

        properties = _schema_virtual_network_gateway_read.properties.ip_configurations.Element.properties
        properties.private_ip_address = AAZStrType(
            serialized_name="privateIPAddress",
            flags={"read_only": True},
        )
        properties.private_ip_allocation_method = AAZStrType(
            serialized_name="privateIPAllocationMethod",
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.public_ip_address = AAZObjectType(
            serialized_name="publicIPAddress",
        )
        cls._build_schema_sub_resource_read(properties.public_ip_address)
        properties.subnet = AAZObjectType()
        cls._build_schema_sub_resource_read(properties.subnet)

        nat_rules = _schema_virtual_network_gateway_read.properties.nat_rules
        nat_rules.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.nat_rules.Element
        _element.etag = AAZStrType(
            flags={"read_only": True},
        )
        _element.id = AAZStrType()
        _element.name = AAZStrType()
        _element.properties = AAZObjectType(
            flags={"client_flatten": True},
        )
        _element.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_virtual_network_gateway_read.properties.nat_rules.Element.properties
        properties.external_mappings = AAZListType(
            serialized_name="externalMappings",
        )
        properties.internal_mappings = AAZListType(
            serialized_name="internalMappings",
        )
        properties.ip_configuration_id = AAZStrType(
            serialized_name="ipConfigurationId",
        )
        properties.mode = AAZStrType()
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.type = AAZStrType()

        external_mappings = _schema_virtual_network_gateway_read.properties.nat_rules.Element.properties.external_mappings
        external_mappings.Element = AAZObjectType()
        cls._build_schema_vpn_nat_rule_mapping_read(external_mappings.Element)

        internal_mappings = _schema_virtual_network_gateway_read.properties.nat_rules.Element.properties.internal_mappings
        internal_mappings.Element = AAZObjectType()
        cls._build_schema_vpn_nat_rule_mapping_read(internal_mappings.Element)

        sku = _schema_virtual_network_gateway_read.properties.sku
        sku.capacity = AAZIntType(
            flags={"read_only": True},
        )
        sku.name = AAZStrType()
        sku.tier = AAZStrType()

        vpn_client_configuration = _schema_virtual_network_gateway_read.properties.vpn_client_configuration
        vpn_client_configuration.aad_audience = AAZStrType(
            serialized_name="aadAudience",
        )
        vpn_client_configuration.aad_issuer = AAZStrType(
            serialized_name="aadIssuer",
        )
        vpn_client_configuration.aad_tenant = AAZStrType(
            serialized_name="aadTenant",
        )
        vpn_client_configuration.radius_server_address = AAZStrType(
            serialized_name="radiusServerAddress",
        )
        vpn_client_configuration.radius_server_secret = AAZStrType(
            serialized_name="radiusServerSecret",
        )
        vpn_client_configuration.radius_servers = AAZListType(
            serialized_name="radiusServers",
        )
        vpn_client_configuration.vpn_authentication_types = AAZListType(
            serialized_name="vpnAuthenticationTypes",
        )
        vpn_client_configuration.vpn_client_address_pool = AAZObjectType(
            serialized_name="vpnClientAddressPool",
        )
        cls._build_schema_address_space_read(vpn_client_configuration.vpn_client_address_pool)
        vpn_client_configuration.vpn_client_ipsec_policies = AAZListType(
            serialized_name="vpnClientIpsecPolicies",
        )
        vpn_client_configuration.vpn_client_protocols = AAZListType(
            serialized_name="vpnClientProtocols",
        )
        vpn_client_configuration.vpn_client_revoked_certificates = AAZListType(
            serialized_name="vpnClientRevokedCertificates",
        )
        vpn_client_configuration.vpn_client_root_certificates = AAZListType(
            serialized_name="vpnClientRootCertificates",
        )

        radius_servers = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.radius_servers
        radius_servers.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.radius_servers.Element
        _element.radius_server_address = AAZStrType(
            serialized_name="radiusServerAddress",
            flags={"required": True},
        )
        _element.radius_server_score = AAZIntType(
            serialized_name="radiusServerScore",
        )
        _element.radius_server_secret = AAZStrType(
            serialized_name="radiusServerSecret",
        )

        vpn_authentication_types = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_authentication_types
        vpn_authentication_types.Element = AAZStrType()

        vpn_client_ipsec_policies = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_ipsec_policies
        vpn_client_ipsec_policies.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_ipsec_policies.Element
        _element.dh_group = AAZStrType(
            serialized_name="dhGroup",
            flags={"required": True},
        )
        _element.ike_encryption = AAZStrType(
            serialized_name="ikeEncryption",
            flags={"required": True},
        )
        _element.ike_integrity = AAZStrType(
            serialized_name="ikeIntegrity",
            flags={"required": True},
        )
        _element.ipsec_encryption = AAZStrType(
            serialized_name="ipsecEncryption",
            flags={"required": True},
        )
        _element.ipsec_integrity = AAZStrType(
            serialized_name="ipsecIntegrity",
            flags={"required": True},
        )
        _element.pfs_group = AAZStrType(
            serialized_name="pfsGroup",
            flags={"required": True},
        )
        _element.sa_data_size_kilobytes = AAZIntType(
            serialized_name="saDataSizeKilobytes",
            flags={"required": True},
        )
        _element.sa_life_time_seconds = AAZIntType(
            serialized_name="saLifeTimeSeconds",
            flags={"required": True},
        )

        vpn_client_protocols = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_protocols
        vpn_client_protocols.Element = AAZStrType()

        vpn_client_revoked_certificates = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_revoked_certificates
        vpn_client_revoked_certificates.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_revoked_certificates.Element
        _element.etag = AAZStrType(
            flags={"read_only": True},
        )
        _element.id = AAZStrType()
        _element.name = AAZStrType()
        _element.properties = AAZObjectType(
            flags={"client_flatten": True},
        )

        properties = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_revoked_certificates.Element.properties
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.thumbprint = AAZStrType()

        vpn_client_root_certificates = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_root_certificates
        vpn_client_root_certificates.Element = AAZObjectType()

        _element = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_root_certificates.Element
        _element.etag = AAZStrType(
            flags={"read_only": True},
        )
        _element.id = AAZStrType()
        _element.name = AAZStrType()
        _element.properties = AAZObjectType(
            flags={"required": True, "client_flatten": True},
        )

        properties = _schema_virtual_network_gateway_read.properties.vpn_client_configuration.vpn_client_root_certificates.Element.properties
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )
        properties.public_cert_data = AAZStrType(
            serialized_name="publicCertData",
            flags={"required": True},
        )

        tags = _schema_virtual_network_gateway_read.tags
        tags.Element = AAZStrType()

        _schema.etag = cls._schema_virtual_network_gateway_read.etag
        _schema.extended_location = cls._schema_virtual_network_gateway_read.extended_location
        _schema.id = cls._schema_virtual_network_gateway_read.id
        _schema.location = cls._schema_virtual_network_gateway_read.location
        _schema.name = cls._schema_virtual_network_gateway_read.name
        _schema.properties = cls._schema_virtual_network_gateway_read.properties
        _schema.tags = cls._schema_virtual_network_gateway_read.tags
        _schema.type = cls._schema_virtual_network_gateway_read.type

    _schema_vpn_nat_rule_mapping_read = None

    @classmethod
    def _build_schema_vpn_nat_rule_mapping_read(cls, _schema):
        if cls._schema_vpn_nat_rule_mapping_read is not None:
            _schema.address_space = cls._schema_vpn_nat_rule_mapping_read.address_space
            _schema.port_range = cls._schema_vpn_nat_rule_mapping_read.port_range
            return

        cls._schema_vpn_nat_rule_mapping_read = _schema_vpn_nat_rule_mapping_read = AAZObjectType()

        vpn_nat_rule_mapping_read = _schema_vpn_nat_rule_mapping_read
        vpn_nat_rule_mapping_read.address_space = AAZStrType(
            serialized_name="addressSpace",
        )
        vpn_nat_rule_mapping_read.port_range = AAZStrType(
            serialized_name="portRange",
        )

        _schema.address_space = cls._schema_vpn_nat_rule_mapping_read.address_space
        _schema.port_range = cls._schema_vpn_nat_rule_mapping_read.port_range


__all__ = ["Create"]
