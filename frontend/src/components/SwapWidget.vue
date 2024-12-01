<script setup lang="ts">
import { ethers, parseUnits, formatUnits } from 'ethers'
import QuoterV2 from '@uniswap/v3-periphery/artifacts/contracts/lens/QuoterV2.sol/QuoterV2.json'
import SwapRouter02 from '@uniswap/swap-router-contracts/artifacts/contracts/SwapRouter02.sol/SwapRouter02.json'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Message from 'primevue/message'
import { ref } from 'vue'
import {
  UNISWAP_SWAP_ROUTER_ADDRESSES,
  USDC_CONTRACT_ADDRESSES,
  WTIST_CONTRACT_ADDRESSES,
  UNISWAP_POOL_ADDRESSES,
  UNISWAP_QUOTER_ADDRESSES
} from '@/utils/constants'
import { convertX96ToPrice } from '@/utils/price'

const props = defineProps({
  provider: Object,
  balance: Number
})

const chain = 'arbSepolia'
const poolFee = 10000

const isInvalidAmountPay = ref<boolean>(false)
const isInvalidAmountReceive = ref<boolean>(false)

const swapStatus = ref<string>('')
const loadingSwap = ref<boolean>(false)

type Token = {
  symbol: string
  address: string
  value: string | undefined
}

type PoolData = {
  sqrtPriceX96: number
  tick: number
  observationIndex: number
  observationCardinality: number
  observationCardinalityNext: number
  feeProtocol: number
  unlocked: boolean
}

const poolData = ref<PoolData>({
  sqrtPriceX96: 0,
  tick: 0,
  observationIndex: 0,
  observationCardinality: 0,
  observationCardinalityNext: 0,
  feeProtocol: 0,
  unlocked: false
})

type PriceQuote = {
  amountOut: number
  sqrtPriceX96After: number
  initializedTicksCrossed: boolean
  gasEstimate: number
}

const priceQuote = ref<PriceQuote>({
  amountOut: 0,
  sqrtPriceX96After: 0,
  initializedTicksCrossed: false,
  gasEstimate: 0
})

const payToken = ref<Token>({
  symbol: 'USDC',
  address: '',
  value: ''
})
const receiveToken = ref<Token>({
  symbol: 'WTIST',
  address: '',
  value: ''
})

const switchTokens = () => {
  const temp = { ...payToken.value }

  payToken.value = receiveToken.value
  receiveToken.value = temp
}

async function calculateBuyPrice(isPay = true) {
  const signer = await props.provider?.getSigner()

  const quoterContractAddress = UNISWAP_QUOTER_ADDRESSES[chain]
  const quoterAbi = QuoterV2.abi

  const usdcContractAddress = USDC_CONTRACT_ADDRESSES[chain]
  const wtistContractAddress = WTIST_CONTRACT_ADDRESSES[chain]

  const quoterContract = new ethers.Contract(quoterContractAddress, quoterAbi, signer)

  const decPay = payToken.value.symbol === 'USDC' ? 6 : 18
  const amountIn = isPay ? payToken.value.value : receiveToken.value.value

  if (amountIn === undefined || amountIn === '') {
    receiveToken.value.value = ''
    return
  }

  const parsedAmountIn = parseUnits(amountIn!.toString(), decPay)

  if (parsedAmountIn.valueOf() <= 0) {
    receiveToken.value.value = ''
    return
  }

  const amountOutData = await quoterContract.quoteExactInputSingle
    .staticCall({
      tokenIn: payToken.value.symbol === 'USDC' ? usdcContractAddress : wtistContractAddress,
      tokenOut: receiveToken.value.symbol === 'USDC' ? usdcContractAddress : wtistContractAddress,
      amountIn: parsedAmountIn,
      fee: poolFee,
      sqrtPriceLimitX96: 0
    })
    .then((data: Array<number>) => {
      return {
        amountOut: data[0],
        sqrtPriceX96After: data[1],
        initializedTicksCrossed: data[2],
        gasEstimate: data[3]
      }
    })

  console.log('Amount out data:', amountOutData)

  const decReceive = receiveToken.value.symbol === 'USDC' ? 6 : 18
  receiveToken.value.value = formatUnits(amountOutData.amountOut, decReceive).slice(0, 10)
}

