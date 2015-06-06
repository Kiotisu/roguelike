# -*- coding: utf-8 -*-
"""
definicja klas postaci

Struktura Obrażeń(Damage):
przebicie(pierce) = liczba ~ 1.0 +-1.0
zranienie(hurt) = liczba ~ 1.0 +-1.0
baza(base) = liczba całkowita
dodatkowe(extra) = liczba całkowita

Struktura Pancerza(Armor):
kaliber(gauge) = liczba z zakresu <0.0 , 1.0>
wytrzymałość(durability) = liczba całkowita

"""
from random import random
from collections import namedtuple
from equipment import Equipment

Damage = namedtuple('Damage', 'pierce hurt base extra')
Armor = namedtuple('Armor', 'gauge durability')


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
        """Atak - "Rzut" przeciwko stosunkowi ataku do obrony przeciwnika"""
        if (self._attack/opponent.get_defense())*0.5 > random():
            opponent.hurt(self._damage)
        return opponent.is_dead()

    def hurt(self, damage):
        """
        Wyliczanie zadanych obrażeń:
        -broń zadaje "domyślnie" obrażenia z zakresu base do base+extra
        -bierzemy poprawkę na grubość pancerza
        -oraz jego jakość
        -finalnie mnożymy jeszcze zredukowane obrażenia przez współczynnik zranienia
        """
        armor = self._armor #just for beauty :)
        delivered_damage = damage.base + (random() * damage.extra)
        reduction_base = min(delivered_damage * damage.pierce, armor.durability)
        damage_reduction = reduction_base/damage.pierce * armor.gauge
        self._hp -= (delivered_damage - damage_reduction) * damage.hurt

    def is_dead(self):
        """Sprawdza czy jest się martwym i ewentualnie daje doświadczenie"""
        # give_exp() NIE TO NIE TUTAJ!!!!
        # chyba, że np zwraca -1 jak żyje
        # jak nie żyje to dodatnią liczbę - exp
        return self._hp <= 0

    def get_hp(self):
        """zwraca hp postaci"""
        return self._hp

    def get_attack(self):
        """zwraca atak postaci"""
        return self._attack

    def get_defense(self):
        """zwraca obrone postaci"""
        return self._defense

    def get_armor(self):
        """zwraca pancerz postaci"""
        return self._armor

    def get_x(self):
        """zwraca współrzędną x położenia postaci na mapie"""
        return self._position[0]

    def get_y(self):
        """zwraca współrzędną y położenia postaci na mapie"""
        return self._position[1]

    def get_position(self):
        """zwraca położenie postaci na mapie"""
        return self._position

    def change_position(self, position):
        """zmienia współrzędne postaci na mapie na podane jako argument"""
        self._position = position

    def change_x(self, change):
        """zmienia tylko współrzędną x położenia postaci na mapie"""
        self._position = (self._position[0] + change, self._position[1])

    def change_y(self, change):
        """zmienia tylko współrzędną y położenia postaci na mapie"""
        self._position = (self._position[0], self._position[1] + change)


class Hero(Character):
    """Klasa reprezentująca naszego bohatera"""
    def __init__(self, strength, dexterity, attack, defense, damage, armor, hp, x, y):
        super(Hero, self).__init__(attack, defense, damage, armor, hp, x, y)
        self._equipment = Equipment()
        self._strength = strength
        self._dexterity = dexterity


class Enemy(Character):
    """Klasa reprezentująca wrogów"""
    def __init__(self, attack, defense, damage, armor, hp, x, y):
        super(Enemy, self).__init__(attack, defense, damage, armor, hp, x, y)

    def give_exp(self):
        """ma zwracać exp, który przyznaje po zabiciu?"""
        pass
    