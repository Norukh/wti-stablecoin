"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const chai_1 = require("chai");
const hardhat_1 = require("hardhat");
describe("WTI Token Contract", function () {
    it("Deployment should assign the total supply of tokens to the owner", async function () {
        const [owner] = await hardhat_1.ethers.getSigners();
        const priceFeed = "0x4fB44FC4FA132d1a846Bd4143CcdC5a9f1870b06";
        const hardhatToken = await hardhat_1.ethers.deployContract("WTIStablecoin", [owner.address, priceFeed]);
        const ownerBalance = await hardhatToken.balanceOf(owner.address);
        (0, chai_1.expect)(await hardhatToken.totalSupply()).to.equal(ownerBalance);
    });
});
