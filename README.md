# Sneaker Resell Marketplace Automation

__NOTE: This project is no longer actively maintained and won't be updated in the future. While you're welcome to use the existing codebase, please be aware that it may contain outdated dependencies or security vulnerabilities. Use at your own risk, and feel free to fork the repository and continue development on your own.__

This is a Python program that allows you to automatically adjust the pricing of your sneaker listings for two popular sneaker resell marketplaces - Restocks.net and Hypeboost.com. It allows you to retrieve all your current listings on both platforms and provides you with three options to manage your listings:

* Find and match the listing price to the current lowest market price of that sneaker
* Undercut the current lowest market price of that sneaker by 1 EUR
* Add a custom price to all listings

The program is completely request-based, and all listing updates, skips, and errors will be sent to a Discord webhook notification.

## Requirements
* Python 3.x
* requests
* beautifulsoup4
* dhooks

## Installation
1. Clone this repository.
2. Install the required packages using pip:
```
pip install requests
pip install beautifulsoup4
pip install dhooks
```
3. Fill in the necessary information in the **config.json** file:
* **`webhook`**: Discord webhook URL
* **`restocks_email`**: Your email address for Restocks.net
* **`restocks_password`**: Your password for Restocks.net
* **`restocks_mode`**: Either "resell" or "consignment" (depending on your listings)
* **`hypeboost_email`**: Your email address for Hypeboost.com
* **`hypeboost_password`**: Your password for Hypeboost.com
* **`custom_price`**: The custom price that you want to add to all your listings

If you want to exclude any listings from being updated, add the listing ID to the **exceptions.csv** file.

## Usage
To run the program, simply execute **main.py** in your Python environment.

## Examples
* Undercut

  ![Undercut](https://i.imgur.com/TzIRoXQ.png "Undercut")

* Skip

  ![Skip](https://i.imgur.com/5LVSwx8.png "Skip")

* Lower By €1

  ![Lower By 1](https://i.imgur.com/oAaXs4L.png "Lower By 1")


## Disclaimer
This program is intended for educational and personal use only. Please use it at your own risk. The developer assumes no responsibility for any accidental sales or account bans that may result from the use of this program.

## License
This project is licensed under the MIT License. See the [MIT License](LICENSE) file for more information.
