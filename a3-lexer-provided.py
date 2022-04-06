import ply.lex as lex
from ply.lex import TOKEN

class ClifLexer():

	# CONSTRUCTOR
	def __init__(self):
		print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		# start in the (standard) initial state
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		print('Lexer destructor called.')

	reserved_bool = {
		'and': 'AND',
		'or': 'OR'
	}

	tokens = [
		'OPEN', 
		'CLOSE', 
		'CHAR',
		'DIGIT',
		'NUMERAL',
		'QUOTEDSTRING', 
		'RESERVEDELEMENT'
	]

	tokens += reserved_bool.values()

	t_ignore = ' \t\r\n\f\v' # code as written in this file did not have beginning whitespace; added whitespace based on Brightspace announcement

	digit = r'([0-9])'
	numeral = r'(' + digit + r')+'
	character = r'(' + digit + r'|[^0-9\)\()])' # gross - currently necessary because t_CHAR (a function) has higher priority than t_OPEN and t_CLOSE

	def t_NEWLINE(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	def t_error(self,t):
		print("Lexing error: Unknown character \"{}\" at line {}".format(t.value[0], t.lexer.lineno))
		t.lexer.skip(1)

	# token specification as a string (no regular expression)

	t_OPEN= '\('
	t_CLOSE= '\)'

	# token specification as a regular expression

	# the digit token is recognized, but... numbers will always get tagged as numerals because they're one or more digits
	t_DIGIT= r'([0-9])'
	#t_NUMERAL=

	# right now the r'\w+' in this function is catching the above tokens
	# causing them to not be printed - so for now it is commented out
	'''def t_RESERVEDELEMENT(self, t):
		# here we use a regular expression to say what matches this particular token:
		# any sequence of standard characters of length 1 or greater
		# but this does not yet cover all reservedelements
		r'\w+'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			#print("Boolean reserved word: " + t.value)
			return t
		else:
			pass'''

	def t_QUOTEDSTRING(self, t):
		# This is not yet correct: you need to complete the lexing of quotedstring
		r'\''
		return t

	@TOKEN(numeral)
	def t_NUMERAL(self, t):
		return t

	@TOKEN(character)
	def t_CHAR(self, t):
		return t

	def lex(self, input_string):
		self.lexer.input(input_string)
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)


lex = ClifLexer()
s = "(and ('max' 1 2 15) (or  ('Func' 'D')))"
print('Lexing '+s)
lex.lex(s)

s = "(and ('B' 'C') (or ('C' 'D'))))"
print('\nLexing '+s)
lex.lex(s)

# the following is currently not working but should be accepted because ? is in the set char
s = "('who' 'is' '?')" # there was a space between the last ' and )
print('\nLexing '+s)
lex.lex(s)

# remove later - just to test as u go along

s = "(56e7)"
print('\nLexing '+s)
lex.lex(s)