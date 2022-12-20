import json
from dhooks import Webhook, Embed

config = json.load(open('config.json'))
WEBHOOK = config['webhook']


def price_update_success(name, listing_id, img, current_price, new_price, current_payout, new_payout, site, mode):
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


def price_update_skip(name, listing_id, img, current_price, current_payout, site, mode):
    print(f"SKIPPING {name} ({listing_id}): {current_price}")

    embed = Embed(
        color=0xfe7ba7,
        description=None,
        timestamp='now'
    )

    embed.set_title(title='SKIPPED ITEM ⏭')
    embed.add_field(name='Product Name', value=name)
    embed.add_field(name='Listing ID 🏷️', value=listing_id, inline=False)
    embed.add_field(name='Price 💵', value=f'€{current_price}')
    embed.add_field(name='Payout 💶', value=f'€{float(current_payout):.2f}')
    embed.set_footer(text=f"{site} - {mode}")
    embed.set_thumbnail(img)

    hook = Webhook(WEBHOOK)
    hook.send(embed=embed)
