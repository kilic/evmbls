import * as mcl from './mcl';
import { wallet } from './provider';
import { GasBls } from '../types/ethers-contracts/GasBls';
import { assert } from 'chai';
import { GasBlsFactory } from '../types/ethers-contracts/GasBlsFactory';
import { TestBlsFactory } from '../types/ethers-contracts/TestBlsFactory';
import { TestBls } from '../types/ethers-contracts/TestBls';
import { bigToHex, randHex, randFsHex, randFs } from './utils';
import { ContractFactory } from 'ethers';
const FACTORY_GAS_BLS = new GasBlsFactory(wallet);
const FACTORY_TEST_BLS = new TestBlsFactory(wallet);
const modexp_sqrt = require('../modexp/modexp_c191_3f52.json');
const modexp_inverse = require('../modexp/modexp_3064_fd54.json');
const FACTORY_MODEXP_SQRT = new ContractFactory(modexp_sqrt.abi, modexp_sqrt.bytecode, wallet);
const FACTORY_MODEXP_INVERSE = new ContractFactory(modexp_inverse.abi, modexp_inverse.bytecode, wallet);
const DOMAIN_STR = 'gas-bench-evmbls';
const DOMAIN = Uint8Array.from(Buffer.from(DOMAIN_STR, 'utf8'));

describe('BLS', () => {
  let bls: GasBls;
  let _bls: TestBls;
  before(async function () {
    await mcl.init();
    mcl.setDomain(DOMAIN_STR);
    const modexpSqrt = await FACTORY_MODEXP_SQRT.deploy();
    const modexpInv = await FACTORY_MODEXP_INVERSE.deploy();
    bls = await FACTORY_GAS_BLS.deploy(modexpInv.address, modexpSqrt.address);
    _bls = await FACTORY_TEST_BLS.deploy(modexpInv.address, modexpSqrt.address);
  });
  it('sqrt', async function () {
    const a = randFs();
    const cost = await bls.callStatic._sqrt(a);
    console.log(`sqrt cost: ${cost.toNumber()}`);
    const costMagic = await bls.callStatic._sqrtFaster(a);
    console.log(`magic sqrt cost: ${costMagic.toNumber()}`);
  });
  it('verify signature', async function () {
    const n = 100;
    const messages = [];
    const pubkeys = [];
    let aggSignature = mcl.newG1();
    for (let i = 0; i < n; i++) {
      const message = randHex(12);
      const { pubkey, secret } = mcl.newKeyPair();
      const { signature, M } = mcl.sign(message, secret);
      aggSignature = mcl.aggreagate(aggSignature, signature);
      messages.push(M);
      pubkeys.push(pubkey);
    }
    let messages_ser = messages.map((p) => mcl.g1ToBN(p));
    let pubkeys_ser = pubkeys.map((p) => mcl.g2ToBN(p));
    let sig_ser = mcl.g1ToBN(aggSignature);
    let cost = await bls.callStatic._verifyMultipleGasCost(sig_ser, pubkeys_ser, messages_ser);
    console.log(`verify signature for ${n} distinct message: ${cost.toNumber()}`);
  });
  it('verify single signature', async function () {
    const message = randHex(12);
    const { pubkey, secret } = mcl.newKeyPair();
    const { signature, M } = mcl.sign(message, secret);
    let message_ser = mcl.g1ToBN(M);
    let pubkey_ser = mcl.g2ToBN(pubkey);
    let sig_ser = mcl.g1ToBN(signature);
    let cost = await bls.callStatic._verifySingleGasCost(sig_ser, pubkey_ser, message_ser);
    console.log(`verify single signature:: ${cost.toNumber()}`);
  });
  it('map to point ti', async function () {
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const data = randHex(32);
      let cost = await bls.callStatic._mapToPointTIGasCost(data);
      totalCost += cost.toNumber();
    }
    console.log(`map to point ti average cost: ${totalCost / n}`);
  });
  it('map to point ft', async function () {
    // average
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const e = randFsHex();
      let cost = await bls.callStatic._mapToPointFTGasCost(e);
      totalCost += cost.toNumber();
    }
    console.log(`map to point ft average cost: ${totalCost / n}`);
    // worst-case
    const data = '0x8ee7693e1f305986e0b6b703c808a0c7c5a7404f08b55401baf5ab735705fbb';
    const out1 = '0x1df8e11fbe95fd67672c36a338f54f329c18b412416f878520afcc3999600959';
    const out2 = '0x154d89ff22da42dd1db7ef090db1d5cbb1193d47bebf7fed54f450a48078eeaa';
    const res = await _bls._mapToPointFT(data);
    assert.equal(out1, bigToHex(res[0]));
    assert.equal(out2, bigToHex(res[1]));
    const cost = await bls.callStatic._mapToPointFTGasCost(data);
    console.log(`map to point ft worst-case cost: ${cost}`);
  });
  it('hash to field', async function () {
    // average
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const msg = randHex(20);
      let cost = await bls.callStatic._hashToFieldGasCost(DOMAIN, msg);
      totalCost += cost.toNumber();
    }
    console.log(`hash to field average cost: ${totalCost / n}`);
  });
  it('hash to point', async function () {
    // average
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const msg = randHex(20);
      let cost = await bls.callStatic._hashToPointGasCost(DOMAIN, msg);
      totalCost += cost.toNumber();
    }
    console.log(`hash to point average cost: ${totalCost / n}`);
  });
  it('is on curve g1', async function () {
    let point = mcl.randG1();
    let cost = await bls.callStatic._isOnCurveG1GasCost(mcl.g1ToBN(point));
    console.log(`is on curve g1 gas cost: ${cost.toNumber()}`);
    cost = await bls.callStatic._isOnCurveG1CompressedGasCost(mcl.g1ToCompressed(point));
    console.log(`is on curve compressed g1 gas cost: ${cost.toNumber()}`);
  });
  it('is on curve g2', async function () {
    let point = mcl.randG2();
    let cost = await bls.callStatic._isOnCurveG2GasCost(mcl.g2ToBN(point));
    console.log(`is on curve g2 gas cost: ${cost.toNumber()}`);
    cost = await bls.callStatic._isOnCurveG2CompressedGasCost(mcl.g2ToCompressed(point));
    console.log(`is on curve compressed g2 gas cost: ${cost.toNumber()}`);
  });
});
