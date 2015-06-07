# -*- coding: utf-8 -*-
"""equipment"""

from auxil import Damage, Armor
from random import choice


class Item(object):
    """"""

    def __init__(self, name, use_requirements, sprite):
        self._name = name
        self._requirements = use_requirements 
        self._sprite = sprite
        #(strength_require, dexterity_require)

    def can_be_used(self, by_who):
        return self._requirements[0] <= by_who.get_strength()\
                and self._requirements[1] <= by_who.get_dexterity()

    def get_sprite(self):
        """zwraca nazwę sprite'a"""
        return self._sprite

class Consumable(Item):
    """Jedzenie"""

    def __init__(self, name, use_requirements, restoring_abilities, sprite):
        super(Consumable, self).__init__(name, use_requirements, sprite)
        self._restoring_abilities = restoring_abilities
        
    def eat(self, who):
        """jemy"""
        who.restore_hp(self._restoring_abilities)
        self._restoring_abilities = 0

class Weapon(Item):
    """"""

    def __init__(self, name, use_requirements, damage_type, sprite):
        super(Weapon, self).__init__(name, use_requirements, sprite)
        self._damage = damage_type #namedtuple z characters
        
    def get_damage(self):
        """zwraca obrażenia"""
        return self._damage


class Suit(Item):
    """Reprezentuje stroje i pancerze"""

    def __init__(self, name, use_requirements, armor_type, sprite):
        super(Suit, self).__init__(name, use_requirements, sprite)
        self._armor = armor_type #jak damage
        
    def get_armor(self):
        """zwraca obrażenia"""
        return self._armor

#lista przedmiotów w grze, zostawiane przez przeciwników
item_list = [Weapon('Miecz', (10, 5), Damage(1.1, 1.0, 20, 5), "weapon3.png"),
             Suit('Kolczuga', (7, 7), Armor(0.5, 10), "ar2.png"),
             Weapon('Miecz Dwuręczny', (20, 3), Damage(1.0, 1.2, 30, 10), "weapon4.png"),
             Consumable('Japko', (0, 0), 15, "apple.png"),
             Consumable('Dobre Japko', (0, 0), 40, "apple.png"),
             Consumable('Rogal', (0, 0), 300, "rogal.jpg")]

def get_random_item():
    return choice(item_list)


class Equipment(object):

    def __init__(self, owner):
        """
        bron, zbroja, plecak
        """
        self._owner = owner
        self._weapon = None
        self._suit = None
        self._backpack = []

    def use_item(self, list_positon):
        """
        używanie przedmiotu
        -pancerze i miecze zakłada a jabłko je
        """
        if list_positon < len(self._backpack)\
            and self._backpack[list_positon].can_be_used(self._owner):
            if type(self._backpack[list_positon]) is Weapon:
                swap = self._weapon
                self._weapon = self._backpack[list_positon]
                self._backpack[list_positon] = swap
                self._owner.change_damage(self._weapon.get_damage())
            elif type(self._backpack[list_positon]) is Suit:
                swap = self._suit
                self._suit = self._backpack[list_positon]
                self._backpack[list_positon] = swap
                self._owner.change_armor(self._suit.get_armor())
            elif type(self._backpack[list_positon]) is Consumable:
                self._backpack[list_positon].eat(self._owner)
                del self._backpack[list_positon]
            else:
                pass
        print self._backpack
        self._backpack = [x for x in self._backpack if x is not None]
        # delete all None from list
        print "after"
        print self._backpack

    def get_weapon(self):
        return self._weapon

    def get_suit(self):
        return self._suit

    def backpack_len(self):
        return len(self._backpack)

    def add_to_backpack(self, what):
        if len(self._backpack) < 20:
            self._backpack.append(what)

    def get_backpack(self):
        return self._backpack