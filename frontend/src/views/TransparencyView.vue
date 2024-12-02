<script setup lang="ts">
import { ref } from 'vue'
import Panel from 'primevue/panel'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'

import { oilService } from '../services/oil.service'

const currentOilSupply = ref(0)
const transactions = ref([])

const transactionsVisible = ref<boolean>(false)

oilService.getCurrentOilSupply().then((res) => {
  currentOilSupply.value = res.amount
})

oilService.getTransactions().then((res) => {
  transactions.value = res
  console.log(res)
})
</script>

<template>
  <div class="flex flex-col justify-center">
    <h1 class="text-4xl">Transparency & Stability</h1>
    <p class="text-lg mt-5">
      The WTIST stablecoin is a transparent and stable digital currency that is backed by real-world
      oil reserves.
    </p>

    <div class="card mt-4">
      <Panel toggleable collapsed>
        <template #header>
          <div class="flex items-center gap-2">
            <Avatar
              icon="pi pi-key"
              shape="circle"
              size="normal"
              style="
                background-color: var(--p-success-color);
                color: var(--p-success-contrast-color);
              "
            />
            <span class="font-bold">Oil Reserves Composition</span>
          </div>
        </template>

        <p class="font-bold">Current Reserves:</p>

        <p>{{ currentOilSupply }} Barrels.</p>

        <p class="font-bold mt-4">Last 10 Transactions</p>

        <Button class="mt-2" label="Show Transactions" @click="transactionsVisible = true" icon="pi pi-truck" />

        <p class="m-0 mt-4">
          The WTIST stablecoin is backed by oil reserves. The Western Texas Intermediate oil
          reserves are stored in secure locations around the world and are audited regularly to
          ensure that the reserves are sufficient to back the WTIST stablecoin.
        </p>
      </Panel>
    </div>

    <div class="card mt-4">
      <Panel toggleable collapsed>
        <template #header>
          <div class="flex items-center gap-2">
            <Avatar
              icon="pi pi-share-alt"
              shape="circle"
              size="normal"
              style="
                background-color: var(--p-success-color);
                color: var(--p-success-contrast-color);
              "
            />
            <span class="font-bold">Blockchain Transparency</span>
          </div>
        </template>

        <p class="m-0">
          The WTI Stablecoin DApp is built on the Ethereum blockchain, which is a public and
          transparent blockchain.
        </p>

        <Button
          as="a"
          label="WTI Stablecoin Github Repository"
          href="https://github.com/Norukh/wti-stablecoin"
          target="_blank"
          rel="noopener"
          class="mt-4"
          icon="pi pi-github"
        />

        <Button
          as="a"
          label="WTIST Coin Contract on Sepolia Arbiscan"
          href="https://sepolia.arbiscan.io/token/0x58c653f1d11c3d334c3ee8fe813f4d0a5d5b4a9f"
          target="_blank"
          rel="noopener"
          class="mt-4"
          icon="pi pi-ethereum"
        />
      </Panel>
    </div>

    <Dialog
      v-model:visible="transactionsVisible"
      modal
      header="Last 10 Transactions"
      :style="{ width: '35rem' }"
    >
      <DataTable :value="transactions" class="mt-4">
        <Column field="timestamp" header="Time"></Column>
        <Column field="action" header="Action"></Column>
        <Column field="amount" header="Amount"></Column>
        <Column field="position" header="Position"></Column>
      </DataTable>
    </Dialog>
  </div>
</template>
