'''deck_cost.py parses a deck input file and outputs deck cost info'''
from collections import defaultdict
import json
import time

import requests

with open('deck_file.txt', 'r') as f:
    lines = [line.rstrip() for line in f]

deck = defaultdict(dict)
for line in lines:
    quantity, name, card_set = line.split(';')
    name = '+'.join(name.split(' '))
    deck[name].update({card_set: {'quantity': quantity}})

for name, card_sets in deck.iteritems():
    for card_set in card_sets:
        url = ''.join(['https://api.scryfall.com/cards/named?exact=',
                       name, '&set=', card_set])
        r = requests.get(url)
        r.raise_for_status()
        card = json.loads(r.text)
        deck[name][card_set].update({'usd': card['usd']})
        #don't overload scryfall.com
        time.sleep(1)

total = 0
for name, card_sets in deck.iteritems():
    for card_set, info in card_sets.iteritems():
        total += float(info['usd']) * int(info['quantity'])

print json.dumps(deck, indent=4)
print 'total dollars: ' + str(total)
