from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import base64

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
        self.pub_cipher = PKCS1_OAEP.new(self.key["public"])
        self.priv_cipher = PKCS1_OAEP.new(self.key["private"])
        pass

    def encrypt(self, msg):
        return base64.b64encode(self.pub_cipher.encrypt(msg))

    def decrypt(self, ciphermsg):
        return self.priv_cipher.decrypt(base64.b64decode(ciphermsg))
