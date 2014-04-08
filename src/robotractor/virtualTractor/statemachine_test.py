from statemachine import StateMachine
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from math import *
from TPM import TPM
import json
import time
from Queue import Queue

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
			q.put(msg, True)
			print "Message in queue:"+str(q.qsize())

def calcBearing(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)
    result = atan2(y, x)
    return degrees(result) 

def coordinatesAfterMovement(heading, speedkm, duration):
    earthradius = 6371
    x = speedkm * sin(heading * pi / 180) * duration / 3600
    y = speedkm * cos(heading * pi / 180) * duration / 3600
    newLat = m.currentpos[0] + 180 / pi * y / earthradius
    newLong = m.currentpos[1] + 180 / pi / sin(m.currentpos[0] * pi / 180) * x / earthradius
    return (newLat, newLong)

def calcDistance(origin, destination):
    radius = 6371
    lat1, lon1 = origin
    lat2, lon2 = destination
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dLon = lon2 - lon1
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    dist = radius * c
    return dist

def at_rest(cargo):
    print "AT_REST State"
    newState = "DOWNLOAD_PATH"
    return (newState, cargo)

def shutdown(cargo):
    print "SHUTTING_DOWN state"
    msg = "shutting down"
    msg = m.tractor.encrypt(msg)
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)
    xmpp.disconnect()
    m.running = 0
    newState = "OFF"
    return (newState, cargo)

def download_path(cargo):
    print "DOWNLOAD_PATH State"

    if (m.running == 0):
	msg = "gimmekey"
    	msg = m.tractor.pki_encrypt(msg)
        xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)
        xmppreply = q.get()
	xmppreplybody = xmppreply['body']
	m.tractor.session_key = m.tractor.pki_decrypt(xmppreply['body'])
	#print m.tractor.session_key
	
    msg = "gimmeinfo"
    msg = m.tractor.encrypt(msg)
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)
    xmppreply = q.get(True)

    #print xmppreply
    xmppreplybody = xmppreply['body']
    usabledata = json.loads(m.tractor.decrypt(xmppreply['body']))
    print usabledata
    #print usabledata['job']

    if (usabledata == "KillTractor"):
	print "killing tractor"
	newState = "SHUTTING_DOWN"
    	return (newState, cargo)

    #pull in the waypoints
    m.waypoints = usabledata['waypoints']
    num_waypoints = len(m.waypoints)
    #print("#wps: " + str(num_waypoints))

    if (m.running == 0):
	    for i in range(num_waypoints):
		temp_lat = m.waypoints[i]['fields']['lat']
		temp_long = m.waypoints[i]['fields']['longitude']
		m.waypointlist.append((temp_lat, temp_long))
    print m.waypointlist

    #if (m.nextwp == 0):
	#m.nextwp = 1
        
    if (m.running == 0):
	m.currentpos = m.waypointlist[0]
	m.nextwp = 1

    #print("currentpos: " + str(m.currentpos))

    m.endwp = (num_waypoints - 1)

    m.se_lat = usabledata['boundary'][0]['fields']['se_lat']
    m.se_long = usabledata['boundary'][0]['fields']['se_long']
    m.nw_lat = usabledata['boundary'][0]['fields']['nw_lat']
    m.nw_long = usabledata['boundary'][0]['fields']['nw_long']
    #print ("boundary is from: " + str((m.nw_lat, m.nw_long)) + " to " + str((m.se_lat, m.se_long)))

    checklat = round(m.waypointlist[m.nextwp][0], 5)
    checklong = round(m.waypointlist[m.nextwp][1], 5)
    checktup = (checklat, checklong)
    cposlat = round(m.currentpos[0], 5)
    cposlong = round(m.currentpos[1], 5)
    checkcpostup = (cposlat, cposlong)
    print ("cposwp: " + str(checkcpostup))
    print ("nextwp: " + str(checktup))

    if ((abs(checkcpostup[0] - checktup[0]) < .0001) and (abs(checkcpostup[1] - checktup[1]) < .0001)):
    	m.lastwp = m.nextwp
	m.currentpos = m.waypointlist[m.lastwp]
	if ((m.nextwp + 1) < num_waypoints):
		m.nextwp += 1
	print "===="
	print("hit waypoint: " + str(m.lastwp+1) + " and moving to waypoint: " + str(m.nextwp+1))
	print "===="

    if (m.lastwp == m.endwp):
	newState = "SHUTTING_DOWN"
	return (newState, cargo)
    
    newState = "EXECUTE_PATH"
    return (newState, cargo)

def execute_path(cargo):
    print "EXECUTE_PATH State"
    
    tractorspeed = 10.0     #km per hour tractor speeds
    
    hdist = calcDistance(m.currentpos, m.waypointlist[m.nextwp])
    hhead = calcBearing(m.currentpos, m.waypointlist[m.nextwp])
    print("distance is " + str(hdist) + " km")
    print("heading is " + str(hhead))

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
    print "UPLOAD_DATA State"

    currentPos = m.currentpos
    msg = json.dumps(currentPos)
    msg = m.tractor.encrypt(msg)
    xmpp.send_message(mto="tractor-server@jabber.co.nz", mbody=msg)

    #time.sleep(1)
    
    newState = "AT_REST"
    print "///////////////////////////////////////////"
    return (newState, cargo)

if __name__ == '__main__':
	try:
	    q = Queue(1)     
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
	finally:
	    xmpp.disconnect()
