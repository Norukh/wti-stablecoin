import http from './http.service'
import { formatUnits } from 'ethers'

export default class OilService {
    async getPrice() {
        return http.get('/price').then((response) => {
            return Number(formatUnits(response.data.price, response.data.decimals)).toFixed(2)
        })
    }

    async calculateBarrelsInUSD(amount: number) {
        return http.get('/price').then((response) => {
            return (amount * Number(formatUnits(response.data.price, response.data.decimals))).toFixed(2)
        })
    }

    async getTransactions() {
        return http.get('/transactions').then((response) => {
            return response.data
        })
    }

    async getCurrentOilSupply() {
        return http.get('/oil').then((response) => {
            return response.data
        })
    }
  }
  
  export const oilService = new OilService()