pragma solidity ^0.6.10;

import { BLS } from "../BLS.sol";
import { modexp } from "../modexp.sol";

contract TestBLS is BLS {
  constructor(modexp _modexp_3064_fd54, modexp _modexp_c191_3f52) public {
    modexp_3064_fd54 = _modexp_3064_fd54;
    modexp_c191_3f52 = _modexp_c191_3f52;
  }

  function _sqrt(uint256 xx) external view returns (uint256, bool) {
    return sqrt(xx);
  }

  function _sqrtFaster(uint256 xx) external view returns (uint256, bool) {
    return sqrtFaster(xx);
  }

  function _inverse(uint256 a) external view returns (uint256) {
    return inverse(a);
  }

  function _inverseFaster(uint256 a) external view returns (uint256) {
    return inverseFaster(a);
  }

  function _verifyMultiple(
    uint256[2] calldata signature,
    uint256[4][] calldata pubkeys,
    uint256[2][] calldata messages
  ) external view returns (bool) {
    return verifyMultiple(signature, pubkeys, messages);
  }

  function _verifySingle(
    uint256[2] calldata signature,
    uint256[4] calldata pubkey,
    uint256[2] calldata message
  ) external view returns (bool) {
    return verifySingle(signature, pubkey, message);
  }

  function _mapToPointTI(bytes32 e) external view returns (uint256[2] memory p) {
    return mapToPointTI(e);
  }

  function _mapToPointFT(uint256 e) external view returns (uint256[2] memory p) {
    return mapToPointFT(e);
  }

  function _isOnCurveG1Compressed(uint256 point) external view returns (bool) {
    return isOnCurveG1(point & FIELD_MASK);
  }

  function _isOnCurveG1(uint256[2] calldata point) external pure returns (bool) {
    return isOnCurveG1(point);
  }

  function _isOnCurveG2Compressed(uint256[2] calldata point) external view returns (bool) {
    uint256 x0 = point[0] & FIELD_MASK;
    uint256 x1 = point[1];
    return isOnCurveG2([x0, x1]);
  }

  function _isOnCurveG2(uint256[4] calldata point) external pure returns (bool) {
    return isOnCurveG2(point);
  }

  function _isNonResidueFP(uint256 e) external view returns (bool) {
    return isNonResidueFP(e);
  }

  function _isNonResidueFP2(uint256[2] calldata e) external view returns (bool) {
    return isNonResidueFP2(e);
  }

  function _pubkeyToUncompresed(uint256[2] calldata compressed, uint256[2] memory y) external pure returns (uint256[4] memory uncompressed) {
    return pubkeyToUncompresed(compressed, y);
  }

  function _signatureToUncompresed(uint256 compressed, uint256 y) external pure returns (uint256[2] memory uncompressed) {
    return signatureToUncompresed(compressed, y);
  }

  function _isValidCompressedPublicKey(uint256[2] calldata compressed) external view returns (bool) {
    return isValidCompressedPublicKey(compressed);
  }

  function _isValidCompressedSignature(uint256 compressed) external view returns (bool) {
    return isValidCompressedSignature(compressed);
  }

  function _expandMsg(bytes calldata domain, bytes calldata message) external view returns (bytes memory) {
    return expandMsgTo96(domain, message);
  }

  function _hashToField(bytes calldata domain, bytes calldata message) external view returns (uint256[2] memory) {
    return hashToField(domain, message);
  }

  function _hashToPoint(bytes memory domain, bytes memory message) external view returns (uint256[2] memory) {
    return hashToPoint(domain, message);
  }
}
