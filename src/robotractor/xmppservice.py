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
            #msg.reply("Processing command\n%(body)s" % msg)
            #msg.reply("Now sending tou some databse stuff.")
            data = serializers.serialize("json", Tractor.objects.all())
            msg.reply(data).send()

if __name__ == '__main__':
    print Tractor.objects.all()
    xmpp = EchoBot('robot@54.83.55.95', 'robot')
    xmpp.connect()
    xmpp.process(block=True)
	
