pragma solidity ^0.6.10;

import { BLS } from "../BLS.sol";

contract GasBLS {
  function verifyMultipleGasCost(
    uint256[2] calldata signature,
    uint256[4][] calldata pubkeys,
    uint256[2][] calldata messages
  ) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    require(BLS.verifyMultiple(signature, pubkeys, messages), "BLSTest: expect succesful verification");
    return operationGasCost - gasleft();
  }

  function verifySingleGasCost(
    uint256[2] calldata signature,
    uint256[4] calldata pubkey,
    uint256[2] calldata message
  ) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    require(BLS.verifySingle(signature, pubkey, message), "BLSTest: expect succesful verification");
    return operationGasCost - gasleft();
  }

  function mapToPointTIGasCost(bytes32 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.mapToPointTI(e);
    return operationGasCost - gasleft();
  }

  function mapToPointFTGasCost(bytes32 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.mapToPointFT(e);
    return operationGasCost - gasleft();
  }

  function isOnCurveG1CompressedGasCost(uint256 point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isOnCurveG1(point);
    return operationGasCost - gasleft();
  }

  function isOnCurveG1GasCost(uint256[2] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isOnCurveG1(point);
    return operationGasCost - gasleft();
  }

  function isOnCurveG2CompressedGasCost(uint256[2] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isOnCurveG2(point);
    return operationGasCost - gasleft();
  }

  function isOnCurveG2GasCost(uint256[4] calldata point) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isOnCurveG2(point);
    return operationGasCost - gasleft();
  }

  function isNonResidueFQGasCost(uint256 e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isNonResidueFQ(e);
    return operationGasCost - gasleft();
  }

  function isNonResidueFQ2GasCost(uint256[2] calldata e) external returns (uint256 operationGasCost) {
    operationGasCost = gasleft();
    BLS.isNonResidueFQ2(e);
    return operationGasCost - gasleft();
  }
}
