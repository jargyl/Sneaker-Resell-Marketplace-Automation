SITELIST = ['Hypeboost', "Restocks"]


def choose_action(actions):
    user_input = ''
    input_message = ""
    for index, action in enumerate(actions):
        input_message += f'{index + 1}) {action}\n'
    input_message += 'Option: '
    while user_input not in map(str, range(1, len(actions) + 1)):
        user_input = input(input_message)
    return user_input


site_input = ''
input_message = ""
for index, site in enumerate(SITELIST):
    input_message += f'{index + 1}) {site}\n'
input_message += 'Option: '
while site_input not in map(str, range(1, len(SITELIST) + 1)):
    site_input = input(input_message)

site = SITELIST[int(site_input) - 1]
modes = []
if 'Restocks' in site:
    import restocks
    while True:
        mode = choose_action(restocks.MODES)
        restocks.change_price(int(mode))
if 'Hypeboost' in site:
    import hypeboost
    while True:
        mode = choose_action(hypeboost.MODES)
        hypeboost.change_price(int(mode))
