from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Get Azure CLI credentials
credential = AzureCliCredential()

# Define variables for resource group and VM name
resource_group_name = "myResourceGroup"
vm_name = "myVM"
vnet_name = "myVnet"
subnet_name = "mySubnet"
public_ip_name = "myPublicIP"
nic_name = "myNic"
admin_username = "myAdminUsername"
admin_password = "myAdminPassword"
subscription_id = "mySubscriptionID"
location = "eastus"
vm_size = "Standard_DS1_v2"


# Define function to create a resource group
def create_resource_group(resource_group_name, location):
    resource_client = ResourceManagementClient(credential, subscription_id)
    resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": location}
    )

# Define function to create a virtual network
def create_vnet(resource_group_name, vnet_name, location,address_prefixes):
    network_client = NetworkManagementClient(credential, subscription_id)
    network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        vnet_name,
        {
            "location": location,
            "address_space": {"address_prefixes": ["192.168.0.0/16"]},
        },
    ).result()

# Define function to create a subnet
def create_subnet(resource_group_name, vnet_name, subnet_name, location, address_prefix):
    network_client = NetworkManagementClient(credential, subscription_id)
    network_client.subnets.begin_create_or_update(
        resource_group_name,
        vnet_name,
        subnet_name,
        {"address_prefix": "192.168.0.0/24"},
    ).result()

# Define function to create a public IP address
def create_public_ip(resource_group_name, public_ip_name, location):
    network_client = NetworkManagementClient(credential, subscription_id)
    network_client.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        public_ip_name,
        {"location": location, "sku": {"name": "Basic"}},
    ).result()

# Define function to create a network interface
def create_nic(resource_group_name, nic_name, location, subnet_id, public_ip_id):
    network_client = NetworkManagementClient(credential, subscription_id)
    network_client.network_interfaces.begin_create_or_update(
        resource_group_name,
        nic_name,
        {
            "location": location,
            "ip_configurations": [
                {
                    "name": "ipconfig1",
                    "subnet": {"id": create_subnet().id},
                    "public_ip_address": {"id": create_public_ip().id},
                }
            ],
        },
    ).result()

# Define function to create a virtual machine
def create_vm(resource_group_name, vm_name, location, vm_size, admin_username, admin_password, nic_id):
    compute_client = ComputeManagementClient(credential, subscription_id)
    compute_client.virtual_machines.begin_create_or_update(
        resource_group_name,
        vm_name,
        {
            "location": location,
            "storage_profile": {
                "image_reference": {
                    "publisher": "Canonical",
                    "offer": "UbuntuServer",
                    "sku": "18.04-LTS",
                    "version": "latest",
                }
            },
            "hardware_profile": {"vm_size": vm_size},
            "os_profile": {
                "computer_name": vm_name,
                "admin_username": admin_username,
                "admin_password": admin_password,
            },
            "network_profile": {"network_interfaces": [{"id": create_nic().id}]},
        },
    )