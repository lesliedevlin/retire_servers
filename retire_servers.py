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

        # create aware datetime object for last time seen
	lastseen = iso8601.parse_date(server['last_state_change'])

        # create aware datetime object for current time
        utc = pytz.timezone('UTC')
        utcnow = datetime.datetime.utcnow()
        utcnow_aware = utc.fromutc(utcnow)
	print "%s (id %s) was last seen at %s." % (server_hostname, server_id, lastseen)

        # calculate time diff in days
        # after 1 day, last_state_change rounds off to days
        time_diff = utcnow_aware - lastseen
	print "Last seen %s, now %s.\n" % (lastseen, utcnow_aware)
	print "Server was last seen %s days ago.\n" % int(time_diff.days)
        print "Hostname: %s, ID %s\n" % (server_hostname, server_id)

        # don't retire a server that's already retired
        if server['group_name'] == 'Retired':
            print "Server %s already retired -- ignoring." % server_id
        # if server older than 7 days, move to retired
        elif (int(time_diff.days) > 7 and server_id):
            data, autherr = apiCon.doRetireServer(server_id)
            if not autherr:
                print "Server %s retired successfully." % server_id
        else:
            print "Unable to move server."
            if not server_id:
                print "Server: %s does not exist.\n" % server_id
            elif int(time_diff.days) <= 7:
                print "Server %s has been offline for fewer than 7 days.\n" % server_id


#---MAIN---------------------------------------------------------------------

create_api_connection()
get_server_data()
