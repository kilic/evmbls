import hashlib

from py_ecc.optimized_bn128 import FQ, b as BN128_B, is_on_curve, field_modulus
from py_ecc.utils import prime_field_inv
from ecc.utils import sqrt, is_valid_g1_point

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
  x = raw_hash % field_modulus
  y = FQ.zero()
  while True:
    y = x * x * x + BN128_B
    y = sqrt(y)
    if y is not None:
      break
    x += one
  point = (x, y, FQ.one())
  assert is_valid_g1_point(point)
  return point


#    sqrt(-3)
Z0 = FQ(0x0000000000000000b3c4d79d41a91759a9e4c7e359b6b89eaec68e62effffffd)
#   (sqrt(-3) - 1)  / 2
Z1 = FQ(0x000000000000000059e26bcea0d48bacd4f263f1acdb5c4f5763473177fffffe)


def inverse(x):
  return prime_field_inv(x.n, field_modulus)


def map_to_g1_ft(raw_hash):
  from py_ecc.optimized_bn128 import b as BN128_B

  one = FQ.one()
  x = FQ(raw_hash % field_modulus)

  decision = bool(sqrt(x))

  def find_point(x):
    yy = x * x * x + BN128_B
    y = sqrt(yy)
    if y is not None:
      point = (x, -y, one) if not decision else (x, y, one)
      assert is_valid_g1_point(point)
      return point
    else:
      return None

  a0 = x * x + BN128_B + one
  a1 = x * Z0
  a2 = inverse(a1 * a0)
  a1 = a1 * a1 * a2

  # x1
  a1 = x * a1
  x = Z1 - a1
  point = find_point(x)
  if point:
    return point

  # x2
  x = -(x + one)
  point = find_point(x)
  if point:
    return point

  # x3
  x = a0 * a0
  x = x * x * a2 * a2 + one
  # must be on curve
  point = find_point(x)
  if not point:
    raise "bad implementation"
  return point


def map_to_g1_ti_and_helps(raw_hash):
  one = FQ.one()
  x = raw_hash % field_modulus
  y = FQ.zero()
  helps = []
  while True:
    t = x * x * x + BN128_B
    y = sqrt(t)
    if y is not None:
      helps.append(y)
      break
    else:
      h = sqrt(-t)
      assert h is not None
      helps.append(h)
    x += one
  point = (x, y, FQ.one())
  assert is_valid_g1_point(point)
  return point, helps


def map_to_g1_ft_and_helps(raw_hash):
  from py_ecc.optimized_bn128 import b as BN128_B
  helps = []
  one = FQ.one()
  zero = FQ.zero()
  x = FQ(raw_hash % field_modulus)

  decision = False
  decision_el = sqrt(x)
  if decision_el is not None:
    helps.append(decision_el)
    decision = True
  else:
    h = sqrt(-x)
    assert h is not None
    helps.append(h)

  def find_point(x):
    t = x * x * x + BN128_B
    y = sqrt(t)
    if y is not None:
      point = (x, -y, one) if not decision else (x, y, one)
      assert is_valid_g1_point(point)
      helps.append(y)
      return point
    else:
      h = sqrt(-t)
      assert h is not None
      helps.append(h)
      return None

  a0 = x * x + BN128_B + one
  a1 = x * Z0
  a2 = inverse(a1 * a0)
  helps.append(a2)
  a1 = a1 * a1 * a2

  # x1
  a1 = x * a1
  x = Z1 - a1
  point = find_point(x)
  if point is not None:
    helps.append(zero)
    helps.append(zero)
    return point, helps

  # x2
  x = -(x + one)
  point = find_point(x)
  if point is not None:
    helps.append(zero)
    return point, helps

  # x3
  x = a0 * a0
  x = x * x * a2 * a2 + one
  # must be on curve
  point = find_point(x)
  if point is None:
    raise "bad implementation"
  return point, helps
