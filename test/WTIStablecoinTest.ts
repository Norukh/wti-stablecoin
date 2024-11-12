import { expect } from "chai";
import { FallbackProvider } from "ethers";
import { ethers } from "hardhat";

describe("WTI Token Contract", function () {

  let owner: any;

  let priceFeedContract: any;
  let priceFeedAddress: any;
  let stablecoinTokenContract: any;

  const decimals = 8;
  const formatUSD = (value: any) => ethers.formatUnits(value, decimals);

  // 70 USD
  const initialPrice = ethers.parseUnits("70", decimals);

  it("Deployment should be successful", async function () {
    [owner] = await ethers.getSigners();

    priceFeedContract = await ethers.deployContract("MockAggregator", [initialPrice, decimals]);
    expect(priceFeedContract.target).to.not.equal(0);

    priceFeedAddress = priceFeedContract.target;

    stablecoinTokenContract = await ethers.deployContract("WTIStablecoin", [owner.address, priceFeedAddress]);
    expect(stablecoinTokenContract.target).to.not.equal(0);
  });

  it("MockAggregator should have the initial price set", async function () {
    const price = await priceFeedContract.latestRoundData();
    console.log(price);
    console.log(`Initial price: ${formatUSD(price.answer)} USD`);
  });

  it("Deployment should assign the total supply of tokens to the owner", async function () {
    const ownerBalance = await stablecoinTokenContract.balanceOf(owner.address);
    expect(await stablecoinTokenContract.totalSupply()).to.equal(ownerBalance);
  });

  it("Should have the correct initial price set", async function () {
    const price = await stablecoinTokenContract.getPriceFeedLatestAnswer();
    expect(price).to.equal(initialPrice);
  });

  it("Should update the price feed", async function () {
    const newPrice = ethers.parseUnits("80", decimals);
    await priceFeedContract.setPrice(newPrice);
    const price = await stablecoinTokenContract.getPriceFeedLatestAnswer();
    expect(price).to.equal(newPrice);
  });

  it("Should update the price feed by owner", async function () {
    const newPrice = ethers.parseUnits("90", decimals);
    await stablecoinTokenContract.setPriceFeedAddress(priceFeedAddress);
    await priceFeedContract.setPrice(newPrice);
    const price = await stablecoinTokenContract.getPriceFeedLatestAnswer();
    expect(price).to.equal(newPrice);
  });

  
});
