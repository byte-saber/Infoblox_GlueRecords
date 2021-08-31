There have been some instances where GLUE RECORDS of all sub-domains in a parent domain disappear. This causes SERVFAIL responses for any query pertaining to these affected subdomains. 

This script helps to re-add glue records by first temporarily assigning a 'DummyNS' to the sub-domain as NS-group. Then re-assigns the original NS-group to the sub-domain thereby adding the correct glue records to parent domain

The zones must be listed in a file the path of which is the first command line argument. Alternatively, user input can be taken as a list which needs modification in `read_zone_list()`

Finally, it restarts the grid members simultaneously if needed.

Usage:
```
$ ./Infoblox_addMissingGlueRecords.py ./listOfZones.txt
```
