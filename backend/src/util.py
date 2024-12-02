def format_units(number, decimals) -> float:
    return number / 10 ** decimals


def parse_units(number, decimals) -> int:
    return int(number * 10 ** decimals)


def sqrt_price_X96_to_price(sqrtPriceX96: int) -> float:
    return (sqrtPriceX96 ** 2 / ((2 ** 96) ** 2)) * 10 ** 12
