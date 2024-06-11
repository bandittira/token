// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Point is ERC20 {
    constructor(uint256 initialSupply) ERC20("Point", "P") {
        _mint(msg.sender, initialSupply);
    }

    // Function to demonstrate pushing zero onto the stack
    function pushZero() public pure returns (uint256) {
        uint256 value = 0; // Assigning zero to a variable
        return value;
    }

    // Another function using zero in an expression
    function multiplyByZero(uint256 input) public pure returns (uint256) {
        uint256 result = input * 0; // Multiplying by zero
        return result;
    }
}
