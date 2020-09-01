from typing import Sequence
from py_ecc.optimized_bn128 import G2, final_exponentiate, neg, pairing, FQ12
from pybls.typings import Message, G1Point, G2Point
from pybls.g2pubs.hash import hash_to_g1

TARGET = FQ12.one()


def pair_check(sig: G1Point, msg: Message, pub: G2Point) -> bool:
    f = pairing(neg(G2), sig, final_exponentiate=False) * pairing(
        pub, hash_to_g1(msg), final_exponentiate=False
    )
    return final_exponentiate(f) == TARGET


def pair_check_multiple(
    sig: G1Point, pubs: Sequence[G2Point], msgs: Sequence[Message]
) -> bool:
    size = len(pubs)
    if size == 0:
        raise Exception("empty pubkey vector")
    if len(msgs) == 0:
        raise Exception("empty message vector")
    if size != len(msgs):
        raise Exception("size of public keys and messages should be equal")
    f = pairing(neg(G2), sig, final_exponentiate=False)
    for i in range(size):
        f *= pairing(pubs[i], hash_to_g1(msgs[i]), final_exponentiate=False)
    return final_exponentiate(f) == TARGET
