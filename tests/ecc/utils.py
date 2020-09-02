from py_ecc.optimized_bn128 import b as BN128_B, b2 as BN128_B2, is_on_curve
from py_ecc.optimized_bn128 import field_modulus, curve_order
from py_ecc.optimized_bn128 import G1, G2, multiply, normalize
from py_ecc.optimized_bn128 import FQ, FQ2
from py_ecc.utils import prime_field_inv as inv
from random import randint


P, Q = field_modulus, curve_order
P_MINUS3_OVER4 = ((P - 3) * inv(4, P)) % P
P_MINUS1_OVER2 = ((P - 1) * inv(2, P)) % P
P_PLUS1_OVER4 = ((P + 1) * inv(4, P)) % P
R = 2**256


def rand_fs():
    return randint(0, curve_order-1)


def rand_fq():
    return FQ(randint(0, field_modulus - 1))


def rand_r():
    return randint(0, R)


def rand_fq2():
    return FQ2([rand_fq(), rand_fq()])


def rand_g1():
    p = multiply(G1, rand_fs())
    assert is_valid_g1_point(p)
    return p


def rand_g2():
    p = multiply(G2, rand_fs())
    assert is_valid_g2_point(p)
    return p


def is_valid_g1_point(p):
    return is_on_curve(p, BN128_B)


def is_valid_g2_point(p):
    return is_on_curve(p, BN128_B2)


def compress_g1(p):
    sgn = sign_of_g1(p)
    normalized = normalize(p)
    compressed = normalized[0].n
    if sgn:
        compressed = compressed | 0x8000000000000000000000000000000000000000000000000000000000000000
    return compressed, normalized[1]


def compress_g2(p):
    sgn = sign_of_g2(p)
    normalized = normalize(p)
    compressed = [normalized[0].coeffs[0], normalized[0].coeffs[1]]
    if sgn:
        compressed[0] = compressed[0] | 0x8000000000000000000000000000000000000000000000000000000000000000
    return compressed, normalized[1]


def sign_of_g1(p_0):
    p_1 = normalize(p_0)
    return p_1[1].sgn0


def sign_of_g2(p_0):
    p_1 = normalize(p_0)
    return p_1[1].sgn0


def sqrt(a):
    """
    https://eprint.iacr.org/2012/685.pdf
    algoritm 2 for fq
    algoritm 9 and fq2
    """

    def _try_sqrt_in_fp2(a):
        a1 = a ** P_MINUS3_OVER4
        alpha = a1 * a1 * a
        x0 = a1 * a
        if alpha == FQ2([-1, 0]):
            return FQ2((x0.coeffs[1], x0.coeffs[0]))
        alpha = alpha + FQ2.one()
        alpha = alpha ** P_MINUS1_OVER2
        return alpha * x0

    def _try_sqrt_in_fp(a: FQ) -> FQ:
        return a ** P_PLUS1_OVER4

    x = 0
    if isinstance(a, FQ):
        x = _try_sqrt_in_fp(a)
    elif isinstance(a, FQ2):
        x = _try_sqrt_in_fp2(a)
    return x if x * x == a else None
