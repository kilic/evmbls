import { GasBLSInstance } from '../types/truffle-contracts';

const GasBLS = artifacts.require('GasBLS');
import * as mcl from './mcl';

contract('BLS', (accounts) => {
  let bls: GasBLSInstance;
  before(async function () {
    await mcl.init();
    bls = await GasBLS.new();
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
    console.log(`hash to point average cost: ${totalCost / n}`);
  });
  it('is on curve', async function () {
    let point = mcl.randG2();
    let cost = await bls.isOnCurveG2GasCost.call(mcl.g2ToBN(point));
    console.log(`is on curve g2 gas cost: ${cost.toNumber()}`);
    cost = await bls.isOnCurveG2CompressedGasCost.call(mcl.g2ToCompressed(point));
    console.log(`is on curve compressed g2 gas cost: ${cost.toNumber()}`);
  });
});
