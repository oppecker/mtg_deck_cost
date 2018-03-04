import requests
import json
import time

with open('deck_file.txt', 'r') as f:
    lines = [line.rstrip() for line in f]

deck = {}
for line in lines:
    quantity, name, card_set = line.split(';')
    name = '+'.join(name.split(' '))
    try:
        deck[name].update({card_set: {'quantity': quantity}})
    except KeyError:
        deck[name] = {card_set: {'quantity': quantity}}

for name, card_sets in deck.iteritems():
    for card_set in card_sets:
        time.sleep(1)
        url = ''.join(['https://api.scryfall.com/cards/named?exact=',
                       name, '&set=', card_set])
        r = requests.get(url)
        r.raise_for_status()
        card = json.loads(r.text)
        deck[name][card_set].update({'usd': card['usd']})
        #print 'card: ' + name + ' from set: ' + card_set + ' costs: ' + str(card['usd'])

total = 0
for name, card_sets in deck.iteritems():
    for card_set, info in card_sets.iteritems():
        total += float(info['usd']) * int(info['quantity'])

print deck
print 'total dollars: ' + str(total)
