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
    console.log(`Deploying contracts with the account: ${owner.address}`);    

    const initialPrice = ethers.parseUnits("60", 8);
    const mockAggregator = await ethers.deployContract("MockAggregator", [initialPrice, 8]);
    await mockAggregator.waitForDeployment();

    console.log("***********************************");
    console.log(`Mock Aggregator deployed 
        with initial price ${initialPrice}
        to ${mockAggregator.target}
        by owning address ${owner.address}`);

    // setting the mock price feed address
    const priceFeedAddress = mockAggregator.target;

    const stablecoinContract = await ethers.deployContract("WTIStablecoin", [owner.address, priceFeedAddress]);
    await stablecoinContract.waitForDeployment();
    
    console.log("***********************************");
    console.log(`WTI Stablecoin deployed 
        to ${stablecoinContract.target}
        by owning address ${owner.address}`);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
})