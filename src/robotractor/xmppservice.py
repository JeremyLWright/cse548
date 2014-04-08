import logging
import json
from django.utils import timezone
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from virtualTractor.TPM import TPM

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "robotractor.settings")
from backend.models import Tractor, RunningJob, Waypoint, Job, WorkingBoundary, CompletedPoint
from django.core import serializers

import pdb
class EchoBot(ClientXMPP):
    def __init__(self, jid, password):
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.tpm = TPM("keys/robot-server.pub", "keys/tractor01.priv")
        
    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sender = msg['from']
            print "=========================="
            print "Received Raw message, "+msg['body']
            data = self.tpm.decrypt(msg['body'])
            print "Decrypted Data "+data

            tractor = Tractor.objects.filter(jabberid=sender.username+'@'+sender.domain)
            active_job = RunningJob.objects.filter(tractor=tractor)[0]
            if data != 'gimmeinfo':
                points = json.loads(data)
                c = CompletedPoint()
                c.lat = points[0]
                c.longitude = points[1]
                c.active_job = active_job
                c.save()

            waypoints = Waypoint.objects.filter(job=active_job.job).order_by('sort_order')

            active_job.last_checkin_time = timezone.now()
            if not active_job.active:
                print "Sending Kill Machine..."
                msg.reply(json.dumps("KillTractor")).send()
            else:
                active_job.save()
                print "Sending data."
                data = {}
                data["boundary"] = json.loads(serializers.serialize("json", [active_job.job.boundary]))
                data["tractor"] = json.loads(serializers.serialize("json", tractor))
                data["job"]     = json.loads(serializers.serialize("json", [active_job.job]))
                data["waypoints"] = json.loads(serializers.serialize("json", waypoints))
                rdata = json.dumps(data)
                print "Send Data: "+rdata
                edata = self.tpm.encrypt(rdata)
                print "Encrypted: "+edata
                msg.reply(edata).send()
            print "================================"

if __name__ == '__main__':
    print Tractor.objects.all()
    #xmpp = EchoBot('tractor-server@54.83.55.95', 'Q9MTZx14we')
    xmpp = EchoBot('tractor-server@jabber.co.nz', 'Q9MTZx14we')
    xmpp.connect()
    xmpp.process(block=True)
	
