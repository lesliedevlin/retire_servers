import json
import datetime
import pytz
import iso8601
import cpapi

apiCon = None

def create_api_connection():
    from config import clientid, clientsecret

    global apiCon
    apiCon = cpapi.CPAPI()

    apiCon.key_id = clientid
    apiCon.secret = clientsecret

    resp = apiCon.authenticateClient()

def get_server_data():
    data, autherr = apiCon.getServerListDeactiv()
    count = data['count']
    print "\n%d inactive servers:" % (count)
    servers = data['servers']
    for server in servers:
        server_id = server['id']
        server_hostname = server['hostname']

        # How many days should a server be offline before being retired?
        retire_days = 7

        # Create aware datetime object for last time seen
	lastseen = iso8601.parse_date(server['last_state_change'])

        # Create aware datetime object for current time
        utc = pytz.timezone('UTC')
        utcnow = datetime.datetime.utcnow()
        utcnow_aware = utc.fromutc(utcnow)

        # Calculate time diff in days
        # After 1 day, last_state_change rounds off to days
        time_diff = utcnow_aware - lastseen
        diff_days = int(time_diff.days)

        # Don't retire a server that's already retired
        if server['group_name'] == 'Retired':
            print "Server %s already retired -- ignoring." % server_hostname
        # If server older than retire_days days, move to retired
        elif (diff_days > retire_days and server_id):
            data, autherr = apiCon.doRetireServer(server_id)
            if not autherr:
                print "Server %s retired successfully." % server_hostname
        else:
            print "Unable to move server."
            if not server_id:
                print "Server: %s (id %s) does not exist.\n" % (server_hostname, server_id)
            elif diff_days <= retire_days:
                print "Server %s has been offline for %s days.\n" % (server_hostname, diff_days)



#---MAIN---------------------------------------------------------------------

create_api_connection()
get_server_data()
