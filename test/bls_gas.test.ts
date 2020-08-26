import { GasBLSInstance, TestBLSInstance } from '../types/truffle-contracts';

const GasBLS = artifacts.require('GasBLS');
const TestBLS = artifacts.require('TestBLS');
import * as mcl from './mcl';

contract('BLS', (accounts) => {
  let bls: GasBLSInstance;
  let _bls: TestBLSInstance;
  before(async function () {
    await mcl.init();
    bls = await GasBLS.new();
    _bls = await TestBLS.new();
  });
  it('verify signature', async function () {
    const n = 100;
    const messages = [];
    const pubkeys = [];
    let aggSignature = mcl.newG1();
    for (let i = 0; i < n; i++) {
      const message = web3.utils.randomHex(12);
      const { pubkey, secret } = mcl.newKeyPair();
      const { signature, M } = mcl.sign(message, secret);
      aggSignature = mcl.aggreagate(aggSignature, signature);
      messages.push(M);
      pubkeys.push(pubkey);
    }
    let messages_ser = messages.map((p) => mcl.g1ToBN(p));
    let pubkeys_ser = pubkeys.map((p) => mcl.g2ToBN(p));
    let sig_ser = mcl.g1ToBN(aggSignature);
    let cost = await bls.verifyMultipleGasCost.call(sig_ser, pubkeys_ser, messages_ser);
    console.log(`verify signature for ${n} distinct message: ${cost.toNumber()}`);
  });
  it('verify single signature', async function () {
    const message = web3.utils.randomHex(12);
    const { pubkey, secret } = mcl.newKeyPair();
    const { signature, M } = mcl.sign(message, secret);
    let message_ser = mcl.g1ToBN(M);
    let pubkey_ser = mcl.g2ToBN(pubkey);
    let sig_ser = mcl.g1ToBN(signature);
    let cost = await bls.verifySingleGasCost.call(sig_ser, pubkey_ser, message_ser);
    console.log(`verify single signature:: ${cost.toNumber()}`);
  });
  it('map to point ti', async function () {
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const data = web3.utils.randomHex(32);
      let cost = await bls.mapToPointTIGasCost.call(data);
      totalCost += cost.toNumber();
    }
    console.log(`map to point ti average cost: ${totalCost / n}`);
  });
  it('map to point ft', async function () {
    // average
    const n = 50;
    let totalCost = 0;
    for (let i = 0; i < n; i++) {
      const data = web3.utils.randomHex(32);
      let cost = await bls.mapToPointFTGasCost.call(data);
      totalCost += cost.toNumber();
    }
    console.log(`map to point ft average cost: ${totalCost / n}`);
    // worst-case
    const data = '0xfae3fed247eb2669079cc800c40743e071e188dbfac44a02485217296fe1521e';
    const out1 = '0x1df8e11fbe95fd67672c36a338f54f329c18b412416f878520afcc3999600959';
    const out2 = '0x154d89ff22da42dd1db7ef090db1d5cbb1193d47bebf7fed54f450a48078eeaa';
    const res = await _bls.mapToPointFT(data);
    assert.equal(out1, mcl.bnToHex(res[0]));
    assert.equal(out2, mcl.bnToHex(res[1]));
    const cost = await bls.mapToPointFTGasCost.call(data);
    console.log(`map to point ft worst-case cost: ${cost}`);
  });
  it('is on curve g1', async function () {
    let point = mcl.randG1();
    let cost = await bls.isOnCurveG1GasCost.call(mcl.g1ToBN(point));
    console.log(`is on curve g1 gas cost: ${cost.toNumber()}`);
    cost = await bls.isOnCurveG1CompressedGasCost.call(mcl.g1ToCompressed(point));
    console.log(`is on curve compressed g1 gas cost: ${cost.toNumber()}`);
  });
  it('is on curve g2', async function () {
    let point = mcl.randG2();
    let cost = await bls.isOnCurveG2GasCost.call(mcl.g2ToBN(point));
    console.log(`is on curve g2 gas cost: ${cost.toNumber()}`);
    cost = await bls.isOnCurveG2CompressedGasCost.call(mcl.g2ToCompressed(point));
    console.log(`is on curve compressed g2 gas cost: ${cost.toNumber()}`);
  });
});
