  function mapToPointFT(bytes32 _in) internal view returns (uint256[2] memory p) {
    uint256 x = uint256(_in) % N;
    bool decision = isNonResidueFQ(x);
    uint256 a0 = mulmod(x, x, N);
    a0 = addmod(a0, 4, N);
    uint256 a1 = mulmod(x, z0, N);
    uint256 a2 = mulmod(a1, a0, N);
    a2 = inverse(a2);
    a1 = mulmod(a1, a1, N);
    a1 = mulmod(a1, a2, N);

    // x1
    a1 = mulmod(x, a1, N);
    x = addmod(z1, N - a1, N);
    // check curve
    a1 = mulmod(x, x, N);
    a1 = mulmod(a1, x, N);
    a1 = addmod(a1, 3, N);
    bool found;
    (a1, found) = sqrt(a1);
    if (found) {
      if (decision) {
        a1 = N - a1;
      }
      return [x, a1];
    }

    // x2
    x = N - addmod(x, 1, N);
    // check curve
    a1 = mulmod(x, x, N);
    a1 = mulmod(a1, x, N);
    a1 = addmod(a1, 3, N);
    (a1, found) = sqrt(a1);
    if (found) {
      if (decision) {
        a1 = N - a1;
      }
      return [x, a1];
    }

    // x3
    x = mulmod(a0, a0, N);
    x = mulmod(x, x, N);
    x = mulmod(x, a2, N);
    x = mulmod(x, a2, N);
    x = addmod(x, 1, N);
    // must be on curve
    a1 = mulmod(x, x, N);
    a1 = mulmod(a1, x, N);
    a1 = addmod(a1, 3, N);
    (a1, found) = sqrt(a1);
    require(found, "BLS: bad ft mapping implementation");
    if (decision) {
      a1 = N - a1;
    }
    return [x, a1];
  }