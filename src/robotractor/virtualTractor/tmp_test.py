from TPM import TPM



tractor = TPM("../keys/robot-server.pub", "../keys/tractor01.priv")
server = TPM("../keys/tractor01.pub", "../keys/robot-server.priv")


#Generate a session key on the server to send to the tractor
session_key = server.pki_encrypt(server.session_key)

# Send David the session key

#David initialized his TPM with the session key.
my_key = tractor.pki_decrypt(session_key)
tractor.session_key = my_key

print "Session: "+tractor.session_key

for i in range(10):
    t = tractor.encrypt("hello server")
    print "Ciphered: "+t
    print "decrypted: "+ server.decrypt(t)

    s = server.encrypt("Hello david.")
    print tractor.decrypt(s)


