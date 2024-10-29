// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

import "hardhat/console.sol";

contract WTIStablecoin is ERC20, ERC20Burnable, ERC20Pausable, Ownable {
    AggregatorV3Interface internal priceFeed;

    uint256 public cachedFeedPrice;
    uint256 public lastPriceFetchTime;
    uint256 public priceFetchCooldown = 0.5 hours;

    constructor(
        address initialOwner,
        address priceFeedAddress
    ) ERC20("WTI Stablecoin", "WTIS") Ownable(initialOwner) {
        _mint(initialOwner, 1000000 * 10 ** decimals());

        /* Testing SPY/USD price feed
         * Network: Arbitrum Sepolia
         * Address: 0x4fB44FC4FA132d1a846Bd4143CcdC5a9f1870b06
         */
        priceFeed = AggregatorV3Interface(priceFeedAddress);
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public override onlyOwner {
        _burn(owner(), amount);
    }

    function rebalance() internal {
        if (block.timestamp >= lastPriceFetchTime + priceFetchCooldown) {
            cachedFeedPrice = uint256(getChainlinkPriceFeedLatestAnswer());
            lastPriceFetchTime = block.timestamp;
        }

        uint256 targetSupply = (totalSupply() * cachedFeedPrice) / 1e8;

        if (totalSupply() > targetSupply) {
            uint256 excessAmount = totalSupply() - targetSupply;
            _burn(owner(), excessAmount);
        } else if (totalSupply() < targetSupply) {
            uint256 mintAmount = targetSupply - totalSupply();
            _mint(owner(), mintAmount);
        }
    }

    function transfer(
        address to,
        uint256 amount
    ) public override returns (bool) {
        bool success = super.transfer(to, amount);
        if (success) {
            rebalance();
        }
        return success;
    }

    // The following functions are overrides required by Solidity.
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override(ERC20, ERC20Pausable) {
        super._update(from, to, value);
    }

    function getChainlinkPriceFeedLatestAnswer() public view returns (int) {
        (
            ,
            /* uint80 roundId */ int answer /* uint startedAt */ /* uint timeStamp */ /* uint80 answeredInRound */,
            ,
            ,

        ) = priceFeed.latestRoundData();
        require(answer > 0, "Invalid price feed answer");
        return answer;
    }
}
