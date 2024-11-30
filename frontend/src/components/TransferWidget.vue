<script setup lang="ts">
import { ethers, formatEther, parseUnits } from 'ethers'
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputGroup from 'primevue/inputgroup'
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import Dialog from 'primevue/dialog'
import Message from 'primevue/message'
import { ref } from 'vue'
import { WTIST_CONTRACT_ADDRESSES } from '@/utils/constants'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

const props = defineProps({
  provider: Object,
  balance: Number,
  gasPrice: String
})

const isInvalidAddress = ref<boolean>(false)
const isInvalidAmount = ref<boolean>(false)
const isInsufficientBalance = ref<boolean>(false)

const estimatedGas = ref('')
const transferStatus = ref('')

const loadingTransfer = ref(false)

const transactionHash = ref('')

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

const contractAddress = WTIST_CONTRACT_ADDRESSES['arbSepolia']
const abi = [
  'function balanceOf(address owner) external view returns (uint256)',
  'function approve(address spender, uint256 amount) external',
  'function transferFrom(address sender, address recipient, uint256 amount) external returns (bool)'
]

async function estimateGas() {
  const signer = await props.provider?.getSigner()
  const contract = new ethers.Contract(contractAddress, abi, signer)

  const signerAddress = await signer?.getAddress()

  const txApprove = await contract.approve.estimateGas(signerAddress, transferInfo.value.amount)

  estimatedGas.value = txApprove.toString()
}

async function openApproveDialog() {
  if (!ethers.isAddress(transferInfo.value.recipientAddress)) {
    isInvalidAddress.value = true
    console.error('Invalid recipient address')
    return
  }

  if (
    transferInfo.value.amount === undefined ||
    transferInfo.value.amount <= 0 ||
    isNaN(transferInfo.value.amount)
  ) {
    isInvalidAmount.value = true
    console.error('Invalid transfer amount')
    return
  }

  if (transferInfo.value.amount && props.balance && props.balance < transferInfo.value.amount) {
    isInsufficientBalance.value = true
    console.error('Insufficient balance')
    return
  }

  loadingTransfer.value = false
  showApproveDialog.value = true
}

async function approveTransfer() {
  loadingTransfer.value = true

  const signer = await props.provider?.getSigner()
  const signerAddress = await signer?.getAddress()

  const contract = new ethers.Contract(contractAddress, abi, signer)

  let balance = await contract.balanceOf(signerAddress)
  balance = formatEther(balance)

  if (transferInfo.value.amount && balance < transferInfo.value.amount) {
    isInsufficientBalance.value = true
    console.error('Insufficient balance')

    showApproveDialog.value = false
    toast.add({
      severity: 'error',
      summary: 'Insufficient balance',
      detail: 'Your balance is not enough to complete the transfer',
      life: 5000
    })
    return
  }

  const parsedAmount = parseUnits(transferInfo.value.amount!.toString(), 18)

  try {
    transferStatus.value = `Approving WTIST transfer...`

    const tx = await contract.approve(signerAddress, parsedAmount)
    console.log('Transaction hash: ', tx.hash)

    const receipt = await tx.wait()
    console.log('Transaction receipt: ', receipt)

    transferStatus.value = `WTIST transfer approved successfully`

    showApproveDialog.value = true
  } catch (error: any) {
    toast.add({
      severity: 'error',
      summary: 'Error approving WTIST transfer',
      detail: error.message.toString(),
      life: 5000
    })
    console.error('Error approving WTIST transfer: ', error)

    showApproveDialog.value = false
  }

  try {
    transferStatus.value = `Transferring WTIST...`

    const tx = await contract.transferFrom(
      signerAddress,
      transferInfo.value.recipientAddress,
      parsedAmount
    )
    console.log('Transaction hash: ', tx.hash)

    const receipt = await tx.wait()
    console.log('Transaction receipt: ', receipt)

    transferStatus.value = `WTIST transferred successfully`

    showApproveDialog.value = false
    loadingTransfer.value = false

    transactionHash.value = tx.hash

    toast.add({
      severity: 'success',
      summary: `WTIST transferred successfully`,
      detail: `Gas used: ${receipt.gasUsed}, Transaction hash: ${tx.hash}`,
      life: 5000
    })
  } catch (error: any) {
    toast.add({
      severity: 'error',
      summary: 'Error transferring WTIST',
      detail: error.message.toString(),
      life: 5000
    })
    console.error('Error transferring WTIST: ', error)

    showApproveDialog.value = false
  }
}

