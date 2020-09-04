pragma solidity ^0.6.10;

library HashToFieldV9 {
  uint256 constant N = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
  uint256 constant T24 = 0x1000000000000000000000000000000000000000000000000;
  uint256 constant MASK24 = 0xffffffffffffffffffffffffffffffffffffffffffffffff;

  function hashToField(bytes memory domain, bytes memory messages) internal pure returns (uint256[2] memory) {
    bytes memory _msg = expandMsgTo96(domain, messages);
    uint256 z0;
    uint256 z1;
    uint256 a0;
    uint256 a1;
    // solium-disable-next-line security/no-inline-assembly
    assembly {
      let p := add(_msg, 24)
      z1 := and(mload(p), MASK24)
      p := add(_msg, 48)
      z0 := and(mload(p), MASK24)
      a0 := addmod(mulmod(z1, T24, N), z0, N)
      p := add(_msg, 72)
      z1 := and(mload(p), MASK24)
      p := add(_msg, 96)
      z0 := and(mload(p), MASK24)
      a1 := addmod(mulmod(z1, T24, N), z0, N)
    }
    return [a0, a1];
  }

  function expandMsgTo96(bytes memory domain, bytes memory message) internal pure returns (bytes memory) {
    uint256 t1 = domain.length;
    require(t1 < 256, "HashToFieldV9: invalid domain length");
    // zero<64>|msg<var>|lib_str<2>|I2OSP(0, 1)<1>|dst<var>|dst_len<1>
    uint256 t0 = message.length;
    bytes memory msg0 = new bytes(t1 + t0 + 64 + 4);
    bytes memory out = new bytes(96);
    // b0
    // solium-disable-next-line security/no-inline-assembly
    assembly {
      let p := add(msg0, 96)

      let z := 0
      for {

      } lt(z, t0) {
        z := add(z, 32)
      } {
        mstore(add(p, z), mload(add(message, add(z, 32))))
      }
      p := add(p, t0)

      mstore8(p, 0)
      p := add(p, 1)
      mstore8(p, 96)
      p := add(p, 1)
      mstore8(p, 0)
      p := add(p, 1)

      mstore(p, mload(add(domain, 32)))
      p := add(p, t1)
      mstore8(p, t1)
    }
    bytes32 b0 = sha256(msg0);
    bytes32 bi;
    t0 = t1 + 34;

    // resize intermediate message
    // solium-disable-next-line security/no-inline-assembly
    assembly {
      mstore(msg0, t0)
    }

    // b1

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      mstore(add(msg0, 32), b0)
      mstore8(add(msg0, 64), 1)
      mstore(add(msg0, 65), mload(add(domain, 32)))
      mstore8(add(msg0, add(t1, 65)), t1)
    }

    bi = sha256(msg0);

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      mstore(add(out, 32), bi)
    }

    // b2

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      let t := xor(b0, bi)
      mstore(add(msg0, 32), t)
      mstore8(add(msg0, 64), 2)
      mstore(add(msg0, 65), mload(add(domain, 32)))
      mstore8(add(msg0, add(t1, 65)), t1)
    }

    bi = sha256(msg0);

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      mstore(add(out, 64), bi)
    }

    // // b3

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      let t := xor(b0, bi)
      mstore(add(msg0, 32), t)
      mstore8(add(msg0, 64), 3)
      mstore(add(msg0, 65), mload(add(domain, 32)))
      mstore8(add(msg0, add(t1, 65)), t1)
    }

    bi = sha256(msg0);

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      mstore(add(out, 96), bi)
    }

    return out;
  }
}
