# evmbls

> [BLS Signature](https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html) verification and ECC utility contracts.

Signature verification scheme is implemented on BN254 elliptic curve. Currently only public-key-on-G2 setup is available.

# Roadmap

- [x] Aggregated signature verification
- [x] Compressed point suport
- [ ] Example for signature verification in optimistic way
- [ ] Optimistic hash to curve example
- [x] Hash to field [v9](https://tools.ietf.org/html/draft-irtf-cfrg-hash-to-curve-09#appendix-I.1)
- [x] Map to curve: try and increment G1
- [ ] Map to curve: try and increment, using helpers to get rid of modExp call
- [ ] Map to curve: try and increment G2
- [x] Map to curve: [Fouque Tibouchi](https://www.di.ens.fr/~fouque/pub/latincrypt12.pdf)
- [ ] Map to curve: [Fouque Tibouchi](https://www.di.ens.fr/~fouque/pub/latincrypt12.pdf) with modExp helpers
- [ ] EIP-2537 support
- [x] [Cheaper modexp for inversion and sqrt](https://github.com/ChihChengLiang/modexp)