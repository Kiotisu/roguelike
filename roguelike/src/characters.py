# -*- coding: utf-8 -*-
"""
definicja klas postaci
"""
from random import random
from collections import namedtuple
from equipment import Equipment


Damage = namedtuple('Damage', 'pierce hurt base extra')
"""
Struktura Obrażeń(Damage):
przebicie(pierce) = liczba ~ 1.0 +-1.0
zranienie(hurt) = liczba ~ 1.0 +-1.0
baza(base) = liczba całkowita
dodatkowe(extra) = liczba całkowita
"""
Armor = namedtuple('Armor', 'gauge durability')
"""
Struktura Pancerza(Armor):
kaliber(gauge) = liczba z zakresu <0.0 , 1.0>
wytrzymałość(durability) = liczba całkowita
"""

class Character(object):
    """Interfejs dla wszystkich postaci"""
    def __init__(self, attack, defense, damage, armor, hp, x, y):
        self._attack = attack
        self._defense = defense
        self._damage = damage
        self._armor = armor
        self._max_hp = hp
        self._hp = hp
        self._position = (x, y)

    def attack(self, opponent):
        if (self._attack/opponent.get_defense)*0.5 > random.random(0, 1):
            opponent.hurt(self._damage)

    def hurt(self, damage):
        """Wyliczanie zadanych obrażeń"""
        armor = self._armor #just for beauty :)
        deliverd_damage = damage.base + (random() * damage.extra)       #broń zadaje "domyślnie" obrażenia z zakresu base do base+extra
        reduction_base = min(dam * damage.pierce, armor.durability)     #bierzemy poprawkę na grubość pancerza
        damage_reduction = reduction_base/damage.pierce * armor.gauge   #oraz jego jakość
        self._hp -= (deliverd_damage - damage_reduction) * damage.hurt  #finalnie mnożymy jeszcze zredukowane obrażenia przez współczynnik zranienia

    def get_defense(self):
        return self._defense

    def is_dead(self):#nie wiem XD
        return True if self._hp > 0 else False


class Hero(Character):
    """Klasa postaci"""
    def __init__(self, strength, dexterity, attack, defense, damage, hp):
        super(Hero, self).__init__(attack, defense, damage, hp)
        #docelowo = Equipment()
        self._equipment = Equipment()
        self._strength = strength
        self._dexterity = dexterity


class Enemy(Character):
    """Klasa przeciwnika"""
    def __init__(self, attack, defense, damage, hp, posx, posy):
        super(Enemy, self).__init__(attack, defense, damage, hp)
        self._posx = posx
        self._posy = posy
# czy wrzucamy pozycje do Character ?
# w pygs tez jest pozycja Hero