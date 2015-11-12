#!/bin/python
# coding=utf-8

"""

Juoma-tietokanta
TTZC0200.5S0V4 - Ohjelmoinnin Perusteet -  Osaamisen näyttö
Sami Pitkänen 2015

"""

# sisällytetään tarvittavat kirjastot
from collections import OrderedDict
import pickle as pickle

# tietokanta tiedoston nimi
DATABASE = 'database'

# taulukko johon Drink luokan instanssit tullaan säilömään
all_drinks = []
running = True

# ohjelman tuntemat komennot
commands = [
    'lopeta',
    'kaikki',
    'uusi',
    'tulosta',
    'apua',
    'etsi',
    'alusta',
    'poista'
]


help_string = u"""

Tervetuloa Juoma-tietokantaan!

Tunnetut komennot:
    lopeta:    lopettaa ohjelman.
    kaikki:    tulostaa kaikkien juomien nimet.
    uusi:      lisää uuden juoman.
    etsi:      etsi juomia hakusanalla.
    tulosta:   tulostaa halutun juoman tiedot.
    alusta:    alustaa tietokannan HUOM! Kaikki tiedot menetetään.
    poista:    poistaa juoman.
    apua:      tulostaa tämän apuviestin.

"""

# Drink luokan data taulukon malli
data_template = OrderedDict(name=None, brewery=None, abv=None, points=None)


# Drink luokka jonka instansseihin tallennetaan juoman tiedot
class Drink:
    # luokan konstruktori
    def __init__(self, data):
        # data on linkitetty lista jossa juoman tiedot sijaitsevat
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
        # tulostetaan juoman tiedot siististi 
        print '\n{}.'.format(all_drinks.index(self))
        print '-' * len(self.get_name()) + '--'
        print '-' + self.get_name() + '-'
        print '-' * len(self.get_name()) + '--'
        print 'Panimo / Valmistaja  | ' + self.get_brewery()
        print 'Tilavuusprosentit    | ' + self.get_abv() + '%'
        print 'Pisteet              | ' + self.get_points() + '/10.0'


# haetaan all_drinks listasta annetussa indeksissä sijaitsevan juoman tiedot
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

suomennukset = {'name': 'nimi', 'brewery': 'panimo/valmistaja', 'abv': 'alkoholi tilavuusprosentti', 'points': 'pisteet (0.1-10.0)' }


def add_drink():
    print '\n--UUSI JUOMA--\n'
    data = OrderedDict(data_template)
    # kysytään käyttäjältä juoman tiedot ja lisätään syntynyt Drink -luokan instanssi all_drinks -taulukkoon
    for field in data:
        data.update({field: raw_input(suomennukset[field] + '> ')})
    all_drinks.append(Drink(data))


# Etsitään juomia käyttäjän määrittelemän hakusanan mukaan
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


# tietokannan alustus
def db_init():
    global all_drinks
    print u'\nVAROITUS! TÄMÄ POISTAA KAIKKI JUOMAT TIETOKANNASTA.\nKOMENTOA EI VOI PERUTTAA.'
    c = raw_input('JATKETAANKO [k/e]')
    if c.lower() == 'k':
        print 'ALUSTETAAN...'
        all_drinks = [Drink({'name': None, 'brewery': None, 'abv': None, 'points': None})]


# poistetaan käyttäjän antamassa indeksissä sijaitseva juoma
def delete():
    global all_drinks
    index = int(raw_input('juoman numero> '))
    if -1 < index < len(all_drinks):
        all_drinks.remove(all_drinks[index])


# avataan tietokanta ja luetaan data all_drinks listaan
def init():
    print '\nLuetaan tietokannasta...',
    f = open(DATABASE, 'ab')
    f.close()
    global all_drinks
    with open(DATABASE, 'rb') as handle:
        data = pickle.load(handle)
        all_drinks = data
    print ' valmis!'


# tallennetaan data, kun ohjelma suljetaan
def save_data():
    print '\nTallennetaan tiedot...',
    with open(DATABASE, 'wb') as handle:
        pickle.dump(all_drinks, handle)
    print ' valmis!'


# ohjelman "I/O" -looppi, jossa luetaan käyttäjän syöte ja suoritetaan sitten halutut funktiot
def run():
    global running
    
    # tulostetaan helppi teksti
    print help_string

    while running:
        cmd = raw_input('\nkomento> ').lower()

        # jos syöte ei ole tunnetuissa komennoissa, kerrotaan siitä käyttäjälle.
        if cmd not in commands:
            print 'Tuntematon komento "{}"'.format(cmd)
        
        # syöte on validi komento
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
            if cmd == 'alusta':
                db_init()
            if cmd == 'poista':
                delete()

# Tämä on pythonin int main(){} funktion vastine
if __name__ == '__main__':
    init()
    run()
    print '\nTervetuloa uudelleen!'

