from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


# Define variables for resource group and VM
subsciption_id = '5bac6c1e-7aad-4a4a-a58f-a4565054dbb8'
resource_group_name = 'myResourceGroup'
location = 'eastus2'
vm_name = 'myVM'
vm_size = 'Standard_D2s_v3'
admin_username = 'pocadmin'
admin_password = 'Poct3sting!'
virtual_network_name = 'myVNET'
subnet_name = 'mySubnet'
network_interface_name = 'myNIC'
ip_config_name = 'myIPConfig'
public_ip_name = 'myPublicIP'
public_ip_allocation_method = 'Dynamic'

# initialize clients
credential = AzureCliCredential()
resource_client = ResourceManagementClient(credential, subsciption_id)
compute_client = ComputeManagementClient(credential, subsciption_id)
network_client = NetworkManagementClient(credential, subsciption_id)

# create resource group
resource_client.resource_groups.create_or_update(resource_group_name, {'location': location})

# create virtual network
vnet = network_client.virtual_networks.begin_create_or_update(
    resource_group_name,
    virtual_network_name,
    {
        'location': location,
        'address_space': {
            'address_prefixes': ['192.168.0.0/16']
        }
    }
).result()

# create subnet
subnet = network_client.subnets.begin_create_or_update(
    resource_group_name,
    virtual_network_name,
    subnet_name,
    {'address_prefix': '192.168.0.0/24'}
).result()

# create public IP
public_ip = network_client.public_ip_addresses.begin_create_or_updates(
    resource_group_name,
    public_ip_name,
    {
       

# create network interface
network_interface = network_client.network_interfaces.begin_create_or_update(
    resource_group_name,
    network_interface_name,
    {
        'location': location,
        'ip_configurations': [{
            'name': ip_config_name,
            'subnet': {'id': subnet.id},
            'public_ip_address': {'id': public_ip.id}
        }]
    }
).result()

# create VM
vm = compute_client.virtual_machines.begin_create_or_update(
    resource_group_name,
    vm_name,
    {
        'location': location,
        'hardware_profile': {
            'vm_size': vm_size
        },
        'storage_profile': {
            'image_reference': {
                'publisher': 'Canonical',
                'offer': 'UbuntuServer',
                'sku': '18.04-LTS',
                'version': 'latest'
            }
        },
        'os_profile': {
            'computer_name': vm_name,
            'admin_username': admin_username,
            'admin_password': admin_password
        },
        'network_profile': {
            'network_interfaces': [{
                'id': network_interface.id
            }]
        }
    }
).result()

# print VM details
print('VM created: {}'.format(vm.name))
print('VM IP address: {}'.format(public_ip.ip_address))

# This script is used to create a VM in Azure using the Azure SDK for Python. The script uses the Azure CLI to authenticate to Azure. The script creates a resource group, virtual network, subnet, public IP, network interface, and a VM. The script prints the name and IP address of the VM.
# Usage: python create_azurevm.py
# Path: demo\create_azurevm.py

# this script 