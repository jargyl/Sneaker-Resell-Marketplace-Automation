import json
from dhooks import Webhook, Embed

config = json.load(open('config.json'))
WEBHOOK = config['webhook']


def notify(name, listing_id, img, current_price, new_price, current_payout, new_payout, site, mode):
    print(f"{name} ({listing_id}): {current_price} -> {new_price}")

    embed = Embed(
        color=0x6a00ff,
        description=None,
        timestamp='now'
    )

    embed.set_title(title='PRICE UPDATED ✅')
    embed.add_field(name='Product Name', value=name)
    embed.add_field(name='Listing ID 🏷️', value=listing_id, inline=False)
    embed.add_field(name='Price 💵', value=f'€{current_price} -> €{new_price}')
    embed.add_field(name='Payout 💶', value=f'€{float(current_payout):.2f} -> **€{float(new_payout):.2f}**')
    embed.set_footer(text=f"{site} - {mode}")
    embed.set_thumbnail(img)

    hook = Webhook(WEBHOOK)
    hook.send(embed=embed)
