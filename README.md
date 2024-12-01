# Stablecoin

## Overview

The WTI - Stablecoin represents the oil price of "West Texas Intermediate", which is a grade crude oil from the United States.

## Stability
How do we ensure stability?

- Liquidity Pool
Idea : - Users can buy / sell coins directly with better fees
- Over collateralization 10%

Liquidity Mining
- Staking with uniswap v3 staker

### Two scenarios
Price of the WTI asset goes up in the real world:

- Mint and put in pool
- USDC receive
- price goes up for WTIST
- with usdc buy real life assets

- sell real life assets
- receive 

Price of the WTI asset goes down in the real world:
- We will add liquidity for USDC - WTIST pair
- Price goes down for WTIST
- We will sell real-life assets

### Burning / Minting
We will burn and mint

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
yarn hardhat run scripts/deploy.ts --network localhost 

# set variables
yarn hardhat vars set ARBITRUM_PRIVATE_KEY <your-private-key>
yarn hardhat vars set ARBITRUM_SEPOLIA_API_KEY <your-api-key>

# set variables for testing
yarn hardhat vars set ARBITRUM_PRIVATE_KEY 0x0000000000000000000000000000000000000000000000000000000000000000
yarn hardhat vars set ARBITRUM_SEPOLIA_API_KEY 0x0000000000000000000000000000000000000000
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
