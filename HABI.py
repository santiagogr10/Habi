import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://habi.co/venta-apartamentos'
XPATH_PRICE = '//div[@class="card-price-header"]/p[@class="price"]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_PRICE)
                if len(title) > 0:
                    cleaned_price = "".join(title).replace(
                        "$", "").replace(".", "").strip()
                    formatted_price = f"${cleaned_price}"
                    with open(f'{today}/{formatted_price}.txt', 'w', encoding='utf-8') as f:
                        f.write(formatted_price)
            except IndexError:
                print("Se produjo un IndexError. Manejar la excepción aquí.")
                return
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_noticed = parsed.xpath(XPATH_PRICE)

            today = datetime.date.today().strftime(' %d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_noticed:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        pass


def run():
    parse_home()


if __name__ == '__main__':
    run()
