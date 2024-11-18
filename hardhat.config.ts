import { HardhatUserConfig, vars } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const ARBITRUM_PRIVATE_KEY = vars.get("ARBITRUM_PRIVATE_KEY");
const ARBITRUM_SEPOLIA_API_KEY = vars.get("ARBITRUM_SEPOLIA_API_KEY");

const config: HardhatUserConfig = {
  solidity: "0.8.27",
  networks: {
    hardhat: {
      chainId: 1337,
    },
    arbitrumSepolia: {
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      chainId: 421614,
      accounts: [ `${ARBITRUM_PRIVATE_KEY}` ],
    },
  },
  etherscan: {
    apiKey: {
      arbitrumSepolia: ARBITRUM_SEPOLIA_API_KEY,
    },
    customChains: [
      {
        network: "Arbitrum Sepolia",
        chainId: 421614,
        urls: {
          apiURL: "https://api-sepolia.arbiscan.io/api",
          browserURL: "https://sepolia.arbiscan.io/",
        },
      },
    ],
  },
};

export default config;
