#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 22 22:31:57 2021

@author: tushar2911@gmail.com
@name  : Infoblox_addMissingGlueRecords.py
@short_description: Assigns temporary ns-group, and then re-assigns the original ns-group to a DNS zone
@description: Uses Infoblox WAPI to first assign a ns-group DummyNS to the affected DNS zones stored in a file
              and then reassigns the original ns-group 
              This helps resolves the issue observed where glue records of sevaral sub-domains in an 
              authoritative zone go missing even though the configuration for name-servers exist.
@input : 1. URL of infoblox, 2. path of file where the list of zones is stored
@output: None
"""

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
import json
import time
import sys

load_dotenv()

class glueRecords():
    url_common = 'https://'+sys.argv[1]+'/wapi/v2.9.1/'
    sess=requests.Session()
    sess.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    
    def read_zone_list(self,filepath):
        """ 
        @description: Read the affected zones from a file
        @input: Filepath string
        @output: list of zones
        """
        # sentinel=''
        # print('Enter list of zones: (Terminate list by an extra newline)')
        # zones='\n'.join(iter(input,sentinel)).splitlines()
        try:
            with open(filepath,'r') as f:
                zones=f.readlines()
            return zones
        except Exception as e:
            print("Exception occured : ",e)
            
    def get_grid(self):
        """
        @description: get _ref of the grid
        @input: None
        @output:_ref string for the grid
        """
        try:
            url_grid = self.url_common + 'grid'
            return self.sess.get(url_grid,auth=HTTPBasicAuth(os.getenv('infoblox_api_user'), os.getenv('infoblox_api_password')),verify=False).json()[0]['_ref']
        except Exception as e:
            print("Exception occured : ",e)


    def restart_grid(self):
        """
        @description: Restart grid services if needed after reassigning NS-group to affected zones
        @input: None
        @output: None
        """
        try:
            payload = json.dumps({
                                  "restart_option": "RESTART_IF_NEEDED",
                                  "member_order": "SIMULTANEOUSLY",
                                  "service_option": "ALL"
                                })
            self.sess.headers.update({'Content-Type': 'application/json'})
            self.sess.post(self.url_common+self.get_grid()+"?_function=restartservices", data=payload, verify=False)
        except Exception as e:
            print("Exception occured : ",e)
        
        
    def rectify_zones(self):
        """
        @description: Assign a temp and reassign actual NS-group to affected zones
        @input: None
        @output: None
        """
        try:
            url_authzone = self.url_common + r'zone_auth?_return_fields=ns_group&fqdn='
            for zone in self.read_zone_list(sys.argv[2]):
                zone_object = self.sess.get(url_authzone+zone,verify=False)
                zone_ref=zone_object.json()[0]['_ref']
                zone_ns_group=zone_object.json()[0]['ns_group']
                self.url_authzone_put= self.url_common + zone_ref
                
                
                payload_dummy_ns = 'ns_group=DummyNS'
                sess.put(self.url_authzone_put,data=payload_dummy_ns,verify=False)
                time.sleep(1)
                payload_ns='ns_group='+zone_ns_group
                sess.put(self.url_common+zone_ref,data=payload_ns,verify=False)
        except Exception as e:
            print("Exception occured : ",e)


def main():
    glueRecordsFix=glueRecords()
    glueRecordsFix.rectify_zones()
    glueRecordsFix.restart_grid()
    
if __name__ == "__main__":
    main()

