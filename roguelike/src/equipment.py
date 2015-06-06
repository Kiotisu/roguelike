# -*- coding: utf-8 -*-
"""equipment"""

from aux import Damage, Armor
from random import choice


class Item(object):
    
    def __init__(self, name, use_requirements):
        self._name = name
        self._requirements = use_requirements #(strength_require, dexterity_require)


class Weapon(Item):
    
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
        self._backpack = [[None for x in xrange(5)] for x in xrange(5)] #cols_count, rows_count

    def wear_item(self, row, col, my_stats):
        """
        to do, jeszcze pomyślę
        """
        print self._backpack[col][row]  # debug

        #swap = self._wearing[str()]  # jak sprawdzic typ? -type(obiekt)@WJ
        #self._wearing[str()] = self._backpack[col][row]
        self._backpack[col][row] = None # = swap

        self.calc_attack()  # wystarczy policzyc przy dodawaniu
        self.calc_defense()

    def get_damage(self):
        """Podaje zadawane przez bohatera obrażenia"""
        if self._weapon == None:
            return Damage(0.5, 1.0, 5, 2)
        else:
            return self._weapon.get_damage()
        
    def get_armor(self):
        """Podaje posiadany przez bohatera pancerz"""
        if self._suit == None:
            return Armor(0.0, 0)
        else:
            return self._suit.get_armor()

    def add_to_backpack(self, what, row, col): 	#add to specific position
        """dodaje przedmiot do plecaka na określoną pozycję"""
        if self._backpack[col][row] is None:
            self._backpack[col][row] = what
        else:
            print "something already there"

    def add_to_backpack(self, what):
        """dodaje przedmiot do plecaka na pierwszą wolną pozycję"""
        flag = False
        for row in xrange(5):
            for slot in xrange(5):
                if self._backpack[row][slot] is None:
                    self._backpack[row][slot] = what
                    flag = True
        if not flag:
            print "all slots taken"
