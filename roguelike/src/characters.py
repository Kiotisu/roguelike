# -*- coding: utf-8 -*-
"""
definicja klas postaci
"""
from random import random, choice
from equipment import Equipment, get_random_item
from aux import Damage, Armor


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
        """sprawdza czy postaci skończyło się życie
        i zwraca true jeśli zginęła, false w przeciwnym wypadku"""
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

exp_cap = 10000


class Hero(Character):
    """Klasa reprezentująca naszego bohatera"""
    def __init__(self, strength, dexterity, attack, defense, damage, armor, hp, x, y):
        super(Hero, self).__init__(attack, defense, damage, armor, hp, x, y)
        self._equipment = Equipment()
        self._strength = strength
        self._dexterity = dexterity
        self._experience = 0
        
    def set_eq_stats(self):
        """Przekazuje statystyki z ekwipunktu do postaci"""
        self._damage = self._equipment.get_damage()
        self._armor = self._equipment.get_armor()

    def gain_exp(self, how_much):
        """
        Dodaje doświadczenie,
        sprawdza poziom 
        i ewentualnie wykonuje lvl_up
        """
        self._experience += how_much
        if self._experience > exp_cap:
            self.lvl_up()
            
    def lvl_up(self):
        """
        Podnosi statystyki za doświadczenie
        w oparciu o broń i pancerz
        """
        print "I'm learning!"
        self._experience -= exp_cap
        self._strength += 3 * self._damage.hurt
        self._dexterity += 3 * self._damage.pierce
        self._attack += 5 * (self._damage.hurt+self._damage.pierce)/2
        self._defense += 5 * self._armor.gauge


class Enemy(Character):
    """Klasa reprezentująca wrogów"""
    def __init__(self, attack, defense, damage, armor, hp, x, y):
        super(Enemy, self).__init__(attack, defense, damage, armor, hp, x, y)

    def give_exp(self):
        """ma zwracać exp, który przyznaje po zabiciu?"""
        return self._attack*(self._damage.base+self._damage.extra) + \
               self._defense*self._armor.gauge*self._armor.durability
    
    def leave_items(self):
        """
        Zwraca przedmiot wyrzucony przez zabitego przeciwnika
        Jeżeli przeciwniki nic nie zostawia, zwraca None
        """
        if 0.8 < random():
            return get_random_item()
        else:
            return None
