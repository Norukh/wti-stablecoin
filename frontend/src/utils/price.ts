export function convertX96(x96: Number): string {
    return (Number(x96) ** 2 / 2 ** 192).toFixed(5) + "";
}