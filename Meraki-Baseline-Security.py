import requests
from prettytable import PrettyTable
table= PrettyTable()

# API endpoint for organizations
org_url = 'https://api.meraki.com/api/v1/organizations'

# API endpoint for firewalls
fw_url = 'https://api.meraki.com/api/v1/networks/{}/appliance/'

# Read the file containing the API keys and org IDs
with open("api_keys_org_ids.txt", "r") as f:
    lines = f.readlines()

# Create a table header
table.field_names = ["Organization", "Network", "License Edition", "Anti-Malware", "Intrusion Prevention", "Spoof Protection"]
table.align["Organization"] = "l"
table.align["Network"] = "l"
table.align["License Edition"] = "l"
table.align["Anti-Malware"] = "l"
table.align["Intrusion Prevention"] = "l"
table.align["Spoof Protection"] = "l"

# Loop through each line in the file
for line in lines:
    api_key, org_id = line.strip().split(",")

    # Get list of networks for the selected organization
    networks_url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    response = requests.get(networks_url, headers={'X-Cisco-Meraki-API-Key': api_key})
    networks = response.json()

    # Filter the networks to find MX firewalls
    mx_firewalls = [network for network in networks if network['productTypes'][0] == 'appliance']

    # Loop through the firewall list
    for firewall in mx_firewalls:

         # Get the organization name
        org_response = requests.get(f"{org_url}/{org_id}", headers={'X-Cisco-Meraki-API-Key': api_key})
        org = org_response.json()
        org_name = org['name']

        
        # Network Name
        network_name = firewall['name']

        # Get the current license version for the MX
        licenses_response = requests.get(f"{org_url}/{org_id}/licensing/coterm/licenses/", headers={'X-Cisco-Meraki-API-Key': api_key}).json()
        license_edition = "Enterprise"
        for item in licenses_response:
            counts = item.get('counts')
            for count in counts:
                if count.get('model').startswith('MX'):
                    editions = item.get('editions')
                    for edition in editions:
                        if 'Advanced Security' in edition.get('edition'):
                            license_edition = 'Advanced Security'
                        break

        # Get anti-malware settings
        fw_url_antimalware = (fw_url + "security//malware")
        firewall_settings = requests.get(fw_url_antimalware.format(firewall['id']), headers={'X-Cisco-Meraki-API-Key': api_key}).json()
        anti_malware_enabled = firewall_settings['mode']

        # Get intrusion prevention settings
        fw_url_intrusion = (fw_url + "security//intrusion")
        firewall_settings = requests.get(fw_url_intrusion.format(firewall['id']), headers={'X-Cisco-Meraki-API-Key': api_key}).json()
        if 'mode' in firewall_settings:
            intrusion_prevention_enabled = firewall_settings['mode']
        else:
            intrusion_prevention_enabled = "Not Supported"
    
        # Get Ip Spoof Protection settings
        fw_url_spoof = (fw_url + "firewall//settings")
        firewall_settings = requests.get(fw_url_spoof.format(firewall['id']), headers={'X-Cisco-Meraki-API-Key': api_key}).json()
        spoof_protection_enabled = firewall_settings['spoofingProtection']['ipSourceGuard']['mode']
        
        # Add rows to the table
        table.add_row([org_name, network_name, license_edition, anti_malware_enabled, intrusion_prevention_enabled, spoof_protection_enabled ])

# Print the results
print (table)