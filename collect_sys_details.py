#!/usr/bin/python3

import sys
import os
import json
import csv
import time
import math
from pathlib import Path

def _obtain_detail(filename):

    # Open file and load the JSON data
    with open(filename) as f:
      data = json.load(f)

    # Source the required data from the JSON
    memory = data['ansible_facts']['ansible_memtotal_mb']
    cpus = data['ansible_facts']['ansible_processor_vcpus']

    # Calculate the cost per item
    cost_mem = math.ceil(memory / 1024) * 20
    cost_cpus = cpus * 100

    return {
        "memory": memory,
        "cost_memory": cost_mem,
        "cpus": cpus,
        "cost_cpus": cost_cpus,
    }

# Main/Start
# Setup variables from those being passed, plus location of this script
if ( len(sys.argv) == 2 ):
    factspath = Path(sys.argv[1])
else:
    sys.exit('Path to files is required.')
dirpath = os.path.dirname(os.path.realpath(__file__))
outfile = Path(dirpath + '/system_details.csv')

# Start processing
# Confirm Path passed to script is valid, else...
if factspath.is_dir():

    # Remove output file if exists
    if outfile.is_file():
      outfile.unlink()

    # Sleep to allow Logstash to reset pointer within output file
    time.sleep(3)

    # Obtain list of Ansible facts files
    with os.scandir(factspath) as filename:
      # Run through list of files
      for entry in filename:
        # Gather system details via function
        output_detail = _obtain_detail(entry.path)
        # Open output file, create if missing, append data if existing
        with open(outfile, 'a', newline='') as csvfile:
          # Use CSV library to write collected data to file, starting with hostname of server in CSV format
          outwrite = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
          outwrite.writerow([entry.name, output_detail['memory'], output_detail['cost_memory'], output_detail['cpus'], output_detail['cost_cpus']])
else:
    print('Directory not found: ' + str(factspath))
