# -*- coding: utf-8 -*-
"""
definicja klas postaci


Są trzy typy pancerza:
lekki - 25%
średni - 50%
ciężki - 75%
i trzy typy obrażeń:
Miażdżone/Obuchowe - pancerz * 2; obrażenia zadawane do hp * 1,5
Sieczne - standard
Przebijające/Kłute - pancerz * 0,5; obrażenia zadawane do hp 0,75
I teraz jeżeli zadajesz x obrażeń przeciwnikowi o y pancerza to y obrażeń
(x jeżeli x < y) zostaje zmiejszone o tyle procent ile masz przy typie
To do:




Klasa Pancerz(Armor):
pola:
etykieta(?) = ciężki/lekki/średni
typ/klasa(type/class) = liczba z zakresu 0 do 100 lub 0 do 1 (procenty)
odporność/grubość(thickness) = liczba całkowita






Klasa Obrażenia(Damage):
pola:
etykieta(?) = Sieczne/Kłute/Obuchowe
przebicie(pierce) = liczba ~ 1.0 +-1.0 (vs armor)
efektywność(efficiency) = liczba ~ 1.0 +-1.0 (vs hp)




bazowe obrażenia = liczba całkowita
zasięg obrażeń = liczba całkowita


tu chodzi o to że jak masz obrażenia 50-70 to bazowe = 50; zasięg = 20
wyliczasz: bazowe + random()*zasięg

generalnie te klasy nie będą miały metod więc możnaby je wstawiać jako tuple,
ale to będzie mało czytelne. daj znać co myślisz
"""
from random import random
from collections import namedtuple
from equipment import Equipment
"""
from enum import Enum


class ArmorWeight(Enum):
    heavy = 1
    medium = 2
    light = 3


class TypeOfInjury(Enum):#slaby pomysł, lepsze jest trzymać to jako statystyki
    slashing = 1         # w namedtuple tak jak ustalaliśmy
    stabing = 2
    crushing = 3
"""


class Damage(object):
    pass


class Character(object):
    """Interfejs dla wszystkich postaci"""
    def __init__(self, attack, defense, damage, hp):
        self._attack = attack
        self._defense = defense
        #zróbmy klasę do otypów obrażeń albo coś, nie wiem XD
        self._damage = damage
        self._max_hp = hp
        self._hp = hp

    def attack(self, opponent):
        if (self._attack/opponent.get_defense)*0.5 > random.random(0, 1):
            opponent.hurt(self._damage)

    def hurt(self, damage):#== lost_life; tu będziemy te obrażenia wyliczać,
        pass               #może w sumie się przyda też klasa do pancerza

    def get_defense(self):
        return self._defense

    def is_dead(self):#nie wiem XD
        return True if self._hp > 0 else False


class Hero(Character):
    """Klasa postaci"""
    def __init__(self, power, dexterity, attack, defense, damage, hp):
        super(Hero, self).__init__(attack, defense, damage, hp)
        #docelowo = Equipment()
        self._equipment = Equipment()
        self._power = power
        self._dexterity = dexterity
        self._breastplate = None #dobra inicjatywa,
        #ale w sumie przeciwnik też może mieć jakiś pancerz

        # czy breastplate nie jest jako Equipment?


class Enemy(Character):
    """Klasa przeciwnika"""
    def __init__(self, attack, defense, damage, hp, posx, posy):
        super(Enemy, self).__init__(attack, defense, damage, hp)
        self._posx = posx
        self._posy = posy
# czy wrzucamy pozycje do Character ?
# w pygs tez jest pozycja Hero