from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Define the function to create a resource group
def create_resource_group(resource_client, resource_group_name, location):
    if resource_client.resource_groups.check_existence(resource_group_name):
        print(f'Resource group {resource_group_name} already exists')
    else:
        print(f'Creating resource group {resource_group_name}')
    resource_client.resource_groups.create_or_update(resource_group_name, {'location': location})

# Define the function to create a virtual network
def create_virtual_network(network_client, resource_group_name, virtual_network_name, location, address_spaces):
    if network_client.virtual_networks.check_existence(resource_group_name, virtual_network_name):
        print(f'Virtual network {virtual_network_name} already exists')
    else:
        print(f'Creating virtual network {virtual_network_name}')
    vnet = network_client.virtual_networks.begin_create_or_update(
        resource_group_name,
        virtual_network_name,
        {
            'location': location,
            'address_space': {
                'address_prefixes': [address_spaces]
            }
        }
    ).result()

# Define the function to create a subnet
def create_subnet(network_client, resource_group_name, virtual_network_name, subnet_name, address_prefix):
    if network_client.subnets.check_existence(resource_group_name, virtual_network_name, subnet_name):
        print(f'Subnet {subnet_name} already exists')
    else:
        print(f'Creating subnet {subnet_name}')
    subnet = network_client.subnets.begin_create_or_update(
        resource_group_name,
        virtual_network_name,
        subnet_name,
        {'address_prefix': address_prefix}
    ).result()

# Define the function to create a public IP
def create_public_ip(network_client, resource_group_name, public_ip_name, location, public_ip_allocation_method):
    if network_client.public_ip_addresses.check_existence(resource_group_name, public_ip_name):
        print(f'Public IP {public_ip_name} already exists')
    else:
        print(f'Creating public IP {public_ip_name}')
    public_ip = network_client.public_ip_addresses.begin_create_or_update(
        resource_group_name,
        public_ip_name,
        {
            'location': location,
            'sku': {'name': 'Basic'},
            'public_ip_allocation_method': public_ip_allocation_method,
            'public_ip_address_version': 'IPv4'
        }
    ).result()

# Define the function to create a network interface
def create_network_interface(network_client, resource_group_name, network_interface_name, location, ip_config_name, subnet_id, public_ip_id):
    if network_client.network_interfaces.check_existence(resource_group_name, network_interface_name):
        print(f'Network interface {network_interface_name} already exists')
    else:
        print(f'Creating network interface {network_interface_name}')
    network_interface = network_client.network_interfaces.begin_create_or_update(
        resource_group_name,
        network_interface_name,
        {
            'location': location,
            'ip_configurations': [{
                'name': ip_config_name,
                'subnet': {'id': subnet_id},
                'public_ip_address': {'id': public_ip_id}
            }]
        }
    ).result()

# Define the function to create a virtual machine
def create_virtual_machine(compute_client, resource_group_name, virtual_machine_name, location, network_interface_id, vm_size):
    if compute_client.virtual_machines.check_existence(resource_group_name, virtual_machine_name):
        print(f'Virtual machine {virtual_machine_name} already exists')
    else:
        print(f'Creating virtual machine {virtual_machine_name}')
    vm = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name,
        virtual_machine_name,
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
                'computer_name': virtual_machine_name,
                'admin_username': 'azureuser',
                'admin_password': 'Azure123456789'
            },
            'network_profile': {
                'network_interfaces': [{
                    'id': network_interface_id
                }]
            }
        }
    ).result()

