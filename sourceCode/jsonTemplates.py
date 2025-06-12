#This class contains the different tamplates that will be used as blueprints to send the future network request
class jsonTemplates():
    serviceEndPointsTemplate = {
        "device_id": {
            "device_uuid": {
                "uuid": "{{deviceUuid}}"
            }
        },
        "endpoint_uuid": {
            "uuid": "{{endpointUuid}}"
        }
    }

    serviceConstraints = {
        "custom": {
            "constraint_type": "{{contraintType}}",
            "constraint_value": "{{contraintValue}}"
        }
    }

    serviceTemplate = {
        "services": [{
            "service_id": {
                "context_id": {"context_uuid": {"uuid": "admin"}},
                "service_uuid": {"uuid": "netx-l3-svc"}
            },
            "service_type": 1,
            "service_status": {"service_status": 1},
            "service_endpoint_ids": [],
            "service_constraints": [],
            "service_config": {
                "config_rules": [{
                    "action": 1,
                    "custom": {
                        "resource_key": "/settings",
                        "resource_value": {
                            "address_families": ["IPV4"],
                            "bgp_as": 65000,
                            "bgp_route_target": "65000:333",
                            "mtu": 1512
                        }
                    }
                }]
            }
        }
        ]
    }
    
    slaTemplate = {
        "id": "0001",
        "name": "SSLA_1",
        "capabilities": [{
                "id" : "{{id1}}",
                "metric" : "{{metric1}}",
                "objectives" : "{{obj1}}"
            },
            {
                "id" : "{{id2}}",
                "metric" : "{{metric2}}",
                "objectives" : "{{obj2}}"
            }]
    }
    
    intentTemplate = {
        "id": "0001",
        "intentstring": "{{intentstring}}",
        "timestamp": "{{timestamp}}",
        "sla_ref": "001",
        "policy_ref": "[]",
        "request_ref": "001",
        "grouping info": "{{groupingInfo}}"
    }

