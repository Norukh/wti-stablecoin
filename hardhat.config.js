"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require("@nomicfoundation/hardhat-toolbox");
const config = {
    solidity: "0.8.27",
    networks: {
        hardhat: {
            chainId: 1337,
        },
        arbitrumSepolia: {
            url: "https://sepolia-rollup.arbitrum.io/rpc",
            chainId: 421614,
            //accounts: ["<account-private-key>"]
        },
    },
};
exports.default = config;
