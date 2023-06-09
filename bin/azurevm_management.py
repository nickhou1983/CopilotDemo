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
admin_username = "pocadmin"
admin_password = "P@ssw0rd1234"
subscription_id = "5bac6c1e-7aad-4a4a-a58f-a4565054dbb8"
location = "eastus"
vm_size = "Standard_DS1_v2"


# Define function to create a resource group
def create_resource_group():
    resource_client = ResourceManagementClient(credential, subscription_id)
    if resource_client.resource_groups.check_existence(resource_group_name):
        print("Resource group already exists")
    else:
        resource_client.resource_groups.create_or_update(resource_group_name, {"location": location})


# Define function to create a virtual network
def create_vnet():
    network_client_vnet = NetworkManagementClient(credential, subscription_id)
    virtual_network = network_client_vnet.virtual_networks.begin_create_or_update(
        resource_group_name,
        vnet_name,
        {
            "location": location,
            "address_space": {"address_prefixes": ["192.168.0.0/16"]},
        },
    ).result()
    print(virtual_network.name + " created.")
    return virtual_network

# Define function to create a subnet
def create_subnet():
    network_client_subnet = NetworkManagementClient(credential, subscription_id)
    subnet = network_client_subnet.subnets.begin_create_or_update(
        resource_group_name,
        vnet_name,
        subnet_name,
        {"address_prefix": "192.168.1.0/24"},
    ).result()
    print(subnet.name + " created.")
    print(subnet.id)
    return subnet

# Define function to create a public IP address
def create_public_ip():
    network_client_public_ip = NetworkManagementClient(credential, subscription_id)
    public_ip = network_client_public_ip.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        public_ip_name,
        {"location": location, "sku": {"name": "Basic"}},
    ).result()
    print(public_ip.name + " created.")
    return public_ip


# Define function to create a network interface
def create_nic():
    network_client_nic = NetworkManagementClient(credential, subscription_id)
    nic = network_client_nic.network_interfaces.begin_create_or_update(
        resource_group_name,
        nic_name,
        {
            "location": location,
            "ip_configurations": [
                {
                    "name": "ipconfig1",
                    "subnet": {"id": subnet.id},
                    "public_ip_address": {"id": public_ip.id},
                }
            ],
        },
    ).result()
    print(nic.name + " created.")
    return nic


# Define function to create a virtual machine
def create_vm():
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
            "network_profile": {"network_interfaces": [{"id": nic.id}]},
        },
    )

if __name__ == "__main__":
    create_resource_group()
    create_vnet()
    create_subnet()
    create_public_ip()
    create_nic()
    create_vm()


