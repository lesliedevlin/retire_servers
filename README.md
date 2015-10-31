# retire_servers

This Python script will retire any servers that have not been detected by Halo after several days.
This will help large cloud environments with high server turnover reduce the clutter in their
Halo accounts. 

The script takes advantage of the new server field last_state_change and is intended to be run from
cron on a restricted-access tools server or bastion box once daily.  Since last_state_change is only 
expressed in whole days after a server has been offline for more than 24 hours, there is little advantage
to running it more often.

You will need a config.py file that includes your API key and secret key -- see the sample file.
The keypair must have full access (read-write), and as always, you will want to protect the security
of those keys with restrictive permissions.  You will also need a version of cpapi from
October 30, 2015 or later.

By default, servers that have been deactivated for more than 7 days will be retired by the script.
To change this, modify the value of retire_days.

Note that servers must be deactivated before they can be moved into the retired group.
Missing servers should be investigated rather than automatically retired.

