import { randomBytes, hexlify, hexZeroPad } from 'ethers/lib/utils';
import { BigNumber } from 'ethers';

export const FIELD_ORDER = BigNumber.from('0x30644e72e131a029b85045b68181585d97816a916871ca8d3c208c16d87cfd47');

export const ZERO = BigNumber.from('0');

export function toBig(n: any): BigNumber {
  return BigNumber.from(n);
}

export function randHex(n: number): string {
  return hexlify(randomBytes(n));
}

export function randBig(n: number): BigNumber {
  return toBig(randomBytes(n));
}

export function bigToHex(n: BigNumber): string {
  return hexZeroPad(n.toHexString(), 32);
}

export function randFs(): BigNumber {
  const r = randBig(32);
  return r.mod(FIELD_ORDER);
}

export function randFsHex(): string {
  const r = randBig(32);
  return bigToHex(r.mod(FIELD_ORDER));
}
