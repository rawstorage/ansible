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
  - "Deleting a Masking View WILL remove access to storage devices for the 
  hosts in the view, please use this module with extreme caution as this is 
  destructive. This module has been tested against UNI 9.0. Every effort has
  been made to verify the scripts run with valid input. These modules are a
  tech preview."
module: dellemc_pmax_createsg
options:
  array_id:
    description:
      - "Integer 12 Digit Serial Number of PowerMAX or VMAX array."
    required: true
  unispherehost:
    description:
      - "Fully Qualified Domain Name or IP address of Unisphere for PowerMax
      host."
    required: true
  universion:
    description:
      - "Integer, version of unipshere software  e.g. 90"
    required: true
  verifycert:
    description:
      - "Boolean, security check on ssl certificates"
    type: bool
    required: true
  user:
    description:
      - "Unisphere username"
  password:
    description:
      - "password for Unisphere user"
requirements:
  - Ansible
  - "Unisphere for PowerMax version 9.0 or higher."
  - "VMAX All Flash, VMAX3, or PowerMax storage Array."
  - "PyU4V version 3.0.0.8 or higher using PIP python -m pip install PyU4V"
'''
EXAMPLES = '''
---
- name: "Delete Masking View"
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
    - name: "Delete Masking View"
      dellemc_pmax_deletemaskingview:
        array_id: "{{array_id}}"
        password: "{{password}}"
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        user: "{{user}}"
        verifycert: "{{verifycert}}"
        maskingview_name: "Ansible_MV"
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
            maskingview_name=dict(type='str', required=True)
        )
    )
    module = AnsibleModule(argument_spec=argument_spec)
    # Setup connection to API and import  modules.
    conn = pmaxapi(module)
    dellemc = conn.provisioning
    mvlist = dellemc.get_masking_view_list()
    # Check if Masking View Exists
    if module.params['maskingview_name'] in mvlist:
        dellemc.delete_masking_view(
            maskingview_name=module.params['maskingview_name']
        )
        changed = True

    else:
        module.fail_json(msg='Masking View Does Not Exist, Please verify the '
                             'input parameters', changed=changed)

    module.exit_json(changed=changed)
    facts = "some facts to help user in task"
    result = {'state': 'info', 'changed': changed}
    module.exit_json(ansible_facts={'some_detail': facts}, **result)


if __name__ == '__main__':
    main()