async function swapTokens() {
  const signer = await props.provider?.getSigner()

  const swapContractAddress = UNISWAP_SWAP_ROUTER_ADDRESSES[chain]
  const swapAbi = SwapRouter02.abi

  const erc20abi = [
    'function approve(address spender, uint256 amount) external returns (bool)',
    'function decimals() external view returns (uint8)'
  ]

  const usdcContractAddress = USDC_CONTRACT_ADDRESSES[chain]
  const wtistContractAddress = WTIST_CONTRACT_ADDRESSES[chain]

  const swapContract = new ethers.Contract(swapContractAddress, swapAbi, signer)
  const usdcContract = new ethers.Contract(usdcContractAddress, erc20abi, signer)
  const wtistContract = new ethers.Contract(wtistContractAddress, erc20abi, signer)

  const usdcDecimals = await usdcContract.decimals()
  const wtistDecimals = await wtistContract.decimals()

  const usdcAmount = parseUnits(payToken.value.value!.toString(), usdcDecimals)
  const wtistAmount = parseUnits(receiveToken.value.value!.toString(), wtistDecimals)

  console.log('USDC amount:', usdcAmount.toString())
  console.log('WTIST amount:', wtistAmount.toString())

  if (payToken.value.symbol === 'USDC') {
    const usdcApprove = await usdcContract.approve(swapContractAddress, usdcAmount)
    console.log('USDC approve:', usdcApprove)
  } else {
    const wtistApprove = await wtistContract.approve(swapContractAddress, wtistAmount)
    console.log('WTIST approve:', wtistApprove)
  }

  const swap = await swapContract.exactInputSingle({
    tokenIn: payToken.value.symbol === 'USDC' ? usdcContractAddress : wtistContractAddress,
    tokenOut: receiveToken.value.symbol === 'USDC' ? usdcContractAddress : wtistContractAddress,
    fee: poolFee,
    recipient: await signer.getAddress(),
    amountIn: payToken.value.symbol === 'USDC' ? usdcAmount : wtistAmount,
    amountOutMinimum: 0,
    sqrtPriceLimitX96: 0
  })

  console.log('Swap:', swap)
}

async function evaluateSwap() {
  if (
    payToken.value.value === undefined ||
    payToken.value.value <= 0 ||
    isNaN(payToken.value.value)
  ) {
    isInvalidAmountPay.value = true
    return
  }

  if (
    receiveToken.value.value === undefined ||
    receiveToken.value.value <= 0 ||
    isNaN(receiveToken.value.value)
  ) {
    isInvalidAmountReceive.value = true
    return
  }

  if (payToken.value.symbol === receiveToken.value.symbol) {
    swapStatus.value = 'Tokens must be different'
    return
  }

  swapStatus.value = ''
  loadingSwap.value = true

  await swapTokens()

  loadingSwap.value = false
}

async function getSwapPrice() {
  const signer = await props.provider?.getSigner()

  const poolContractAddress = UNISWAP_POOL_ADDRESSES[chain]
  const poolAbi = [
    'function slot0() external view returns (uint160 sqrtPriceX96, int24 tick, uint16 observationIndex, uint16 observationCardinality, uint16 observationCardinalityNext, uint8 feeProtocol, bool unlocked)'
  ]

  const poolContract = new ethers.Contract(poolContractAddress, poolAbi, signer)

  const slot0 = (await poolContract.slot0().then((data: Array<number>) => {
    return {
      sqrtPriceX96: data[0],
      tick: data[1],
      observationIndex: data[2],
      observationCardinality: data[3],
      observationCardinalityNext: data[4],
      feeProtocol: data[5],
      unlocked: data[6]
    }
  })) as PoolData
  console.log('Pool data:', slot0)
  poolData.value = slot0
}

getSwapPrice()
</script>

<template>
  <Card style="height: auto; max-width: 50vh" class="m-auto">
    <template #header>
      <img alt="user header" src="https://picsum.photos/600/150" />
    </template>
    <template #title>Swap WTIST with USDC</template>
    <template #subtitle>
      <p class="text-sm mb-4">
        Invest in the Western Texas Intermediate Stablecoin (WTIST) and contribute to the future of
        oil trading.
      </p>
    </template>
    <template #content>
      <div class="flex flex-col gap-4">
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5" :invalid="isInvalidAmountPay">
              {{ payToken.symbol }}
            </InputGroupAddon>
            <FloatLabel variant="in">
              <InputText
                id="in_label"
                v-model="payToken.value"
                :invalid="isInvalidAmountPay"
                @keydown="calculateBuyPrice(), (isInvalidAmountPay = false)"
              />
              <label for="in_label">Sell</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="isInvalidAmountPay" severity="error" variant="simple" size="small"
            >Valid amount for selling {{ payToken.symbol }} is required
          </Message>
        </div>
        <div class="text-center">
          <Button
            class="spin"
            icon="pi pi-sort-alt"
            aria-label="Save"
            outlined
            @click="switchTokens"
          />
        </div>
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5" :invalid="isInvalidAmountReceive">
              {{ receiveToken.symbol }}
            </InputGroupAddon>
            <FloatLabel variant="in">
              <InputText
                id="in_label2"
                v-model="receiveToken.value"
                :invalid="isInvalidAmountReceive"
                @keydown="isInvalidAmountReceive = false"
              />
              <label for="in_label2">Buy</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="isInvalidAmountReceive" severity="error" variant="simple" size="small"
            >Valid amount for buying {{ receiveToken.symbol }} is required
          </Message>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex gap-4 mt-5 flex-col">
        <Button
          label="Swap"
          severity="primary"
          outlined
          class="w-full text-center grow"
          @click="evaluateSwap"
        />

        <div class="flex justify-center flex-col gap-1">
          <p>
            <b>Swap Price</b>
          </p>
          <div class="flex flex-row gap-2 items-center">
            <Button size="small" variant="outlined" icon="pi pi-refresh" @click="getSwapPrice" />
            <p>1 WTIST = {{ convertX96ToPrice(poolData.sqrtPriceX96) }} USDC</p>
          </div>
        </div>
      </div>
    </template>
  </Card>
</template>
