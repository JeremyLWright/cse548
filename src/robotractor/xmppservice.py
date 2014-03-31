import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "robotractor.settings")
from backend.models import Tractor
from django.core import serializers

class EchoBot(ClientXMPP):
    def __init__(self, jid, password):
        super(EchoBot, self).__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        
    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            sender = msg['from'];
            import pdb
            pdb.set_trace()
            #msg.reply("Processing command\n%(body)s" % msg)
            #msg.reply("Now sending tou some databse stuff.")
            tractor = Tractor.objects.filter(jabberid=sender.username+'@'+sender.domain)
            data = serializers.serialize("json", tractor)
            msg.reply(data).send()

if __name__ == '__main__':
    print Tractor.objects.all()
    xmpp = EchoBot('tractor-server@jabber.co.nz', 'Q9MTZx14we')
    xmpp.connect()
    xmpp.process(block=True)
	
