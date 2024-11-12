# Stablecoin

## Overview

The WTI - Stablecoin represents the oil price of "West Texas Intermediate", which is a grade crude oil from the United States.

## Technologies
- Solidity
- Vue (Frontend) 

To test the ethers.js package open the following website:
[Ethers Playground](https://playground.ethers.org/)

### Sample Hardhat Project

```shell
# compile the solidity code
yarn hardhat compile

# run a single local node
yarn hardhat node

# deploy to localhost
yarn hardhat run scripts/deploy-test.ts --network localhost 

# set variables
yarn hardhat vars set ARBITRUM_PRIVATE_KEY <your-private-key>
yarn hardhat vars set ARBITRUM_SEPOLIA_API_KEY <your-api-key>

# set variables for testing
yarn hardhat vars set ARBITRUM_PRIVATE_KEY 0x0000000000000000000000000000000000000000
yarn hardhat vars set ARBITRUM_SEPOLIA_API_KEY 0x0000000000000000000000000000000000000000000000000000000000000000
```

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a Hardhat Ignition module that deploys that contract.

Try running some of the following tasks:

```shell
npx hardhat help
npx hardhat test
REPORT_GAS=true npx hardhat test
npx hardhat node
npx hardhat ignition deploy ./ignition/modules/Lock.ts
```
