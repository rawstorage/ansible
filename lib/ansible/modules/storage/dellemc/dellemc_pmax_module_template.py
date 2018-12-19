#!/usr/bin/python
# Copyright: (C) 2018, DellEMC
# Author(s): Paul Martin <paule.martin@dell.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
author:
  - "Paul Martin (@rawstorage)"
short_description: "Template for creating Modules"
version_added: "2.8"
description:
  - "This module has been tested against UNI 9.0. Every effort has been made
  to verify the scripts run with valid input. These modules are a tech preview."
module: dellemc_pmax_createsg
options:

requirements:
  - Ansible
  - "Unisphere for PowerMax version 9.0 or higher."
  - "VMAX All Flash, VMAX3, or PowerMax storage Array."
  - "PyU4V version 3.0.0.8 or higher using PIP python -m pip install PyU4V"
'''
EXAMPLES = '''
---
- name: "Provision Storage For DB Cluster"
  connection: local
  hosts: localhost
  vars:
    array_id: 000197600156
    password: smc
    sgname: Ansible_SG
    unispherehost: "192.168.1.123"
    universion: "90"
    user: smc
    verifycert: false

  tasks:
    - name: "Create New Storage Group and add data volumes"
      dellemc_pmax_createsg:
        array_id: "{{array_id}}"
        cap_unit: GB
        num_vols: 1
        password: "{{password}}"
        sgname: "{{sgname}}"
        slo: Diamond
        srp_id: SRP_1
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        user: "{{user}}"
        verifycert: "{{verifycert}}"
        vol_size: 1
        workload: None
        volumeIdentifier: 'REDO'
'''
RETURN = '''
dellemc_pmax_createsg:
    description: Information about storage group created
    returned: success
    type: dict
    sample: '{
        "some_detail": {
            "somevalues":
            }
        }'
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dellemc import dellemc_pmax_argument_spec, pmaxapi


def main():
    changed = False
    argument_spec = dellemc_pmax_argument_spec()
    argument_spec.update(dict(
        valuesneededforthismodule=dict(type='str', required=True),
    ))
    module = AnsibleModule(argument_spec=argument_spec)
    # Setup connection to API and import  modules.
    conn = pmaxapi(module)
    pmax_prov = conn.provisioning
    # Compile a list of existing storage groups.

    #Your Code here


    facts = "some facts to help user in task"
    result = {'state': 'info', 'changed': changed}
    module.exit_json(ansible_facts={'some_detail': facts}, **result)


if __name__ == '__main__':
    main()
