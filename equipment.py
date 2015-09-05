# -*- coding: utf-8 -*-
"""equipment"""

from auxil import Damage, Armor
from random import choice


class Item(object):
    """przedmiot"""

    def __init__(self, name, use_requirements, sprite):
        self._name = name
        self._requirements = use_requirements
        self._sprite = sprite
        # (strength_require, dexterity_require)

    def can_be_used(self, by_who):
        """Sprawdza czy spełnione są wymagania użycia przedmiotu"""
        return (self._requirements[0] <= by_who.strength
                and self._requirements[1] <= by_who.dexterity)

    @property
    def sprite(self):
        """zwraca nazwę sprite'a"""
        return self._sprite


class Consumable(Item):
    """jedzenie"""

    def __init__(self, name, use_requirements, restoring_abilities, sprite):
        super(Consumable, self).__init__(name, use_requirements, sprite)
        self._restoring_abilities = restoring_abilities

    def eat(self, who):
        """jemy"""
        who.restore_hp(self._restoring_abilities)
        self._restoring_abilities = 0


class Weapon(Item):
    """broń"""

    def __init__(self, name, use_requirements, damage_type, sprite):
        super(Weapon, self).__init__(name, use_requirements, sprite)
        self._damage = damage_type  # namedtuple z characters

    @property
    def damage(self):
        """zwraca obrażenia"""
        return self._damage


class Suit(Item):
    """Reprezentuje stroje i pancerze"""

    def __init__(self, name, use_requirements, armor_type, sprite):
        super(Suit, self).__init__(name, use_requirements, sprite)
        self._armor = armor_type  # jak damage

    @property
    def armor(self):
        """zwraca pancerz"""
        return self._armor

# lista przedmiotów w grze, zostawiane przez przeciwników
ITEM_LIST = [Weapon('Miecz', (10, 5), Damage(1.1, 1.0, 20, 5), "weapon3.png"),
             Weapon('Maczuga', (7, 7), Damage(0.8, 1.5, 15, 10), "weapon2.png"),
             Weapon('Berdysz', (7, 7), Damage(1.3, 1.0, 20, 10), "weapon1.png"),
             Weapon('Miecz Dwuręczny', (20, 3), Damage(1.0, 1.2, 30, 10),
                    "weapon4.png"),
             Suit('Kolczuga', (7, 7), Armor(0.5, 10), "ar3.png"),
             Suit('Dobra Zbroja', (15, 10), Armor(0.7, 25), "ar2.png"),
             Consumable('Japko', (0, 0), 15, "apple.png"),
             Consumable('Dobre Japko', (0, 0), 35, "apple.png"),
             Consumable('Pyszne Japko', (0, 0), 50, "apple.png"),
             Consumable('Rogal', (0, 0), 100, "rogal.jpg"),
             Consumable('Rogal Mocy', (0, 0), 300, "rogal.jpg")]


def get_random_item():
    """zwraca losowy przedmiot z listy przedmiotów"""
    return choice(ITEM_LIST)


class Equipment(object):
    """
        bron, zbroja, plecak
    """

    def __init__(self, owner):
        self._owner = owner
        self._weapon = None
        self._suit = None
        self._backpack = []

    def use_item(self, list_positon):
        """
        używanie przedmiotu
        -pancerze i miecze zakłada a jabłko je
        """
        if list_positon < len(self._backpack) \
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

    def backpack_len(self):
        """zwraca zapełnienie plecaka"""
        return len(self._backpack)

    def add_to_backpack(self, what):
        """dodaje przedmiot do plecaka"""
        if len(self._backpack) < 20:
            self._backpack.append(what)

    @property
    def backpack(self):
        """zwraca plecak"""
        return self._backpack

    @property
    def weapon(self):
        """zwraca broń"""
        return self._weapon

    @property
    def suit(self):
        """zwraca zbroję(?)"""
        return self._suit
