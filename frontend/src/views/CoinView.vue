<script setup lang="ts">
import { ethers, formatEther } from 'ethers'
import { ref } from 'vue'

let address = ref(null)
let balance = ref(null)

let tokenAmount = ref(0)

let provider

async function connectWallet() {
  if (window.ethereum == null) {
    alert('MetaMask not installed; please install MetaMask')
    return
  }

  // Request access to MetaMask
  await window.ethereum.request({ method: 'eth_requestAccounts' })

  // Connect to the provider
  provider = new ethers.BrowserProvider(window.ethereum)

  // Get the signer
  const signer = await provider.getSigner()

  // Get the address
  address.value = await signer.getAddress()

  balance.value = await provider.getBalance(address.value)
  balance.value = formatEther(balance.value)
}

async function getBalance() {
  if (provider == null) {
    alert('Please connect your wallet first')
    return
  }

  balance.value = await provider.getBalance(address.value)

  alert(`Balance: ${balance.value.toString()}`)
}

async function issueToken() {
  if (provider == null) {
    alert('Please connect your wallet first')
    return
  }

  alert('Issue token')
}

async function redeemToken() {
  if (provider == null) {
    alert('Please connect your wallet first')
    return
  }

  alert('Redeem token')
}
</script>

<template>
  <div>
    <h1>Use our coin</h1>

    <h2>Connect Wallet</h2>
    <button @click="connectWallet">Connect Wallet</button>

    <p v-if="address">Address: {{ address }}</p>
    <p v-if="balance">Balance: {{ balance.toString() }}</p>

    <h2>Get Balance</h2>
    <button @click="getBalance">Get Balance</button>

    <h2>Issue Token</h2>
    <input v-model="tokenAmount" type="number" placeholder="Token Amount" />
    <button @click="issueToken">Issue Token</button>

    <h2>Redeem Token</h2>
    <input v-model="tokenAmount" type="number" placeholder="Token Amount" />
    <button @click="redeemToken">Redeem Token</button>
  </div>
</template>

