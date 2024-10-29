import { expect } from "chai";
import { ethers } from "hardhat";

describe("WTI Token Contract", function () {
  it("Deployment should assign the total supply of tokens to the owner", async function () {
    const [owner] = await ethers.getSigners();

    const priceFeed = "0x4fB44FC4FA132d1a846Bd4143CcdC5a9f1870b06";
    const hardhatToken = await ethers.deployContract("WTIStablecoin", [owner.address, priceFeed]);

    const ownerBalance = await hardhatToken.balanceOf(owner.address);
    expect(await hardhatToken.totalSupply()).to.equal(ownerBalance);
  });
});
