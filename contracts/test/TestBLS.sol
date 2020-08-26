pragma solidity ^0.6.10;

import { BLS } from "../BLS.sol";

contract TestBLS {
  function verifyMultiple(
    uint256[2] calldata signature,
    uint256[4][] calldata pubkeys,
    uint256[2][] calldata messages
  ) external view returns (bool) {
    return BLS.verifyMultiple(signature, pubkeys, messages);
  }

  function verifySingle(
    uint256[2] calldata signature,
    uint256[4] calldata pubkey,
    uint256[2] calldata message
  ) external view returns (bool) {
    return BLS.verifySingle(signature, pubkey, message);
  }

  function mapToPointTI(bytes32 e) external view returns (uint256[2] memory p) {
    return BLS.mapToPointTI(e);
  }

  function mapToPointFT(bytes32 e) external view returns (uint256[2] memory p) {
    return BLS.mapToPointFT(e);
  }

  function isOnCurveG1Compressed(uint256 point) external view returns (bool) {
    return BLS.isOnCurveG1(point & BLS.FIELD_MASK);
  }

  function isOnCurveG1(uint256[2] calldata point) external pure returns (bool) {
    return BLS.isOnCurveG1(point);
  }

  function isOnCurveG2Compressed(uint256[2] calldata point) external view returns (bool) {
    uint256 x0 = point[0] & BLS.FIELD_MASK;
    uint256 x1 = point[1];
    return BLS.isOnCurveG2([x0, x1]);
  }

  function isOnCurveG2(uint256[4] calldata point) external pure returns (bool) {
    return BLS.isOnCurveG2(point);
  }

  function isNonResidueFP(uint256 e) external view returns (bool) {
    return BLS.isNonResidueFP(e);
  }

  function isNonResidueFP2(uint256[2] calldata e) external view returns (bool) {
    return BLS.isNonResidueFP2(e);
  }

  function pubkeyToUncompresed(uint256[2] calldata compressed, uint256[2] memory y) external pure returns (uint256[4] memory uncompressed) {
    return BLS.pubkeyToUncompresed(compressed, y);
  }

  function signatureToUncompresed(uint256 compressed, uint256 y) external pure returns (uint256[2] memory uncompressed) {
    return BLS.signatureToUncompresed(compressed, y);
  }

  function isValidCompressedPublicKey(uint256[2] calldata compressed) external view returns (bool) {
    return BLS.isValidCompressedPublicKey(compressed);
  }

  function isValidCompressedSignature(uint256 compressed) external view returns (bool) {
    return BLS.isValidCompressedSignature(compressed);
  }
}
