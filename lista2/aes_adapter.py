from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import ANSIX923, PKCS7
from cryptography.hazmat.backends import default_backend
from getpass import getpass
import random
import jks
import os


_supported_modes = {
    'CBC': modes.CBC,
    'CTR': modes.CTR,
    'OFB': modes.OFB
}

class AdapterError(Exception):
    pass

"""
In encrypted message first 16 bytes of n bytes represents initialization vector, next n-16 bytes represents encrypted message.
"""
class AESAdapter:
    def __init__(self, encryption_mode, key_store_path, key_store_pass, key_id):
        """
        Init AES with args:
            encryption_mode - one of supported modes: 'CBC', 'CTR' or 'OFB'
            key_store_path - path to keystore
            key_store_pass - password to keystore
            key_id - key identifier from keystore
        """
        # load key from keystore
        try:
            key_store = jks.KeyStore.load(key_store_path, key_store_pass)
            key = key_store.entries[key_id].key
        except KeyError as ex:
            raise AdapterError(f'Incorrect key name: {key_id}')
        except jks.util.KeystoreSignatureException as ex:
            raise AdapterError('Incorrect keystore password.')
        except FileNotFoundError as ex:
            raise AdapterError('Incorrect keystore path: ', key_store_path)

        # init AES
        try:
            self._mode = _supported_modes[encryption_mode]
        except KeyError as ex:
            raise AdapterError(f'Encription mode {encryption_mode} is not supported. Try one of: { ", ".join(_supported_modes.keys()) }')

        self._iv = os.urandom(16)
        self._alg = algorithms.AES(key)
        self._backend = default_backend()
        self._enc_mode = encryption_mode

    def inc_iv(self):
        self._iv = (int(self._iv.hex(), 16) + 1).to_bytes(16, 'big')
        
    def _encrypt(self, message):
        if self._enc_mode == 'CBC':
            padder = PKCS7(128).padder()
            message = padder.update(message) + padder.finalize()

        iv = self._iv
        self.inc_iv()
        cipher = Cipher(self._alg, self._mode(iv), self._backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(message) + encryptor.finalize()
        return ct, iv

    def encrypt(self, message):
        """
        Returns encrypted message. First 16 bytes represents initialization vector.
        """
        ct, iv = self._encrypt(message)
        # print(len(ct), len(iv))
        return iv + ct

    def _decrypt(self, message, iv):
        cipher = Cipher(self._alg, self._mode(iv), self._backend)
        decryptor = cipher.decryptor()
        dec = decryptor.update(message) + decryptor.finalize()
        
        if self._enc_mode == 'CBC':
            unpadder = PKCS7(128).unpadder()
            dec = unpadder.update(dec) + unpadder.finalize()
        
        return dec

    def decrypt(self, message):
        """
        Decrypt message. First 16 bytes of message should be initialization vector.
        """
        iv, ct = message[0:16], message[16:]
        return self._decrypt(ct, iv)


def get_oracle(aes_adapter):
    """
    Return oracle for AES instance.
    """
    def oracle(message):
        return aes_adapter.encrypt(message)
    
    return oracle

def get_challenger(aes_adapter):
    """
    Return challenger for AES instance.
    """
    def challenge(message1, message2):
        pick = random.randint(0, 1)
        if pick == 0:
            msg = message1
        else:
            msg = message2
        ct_with_iv = aes_adapter.encrypt(msg)
        return ct_with_iv

    return challenge

def get_decoder(aes_adapter):
    """
    Return decoder for AES instance.
    """
    def decode(cipthertext):
        return aes_adapter.decrypt(cipthertext)
    
    return decode
