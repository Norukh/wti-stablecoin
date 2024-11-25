<script setup lang="ts">
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Dialog from 'primevue/dialog'
import { ref } from 'vue'

type Transfer = {
  recipientAddress: string
  amount: number | undefined
  symbol: string
}

const transferInfo = ref<Transfer>({
  recipientAddress: '',
  amount: undefined,
  symbol: 'WTIST'
})

const showApproveDialog = ref(false)

const approveTransfer = () => {
  console.log(
    `Transfer ${transferInfo.value.amount} WTIST to ${transferInfo.value.recipientAddress}`
  )
}
</script>

<template>
  <Card style="height: auto; max-width: 50vh" class="m-auto">
    <template #header>
      <img alt="user header" src="https://picsum.photos/400/100" />
    </template>
    <template #title>Transfer WTIST</template>
    <template #subtitle>
      <p class="text-sm mb-4">
        Transfer WTIST to another account and contribute to the future of oil trading.
      </p>
    </template>
    <template #content>
      <div class="flex flex-col gap-4">
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5">
              <i class="pi pi-wallet"></i>
            </InputGroupAddon>
            <FloatLabel variant="in">
              <InputText id="in_recipientAddress" v-model="transferInfo.recipientAddress" />
              <label for="in_recipientAddress">Recipient (0x...)</label>
            </FloatLabel>
          </InputGroup>
        </div>
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5">{{ transferInfo.symbol }}</InputGroupAddon>
            <FloatLabel variant="in">
              <InputText id="in_recipientAmount" v-model="transferInfo.amount" />
              <label for="in_recipientAmount">Amount</label>
            </FloatLabel>
          </InputGroup>
        </div>
      </div>
    </template>
    <template #footer>
      <div class="flex gap-4 mt-5">
        <Button
          label="Approve and Transfer"
          severity="primary"
          outlined
          class="w-full text-center grow"
          @click="showApproveDialog = true"
        />
      </div>
    </template>
  </Card>

  <Dialog
    v-model:visible="showApproveDialog"
    modal
    header="Transfer Confirmation"
    :style="{ width: '25rem' }"
  >
    <p>
      Are you sure you want to transfer {{ transferInfo.value }} {{ transferInfo.symbol }} to
      {{ transferInfo.recipientAddress }}?
    </p>
    <template #footer>
      <Button label="Yes" class="p-button-success" />
      <Button label="No" class="p-button-danger" />
    </template>
  </Dialog>
</template>
