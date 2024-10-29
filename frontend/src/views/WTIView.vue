<script>
import { ethers } from "ethers";

export default {
    name: "WTIView",
    data() {
        return {
            account: null, // User's wallet address
            provider: null, // ethers provider
            contract: null, // WTI contract instance
            collateralAmount: 0, // Collateral amount in ETH
            burnAmount: 0, // WTI tokens to burn
            wtiBalance: 0, // User's WTI token balance
            totalSupply: 0, // Total WTI supply
            wtiPrice: 0, // WTI price fetched from Chainlink
        };
    },
    async mounted() {
        await this.checkIfWalletConnected();
    },
    methods: {
        // Connect wallet and initialize contract
        async connectWallet() {
            if (window.ethereum) {
                try {
                    const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
                    this.account = accounts[0];
                    this.provider = new ethers.providers.Web3Provider(window.ethereum);

                    // Initialize contract
                    const signer = this.provider.getSigner();
                    const contractAddress = "<YOUR_CONTRACT_ADDRESS>"; // Replace with your contract address
                    const abi = [
                        "function mint(uint256 collateralAmount) external payable",
                        "function burn(uint256 burnAmount) external",
                        "function balanceOf(address owner) external view returns (uint256)",
                        "function totalSupply() external view returns (uint256)",
                        "function getLatestWTIPrice() external view returns (int256)"
                    ]; // Use your contract ABI
                    this.contract = new ethers.Contract(contractAddress, abi, signer);

                    // Fetch initial data
                    await this.fetchWTIData();
                } catch (error) {
                    console.error("Error connecting to wallet", error);
                }
            } else {
                alert("MetaMask is not installed. Please install MetaMask.");
            }
        },

        // Check if wallet is already connected
        async checkIfWalletConnected() {
            const accounts = await window.ethereum.request({ method: "eth_accounts" });
            if (accounts.length > 0) {
                this.account = accounts[0];
                await this.connectWallet();
            }
        },

        // Fetch WTI balance, total supply, and WTI price
        async fetchWTIData() {
            if (this.contract && this.account) {
                const balance = await this.contract.balanceOf(this.account);
                const supply = await this.contract.totalSupply();
                const price = await this.contract.getLatestWTIPrice();

                // Update state
                this.wtiBalance = ethers.utils.formatUnits(balance, 18);
                this.totalSupply = ethers.utils.formatUnits(supply, 18);
                this.wtiPrice = ethers.utils.formatUnits(price, 8); // Chainlink price with 8 decimals
            }
        },

        // Mint WTI tokens
        async mintWTI() {
            if (!this.collateralAmount || this.collateralAmount <= 0) {
                alert("Enter a valid collateral amount.");
                return;
            }

            try {
                const tx = await this.contract.mint({
                    value: ethers.utils.parseEther(this.collateralAmount.toString()) // ETH collateral
                });
                await tx.wait();
                alert("WTI tokens minted successfully.");
                await this.fetchWTIData();
            } catch (error) {
                console.error("Error minting WTI tokens", error);
            }
        },

        // Burn WTI tokens
        async burnWTI() {
            if (!this.burnAmount || this.burnAmount <= 0) {
                alert("Enter a valid burn amount.");
                return;
            }

            try {
                const tx = await this.contract.burn(ethers.utils.parseUnits(this.burnAmount, 18));
                await tx.wait();
                alert("WTI tokens burned successfully.");
                await this.fetchWTIData();
            } catch (error) {
                console.error("Error burning WTI tokens", error);
            }
        },
    },
};
</script>

<template>
    <div class="wti-view">
        <h1>WTI Stablecoin DApp</h1>

        <!-- Connect Wallet Button -->
        <button v-if="!account" @click="connectWallet">Connect Wallet</button>
        <div v-if="account">Connected as: {{ account }}</div>

        <!-- Display WTI Token Information -->
        <div v-if="account">
            <h3>Your Balance: {{ wtiBalance }} WTI</h3>
            <h3>Total Supply: {{ totalSupply }} WTI</h3>
            <h3>WTI Price (USD): ${{ wtiPrice }}</h3>

            <!-- Mint WTI Tokens Section -->
            <h2>Mint WTI Tokens</h2>
            <input v-model="collateralAmount" placeholder="Enter collateral (ETH)" />
            <button @click="mintWTI">Mint</button>

            <!-- Burn WTI Tokens Section -->
            <h2>Burn WTI Tokens</h2>
            <input v-model="burnAmount" placeholder="Enter WTI amount to burn" />
            <button @click="burnWTI">Burn</button>
        </div>
    </div>
</template>

<style scoped>
.wti-view {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 600px;
    margin: auto;
}

button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
}

input {
    margin-right: 10px;
    padding: 5px;
    border: 1px solid #ccc;
}

h1, h2, h3 {
    color: #333;
}
</style>
