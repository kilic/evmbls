import hashlib

from py_ecc.optimized_bn128 import FQ, b, is_on_curve
from pybls.utils import sqrt

HASHER_KECCAK = "KECCAK"
HASHER_SHA256 = "SHA256"
HASHER = HASHER_KECCAK

MAPPER_TI = "TI"
MAPPER_FT = "FT"
MAPPER = MAPPER_TI


def hasher_use_keccak():
    global HASHER
    HASHER = HASHER_KECCAK


def HASHER_use_sha256():
    global HASHER
    HASHER = HASHER_SHA256


def hasher_use_ti():
    global MAPPER
    MAPPER = MAPPER_TI


def hasher_use_ft():
    global MAPPER
    MAPPER = MAPPER_FT


def sha256(domain, msg):
    data = domain + msg
    return hashlib.sha256(data).digest()


def keccak256(domain, msg):
    data = domain + msg
    return hashlib.sha256(data).digest()


def _hash(domain, msg):
    if HASHER == HASHER_KECCAK:
        return keccak256(domain, msg)
    elif HASHER == HASHER_SHA256:
        return sha256(domain, msg)
    else:
        raise "not expected"


def hash_to_g1(domain, msg):
    raw_hash = _hash(domain, msg)
    return map_to_g1(raw_hash)


def map_to_g1(raw_hash):
    if MAPPER == MAPPER_TI:
        return map_to_g1_ti(raw_hash)
    elif MAPPER == MAPPER_FT:
        return map_to_g1_ft(raw_hash)
    else:
        raise "not expected"


def map_to_g1_ti(raw_hash):
    one = FQ.one()
    x = raw_hash
    while True:
        y = x * x * x + b
        y = sqrt(y)
        if y is not None:
            break
        x += one
    h = (x, y, FQ.one())
    assert is_on_curve(h, b)
    return h


def map_to_g1_ft(raw_hash):
    raise "to be implemented"
