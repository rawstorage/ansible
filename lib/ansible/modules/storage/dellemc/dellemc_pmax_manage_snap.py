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
short_description: "Snapshot managment modules, to be used to link, relink
or unlink snapshots to target storage groups"
version_added: "2.8"
description:
  - "This module has been tested against UNI 9.0. Every effort has been made
  to verify the scripts run with valid input. These modules are a tech preview."
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
  sgname:
    description:
      - "Storage Group Name for Source Snapshot"  
  snapshotname:
    description:
      - "Snapshot Name to be actioned upon"  
  target_sgname:
    description:
      - "Name of Target Storage Group where snapshot is to be linked, 
      relinked or unlinked, if SG doesn't exist for link operation it will 
      get created automatically by the API."  
  action:
    description:
      - "Link will link a snapshot to a target storage group, relink is used to
       refresh a snapshot resetting the data on the target storage group 
       volumes to that of the initial link. Unlink will remove the 
       association between the snapshot and the target storage group, 
       if snapshot time to live value has passed the snapshot will be 
       deleted after the unlink operation"  
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
    - name: "Link a Snapshot"
      dellemc_pmax_manage_snap:
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        array_id: "{{array_id}}"
        user: "{{user}}"
        password: "{{password}}"
        verifycert: "{{verifycert}}"
        sgname: "Ansible_SG"
        snapshotname: "Ansbile_Snap"
        target_sgname: "Ansible_lnk_SG"
        action: "link"
    
    - name: "relink a Snapshot"
      dellemc_pmax_manage_snap:
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        array_id: "{{array_id}}"
        user: "{{user}}"
        password: "{{password}}"
        verifycert: "{{verifycert}}"
        sgname: "Ansible_SG"
        snapshotname: "Ansbile_Snap"
        target_sgname: "Ansible_lnk_SG"
        action: "relink"

    - name: "unink a Snapshot"
      dellemc_pmax_manage_snap:
        unispherehost: "{{unispherehost}}"
        universion: "{{universion}}"
        array_id: "{{array_id}}"
        user: "{{user}}"
        password: "{{password}}"
        verifycert: "{{verifycert}}"
        sgname: "Ansible_SG"
        snapshotname: "Ansbile_Snap"
        target_sgname: "Ansible_lnk_SG"
        action: "unlink"    
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
            sgname=dict(type='str', required=True),
            snapshotname=dict(type='str', required=True),
            target_sgname=dict(type='str', required=True),
            action=dict(type='str', choices=['link', 'relink', 'unlink'],
                        required=True)
        )
    )
    # Make REST call to Unisphere Server and execute create snapshot/

    module = AnsibleModule(argument_spec=argument_spec)
    # Setup connection to API and import  modules.
    conn = pmaxapi(module)
    # Import provisioning and replication functions
    prov = conn.provisioning
    rep = conn.replication

    sglist = prov.get_storage_group_list()
    snaplist = rep.get_storagegroup_snapshot_list(module.params['sgname'])

    if module.params['sgname'] in sglist and module.params['snapshotname'] \
            in snaplist:
        if module.params['action'] == 'link':
            rep.modify_storagegroup_snap(source_sg_id=module.params['sgname'],
                                         snap_name=module.params[
                                             'snapshotname'],
                                         target_sg_id=module.params[
                                             'target_sgname'],
                                         link=True, new_name=None, gen_num=0,
                                         async=True)
        elif module.params['action'] == 'relink':
            rep.modify_storagegroup_snap(source_sg_id=module.params['sgname'],
                                         snap_name=module.params[
                                             'snapshotname'],
                                         target_sg_id=module.params[
                                             'target_sgname'],
                                         relink=True, gen_num=0, async=True)
        elif module.params['action'] == 'unlink':
            rep.modify_storagegroup_snap(source_sg_id=module.params['sgname'],
                                         snap_name=module.params[
                                             'snapshotname'],
                                         target_sg_id=module.params[
                                             'target_sgname'],
                                         unlink=True, gen_num=0,
                                         async=True)

        changed = True

        module.exit_json(changed=changed, msg='SnapVX Action completed '
                                              'Sucessfully')

    else:
        module.fail_json(msg='No Snapshot found with the supplied Parameters')

    facts = "some facts to help user in task"
    result = {'state': 'info', 'changed': changed}
    module.exit_json(ansible_facts={'some_detail': facts}, **result)


if __name__ == '__main__':
    main()
