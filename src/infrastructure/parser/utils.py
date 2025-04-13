import re


def parse_mileage(mileage_str: str) -> int:
    cleaned = mileage_str.lower().replace(" ", "")

    if "тис" in cleaned:
        number_str = re.sub(r"[^\d]", "", cleaned)
        return int(number_str) * 1000
    else:
        number_str = re.sub(r"[^\d]", "", cleaned)
        return int(number_str)


def parse_price(price_str: str) -> int:
    number_str = re.sub(r"[^\d]", "", price_str)
    return int(number_str)
