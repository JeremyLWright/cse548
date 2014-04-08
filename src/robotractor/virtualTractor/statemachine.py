from string import upper
from TPM import TPM

class StateMachine:
    def __init__(self, xmpp, q):
	self.tractor = TPM("../keys/robot-server.pub", "../keys/tractor01.priv")
	#pubkey first #privkey second
	#encrypt with pub key
	#decrypt with priv key
        self.handlers = {}  #each handler is a function for a state
        self.startState = None
        self.endStates = []
        self.queue = q
	self.waypointdata = None
	self.waypointlist = []
        self.lastwp = 0
        self.nextwp = 0
        self.endwp = 0
        self.se_lat = 0.0
        self.se_long = 0.0
	self.nw_lat = 0.0
	self.nw_long = 0.0
	self.currentpos = (0.0, 0.0)
	self.running = 0
            
    def add_state(self, name, handler, end_state=0):  #default state is not an endstate
        name = upper(name)
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
            
    def set_start(self, name):
        self.startState = upper(name)
        
    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise "Error", "must call .set_start() before .run()" 
    
        if not self.endStates:
            raise "Error", "at least one state must be an end state"
        
        while 1:
            (newState, cargo) = handler(cargo)
            
            if upper(newState) in self.endStates:
                break
            else:
                handler = self.handlers[upper(newState)]
