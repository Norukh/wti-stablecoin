import { expect } from "chai";
import { ethers } from "hardhat";


describe.skip("WTI Token Contract Tokenomics Testing", function () {
  let owner: any;

  let priceFeedContract: any;
  let priceFeedAddress: any;
  let stablecoinTokenContract: any;

  const decimals = 8;
  const oneMillion = ethers.parseEther("1000000");
  const formatUSD = (value: any) => ethers.formatUnits(value, decimals);

  // 70 USD
  const initialPrice = ethers.parseUnits("70", decimals);

  it("Deployment should be successful", async function () {
    [owner] = await ethers.getSigners();

    priceFeedContract = await ethers.deployContract("MockAggregator", [
      owner.address,
      initialPrice,
      decimals,
    ]);
    expect(priceFeedContract.target).to.not.equal(0);

    priceFeedAddress = priceFeedContract.target;

    stablecoinTokenContract = await ethers.deployContract("WTIStablecoin", [
      owner.address,
      priceFeedAddress,
    ]);
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

  it("Initial total supply should be correct", async function () {
    const totalSupply = await stablecoinTokenContract.totalSupply();
    console.log(`Total supply: ${totalSupply}`);

    const expectedTotalSupply = oneMillion;
    expect(totalSupply).to.equal(expectedTotalSupply);
  });

  it("Total supply should increase after minting", async function () {
    const totalSupplyBefore = await stablecoinTokenContract.totalSupply();
    const amount = ethers.parseEther("1000");

    await stablecoinTokenContract.mint(owner.address, amount);
    const totalSupplyAfter = await stablecoinTokenContract.totalSupply();

    console.log(`Total supply after minting: ${totalSupplyAfter}`);

    expect(totalSupplyAfter).to.equal(totalSupplyBefore + amount);
  });

  it("Total supply should decrease after burning", async function () {
    const totalSupplyBefore = await stablecoinTokenContract.totalSupply();
    const amount = ethers.parseEther("1000");

    await stablecoinTokenContract.burn(amount);
    const totalSupplyAfter = await stablecoinTokenContract.totalSupply();

    console.log(`Total supply after burning: ${totalSupplyAfter}`);

    expect(totalSupplyAfter).to.equal(totalSupplyBefore - amount);
  });

  it("Only owner should be able to mint tokens", async function () {
    const [_, addr] = await ethers.getSigners();

    const result = stablecoinTokenContract
      .connect(addr)
      .mint(addr.address, ethers.parseEther("1000"));
    await expect(result).to.be.reverted;

    const resultOwner = stablecoinTokenContract
      .connect(owner)
      .mint(owner.address, ethers.parseEther("1000"));
    await expect(resultOwner).to.not.be.reverted;
  });

  it("Only owner should be able to burn tokens", async function () {
    const [_, addr] = await ethers.getSigners();

    const result = stablecoinTokenContract
      .connect(addr)
      .burn(ethers.parseEther("1000"));
    await expect(result).to.be.reverted;

    const resultOwner = stablecoinTokenContract
      .connect(owner)
      .burn(ethers.parseEther("1000"));
    await expect(resultOwner).to.not.be.reverted;
  });

  it("Should approve and transfer tokens", async function () {
    const [_, addr] = await ethers.getSigners();
    const amount = ethers.parseEther("1000");

    await stablecoinTokenContract.mint(owner.address, amount);

    const approveResult = await stablecoinTokenContract.approve(
      owner.address,
      amount
    );
    await expect(approveResult).to.not.be.reverted;

    const transferResult = await stablecoinTokenContract.transferFrom(
      owner.address,
      addr.address,
      amount
    );
    await expect(transferResult).to.not.be.reverted;
  });
});
