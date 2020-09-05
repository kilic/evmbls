pragma solidity ^0.6.10;

import { BLS } from "../BLS.sol";
import { modexp } from "../modexp.sol";

contract GasBLS is BLS {
  constructor(modexp _modexp_3064_fd54, modexp _modexp_c191_3f52) public {
    modexp_3064_fd54 = _modexp_3064_fd54;
    modexp_c191_3f52 = _modexp_c191_3f52;
  }

  function _sqrt(uint256 xx) external view returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    sqrt(xx);
    return operationGasCost - gasleft();
  }

  function _sqrtFaster(uint256 xx) external view returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    sqrtFaster(xx);
    return operationGasCost - gasleft();
  }

  function _verifyMultipleGasCost(
    uint256[2] calldata signature,
    uint256[4][] calldata pubkeys,
    uint256[2][] calldata messages
  ) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    require(verifyMultiple(signature, pubkeys, messages), "BLSTest: expect succesful verification");
    return operationGasCost - gasleft();
  }

  function _verifySingleGasCost(
    uint256[2] calldata signature,
    uint256[4] calldata pubkey,
    uint256[2] calldata message
  ) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    require(verifySingle(signature, pubkey, message), "BLSTest: expect succesful verification");
    return operationGasCost - gasleft();
  }

  function _mapToPointTIGasCost(bytes32 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    mapToPointTI(e);
    return operationGasCost - gasleft();
  }

  function _mapToPointFTGasCost(uint256 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    mapToPointFT(e);
    return operationGasCost - gasleft();
  }

  function _hashToPointGasCost(bytes memory domain, bytes memory message) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    hashToPoint(domain, message);
    return operationGasCost - gasleft();
  }

  function _hashToFieldGasCost(bytes memory domain, bytes memory message) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    hashToField(domain, message);
    return operationGasCost - gasleft();
  }

  function _isOnCurveG1CompressedGasCost(uint256 point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isOnCurveG1(point);
    return operationGasCost - gasleft();
  }

  function _isOnCurveG1GasCost(uint256[2] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isOnCurveG1(point);
    return operationGasCost - gasleft();
  }

  function _isOnCurveG2CompressedGasCost(uint256[2] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isOnCurveG2(point);
    return operationGasCost - gasleft();
  }

  function _isOnCurveG2GasCost(uint256[4] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isOnCurveG2(point);
    return operationGasCost - gasleft();
  }

  function _isNonResidueFPGasCost(uint256 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isNonResidueFP(e);
    return operationGasCost - gasleft();
  }

  function _isNonResidueFP2GasCost(uint256[2] calldata e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    isNonResidueFP2(e);
    return operationGasCost - gasleft();
  }
}
