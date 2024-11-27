import { reactive } from 'vue'

export const store = reactive({
    user: {
        account: '',
        balance: 0
    },
    setAccount(account: string) {
        store.user.account = account
    },
    setBalance(balance: number) {
        store.user.balance = balance
    }
})