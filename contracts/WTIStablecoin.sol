// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

// Importing Chainlink's AggregatorV3Interface for the price feed
interface AggregatorV3Interface {
    function latestRoundData() external view returns (
        uint80 roundId,
        int256 answer,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    );
}

contract WTIStablecoin {
    string public name = "WTIStablecoin";
    string public symbol = "WTI";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public owner;
    AggregatorV3Interface internal priceFeed;  // Chainlink WTI price feed

    // Collateral mapping (e.g., ETH collateral used to mint WTI)
    mapping(address => uint256) public collateral;

    // Price of 1 WTI token in USD (can be pegged to 1 barrel of oil)
    uint256 public constant pricePerWTI = 100 * 1e18;  // 100 USD as example

    // Events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed user, uint256 amount);
    event Burn(address indexed user, uint256 amount);

    constructor(address _priceFeed) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed); // Initialize the WTI price oracle
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    // Function to get the latest WTI oil price (in USD)
    function getLatestWTIPrice() public view returns (int256) {
        (
            ,
            int256 price,
            ,
            ,

        ) = priceFeed.latestRoundData();
        return price;  // Price will have 8 decimals as Chainlink reports in 8 decimals
    }

    // Function to mint new WTI tokens based on collateral
    function mint(uint256 collateralAmount) public {
        // Ensure the user provides collateral (e.g., ETH, or another accepted asset)
        require(collateralAmount > 0, "Collateral amount must be greater than 0");

        // Get the current WTI price
        int256 wtiPrice = getLatestWTIPrice();
        require(wtiPrice > 0, "Invalid WTI price");

        // Calculate how many WTI tokens the user can mint
        uint256 mintAmount = (collateralAmount * uint256(wtiPrice)) / pricePerWTI;

        // Mint the WTI tokens to the user's account
        balanceOf[msg.sender] += mintAmount;
        totalSupply += mintAmount;

        // Update the collateral record
        collateral[msg.sender] += collateralAmount;

        emit Mint(msg.sender, mintAmount);
    }

    // Function to burn WTI tokens and reclaim collateral
    function burn(uint256 burnAmount) public {
        require(balanceOf[msg.sender] >= burnAmount, "Not enough WTI balance");

        // Get the current WTI price
        int256 wtiPrice = getLatestWTIPrice();
        require(wtiPrice > 0, "Invalid WTI price");

        // Calculate how much collateral to return based on burned WTI tokens
        uint256 collateralReturn = (burnAmount * pricePerWTI) / uint256(wtiPrice);

        // Burn the WTI tokens from the user's balance
        balanceOf[msg.sender] -= burnAmount;
        totalSupply -= burnAmount;

        // Return the corresponding collateral
        require(collateral[msg.sender] >= collateralReturn, "Not enough collateral");
        collateral[msg.sender] -= collateralReturn;

        // Logic to return collateral (e.g., transfer ETH or other assets)
        // Example: payable(msg.sender).transfer(collateralReturn);

        emit Burn(msg.sender, burnAmount);
    }

    // Transfer function (standard ERC-20 functionality)
    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    // Approve and transferFrom functions for allowance (standard ERC-20)
    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Allowance exceeded");

        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;

        emit Transfer(from, to, value);
        return true;
    }
}
