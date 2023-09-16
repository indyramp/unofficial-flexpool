import unicodedata
from hashlib import pbkdf2_hmac, sha256
import hmac
from math import ceil
from typing import List


n = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001


def mnemonic_to_seed(mnemonic: str, passphrase: str) -> bytes:
    """
    Uses BIP39 standard to derive a seed from entropy bytes.
    """
    salt_str: str = "mnemonic" + passphrase
    salt = unicodedata.normalize("NFKD", salt_str).encode("utf-8")
    mnemonic_normalized = unicodedata.normalize(
        "NFKD", mnemonic).encode("utf-8")
    seed = pbkdf2_hmac("sha512", mnemonic_normalized, salt, 2048)

    assert len(seed) == 64
    return seed


BLOCK_SIZE = 32


def extract(salt: bytes, ikm: bytes) -> bytes:
    h = hmac.new(salt, ikm, sha256)
    return h.digest()


def expand(L: int, prk: bytes, info: bytes) -> bytes:
    N: int = ceil(L / BLOCK_SIZE)
    bytes_written: int = 0
    okm: bytes = b""

    for i in range(1, N + 1):
        if i == 1:
            h = hmac.new(prk, info + bytes([1]), sha256)
            T: bytes = h.digest()
        else:
            h = hmac.new(prk, T + info + bytes([i]), sha256)
            T = h.digest()
        to_write = L - bytes_written
        if to_write > BLOCK_SIZE:
            to_write = BLOCK_SIZE
        okm += T[:to_write]
        bytes_written += to_write
    assert bytes_written == L
    return okm


def extract_expand(L: int, key: bytes, salt: bytes, info: bytes) -> bytes:
    prk = extract(salt, key)
    return expand(L, prk, info)


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def key_gen(seed: bytes) -> bytes:
    # KeyGen
    # 1. PRK = HKDF-Extract("BLS-SIG-KEYGEN-SALT-", IKM || I2OSP(0, 1))
    # 2. OKM = HKDF-Expand(PRK, keyInfo || I2OSP(L, 2), L)
    # 3. SK = OS2IP(OKM) mod r
    # 4. return SK

    L = 48
    okm = extract_expand(
        L, seed + bytes([0]), b"BLS-SIG-KEYGEN-SALT-", bytes([0, L]))
    return int_to_bytes(int.from_bytes(okm, "big") % n)


def ikm_to_lamport_sk(ikm: bytes, salt: bytes) -> bytes:
    return extract_expand(32 * 255, ikm, salt, b"")


def parent_sk_to_lamport_pk(parent_sk: bytes, index: int) -> bytes:
    salt = index.to_bytes(4, "big")
    ikm = int.from_bytes(parent_sk, "big").to_bytes(32, "big")
    not_ikm = bytes([e ^ 0xFF for e in ikm])  # Flip bits
    lamport0 = ikm_to_lamport_sk(ikm, salt)
    lamport1 = ikm_to_lamport_sk(not_ikm, salt)

    lamport_pk = bytes()
    for i in range(255):
        lamport_pk += sha256(lamport0[i * 32: (i + 1) * 32]).digest()
    for i in range(255):
        lamport_pk += sha256(lamport1[i * 32: (i + 1) * 32]).digest()

    return sha256(lamport_pk).digest()


def derive_child_sk(parent_sk: bytes, index: int) -> bytes:
    """
    Derives a hardened EIP-2333 child private key, from a parent private key,
    at the specified index.
    """
    lamport_pk = parent_sk_to_lamport_pk(parent_sk, index)
    return key_gen(lamport_pk)


def _derive_path(sk: bytes, path: List[int]) -> bytes:
    for index in path:
        sk = derive_child_sk(sk, index)
    return sk


def master_sk_to_farmer_sk(master: bytes) -> bytes:
    return _derive_path(master, [12381, 8444, 0, 0])


mnemonic = input("Enter your mnemonic > ")
seed = mnemonic_to_seed(mnemonic, "")
master_sk = key_gen(seed)
print("Derived Farmer Secret Key:", "0x" +
      bytes(master_sk_to_farmer_sk(master_sk)).hex())
