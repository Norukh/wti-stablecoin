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
  }
  
  export const oilService = new OilService()