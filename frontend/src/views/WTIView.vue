<script setup lang="ts">
import { ethers, formatEther, formatUnits } from 'ethers'
import { ref } from 'vue'
import { USDC_CONTRACT_ADDRESSES, WTIST_CONTRACT_ADDRESSES } from '@/utils/constants'
import Toast from 'primevue/toast'
import { oilService } from '../services/oil.service'

import SwapWidget from '@/components/SwapWidget.vue'
import TransferWidget from '@/components/TransferWidget.vue'

import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import Card from 'primevue/card'
import Dialog from 'primevue/dialog'

declare global {
  interface Window {
    ethereum: any
  }
}

let provider: any
const account = ref(null)
const balance = ref('')
const gasPrice = ref('')

const barrelsInUSD = ref('')
const swapVisible = ref(false)

async function checkMetamask() {
  if (window.ethereum == null) {
    alert('MetaMask not installed; please install MetaMask')
    return
  }
}

async function connectWallet() {
  await checkMetamask()

  provider = new ethers.BrowserProvider(window.ethereum)

  const signer = await provider.getSigner()
  account.value = await signer.getAddress()

  const contractAddress = WTIST_CONTRACT_ADDRESSES['arbSepolia']

  const abi = [
    'function balanceOf(address owner) external view returns (uint256)',
    'function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)'
  ]

  const contract = new ethers.Contract(contractAddress, abi, signer)

  let bal = await contract.balanceOf(account.value)
  balance.value = formatEther(bal)

  barrelsInUSD.value = await calculateBarrels(Number(formatEther(bal)))

  const unformattedGasPrice = (await provider.getFeeData()).gasPrice
  gasPrice.value = formatUnits(unformattedGasPrice, 'gwei')
}

async function checkWalletConnected() {
  await checkMetamask()
  const accounts = await window.ethereum.request({ method: 'eth_accounts' })

  if (accounts.length > 0) {
    account.value = accounts[0]
    await connectWallet()
  }
}

async function disconnectWallet() {
  // Revoke permissions when disconnecting wallet
  await window.ethereum.request({
    method: 'wallet_revokePermissions',
    params: [
      {
        eth_accounts: {}
      }
    ]
  })

  provider = null
  account.value = null
  balance.value = ''
}

async function calculateBarrels(wtist: number) {
  return "$ " + oilService.calculateBarrelsInUSD(wtist)
}
</script>

<template>
  <Toast />
  <div class="m-auto">
    <!-- Connect Wallet Button -->
    <div v-if="!account" class="flex flex-col items-center align-middle gap-4 m-auto">
      <Avatar shape="circle" size="xlarge" icon="pi pi-ethereum" class="ether-logo" />
      <span class="text-lg">Connect your Wallet to get started</span>
      <Button v-if="!account" @click="connectWallet">Connect Wallet</Button>
    </div>

    <!-- Display WTI Token Information -->
    <div v-if="account" class="flex flex-col items-start gap-4">
      <div class="flex flex-row gap-1">
        <Button
          label="Exit"
          variant="link"
          size="small"
          @click="disconnectWallet"
          icon="pi pi-arrow-left"
        />
        <Button
          label="Refresh"
          variant="link"
          @click="checkWalletConnected"
          icon="pi pi-refresh"
          size="small"
        />
      </div>

      <Tabs value="0">
        <TabList>
          <Tab value="0">Start</Tab>
          <Tab value="1">Swap</Tab>
          <Tab value="2">Transfer</Tab>
        </TabList>
        <TabPanels class="w-full m-auto">
          <TabPanel value="0">
            <Card>
              <template #title>
                <Avatar icon="pi pi-ethereum" shape="circle" size="normal" class="mr-2" />
                WTIST Stablecoin DApp
              </template>
              <template #content>
                <div class="flex flex-col gap-3">
                  <p>
                    You're connected to the WTI Stablecoin DApp. Here you can swap your USDC for
                    WTIST, transfer WTIST to other accounts, and view stats and charts.
                  </p>

                  <table class="table-auto">
                    <tbody>
                      <tr>
                        <td class="font-bold" style="width: 20vh">Account:</td>
                        <td>{{ account }}</td>
                      </tr>
                      <tr>
                        <td class="font-bold">Your Balance:</td>
                        <td>{{ balance }} WTIST</td>
                      </tr>
                    </tbody>
                  </table>

                  <p class="font-bold text-xl mt-4">Real-world asset equivalence</p>
                  <table class="table-auto">
                    <tbody>
                      <tr>
                        <td class="font-bold" style="width: 20vh">
                          <span class="pi pi-receipt" />
                          Barrels of WTI (approx.)
                        </td>
                        <td>{{ barrelsInUSD }}</td>
                      </tr>
                    </tbody>
                    <caption class="caption-bottom">
                      <p class="italic">
                        1 WTIST = 1 barrel of Western Texas Intermediate Crude Oil
                      </p>
                    </caption>
                  </table>
                </div>
              </template>
            </Card>
          </TabPanel>
          <TabPanel value="1">
            <div class="flex flex-col gap-4">
              <Card>
                <template #title>
                  <div class="flex items-center gap-2">
                    <Avatar image="https://docs.uniswap.org/img/favicon.png" shape="circle" />
                    <span class="font-bold">Swap your Coins with Uniswap V3 SwapRouter</span>
                  </div>
                </template>
                <template #content>
                  <div class="flex flex-col gap-3">
                    <p>
                      The Uniswap V3 SwapRouter allows you to swap your USDC with the Western Texas
                      Intermediate Stablecoin (WTIST).
                    </p>

                    <Button
                      class="p-button-rounded p-button-outlined"
                      icon="pi pi-arrow-right"
                      label="Swap Now"
                      @click="swapVisible = true"
                    />
                  </div>
                </template>
              </Card>

              <Card>
                <template #title>
                  <div class="flex items-center gap-2">
                    <Avatar image="https://pancakeswap.finance/favicon.ico" shape="circle" />
                    <span class="font-bold">Swap your Coins with Pancakeswap</span>
                  </div>
                </template>
                <template #content>
                  <div class="flex flex-col gap-3">
                    <p>
                      Pancakeswap allows you to swap your USDC with the Western Texas Intermediate
                      Stablecoin (WTIST).
                    </p>

                    <Button
                      as="a"
                      class="p-button-rounded p-button-outlined"
                      icon="pi pi-arrow-right"
                      label="Swap Now on Pancakeswap"
                      target="_blank"
                      rel="noopener"
                      href="https://pancakeswap.finance/?chain=arbSepolia&outputCurrency=0x58C653F1d11C3D334c3ee8fe813f4d0A5D5B4A9F&inputCurrency=0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"
                    />
                  </div>
                </template>
              </Card>
            </div>
          </TabPanel>
          <TabPanel value="2">
            <Card>
              <template #content>
                <div class="flex flex-col gap-3">
                  <TransferWidget
                    :provider="provider"
                    :balance="Number.parseFloat(balance)"
                    :gasPrice="gasPrice"
                  />
                </div>
              </template>
            </Card>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>
  </div>

  <Dialog
    v-model:visible="swapVisible"
    modal
    header="Swap with Uniswap"
    :style="{ width: '35rem' }"
  >
    <div class="flex items-center mt-4 mb-4">
      <SwapWidget :provider="provider" :balance="Number.parseFloat(balance)" />
    </div>
  </Dialog>
</template>

<style>
.ether-logo {
  animation: spin-ether 5s ease-in-out infinite;
}

@keyframes spin-ether {
  0% {
    transform: rotate(0deg);
  }
  10% {
    transform: rotate(360deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
