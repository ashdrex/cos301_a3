import ply.lex as lex
import ply.yacc as yacc

class ClifLexer(object):

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

	tokens = ['OPEN', 'CLOSE', 'QUOTEDSTRING', 'RESERVEDELEMENT']

	tokens += reserved_bool.values()

	t_ignore = ' \t\r\n\f\v' # code as written in this file did not have beginning whitespace; added whitespace based on Brightspace announcement

	def t_NEWLINE(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	def t_error(self,t):
		print("Lexing error: Unknown character \"{}\" at line {}".format(t.value[0], t.lexer.lineno))
		t.lexer.skip(1)

	# token specification as a string (no regular expression)

	t_OPEN= '\('
	t_CLOSE= '\)'

	def t_RESERVEDELEMENT(self, t):
		# here we use a regular expression to say what matches this particular token:
		# any sequence of standard characters of length 1 or greater
		# but this does not yet cover all reservedelements
		r'\w+'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			#print("Boolean reserved word: " + t.value)
			return t
		else:
			pass

	def t_QUOTEDSTRING(self, t):
		# This is not yet correct: you need to complete the lexing of quotedstring
		# This only matches a single quotation character
		r'\''
		return t

	def lex(self, input_string):
		self.lexer.input(input_string)
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)


class ClifParser(object):

	tokens = ClifLexer.tokens

	# CONSTRUCTOR
	def __init__(self):
		print('Parser constructor called.')
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)


	def p_starter(self, p):
		"""
		starter : sentence
				| sentence starter
		"""
		print("Starting the parsing process.")
		pass

	def p_sentence(self, p):
		"""
		sentence : OPEN AND QUOTEDSTRING QUOTEDSTRING CLOSE
		"""
		# note that the rule above is INCORRECT: it is just an example of how to specify a rule
		print("Found a sentence: {} {} {} ".format(p[2], p[3], p[4]))
		if p[3] == p[4]:
			no_quotedstrings = 1
		else:
			no_quotedstrings = 2

		print("Number of distinct quoted strings: " + str(no_quotedstrings))

	def p_error(self, p):

		if p is None:
			raise TypeError("Unexpectedly reached end of file (EOF)")

		# Note the location of the error before trying to lookahead
		error_pos = p.lexpos

		# Reading the symbols from the Parser stack
		stack = [symbol for symbol in self.parser.symstack][1:]

		print("Parsing error; current stack: " + str(stack))


	def parse(self, input_string):
		# initialize the parser
		#parser = yacc.yacc(module=self)

		self.parser.parse(input_string)

# using only the lexer
lexer = ClifLexer()
s = "(and ('B' 'C') (or ('C' 'D'))))"
print('\nLexing '+s)
lexer.lex(s)

parser = ClifParser()
s = "(and 'Func')"
#s = "(and ('max' 1 2 15) (or  ('Func' 'D')))"
print('\nLexing '+s)
parser.lexer.lex(s)
print('\nParsing '+s)
parser.parse(s)

parser = ClifParser()
s = "(or 'Func')"
#s = "(and ('max' 1 2 15) (or  ('Func' 'D')))"
print('\nLexing '+s)
parser.lexer.lex(s)
print('\nParsing '+s)
parser.parse(s)

# the following is currently not working but should be accepted because ? is in the set char
parser = ClifParser()
s = "('who' 'is' '?')" # there was a space between the last ' and )
print('\nLexing '+s)
parser.lexer.lex(s)
print('\nParsing '+s)
parser.parse(s)
