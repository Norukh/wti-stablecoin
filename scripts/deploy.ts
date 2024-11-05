// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// When running the script with `npx hardhat run <script>` you'll find the Hardhat
// Runtime Environment's members available in the global scope.
import { ethers } from "hardhat";

async function main() {
  // Hardhat always runs the compile task when running scripts with its command
  // line interface.
  //
  // If this script is run directly using `node` you may want to call compile
  // manually to make sure everything is compiled
  // await hre.run('compile');
  // We get the contract to deploy
  const [owner] = await ethers.getSigners();
  console.log(owner);
  // https://sepolia.arbiscan.io/address/0x4fB44FC4FA132d1a846Bd4143CcdC5a9f1870b06
  // SPY/USD price feed
  const priceFeedAddress = "0x4fB44FC4FA132d1a846Bd4143CcdC5a9f1870b06";

  const stablecoinContract = await ethers.deployContract("WTIStablecoin", [owner.address, priceFeedAddress]);
  await stablecoinContract.waitForDeployment();

  console.log(`WTI Stablecoin deployed to ${stablecoinContract.target}`);
  console.log(`WTI Stablecoin deployed by owning address ${owner.address}`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
