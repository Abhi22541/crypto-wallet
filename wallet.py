# install dependencies
# pip install ecdsa

import os
import hashlib
import ecdsa

def generate_private_key():
    return os.urandom(32)

def generate_public_key(private_key):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return b'\x04' + vk.to_string()

def generate_wallet_address(public_key):
    sha256_pk = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_pk)
    return ripemd160.hexdigest()

if __name__ == "__main__":
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    wallet_address = generate_wallet_address(public_key)

    print("Private Key:", private_key.hex())
    print("Public Key:", public_key.hex())
    print("Wallet Address:", wallet_address)
