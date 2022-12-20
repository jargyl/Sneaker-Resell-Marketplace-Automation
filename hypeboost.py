import requests
from bs4 import BeautifulSoup
import json
from notification import notify

MODES = ['Marketprice', 'Undercut', 'Custom price']

config = json.load(open('config.json'))

EMAIL = config['hypeboost_email']
PASSWORD = config['hypeboost_password']
WEBHOOK = config['webhook']
CUSTOM_PRICE = config['custom_price']

session = requests.Session()

login_page = session.get("https://hypeboost.com/nl/inloggen")

soup = BeautifulSoup(login_page.text, "html.parser")
token = soup.find("input", {"name": "_token"})['value']
cookies = login_page.cookies

headers = {
    'authority': 'hypeboost.com',
    'accept': '*/*',
    'accept-language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://hypeboost.com/nl/inloggen?tab=login',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-csrf-token': token,
    'x-requested-with': 'XMLHttpRequest',
}

data = {
    '_token': token,
    'email': EMAIL,
    'password': PASSWORD,
}

login_response = session.post('https://hypeboost.com/nl/inloggen', cookies=cookies, headers=headers, data=data)
login_cookies = login_response.cookies

if login_response.status_code == 200:
    print('Login successful!')
else:
    print('Login failed :(')
    quit()


def change_price(option):
    listings_page = session.get("https://hypeboost.com/nl/account/verkopen/huidige/niet-de-laagste-prijs",
                                cookies=login_cookies)
    soup = BeautifulSoup(listings_page.text, "html.parser")
    token = soup.find("input", {"name": "_token"})['value']
    listings = soup.find_all("div", {"class": "grid-row"})
    for product in listings:
        img = product.find('img')['src']
        product_id = str(product.find('input', {'class': 'productid'})['value'])
        price = int(product.find('input', {'class': 'price'})['value'])
        lowest_ask = int(product.find('input', {'class': 'lowestask'})['value'])
        base_id = str(product.find('input', {'class': 'baseproductid'})['value'])
        size_id = str(product.find('input', {'class': 'sizeid'})['value'])
        payout = product.find('span', {"class": "payout"}).text
        payout = payout.replace('€ ', '').replace(',', '.')
        name = product.find('span').text

        option_values = {
            1: lowest_ask,
            2: lowest_ask - 1,
            3: CUSTOM_PRICE
        }

        new_price = option_values.get(option, lowest_ask)
        if price != new_price:

            # Get payout price
            payout_data = {
                '_token': token,
                'price': new_price,
            }
            r_payout = session.post('https://hypeboost.com/nl/get-payout', cookies=login_cookies, data=payout_data)
            data = json.loads(r_payout.text)
            new_payout = data['payout']['numeric']

            # Save new price
            save_data = {
                '_token': token,
                'price': new_price,
                'payout': new_payout,
            }
            r_save = session.post(f"https://hypeboost.com/nl/account/verkopen/huidige/{product_id}/opslaan",
                                  cookies=login_cookies, data=save_data)
            if '"success":true' in r_save.text:
                notify(name, product_id, img, price, new_price, payout, new_payout, "Hypeboost", MODES[int(option) - 1])


