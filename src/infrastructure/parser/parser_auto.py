import logging
import re
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def init_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=uk")

    # Используем webdriver-manager для автоматической загрузки нужной версии ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd("Network.enable", {})

    custom_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/85.0.4183.121 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "uk,ru,en;q=0.8",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": custom_headers})

    return driver


def parse_olx_autos(url: str, driver, offset: int = 1) -> list:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    car_links = []
    page = 0

    while True:
        if page == offset:
            break
        paginated_url = f"{url}?page={page}"
        logging.info(f"Обробляємо сторінку {page}: {paginated_url}")

        driver.get(paginated_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        listings = soup.find_all("div", class_="css-1ut25fa")
        if not listings:
            logging.info("Оголошення не знайдені - закінчуємо обхід пагінації.")
            break

        for listing in listings:
            try:
                link_tag = listing.find("a", href=True)

                if link_tag:
                    product_url = urljoin(url, link_tag["href"])
                    car_links.append(product_url)

            except Exception as e:
                logging.error(f"Помилка при обробці оголошення: {e}")
                continue

        page += 1

    return car_links


def parsing_data_cars(url: str, driver) -> dict:
    logging.info(f"Обробляємо автомобіль: {url}")
    driver.get(url)
    time.sleep(1.4)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    car_details = {}

    try:
        # Base Data
        mark_tag = soup.find("h4", class_="css-10ofhqw")
        if mark_tag:
            car_details["mark"] = mark_tag.get_text(strip=True)

        price_tag = soup.find("h3", class_="css-fqcbii")
        if price_tag:
            car_details["price"] = price_tag.get_text(strip=True)

        # Details Car
        for p in soup.find_all("p", class_="css-1los5bp"):
            text = p.get_text(strip=True)

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
                car_details["engine_capacity"] = text.split(":")[-1].strip().lower()

            if "Тип приводу" in text:
                car_details["drive_type"] = text.split(":")[-1].strip()

            if "Модель" in text:
                car_details["model"] = text.split(":")[-1].strip()

        location_block = soup.find("div", class_="css-1q7h1ph")
        if not location_block:
            logging.warning("Block doesn't found")
        else:
            city_el = location_block.find("p", class_="css-7wnksb")
            region_el = location_block.find("p", class_="css-2n34b3")
            area_el = location_block.find("p", class_="css-z0m36u")

            city = city_el.get_text(strip=True) if city_el else ""
            region = region_el.get_text(strip=True) if region_el else ""
            area = area_el.get_text(strip=True) if area_el else ""

            parts = [part for part in [city, region, area] if part.strip()]

            full_location = ", ".join(parts)

            full_location = re.sub(r",\s*,", ",", full_location)
            full_location = re.sub(r",\s*(\S)", r", \1", full_location)

            car_details["location"] = full_location

        image_tag = soup.find("img", class_="css-1bmvjcs")
        if image_tag and image_tag.get("src"):
            car_details["url_image"] = image_tag["src"]

    except Exception as e:
        logging.error(f"Error While Trying Accumulate Car Data: {e}")

    return car_details


def parsing_olx_cars(offset: int):
    url = "https://www.olx.ua/uk/transport/legkovye-avtomobili/"
    driver = init_driver()

    car_links = parse_olx_autos(url, driver, offset=offset)
    logging.info(f"Found links: {len(car_links)}")

    car_list = []
    for car_url in car_links:
        details = parsing_data_cars(car_url, driver)
        if details:
            car_list.append(details)

    driver.quit()

    return car_list
