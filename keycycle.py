from __future__ import division
from __future__ import print_function
import argparse
import json
import traceback
import aoulib as aou
import kickshaws as ks

'''
# keycycle.py

This script provides a command-line interface to the aoulib
library's 'managekeys.cycle_keys' function, suitable for scheduling/
automating (e.g., via cron).

## Setting up and running

See the "Setting up" section in the documentation at the top of the
refresh.py module -- note that you can skip setting up the database
specification (db_spec) config file (if you just are wanting to cycle keys).

When finished, you should have the following files set up and configured:

- enclave/aou-api-spec.json (or named as you wish)
- enclave/site-config.json

## Actually running keycycle.py 

Example:

    source venv/bin/activate
    python keycycle.py --site-config enclave/site-config.json --aou-api-spec-fpath enclave/aou-api-spec.json
   
... or, use the provided shell script: ...
    
    ./runkeycycle.sh

## Setting up as cron job

The included script runkeycycle.sh shows how to 
initiate the virtual env first and then run the software. Customize for your
environment.

'''

log = ks.smart_logger('keycycle')

def main():
  log.info('========== keycycle.sh started ============')
  try:
    # Parse cmd line arg.
    p = argparse.ArgumentParser()
    p.add_argument('--site-config',
                   required=True,
                   help='Path to a site-config file (see docs in refresh.py).')
    p.add_argument('--aou-api-spec-fpath',
                   required=True,
                   help='Path to a custom aou-api-spec JSON file.')
    args = p.parse_args()
    cfg = ks.slurp_json(args.site_config)
    api_spec_fname = args.aou_api_spec_fpath
    log.info('api spec filename: ' + api_spec_fname)
    api_spec = ks.slurp_json(api_spec_fname)

    # Do the actual key cycling.
    msg = 'Key ID to delete is: ' + aou.managekeys.get_key_id(api_spec)
    log.info(msg)
    result = aou.managekeys.cycle_keys(api_spec)
    msg = 'Keys cycled. ' 
    log.info(msg + str(result))
    print(msg)

  except Exception, ex:
    log.error(traceback.format_exc())
    print('Error. Please check log.')
    if cfg['should-send-emails']:
      ks.send_email(
        cfg['to-email'],
        cfg['from-email'],
        'AoU GCP Key Cycling ' + ks.today_as_str(),
        'There was an issue during key cycling. Please check the log.')

if __name__ == '__main__': main()

