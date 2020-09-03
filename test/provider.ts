import { Signer, Wallet, providers } from 'ethers';

const MNEMONIC = 'myth like bonus scare over problem client lizard pioneer submit female collect';
export const provider = new providers.JsonRpcProvider('http://127.0.0.1:8545');
export const wallet = Wallet.fromMnemonic(MNEMONIC).connect(provider);
