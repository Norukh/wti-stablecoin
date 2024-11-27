<script setup lang="ts">
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import { ref } from 'vue'
import { UNISWAP_SWAP_ROUTER_ADDRESSES } from '@/utils/constants'

defineProps({
  provider: Object,
})

type Token = {
  symbol: string,
  address: string,
  decimals: number,
  value: number | undefined,
}

const payToken = ref<Token>(
  {
    symbol: 'USDC',
    address: '',
    decimals: 6,
    value: undefined,
  }
)
const receiveToken = ref<Token>(
  {
    symbol: 'WTIST',
    address: '',
    decimals: 18,
    value: undefined,
  }
)

const switchTokens = () => {
  const temp = payToken.value
  payToken.value = receiveToken.value
  receiveToken.value = temp
}

async function swapTokens() {
  const signer = await provider.getSigner()

  const contractAddress = UNISWAP_SWAP_ROUTER_ADDRESSES['arbSepolia']

  const abi = [
    'function swapTokens(address tokenA, address tokenB, uint amountA) external'
  ]

  const contract = new ethers.Contract(contractAddress, abi, signer)

  // todo call contract and swap tokens
  // see what can be done with result

}

</script>

<template>
  <Card style="height: auto; max-width: 50vh;" class="m-auto">
    <template #header>
      <img alt="user header" src="https://picsum.photos/400/100" />
    </template>
    <template #title>Swap WTIST</template>
    <template #subtitle>
        <p class="text-sm mb-4">
            Invest in the Western Texas Intermediate Stablecoin (WTIST) and contribute to the future of oil trading.
        </p>
    </template>
    <template #content>
      <div class="flex flex-col gap-4">
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5">{{ payToken.symbol }}</InputGroupAddon>
            <FloatLabel variant="in">
              <InputText id="in_label" v-model="payToken.value" />
              <label for="in_label">Sell</label>
            </FloatLabel>
          </InputGroup>
        </div>
        <div class="text-center">
          <Button class="spin" icon="pi pi-sort-alt" aria-label="Save" outlined @click="switchTokens" />
        </div> 
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5">{{ receiveToken.symbol }}</InputGroupAddon>
            <FloatLabel variant="in">
              <InputText id="in_label2" v-model="receiveToken.value" />
              <label for="in_label2">Buy</label>
            </FloatLabel>
          </InputGroup>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex gap-4 mt-5">
        <Button label="Swap" severity="primary" outlined class="w-full text-center grow" />
      </div>
    </template>
  </Card>
</template>