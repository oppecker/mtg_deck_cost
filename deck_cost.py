'''deck_cost.py parses a deck input file and outputs deck cost info'''
from collections import defaultdict
import json
import time
import argparse

import requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--deck_file', default='sample_deck_file.txt')
    parser.add_argument('--output_file', default='output.txt')
    args = parser.parse_args()

    with open(args.deck_file, 'r') as f:
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

    with open(args.output_file, 'w') as f:
        json.dump(deck, f, indent=4)
        f.write('\ntotal dollars: ' + str(total))
