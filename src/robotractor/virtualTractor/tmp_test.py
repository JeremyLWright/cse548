from TPM import TPM



tractor = TPM("../keys/robot-server.pub", "../keys/tractor01.priv")
server = TPM("../keys/tractor01.pub", "../keys/robot-server.priv")


#Generate a session key on the server to send to the tractor
tractors_session_key = server.pki_encrypt(server.session_key)

print "Session: "+tractors_session_key

for i in range(10):
    t = tractor.encrypt("hello server")
    print "Ciphered: "+t
    print "decrypted: "+ tractor.decrypt(t)


