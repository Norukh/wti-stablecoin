<script setup lang="ts">
import { ethers, formatEther } from 'ethers'
import { ref } from 'vue'

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
const totalSupply = ref(0)

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

  await provider.send('eth_requestAccounts', [])

  const signer = await provider.getSigner()
  account.value = await signer.getAddress()

  // initialize contract
  const contractAddress = '0x58C653F1d11C3D334c3ee8fe813f4d0A5D5B4A9F'

  const abi = [
    'function balanceOf(address owner) external view returns (uint256)',
    'function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)'
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
  <div class="m-auto">
    <!-- Connect Wallet Button -->
    <div v-if="!account" class="flex flex-col items-center align-middle gap-4 m-auto">
      <Avatar icon="pi pi-ethereum" shape="circle" size="xlarge" />
      <span class="text-lg">Connect your Wallet to get started</span>
      <Button v-if="!account" @click="connectWallet">Connect Wallet</Button>
    </div>

    <!-- Display WTI Token Information -->
    <div v-if="account" class="flex flex-col items-start gap-4">

      <div class="flex flex-row gap-1">
        <Button label="Exit" variant="link" size="small" @click="account = null" icon="pi pi-arrow-left" />
        <Button label="Refresh" variant="link" @click="checkWalletConnected" icon="pi pi-refresh" size="small" />
      </div>

      <Tabs value="0">
        <TabList>
          <Tab value="0">Start</Tab>
          <Tab value="1">Swap</Tab>
          <Tab value="2">Transfer</Tab>
          <Tab value="3">Stats and Charts</Tab>
        </TabList>
        <TabPanels class="w-full m-auto">
          <TabPanel value="0">
            <Card>
              <template #title>WTIST Stablecoin DApp</template>
              <template #content>
                <p class="m-0">
                  <div v-if="account">Connected as: {{ account }}</div>
                </p>
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
                    The Uniswap V3 SwapRouter allows you to swap your USDC with the Western Texas Intermediate Stablecoin (WTIST).
                  </p>

                  <Button
                    class="p-button-rounded p-button-outlined"
                    icon="pi pi-arrow-right"
                    label="Swap Now"
                    @click="swapVisible = true"
                    >
                  </Button>
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
                    Pancakeswap allows you to swap your USDC with the Western Texas Intermediate Stablecoin (WTIST).
                  </p>

                  <Button
                    class="p-button-rounded p-button-outlined"
                    icon="pi pi-arrow-right"
                    label="Swap Now on Pancakeswap"
                    >
                  </Button>
                </div>
              </template>
            </Card>
            </div>
          </TabPanel>
          <TabPanel value="2">
            <Card>
              <template #title>Transfer WTIST</template>
              <template #content>
                <div class="flex flex-col gap-3">
                  <TransferWidget />
                </div>
              </template>
            </Card>
          </TabPanel>
          <TabPanel value="3">
            <Card>
              <template #title>WTIST Stablecoin DApp</template>
              <template #content>
                <p class="m-0">
                  <div v-if="account">Connected as: {{ account }}</div>
                </p>
              </template>
            </Card>
          </TabPanel>
        </TabPanels>
      </Tabs>

      <!--
      <h3>Your Balance: {{ balance }} WTI</h3>
      <h3>Total Supply: {{ totalSupply }} WTI</h3>
      <h3>WTI Price (USD): ${{ wtiPrice }}</h3>
      <br />
       
      <h2>Mint WTI Tokens</h2>
      <input v-model="collateralAmount" placeholder="Enter collateral (ETH)" />
      <button @click="mintWTI">Mint</button>


      <h2>Burn WTI Tokens</h2>
      <input v-model="burnAmount" placeholder="Enter WTI amount to burn" />
      <button @click="burnWTI">Burn</button>


      <h2>Send Token</h2>
      <input v-model="recipientAddress" placeholder="Enter recipient address" />
      <input v-model="sendAmount" placeholder="Enter WTI amount to send" />
      <button @click="sendWTI">Send</button>
    </div>
  -->
    </div>
  </div>

  <Dialog v-model:visible="swapVisible" modal header="Swap with Uniswap" :style="{ width: '25rem' }">
            <div class="flex items-center mt-4 mb-4">
              <SwapWidget />
            </div>
        </Dialog>
</template>
