import http from './http.service'

export default class OilService {
    getPrice() {
        return http.get('/oil/price')
    }

    calculateBarrelsInUSD(amount: number) {
        return Math.round(amount)
    }
  }
  
  export const oilService = new OilService()