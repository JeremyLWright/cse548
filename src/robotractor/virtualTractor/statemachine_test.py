from statemachine import StateMachine
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import math
import json
import time
import logging
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
			#process the message
     			#msg.reply("ACK\n%(body)s" % msg).send()
			#print "we got a message"
			q.put(msg)
			
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 #earth's radius at equator
    
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    
    return d

def haversine(lon1, lat1, lon2, lat2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees) using Haversine Formula
        """
    #convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    #haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def at_rest(cargo):
    #1st state. Required?
    print "AT_REST State"
    newState = "DOWNLOAD_PATH"
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
    #xmppreplybody = xmppreply['body']
    usabledata = json.loads(xmppreply['body'])
    print usabledata
    #print data['job']

    se_lat = usabledata['boundary'][0]['fields']['se_lat']
    se_long = usabledata['boundary'][0]['fields']['se_long']
    nw_lat = usabledata['boundary'][0]['fields']['nw_lat']
    nw_long = usabledata['boundary'][0]['fields']['nw_long']
    print se_lat

    #pull in the waypoints next

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
    
    wp1 = [33.382676, -111.912677]  #test coords 1
    wp2 = [34.382676, -110.912677]  #test coords 2 in gmaps decimal degree format
    
    tractorspeed = 15.0     #km per hour tractor speeds up to 40km for road driving. assume avg speed 15km in field?
    # that's 15000 meters per hour, 250 meters per minute, 4.16666666667 meters per second
    # do we assume every second the tractor moves 4.17 meters?

    #wp2 
    
    hdist = distance(wp1, wp2)
    miles = hdist * 0.62137
    print("distance is " + str(hdist) + " km or " + str(miles) + " miles")
    
    timetocomplete = hdist / tractorspeed
    print(str(timetocomplete) + "hours to finish")

    #calculate new location based on movement
    #set cargo to be location data
    #if new location is outside bounds
    #newState = "OFF"
    
    newState = "UPLOAD_DATA"
    return (newState, cargo)

def upload_data(cargo):
    #4th state
    print "UPLOAD_DATA State"
    
    #form a json object with the status data
    #use pycrypto to encrypt this data
    #put this encrypted data in the body of a xmpp msg

    wp1 = (33.382676, -111.912677)
    msg = json.dumps(wp1)
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
    m.add_state("OFF", None, end_state = 1)
    
    m.set_start("AT_REST")
    m.run(1)
