<script setup lang="ts">
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import { ref } from 'vue'

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

</script>

<template>
  <Card style="width: 25rem; overflow: hidden">
    <template #header>
      <img alt="user header" src="https://picsum.photos/400/200" />
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
              <label for="in_label">You pay</label>
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
              <label for="in_label2">You receive</label>
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

<style>
.spin:hover {
  animation: spin 0.3s ease-in-out;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(180deg);
  }
}

.grow:hover {
  animation: grow 0.3s ease-in-out alternate infinite;
}

@keyframes grow {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.1);
  }
}

</style>