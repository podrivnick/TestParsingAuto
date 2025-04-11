import json
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_olx_autos(url: str) -> list:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/85.0.4183.121 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,uk;q=0.7",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    links_all_cars = []
    page = 1
    seen_pages = set()

    while True:
        if page == 2:
            break
        paginated_url = f"{url}?page={page}"

        if paginated_url in seen_pages:
            print(f"Зацикливание обнаружено. Завершаем выполнение на странице {page}.")
            break

        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            print(f"Ошибка запроса на странице {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="css-1ut25fa")

        seen_pages.add(paginated_url)

        for listing in listings:
            try:
                link = listing.find("a", href=True)
                if link:
                    product_url = urljoin(url, link["href"])
                    links_all_cars.append(product_url)

            except Exception as e:
                print(f"Ошибка при обработке объявления: {e}")
                continue

        page += 1

    return links_all_cars


def parsing_data_cars(url: str) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/85.0.4183.121 Safari/537.36"
        ),
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, "html.parser")
    car_details = {}

    try:
        # Base Data
        mark = soup.find("h4", class_="css-10ofhqw").get_text(strip=True)
        car_details["mark"] = mark

        price = soup.find("h3", class_="css-fqcbii").get_text(strip=True)
        car_details["price"] = price

        # Car Details
        for p in soup.find_all("p", class_="css-1los5bp"):
            text = p.get_text(strip=True)
            # logging.info(f"{text}!")
            if "Рік випуску" in text:
                try:
                    car_details["year_created"] = int(text.split(":")[-1].strip())
                except ValueError:
                    pass

            if "Пробіг" in text:
                km = text.split(":")[-1].strip().lower()
                try:
                    car_details["mileage"] = km
                except ValueError:
                    pass

            if "Тип палива" in text:
                car_details["engine_type"] = text.split(":")[-1].strip()

            if "Коробка передач" in text:
                car_details["gear_box"] = text.split(":")[-1].strip()

            if "Об'єм двигуна" in text:
                val = text.split(":")[-1].strip().lower()
                try:
                    car_details["engine_capacity"] = val
                except ValueError:
                    pass

            if "Тип приводу" in text:
                car_details["drive_type"] = text.split(":")[-1].strip()

            if "Модель" in text:
                car_details["model"] = text.split(":")[-1].strip()

        # Location
        location_block = soup.find("div", class_="css-1q7h1ph")
        if not location_block:
            logging.warning("Блок с классом css-1q7h1ph не найден.")
        else:
            city_el = location_block.find("p", class_="css-7wnksb")
            region_el = location_block.find("p", class_="css-2n34b3")

            city = city_el.get_text(strip=True) if city_el else ""
            region = region_el.get_text(strip=True) if region_el else ""

            logging.info(f"Блок локации: {location_block}")
            logging.info(f"Город: {city}")
            logging.info(f"Регион: {region}")

            full_location = ", ".join(filter(None, [city, region]))
            car_details["location"] = full_location

    except Exception as e:
        print(f"Ошибка при обработке деталей автомобиля: {e}")

    return car_details


if __name__ == "__main__":
    url = "https://www.olx.ua/uk/transport/legkovye-avtomobili/"
    car_links = parse_olx_autos(url)

    car_list = []
    for car_url in car_links:
        print(f"Обрабатываем ссылку: {car_url}")
        car_info = parsing_data_cars(car_url)
        if car_info:
            car_list.append(car_info)

    json_output = json.dumps(car_list, ensure_ascii=False, indent=4)
    print(json_output)
