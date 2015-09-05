# -*- coding: utf-8 -*-
"""
definicja klas postaci
"""
from random import random, choice
from equipment import Equipment, get_random_item
from auxil import Damage, Armor
from copy import deepcopy


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

    def do_attack(self, opponent):
        """Atak - "Rzut" przeciwko stosunkowi ataku do obrony przeciwnika"""
        if (self._attack/opponent.defense)*0.5 > random():
            opponent.hurt(self._damage)
        return opponent.is_dead()

    def hurt(self, damage):
        """
        Wyliczanie zadanych obrażeń:
        -broń zadaje "domyślnie" obrażenia z zakresu base do base+extra
        -bierzemy poprawkę na grubość pancerza
        -oraz jego jakość
        -finalnie mnożymy zredukowane obrażenia przez współczynnik zranienia
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

    @property
    def hp(self):
        """zwraca hp postaci"""
        return self._hp

    def restore_hp(self, how_much):
        """dodaje hp postaci"""
        self._hp = min(self._hp+how_much, self._max_hp)

    @property
    def attack(self):
        """zwraca atak postaci"""
        return self._attack

    @property
    def defense(self):
        """zwraca obrone postaci"""
        return self._defense

    def change_damage(self, damage):
        """zmienia obrażenia postaci"""
        self._damage = damage

    @property
    def armor(self):
        """zwraca pancerz postaci"""
        return self._armor

    def change_armor(self, armor):
        """zmienia pancerz postaci"""
        self._armor = armor

    @property
    def x(self):
        """zwraca współrzędną x położenia postaci na mapie"""
        return self._position[0]

    def change_x(self, change):
        """zmienia tylko współrzędną x położenia postaci na mapie"""
        self._position = (self._position[0] + change, self._position[1])

    @property
    def y(self):
        """zwraca współrzędną y położenia postaci na mapie"""
        return self._position[1]

    def change_y(self, change):
        """zmienia tylko współrzędną y położenia postaci na mapie"""
        self._position = (self._position[0], self._position[1] + change)

    @property
    def position(self):
        """zwraca położenie postaci na mapie"""
        return self._position

    def change_position(self, position):
        """zmienia współrzędne postaci na mapie na podane jako argument"""
        self._position = position


EXP_CAP = 1000


class Hero(Character):
    """Klasa reprezentująca naszego bohatera"""
    def __init__(self, strength, dexterity, attack, defense, hp, x, y):
        super(Hero, self).__init__(attack, defense, Damage(0.5, 1.0, 5, 2),
                                   Armor(0.0, 0), hp, x, y)
        self._equipment = Equipment(self)
        self._strength = strength
        self._dexterity = dexterity
        self._experience = 0
        self._skill_points = 0

    def set_eq_stats(self):
        """Przekazuje statystyki z ekwipunktu do postaci"""
        self._damage = self._equipment.damage
        self._armor = self._equipment.armor

    def gain_exp(self, how_much):
        """
        Dodaje doświadczenie,
        sprawdza poziom
        i ewentualnie wykonuje lvl_up
        """
        self._experience += how_much
        if self._experience >= EXP_CAP:
            self.lvl_up()

    def lvl_up(self):
        """
        Podnosi statystyki za doświadczenie
        w oparciu o broń i pancerz
        """
        print "I'm learning!"
        self._hp = self._max_hp
        self._experience -= EXP_CAP
        self._skill_points += 5

    def add_hp(self):
        """Dodaje zdrowia w zamian za punkt umiejętności"""
        if self._skill_points != 0:
            self._skill_points -= 1
            self._max_hp += 5
            self._hp += 5

    def add_strength(self):
        """Dodaje siły w zamian za punkt umiejętności"""
        if self._skill_points > 0:
            self._skill_points -= 1
            self._strength += 3

    def add_dexterity(self):
        """Dodaje zręczności w zamian za punkt umiejętności"""
        if self._skill_points > 0:
            self._skill_points -= 1
            self._dexterity += 3

    def add_attack(self):
        """Dodaje ataku w zamian za punkt umiejętności"""
        if self._skill_points > 0:
            self._skill_points -= 1
            self._attack += 1

    def add_defense(self):
        """Dodaje obrony w zamian za punkt umiejętności"""
        if self._skill_points > 0:
            self._skill_points -= 1
            self._defense += 1

    @property
    def strength(self):
        """zwraca siłę postaci"""
        return self._strength

    @property
    def dexterity(self):
        """zwraca zręczność postaci"""
        return self._dexterity

    @property
    def exp(self):
        """zwraca doświadczenie postaci"""
        return self._experience

    @property
    def equipment(self):
        """zwraca ekwipunek"""
        return self._equipment

    @property
    def skill_points(self):
        """zwraca dostępne do rozdania punkty umiejętności"""
        return self._skill_points


class Enemy(Character):
    """Klasa reprezentująca wrogów"""

    def __init__(self, attack, defense, damage, armor, hp, x, y, sprite):
        super(Enemy, self).__init__(attack, defense, damage, armor, hp, x, y)
        self._sprite = sprite

    def give_exp(self):
        """ma zwracać exp, który przyznaje po zabiciu"""
        return self._attack*(self._damage.base+self._damage.extra) + \
               self._defense*self._armor.gauge*self._armor.durability

    @staticmethod
    def leave_items():
        """
        Zwraca przedmiot wyrzucony przez zabitego przeciwnika
        Jeżeli przeciwniki nic nie zostawia, zwraca None
        """
        if 0.66 < random():
            return deepcopy(get_random_item())
        else:
            return None

    @property
    def sprite(self):
        """zwraca sprite'a potwora"""
        return self._sprite


ENEMY_LIST = [Enemy(7, 5, Damage(0.9, 1.0, 5, 5),
              Armor(0.25, 15), 20, 0, 0, "enemy1.png"),
              Enemy(10, 7, Damage(0.8, 1.0, 10, 5),
              Armor(0.25, 20), 25, 0, 0, "goblin.png"),
              Enemy(15, 10, Damage(1.1, 1.0, 10, 10),
              Armor(0.5, 15), 35, 0, 0, "bfm.png")]


def get_random_enemy():
    """ losuje wroga """
    return choice(ENEMY_LIST)
