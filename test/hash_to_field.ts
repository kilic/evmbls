import { BigNumber } from 'ethers';
import { sha256, arrayify, hexlify } from 'ethers/lib/utils';

export function hash_to_field(domain: Uint8Array, msg: Uint8Array, outLen: number): Uint8Array {
  if (domain.length > 255) {
    throw new Error('bad domain size');
  }

  const out: Uint8Array = new Uint8Array(outLen);

  const len0 = 64 + msg.length + 2 + 1 + domain.length + 1;
  const in0: Uint8Array = new Uint8Array(len0);
  // zero pad
  let off = 64;
  // msg
  in0.set(msg, off);
  off += msg.length;
  // l_i_b_str
  in0.set([(outLen >> 8) & 0xff, outLen & 0xff], off);
  off += 2;
  // I2OSP(0, 1)
  in0.set([0], off);
  off += 1;
  // DST_prime
  in0.set(domain, off);
  off += domain.length;
  in0.set([domain.length], off);

  const b0 = sha256(in0);

  const len1 = 32 + 1 + domain.length + 1;
  const in1: Uint8Array = new Uint8Array(len1);
  // b0
  in1.set(arrayify(b0), 0);
  off = 32;
  // I2OSP(1, 1)
  in1.set([1], off);
  off += 1;
  // DST_prime
  in1.set(domain, off);
  off += domain.length;
  in1.set([domain.length], off);

  const b1 = sha256(in1);

  // b_i = H(strxor(b_0, b_(i - 1)) || I2OSP(i, 1) || DST_prime);
  const ell = Math.floor((outLen + 32 - 1) / 32);
  let bi = b1;

  for (let i = 1; i < ell; i++) {
    const ini: Uint8Array = new Uint8Array(32 + 1 + domain.length + 1);
    const nb0 = BigNumber.from(b0);
    const nbi = BigNumber.from(bi);
    const nb = nb0.xor(nbi);
    const tmp = arrayify(nb);
    ini.set(tmp, 0);
    let off = 32;
    ini.set([1 + i], off);
    off += 1;
    ini.set(domain, off);
    off += domain.length;
    ini.set([domain.length], off);

    out.set(arrayify(bi), 32 * (i - 1));
    bi = sha256(ini);
  }

  out.set(arrayify(bi), 32 * (ell - 1));
  return out;
}
