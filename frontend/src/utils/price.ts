/**
 * Calculate the price of a token from its sqrtPriceX96 value
 * the price is calculated as sqrtPriceX96^2 / (2^96)^2 * 10^12
 * the 12 is to convert the price to the same scale as the token0 and token1 decimals delta (18-6=12)
 * @param x96 
 * @returns 
 */
export function convertX96ToPrice(x96: Number): string {
    return ((Number(x96) ** 2 / ((2 ** 96) ** 2)) * 10 ** 12).toFixed(5) + "";
}