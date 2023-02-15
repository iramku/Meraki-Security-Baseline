# Meraki Security Baseline

This Python script helps you check if your Meraki MX firewalls are configured according to Cisco Meraki's best practice design. The script checks for implementation of the best practices according to the following document: [General MX Best Practices](https://documentation.meraki.com/Architectures_and_Best_Practices/Cisco_Meraki_Best_Practice_Design/Best_Practice_Design_-_MX_Security_and_SD-WAN/General_MX_Best_Practices)

## Prerequisites
To use this script, you'll need:

- Python 3.x installed on your computer
- A Cisco Meraki account
- API keys for the Meraki Dashboard

## Getting Started

- Clone the repository to your local machine.
- Install the required dependencies 
- Open the api_keys_org_ids.txt file and add your Meraki Dashboard API key and organization ID in the following format:
```
<api_key>,<org_id>
```
- Run the script using the following command:
```
python Meraki-Baseline-Security.py
```
The script will output a table with the following information for each MX firewall in your Meraki organization:

- Organization name
- Network name
- License edition
- Anti-malware status
- Intrusion prevention status
- Spoof protection status

| Organization                  | Network                             | License Edition   | Anti-Malware | Intrusion Prevention | Spoof Protection |
| :---------------------------- | :---------------------------------- | :---------------- | :----------- | :------------------- | :--------------- |
| Org A                         | Org A Net A                         | Advanced Security | enabled      | prevention           | block            |
| Org B                         | Org B Net A                         | Advanced Security | enabled      | prevention           | block            |
| Org C                         | Org C Net A                         | Enterprise        | disabled     | disabled             | log              |

## License
This script is licensed under the GPL-3.0 License. See the LICENSE file for more information.
