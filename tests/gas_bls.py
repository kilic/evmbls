from brownie import accounts
from ecc.utils import sqrt, rand_fq, rand_fq2, rand_r
from ecc.utils import rand_g1, is_valid_g1_point, is_valid_g2_point, compress_g1, compress_g2, rand_g2
from ecc.mapping import map_to_g1_ti, map_to_g1_ft, map_to_g1_ti_and_helps, map_to_g1_ft_and_helps
from py_ecc.optimized_bn128 import field_modulus, FQ, FQ2, normalize, G1, neg, b as BN128_B, b2 as BN128_B2
import pytest

TRY = 100
MINUS_ONE = FQ(field_modulus-1)
NON_RESIDUE_1 = MINUS_ONE
NON_RESIDUE_2 = FQ2([9, 1])
ONE = FQ.one()
NEG_G1 = normalize(neg(G1))


def g1_to_call(point):
  point = normalize(point)
  return [point[0].n, point[1].n]


def fq2_to_call(e_0):
  return [e_0.coeffs[0], e_0.coeffs[1]]


def g2_to_call(point):
  point = normalize(point)
  return [point[0].coeffs[0], point[0].coeffs[1], point[1].coeffs[0], point[1].coeffs[1]]


def to_32(n):
  return n.to_bytes(32, "big")


@pytest.fixture(scope="module")
def gas_tester(GasBLS):
  return accounts[0].deploy(GasBLS)


def test_map_to_point_ti(gas_tester):  # pylint: disable=redefined-outer-name
  total = 0
  for _ in range(TRY):
    r = rand_r() % field_modulus
    _ = map_to_g1_ti(r)
    total += gas_tester.mapToPointTIGasCost.call(r)
  print("test_map_to_point_ti average cost", total // TRY)


def test_map_to_point_ti_helped(gas_tester):  # pylint: disable=redefined-outer-name
  total = 0
  for _ in range(TRY):
    r = rand_r() % field_modulus
    _, helps = map_to_g1_ti_and_helps(r)
    total += gas_tester.mapToPointTIHelpedGasCost.call(r, helps)
  print("test_map_to_point_ti_helped average cost", total // TRY)


def test_map_to_point_ft(gas_tester):  # pylint: disable=redefined-outer-name
  total = 0
  for i in range(TRY):
    r = rand_r() % field_modulus
    _ = map_to_g1_ft(r)
    total += gas_tester.mapToPointFTGasCost.call(to_32(r))
  print("test_map_to_point_ft average cost", total // TRY)


def test_map_to_point_ft_helped(gas_tester):  # pylint: disable=redefined-outer-name
  total = 0
  for i in range(TRY):
    r = rand_r() % field_modulus
    _, helps = map_to_g1_ft_and_helps(r)
    total += gas_tester.mapToPointFTHelpedGasCost.call(r, helps)
  print("test_map_to_point_ft_helped average cost", total // TRY)
