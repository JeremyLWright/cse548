from statemachine import StateMachine
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from math import *
import json
import time
from Queue import Queue

### to do: Add XMPP connection capability to connect to XMPP Server
## secure connection is established with XMPP server

## xmpp session will send encrypted json object in xmpp stanza
## this object is to be decrypted, deserialized, then processed as a job

## simulator must also serialize a status update as a json object, encrypt, and send through the stanza to the XMPP server

class EchoBot(ClientXMPP):
	def __init__(self, jid, password, q):
		ClientXMPP.__init__(self, jid, password)
		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.queue = q
		
	def session_start(self, event):
		self.send_presence()
		self.get_roster()
		
	def message(self, msg):
		if msg['type'] in ('chat', 'normal'):
			q.put(msg)

def coordinatesAfterMovement(heading, speedkm, duration):

    earthradius = 6371
    x = speedkm * sin(heading * pi / 180) * duration / 3600
    y = speedkm * cos(heading * pi / 180) * duration / 3600

    newLat = m.currentpos[0] + 180 / pi * y / earthradius
    newLong = m.currentpos[1] + 180 / pi / sin(m.currentpos[0] * pi / 180) * x / earthradius

    return (newLat, newLong)

def distance(origin, destination):
    print("getting data from " + str(origin) + " to " + str(destination))
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 #earth's radius at equator
    
    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = radius * c

    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1)*cos(dlon)
    bearing = degrees(atan2(y,x))
    #bearing = atan2(y,x)
    #bearing = (bearing + 360) % 360

    #bearing = atan2(cos(lat1)*sin(lat2)-sin(lat1)*cos(lon2-lon1), sin(lon2-lon1)*cos(lat2))
    #bearing = degrees(bearing)
    havtuple = (d, bearing)

    return havtuple

def at_rest(cargo):
    #1st state. Required?
    print "AT_REST State"
    newState = "DOWNLOAD_PATH"
    return (newState, cargo)

def shutdown(cargo):
    print "shutting down"
    msg = "shutting down"
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)
    xmpp.disconnect()

    newstate = "OFF"
    return (newState, cargo)

def download_path(cargo):
    #2nd state
    print "DOWNLOAD_PATH State"

    #key = RSA.importKey(open('privkey.key').read())
    #dsize = SHA.digest_size
    #sentinel = Random.new().read(15+dsize)
    #cipher = PKCS1_v1_5.new(key)
    
    msg = "gimmeinfo"
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)
    xmppreply = q.get()
    #print xmppreply
    xmppreplybody = xmppreply['body']
    usabledata = json.loads(xmppreply['body'])
    #print usabledata
    #import pdb
    #pdb.set_trace()
    #print usabledata['job']

    if (usabledata == "KillTractor"):
	print "killing tractor"
	newState = "SHUTTING_DOWN"
    	return (newState, cargo)

    #pull in the waypoints next
    m.waypoints = usabledata['waypoints']
    num_waypoints = len(m.waypoints)
    print("#wps: " + str(num_waypoints))

    if (m.running == 0):
	    for i in range(num_waypoints):
		temp_lat = m.waypoints[i]['fields']['lat']
		temp_long = m.waypoints[i]['fields']['longitude']
		m.waypointlist.append((temp_lat, temp_long))
    print m.waypointlist

    if (m.lastwp == 0):
	m.nextwp = 1
        
    if (m.running == 0):
	m.currentpos = m.waypointlist[0]

    print("currentpos: " + str(m.currentpos))

    m.endwp = num_waypoints

    if (m.lastwp == m.endwp):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)

    m.se_lat = usabledata['boundary'][0]['fields']['se_lat']
    m.se_long = usabledata['boundary'][0]['fields']['se_long']
    m.nw_lat = usabledata['boundary'][0]['fields']['nw_lat']
    m.nw_long = usabledata['boundary'][0]['fields']['nw_long']
    print ("boundary is from: " + str((m.nw_lat, m.nw_long)) + " to " + str((m.se_lat, m.se_long)))

    checklat = round(m.waypointlist[m.nextwp][0], 5)
    checklong = round(m.waypointlist[m.nextwp][1], 5)
    checktup = (checklat, checklong)
    cposlat = round(m.currentpos[0], 5)
    cposlong = round(m.currentpos[1], 5)
    checkcpostup = (cposlat, cposlong)
    print ("nextwp: " + str(checktup))
    print ("cposwp: " + str(checkcpostup))

    if ((abs(checkcpostup[0] - checktup[0]) < .0001) and (abs(checkcpostup[1] - checktup[1]) < .0001)):
    	m.lastwp = m.nextwp
	if (m.nextwp + 1 < num_waypoints):
		m.nextwp = m.nextwp + 1
	print("hit waypoint: " + str(m.lastwp) + " and moving to waypoint: " + str(m.nextwp))
   
    #decrypt this body with pycrypto
    #message = cipher.decrypt(replybody, sentinel)
    #process the data
    
    newState = "EXECUTE_PATH"
    return (newState, cargo)

def execute_path(cargo):

    #print boundarylong
    #print boundarylat

    #3rd state
    print "EXECUTE_PATH State"
    
    #for testing
    #wp1 = (33.421980, -111.939967)  #test coords 1
    #wp2 = (33.419097, -111.938111)  #test coords 2 in gmaps decimal degree format
    #m.currentpos = wp1
    #m.nextwp = 1
    
    tractorspeed = 15.0     #km per hour tractor speeds
    
    #hdist = distance(wp1, wp2)
    hdata = distance(m.currentpos, m.waypointlist[m.nextwp])
    hdist = hdata[0]
    hhead = hdata[1]
    print("distance is " + str(hdist) + " km")
    print("heading is " + str(hhead))
    
    #timetocomplete = hdist / tractorspeed
    #print(str(timetocomplete) + "hours to finish")

    #calculate new location based on movement
    m.running = 1
    newcoords = coordinatesAfterMovement(hhead, tractorspeed, 5)
    m.currentpos = newcoords
    print ("tractor moved to: " + str(newcoords))

    #if new location is outside bounds

    if (m.currentpos[0] > m.nw_lat):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)

    if (m.currentpos[1] < m.nw_long):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)

    if (m.currentpos[0] < m.se_lat):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)

    if (m.currentpos[1] > m.se_long):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)
    
    newState = "UPLOAD_DATA"
    return (newState, cargo)

def upload_data(cargo):
    #4th state
    print "UPLOAD_DATA State"
    
    #form a json object with the status data
    #use pycrypto to encrypt this data
    #put this encrypted data in the body of a xmpp msg

    currentPos = m.currentpos
    msg = json.dumps(currentPos)
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)

    time.sleep(1)
    
    newState = "AT_REST"
    return (newState, cargo)

if __name__ == '__main__':
    q = Queue()     
    xmpp = EchoBot('tractor01@jabber.co.nz', 'Q9MTZx14we',q)
    xmpp.connect()
    xmpp.process(block=False)
    m = StateMachine(xmpp, q)
    
    m.add_state("AT_REST", at_rest)
    m.add_state("DOWNLOAD_PATH", download_path)
    m.add_state("EXECUTE_PATH", execute_path)
    m.add_state("UPLOAD_DATA", upload_data)
    m.add_state("SHUTTING_DOWN", shutdown)
    m.add_state("OFF", None, end_state = 1)
    
    m.set_start("AT_REST")
    m.run(1)
