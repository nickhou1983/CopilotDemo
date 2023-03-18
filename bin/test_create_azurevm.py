from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Create all clients with an Azure CLI credential
credential = AzureCliCredential()
subscription_id = "5bac6c1e-7aad-4a4a-a58f-a4565054dbb8"
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Define variables for resource group and VM name
resource_group_name = "myResourceGroup"
vm_name = "myVM"
vnet_name = "myVnet"
subnet_name = "mySubnet"
public_ip_name = "myPublicIP"
nic_name = "myNic"
admin_username = "pocadmin"
admin_password = "P@ssw0rd1234"
location = "eastus"
vm_size = "Standard_D2s_v3"

# Create resource group
resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})

# Create virtual network
network_client.virtual_networks.begin_create_or_update(
    resource_group_name,
    vnet_name,
    {
        "location": location,
        "address_space": {"address_prefixes": ["192.168.0.0/16"]},
    },
).result()

# Create subnet
network_client.subnets.begin_create_or_update(
    resource_group_name,
    vnet_name,
    subnet_name,
    {"address_prefix": "192.168.1.0/24"},
).result()

# Create public IP address
network_client.public_ip_addresses.begin_create_or_update(
    resource_group_name,
    public_ip_name,
    {
        "location": location,
        "public_ip_allocation_method": "Dynamic",
        "sku": {"name": "Basic"},
    },
).result()

# Create network interface
network_client.network_interfaces.begin_create_or_update(
    resource_group_name,
    nic_name,
    {
        "location": location,
        "ip_configurations": [
            {
                "name": "ipconfig1",
                "subnet": {"id": network_client.subnets.get(resource_group_name, vnet_name, subnet_name).id},
                "public_ip_address": {
                    "id": network_client.public_ip_addresses.get(resource_group_name, public_ip_name).id
                },
            }
        ],
    },
).result()

# Create VM
compute_client.virtual_machines.begin_create_or_update(
    resource_group_name,
    vm_name,
    {
        "location": location,
        "storage_profile": {
            "image_reference": {"publisher": "Canonical", "offer": "UbuntuServer", "sku": "18.04-LTS", "version": "latest"}
        },
        "hardware_profile": {"vm_size": vm_size},
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": admin_username,
            "admin_password": admin_password,
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": network_client.network_interfaces.get(resource_group_name, nic_name).id,
                }
            ]
        },
    },
).result()

