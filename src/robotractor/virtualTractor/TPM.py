from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

class EncryptionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

"""This class simulates a hardware module who's keys are hardware protected at the factory."""
class TPM():
    def __init__(self, pubKey, privKey):
        self.key = {}
        
        self.key["private"] = RSA.importKey(open(privKey).read())
        self.key["public"] = RSA.importKey(open(pubKey).read())
        pass

    def encrypt(self, msg):
        h = SHA.new(msg)
        cipher = PKCS1_v1_5.new(self.key["public"])
        return cipher.encrypt(msg+h.digest())

    def decrypt(self, ciphermsg):
        dsize = SHA.digest_size
        sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15

        cipher = PKCS1_v1_5.new(self.key["private"])
        message = cipher.decrypt(ciphermsg, sentinel)

        digest = SHA.new(message[:-dsize]).digest()
        if digest!=message[-dsize:]:                # Note how we DO NOT look for the sentinel
            raise EncryptionError("Message verification failed.  Communication channel possibly compromised.")
        return message[:-dsize]
