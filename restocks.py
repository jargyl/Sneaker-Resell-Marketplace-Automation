import requests
from bs4 import BeautifulSoup
import json
from notify import price_update_success, price_update_skip

MODES = ['Marketprice', 'Lower by €1', 'Custom price']

config = json.load(open('config.json'))

EMAIL = config['restocks_email']
PASSWORD = config['restocks_password']
MODE = config['restocks_mode']
CUSTOM_PRICE = config['custom_price']

SHIPPING_FEE = 20

# Create a session that gets reused
session = requests.Session()

# Make a GET request to the login page to retrieve the login form and any necessary cookies and tokens
login_page = session.get('https://restocks.net/nl/login')

# Extract the value of the csrf_token and any necessary cookies from the response
soup = BeautifulSoup(login_page.text, "html.parser")
token = soup.find("meta", {"name": "csrf-token"})['content']
cookies = login_page.cookies

# Set headers
headers = {
    'authority': 'restocks.net',
    'accept': '*/*',
    'accept-language': 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://restocks.net/nl/login',
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

# Use the csrf_token and cookies to construct a POST request to the login page with your email and password
data = {
    'email': EMAIL,
    'password': PASSWORD,
    '_token': token
}
login_response = session.post('https://restocks.net/nl/login', data=data, headers=headers, cookies=cookies)

if login_response.status_code == 200:
    print('Login successful!')
else:
    print('Login failed :(')
    quit()


def change_price(option, exceptions):
    r = session.get(f"https://restocks.net/nl/account/listings/{MODE}")
    data = json.loads(r.text)
    inventory = data['products']
    soup = BeautifulSoup(inventory, "html.parser")
    listings = soup.find_all('tr', {'class': 'clickable'})
    for product in listings:
        img = product.find('img')['src']
        listing_id = str(product.find('input', {'class': 'productid'})['value'])
        price = int(product.find('input', {'class': 'price'})['value'])
        name = str(product.find('span').text)
        base_id = str(product.find('input', {'class': 'baseproductid'})['value'])
        size_id = str(product.find('input', {'class': 'sizeid'})['value'])
        current_payout = calculate_payout(price)

        # Skip listing if in exceptions.csv
        if any(listing_id in s for s in exceptions):
            price_update_skip(name, listing_id, img, price, current_payout, "Restocks", MODES[int(option) - 1])
            continue

        # Create a dict that maps the options to their corresponding values
        option_values = {
            1: get_lowest_price(base_id, size_id, listing_id),
            2: price - 1,
            3: CUSTOM_PRICE
        }

        # Use the get() method to look up the value for the selected option
        new_price = option_values.get(option, price)
        if price != new_price:
            r = session.get('https://restocks.net/nl/account/listings', headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            token = soup.find("meta", {"name": "csrf-token"})['content']
            data = {
                'id': listing_id,
                'store_price': str(new_price),
                '_token': token
            }
        r = session.post('https://restocks.net/nl/account/listings/edit', headers=headers, data=data)
        if '"success":true' in r.text:
            new_payout = calculate_payout(new_price)

            price_update_success(name, listing_id, img, price, new_price, current_payout, new_payout, "Restocks",
                                 MODES[int(option) - 1])


def get_lowest_price(base_id, size_id, product_id):
    # Use the session object to get the lowest price for the given product
    r = session.get(
        'https://restocks.net/nl/product/get-lowest-price/' + str(base_id) + '/' + str(size_id) + '/' + str(product_id))
    # Return the lowest price as an integer
    return int(r.text)


def calculate_payout(price):
    payout_percentage = 0.05 if MODE == "consignment" else 0.1
    payout = price - SHIPPING_FEE - price * payout_percentage
    return payout
