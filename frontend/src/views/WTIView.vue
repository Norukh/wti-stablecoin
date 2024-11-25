<script setup lang="ts">
import { ethers, formatEther } from 'ethers'
import { ref } from 'vue'

import Button from 'primevue/button'

declare global {
  interface Window {
    ethereum: any
  }
}

let provider: any
const account = ref(null)
const balance = ref('')
const totalSupply = ref(0)

async function checkMetamask() {
  if (window.ethereum == null) {
    alert('MetaMask not installed; please install MetaMask')
    return
  }
}

async function connectWallet() {
  await checkMetamask()

  provider = new ethers.BrowserProvider(window.ethereum)

  await provider.send('eth_requestAccounts', [])

  const signer = await provider.getSigner()
  account.value = await signer.getAddress()

  // initialize contract
  const contractAddress = '0x58C653F1d11C3D334c3ee8fe813f4d0A5D5B4A9F'

  const abi = [
    'function balanceOf(address owner) external view returns (uint256)',
    'function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)',
  ]

  const contract = new ethers.Contract(contractAddress, abi, signer)
  
  // TODO: call contract functions
  let bal = await contract.balanceOf(account.value)
  balance.value = formatEther(bal)
  
}

async function checkWalletConnected() {
  await checkMetamask()
  const accounts = await window.ethereum.request({ method: 'eth_accounts' })

  if (accounts.length > 0) {
    account.value = accounts[0]
    await connectWallet()
  }
}
</script>

<template>
  <div class="wti-view">
    <h1>WTI Stablecoin DApp</h1>

    <!-- Connect Wallet Button -->
    <Button v-if="!account" @click="connectWallet">Connect Wallet</Button>
    <div v-if="account">Connected as: {{ account }}</div>

    <!-- Display WTI Token Information -->
    <div v-if="account">
      <h3>Your Balance: {{ balance }} WTI</h3>
      <h3>Total Supply: {{ totalSupply }} WTI</h3>
      <h3>WTI Price (USD): ${{ wtiPrice }}</h3>
      <br />
      <!-- Mint WTI Tokens Section -->
      <h2>Mint WTI Tokens</h2>
      <input v-model="collateralAmount" placeholder="Enter collateral (ETH)" />
      <button @click="mintWTI">Mint</button>

      <!-- Burn WTI Tokens Section -->
      <h2>Burn WTI Tokens</h2>
      <input v-model="burnAmount" placeholder="Enter WTI amount to burn" />
      <button @click="burnWTI">Burn</button>

      <!-- Send Token Section -->
      <h2>Send Token</h2>
      <input v-model="recipientAddress" placeholder="Enter recipient address" />
      <input v-model="sendAmount" placeholder="Enter WTI amount to send" />
      <button @click="sendWTI">Send</button>
    </div>
    <div></div>
  </div>
</template>

<style scoped>
.wti-view {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 600px;
  margin: auto;
}
</style>
