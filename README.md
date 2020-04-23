# Python

## Collect_sys_details.py

This script sources, and calculates the charges/cost for cpus, memory etc., from values collected by the Ansible setup module (for example: `ansible localhost -m setup --tree /home/vagrant/.ansible/facts`)

The output of the collected information is then written in CSV format to a file. 
