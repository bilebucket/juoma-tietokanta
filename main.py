#!/bin/python
# coding=utf-8

"""
Juoma-tietokanta -- Ohjelmoinnin perusteiden näyttö
"""

from collections import OrderedDict

import cPickle as pickle

DATABASE = 'database'

all_drinks = []
running = True

commands = [
    'lopeta',
    'kaikki',
    'uusi',
    'tulosta',
    'apua',
    'etsi'
]

help_string = u"""

Tervetuloa Juoma-tietokantaan!
Tunnetut komennot:
    lopeta :    lopettaa ohjelman.
    kaikki :    tulostaa kaikkien juomien nimet.
    uusi :      lisää uuden juoman.
    etsi:       etsi juomia hakusanalla.
    tulosta :   tulostaa halutun juoman tiedot.
    apua :      tulostaa tämän apuviestin.

"""

data_template = OrderedDict(name=None, brewery=None, abv=None, points=None)


class Drink:
    def __init__(self, data):
        self.data = data

    def get_name(self):
        return self.data['name']

    def get_points(self):
        return self.data['points']

    def get_brewery(self):
        return self.data['brewery']

    def get_abv(self):
        return self.data['abv']

    def print_out(self):
        print '\n{}.'.format(all_drinks.index(self))
        print '-' * len(self.get_name()) + '--'
        print '-' + self.get_name() + '-'
        print '-' * len(self.get_name()) + '--'
        print 'Panimo / Valmistaja  | ' + self.get_brewery()
        print 'Tilavuusprosentit    | ' + self.get_abv() + '%'
        print 'Pisteet              | ' + self.get_points() + '/10.0'


def print_drink(index):
    if -1 < index < len(all_drinks):
        all_drinks[index].print_out()
    else:
        print '{} ei ole sopiva indeksi luku\n'.format(index)


def print_all():
    print '\n--KAIKKI JUOMAT--\n'
    i = 0
    for drink in all_drinks:
        print '{0}. {1}'.format(i, drink.get_name())
        i += 1


def add_drink():
    print '\n--UUSI JUOMA--\n'
    data = OrderedDict(data_template)
    for field in data:
        data.update({field: raw_input(field + '> ')})
    all_drinks.append(Drink(data))


def find():
    term = raw_input('hakutermi> ').lower()
    results = []
    for drink in all_drinks:
        for field in drink.data:
            if term in drink.data[field].lower() and drink not in results:
                results.append(drink)

    if results:
        print u'\nLöydettiin {} tulosta.'.format(len(results))
        for result in results:
            result.print_out()
    else:
        print u'\nEi hakutuloksia hakusanalla "{}"'.format(term)


def init():
    f = open(DATABASE, 'ab')
    f.close()
    global all_drinks
    with open(DATABASE, 'rb') as handle:
        data = pickle.load(handle)
        all_drinks = data


def save_data():
    with open(DATABASE, 'wb') as handle:
        pickle.dump(all_drinks, handle)
        # data_file = open('test.json', 'w')
        # for drink in all_drinks:
        #     json.dump(drink.data, data_file)
        # data_file.close()


def run():
    global running
    print help_string
    while running:
        cmd = raw_input('\nkomento> ').lower()
        if cmd not in commands:
            print 'Tuntematon komento "{}"'.format(cmd)
        else:
            if cmd == 'lopeta':
                save_data()
                running = False
            if cmd == 'kaikki':
                print_all()
            if cmd == 'uusi':
                add_drink()
            if cmd == 'tulosta':
                print_drink(int(raw_input('juoman numero> ')))
            if cmd == 'apua':
                print help_string
            if cmd == 'etsi':
                find()

# Tämä on pythonin int main(){} funktion vastine
if __name__ == '__main__':
    init()
    run()