function wtiToUsd(wti: number) {
  return wti * 70
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
          <span class="text-sm">Your balance: {{ props.balance }} WTIST</span>
        </div>
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5" :invalid="isInvalidAddress">
              <i class="pi pi-wallet"></i>
            </InputGroupAddon>
            <FloatLabel variant="in">
              <InputText
                id="in_recipientAddress"
                v-model="transferInfo.recipientAddress"
                :invalid="isInvalidAddress"
                @keydown="(isInvalidAddress = false), (transactionHash = '')"
              />
              <label for="in_recipientAddress">Recipient (0x...)</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="isInvalidAddress" severity="error" variant="simple" size="small"
            >Valid address is required</Message
          >
        </div>
        <div>
          <InputGroup>
            <InputGroupAddon class="w-1/5" :invalid="isInvalidAmount">{{ transferInfo.symbol }}</InputGroupAddon>
            <FloatLabel variant="in">
              <InputText
                id="in_recipientAmount"
                v-model="transferInfo.amount"
                :invalid="isInvalidAmount"
                @keydown="
                  (isInvalidAmount = false), (isInsufficientBalance = false), (transactionHash = '')
                "
              />
              <label for="in_recipientAmount">Amount</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="isInvalidAmount" severity="error" variant="simple" size="small"
            >Valid amount is required</Message
          >
        </div>

        <Message
          severity="info"
          size="small"
          v-if="transferInfo.amount !== undefined && transferInfo.amount > 0 && !transactionHash"
        >
          <p>
            Your transfer is equal to {{ transferInfo.amount }} barrels of oil and to ${{
              wtiToUsd(transferInfo.amount)
            }}.
          </p>
        </Message>

        <Message severity="error" size="small" v-if="isInsufficientBalance">
          <p>Insufficient balance. Your balance is {{ props.balance }} WTIST.</p>
        </Message>

        <Message
          severity="success"
          size="small"
          v-if="!loadingTransfer && transactionHash"
          class="mt-4 w-full"
        >
          <p>
            Transaction successful. Check your wallet for the transfer. Check the transaction
            <Button
              as="a"
              variant="link"
              size="small"
              :href="`https://sepolia.arbiscan.io/tx/${transactionHash}`"
              target="_blank"
              rel="noopener noreferrer"
              label="here"
            />
            on Sepolia Arbiscan.
          </p>
        </Message>
      </div>
    </template>
    <template #footer>
      <div class="flex gap-4 mt-5">
        <Button
          label="Approve and Transfer"
          severity="primary"
          outlined
          class="w-full text-center grow"
          @click="openApproveDialog"
        />
      </div>
    </template>
  </Card>

  <Dialog
    v-model:visible="showApproveDialog"
    modal
    header="Transfer Confirmation"
    :style="{ width: '35rem' }"
  >
    <p>Are you sure you want to execute the following transfer?</p>
    <table class="table-auto mt-4">
      <tbody>
        <tr>
          <td class="font-bold" style="width: 20vh">Recipient:</td>
          <td>{{ transferInfo.recipientAddress }}</td>
        </tr>
        <tr>
          <td class="font-bold">Amount:</td>
          <td>{{ transferInfo.amount }} WTIST</td>
        </tr>
        <tr>
          <td class="font-bold">USD Equivalent:</td>
          <td>${{ wtiToUsd(transferInfo.amount) }}</td>
        </tr>
        <tr>
          <td class="font-bold">Gas Price:</td>
          <td>{{ props.gasPrice }} Gwei</td>
        </tr>
        <tr>
          <td class="font-bold">Estimated Gas:</td>
          <td>
            <div class="flex flex-row gap-2 items-center">
              <Button
                label="Estimate Gas"
                class="p-button-info"
                @click="estimateGas"
                size="small"
                icon="pi pi-refresh"
                variant="outlined"
              />
              <span v-if="estimatedGas">{{ estimatedGas }} Gas Units</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <Message severity="info" size="small" v-if="loadingTransfer" class="mt-4 w-full">
      <p>
        {{ transferStatus }}
      </p>
    </Message>

    <template #footer>
      <Button
        label="Confirm"
        class="p-button-success"
        @click="approveTransfer"
        :loading="loadingTransfer"
        :disabled="loadingTransfer"
      />
      <Button
        label="Cancel"
        class="p-button-danger"
        @click="(showApproveDialog = false), (loadingTransfer = false)"
        :disabled="loadingTransfer"
      />
    </template>
  </Dialog>
</template>
