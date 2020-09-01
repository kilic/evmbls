from brownie import accounts
from bls.utils import sqrt, rand_fq, rand_fq2, rand_g1, is_valid_g1_point, is_valid_g2_point, compress_g1, compress_g2, rand_g2
from py_ecc.optimized_bn128 import field_modulus, FQ, FQ2, normalize, G1, neg, b as BN128_B, b2 as BN128_B2
import pytest

FUZZ = 10
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


@pytest.fixture(scope="module")
def bls_tester(TestBLS):
    return accounts[0].deploy(TestBLS)


def test_quadratic_non_residue_fq(bls_tester):  # pylint: disable=redefined-outer-name
    assert bls_tester.isNonResidueFQ(NON_RESIDUE_1)

    for _ in range(FUZZ):
        e_0 = rand_fq()
        if sqrt(e_0):
            assert not bls_tester.isNonResidueFQ(e_0)
        else:
            assert bls_tester.isNonResidueFQ(e_0)


def test_quadratic_non_residue_fq2(bls_tester):  # pylint: disable=redefined-outer-name
    assert bls_tester.isNonResidueFQ2(fq2_to_call(NON_RESIDUE_2))

    for _ in range(FUZZ):
        e_0 = rand_fq2()
        if sqrt(e_0):
            assert not bls_tester.isNonResidueFQ2(fq2_to_call(e_0))
        else:
            assert bls_tester.isNonResidueFQ2(fq2_to_call(e_0))


def test_negative_g1_one(bls_tester):  # pylint: disable=redefined-outer-name
    pass


def test_is_on_curve_g1(bls_tester):  # pylint: disable=redefined-outer-name
    def rand_point_not_on_curve():
        x_0 = FQ.zero()
        while True:
            x_0 = rand_fq()
            y_non_residue = x_0 * x_0 * x_0 + BN128_B
            if sqrt(y_non_residue) is None:
                break
        y_0 = rand_fq()
        point = (x_0, y_0, FQ.one())
        assert not is_valid_g1_point(point)  # with very high probablity
        return point

    # uncompressed valid
    for _ in range(FUZZ):
        point = rand_g1()
        assert bls_tester.isOnCurveG1(g1_to_call(point))

    # uncompressed invalid
    for _ in range(FUZZ):
        point = rand_point_not_on_curve()
        assert not bls_tester.isOnCurveG1(g1_to_call(point))

    # compressed valid
    for _ in range(FUZZ):
        point = rand_g1()
        compressed, _ = compress_g1(point)
        assert bls_tester.isOnCurveG1Compressed(compressed)

    # compressed invalid
    for _ in range(FUZZ):
        point = rand_point_not_on_curve()
        compressed, _ = compress_g1(point)
        assert not bls_tester.isOnCurveG1Compressed(compressed)


def test_is_on_curve_g2(bls_tester):  # pylint: disable=redefined-outer-name
    def rand_point_not_on_curve():
        x_0 = FQ2.zero()
        while True:
            x_0 = rand_fq2()
            y_non_residue = x_0 * x_0 * x_0 + BN128_B2
            if sqrt(y_non_residue) is None:
                break
        y_0 = rand_fq2()
        point = (x_0, y_0, FQ2.one())
        assert not is_valid_g2_point(point)  # with very high probablity
        return point

    # uncompressed valid
    for _ in range(FUZZ):
        point = rand_g2()
        assert bls_tester.isOnCurveG2(g2_to_call(point))

    # uncompressed invalid
    for _ in range(FUZZ):
        point = rand_point_not_on_curve()
        assert not bls_tester.isOnCurveG2(g2_to_call(point))

    # compressed valid
    for _ in range(FUZZ):
        point = rand_g2()
        compressed, _ = compress_g2(point)
        assert bls_tester.isOnCurveG2Compressed(compressed)

    # compressed valid
    for _ in range(FUZZ):
        point = rand_point_not_on_curve()
        compressed, _ = compress_g2(point)
        assert not bls_tester.isOnCurveG2Compressed(compressed)
