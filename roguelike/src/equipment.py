# -*- coding: utf-8 -*-
"""equipment"""

from auxil import Damage, Armor
from random import choice


class Item(object):
    """"""

    def __init__(self, name, use_requirements):
        self._name = name
        self._requirements = use_requirements #(strength_require, dexterity_require)


class Weapon(Item):
    """"""

    def __init__(self, name, use_requirements, damage_type):
        super(Weapon, self).__init__(name, use_requirements)
        self._damage = damage_type #namedtuple z characters
        
    def get_damage(self):
        """zwraca obrażenia"""
        return self._damage


class Suit(Item):
    """Reprezentuje stroje i pancerze"""

    def __init__(self, name, use_requirements, armor_type):
        super(Suit, self).__init__(name, use_requirements)
        self._armor = armor_type #jak damage
        
    def get_armor(self):
        """zwraca obrażenia"""
        return self._armor

#lista przedmiotów w grze, zostawiane przez przeciwników
item_list = [Weapon('Miecz', (10, 5), Damage(1.1, 1.0, 20, 5)),
             Suit('Kolczuga', (7, 7), Armor(0.5, 10)),
             Weapon('Miecz Dwuręczny', (20, 3), Damage(1.0, 1.2, 30, 10))]


def get_random_item():
    return choice(item_list)


class Equipment(object):

    def __init__(self):
        """
        -słownik był bez sensu skoro mamy tylko dwa pola
        -plecak jako tablica dwuwymiarowa jest potrzebny?
        -ja bym go widział jako lista tutaj
        @SMN
        """
        self._weapon = None
        self._suit = None
        # self._backpack = [[None for x in xrange(5)] for x in xrange(5)] #cols_count, rows_count
        # ok lista
        self._backpack = []

    def wear_item(self, list_positon, my_stats):
        """
        to do, jeszcze pomyślę
        napisac jeszcze raz bo teraz _backpack jest lista
        """
        if list_positon < len(self._backpack):
            swap = self._weapon
            self._weapon = self_backpack[list_positon]
            self_backpack[list_positon] = swap

        # TODO: calculate stats

    def get_damage(self):
        """Podaje zadawane przez bohatera obrażenia"""
        if self._weapon is None:
            return Damage(0.5, 1.0, 5, 2)
        else:
            return self._weapon.get_damage()
        
    def get_armor(self):
        """Podaje posiadany przez bohatera pancerz"""
        if self._suit is None:
            return Armor(0.0, 0)
        else:
            return self._suit.get_armor()

    def backpack_len(self):
        return len(self._backpack)

    def add_to_backpack(self, what):
        if len(self._backpack) < 20:
            self._backpack.append(what)

    def print_backpack(self):
        for item in self._backpack:
            print item

    def get_backpack(self):
        li = []
        for i in self._backpack:
            li.append(i)
        return li
