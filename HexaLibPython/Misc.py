#! /bin/python3


class Misc:
	@staticmethod
	def LeadingCharacters (Number, Char, OrderOfMagnitude): # This puts x number of characters in front of a number, eg spaces, or 0s to make it evenly spaced for display in terminal or log file.
		if OrderOfMagnitude > 9:
			OrderOfMagnitude = 9
		X = ""
		#print (X)
		for i in range (0, OrderOfMagnitude - 1):
			i = OrderOfMagnitude - 1 - i
			if Number / 10 ** i < 1:
				X = X + str (Char)
		X = X + str (Number)
		return X
