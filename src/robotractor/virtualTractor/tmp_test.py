from TPM import TPM
tractor = TPM("../keys/robot-server.pub", "../keys/tractor01.priv")
server = TPM("../keys/tractor01.pub", "../keys/robot-server.priv")
t = tractor.encrypt("hello server")
server.decrypt(t)

