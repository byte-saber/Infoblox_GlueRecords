There have been some instances where GLUE RECORDS of all sub-domains in a Authoritative DNS zone have disappeared without any known trigger. It causes SERVFAIL responses for any query pertaining to these affected subdomains leading to operational instability and high severity incidents.. 

This script helps to re-add glue records by first temporarily assigning a 'DummyNS' to the sub-domain as NS-group. Then re-assigns the original NS-group to the sub-domain thereby adding the correct glue records to parent domain.

The zones must be listed in a file the path of which is the first command line argument. Alternatively, user input can be taken as a list which needs modification in `read_zone_list()` definition and declaration.
Finally, it restarts the grid members simultaneously if needed after all affected zones have been worked upon.

The script uses Infoblox WAPI. Credentials can be fetched from passbolt and stored in a `.env` file in the local directory, or use your own if you have appropriate privilege.


Usage:
```
$ ./Infoblox_addMissingGlueRecords.py infoblox.example.com ./listOfZones.txt
```
