"""equipment"""

class Equipment(object):
	def __init__(self):
		self._wearing = {'weapon': None,
					'armor': None}
		self._backpack = [[None for x in xrange(5)] for x in xrange(5)] #cols_count, rows_count


	def wear_item(self, row, col):	
		print(self._backpack[col][row])	# debug
		
		swap = self._wearing[str()] 					# jak sprawdzic typ?
		self._wearing[str()] = self._backpack[col][row]		
		self._backpack[col][row] = swap				

		self.calc_attack()			# wystarczy policzyc przy dodawaniu
		self.calc_defense()

	def calc_attack(self):
		return self._wearing['weapon'] #+
	def calc_defense(self):
		return self._wearing['armor'] #

	def add_to_backpack(self, what, row, col): 	#add to specific position
		if self._backpack[col][row] == None:
			self._backpack[col][row] = what
		else: 
			print("something already there")

	def add_to_backpack(self, what):			
		flag = False
		for row in xrange(5):
			for slot in xrange(5):
				if self._backpack[row][slot] == None:
					self._backpack[row][slot] = what
					flag = True
		if flag == False:
			print("all slots taken")
