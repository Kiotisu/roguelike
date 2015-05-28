# -*- coding: utf-8 -*-
"""equipment"""


class Item(object):
    
    def __init__(self, use_requirements):
        self._requirements = use_requirements #(strength_require, dexterity_require)
    
class Weapon(Item):
    
    def __init__(self, damage_type):
        self._damage = damage_type #namedtuple z characters
    
class Armor(Item):
    
    def __init__(self, armor_type):
         self._armor = armor_type #jak damage

class Equipment(object):

    def __init__(self):
        """
        -słownik był bez sensu skoro mamy tylko dwa pola
        -plecak jako tablica dwuwymiarowa jest potrzebny?
        -ja bym go widział jako lista tutaj
        @SMN
        """
        self._weapon = None
        self._armor = None
        self._backpack = [[None for x in xrange(5)] for x in xrange(5)] #cols_count, rows_count

    def wear_item(self, row, col, my_stats):
        """
        to do, jeszcze pomyślę
        """
        print self._backpack[col][row]  # debug

        #swap = self._wearing[str()]  # jak sprawdzic typ? -type(obiekt)@WJ
        #self._wearing[str()] = self._backpack[col][row]
        self._backpack[col][row] = swap

        self.calc_attack()  # wystarczy policzyc przy dodawaniu
        self.calc_defense()

#clac_attack i calc_defense to nonsens
#atak i obrona mają znaczenie tylko przy ataku, a więc w characters.
#W tej chwili wyrzucam, jeszcze zamienie na coś sensowniejszego @SMN

    def add_to_backpack(self, what, row, col): 	#add to specific position
        if self._backpack[col][row] is None:
            self._backpack[col][row] = what
        else:
            print "something already there"

    def add_to_backpack(self, what):
        flag = False
        for row in xrange(5):
            for slot in xrange(5):
                if self._backpack[row][slot] is None:
                    self._backpack[row][slot] = what
                    flag = True
        if not flag:
            print "all slots taken"
