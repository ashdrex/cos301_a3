import sys

import ply.yacc as yacc
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

	reserved_bool = {	# consider renaming to match content
		'and' : 'AND',
		'or' : 'OR',
		'iff' : 'IFF',
		'if' : 'IF',
		'not' : 'NOT',
		'cl:comment' : 'CL_COMMENT'
	}

	tokens = [
		'OPEN', 
		'CLOSE', 
		'CHAR',
		'DIGIT',
		'NUMERAL',
		'STRINGQUOTE',
		'NAMEQUOTE',
		'QUOTEDSTRING', 
		'RESERVEDELEMENT'
	]

	tokens += reserved_bool.values()

	t_ignore = ' \t\r\n\f\v' # code as written in this file did not have beginning whitespace; added whitespace based on Brightspace announcement

	# regular expressions used to build decorators for function tokens

	digit = r'([0-9])'
	numeral = r'(' + digit + r')+'
	character = r'(' + digit + r'|[^0-9\)\(\'\"])' # gross - currently necessary because t_CHAR has higher priority than other rules

	stringquote = r'\''
	namequote = r'\"'
	quotedstring = stringquote + r'(' + character + r'|' + namequote + r')*' + stringquote

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
	# should numerals be two or more digits?
	t_DIGIT= r'([0-9])'
	#t_NUMERAL=

	def t_RESERVEDELEMENT(self, t):
		r'[a-zA-Z]+(?::[a-zA-Z]+)*'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			# print("Boolean reserved word: " + t.value)
			return t
		else:
			pass

	@TOKEN(quotedstring)
	def t_QUOTEDSTRING(self, t):
		# This is not yet correct: you need to complete the lexing of quotedstring
		#r'\''
		return t

	@TOKEN(numeral)
	def t_NUMERAL(self, t):
		return t

	@TOKEN(character)
	def t_CHAR(self, t):
		return t

	@TOKEN(stringquote)
	def t_STRINGQUOTE(self, t):
		return t

	@TOKEN(namequote)
	def t_NAMEQUOTE(self, t):
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

	def p_interpretedname(self, p): #neither of these are actually terminals... hmm
		"""
		interpretedname : NUMERAL
						| QUOTEDSTRING
		"""
		pass

	def p_predicate(self, p):
		'''
		predicate : interpretedname
		'''
		pass

	def p_termseq(self, p):
		'''
		termseq : interpretedname
				| interpretedname termseq
		'''
		pass

	def p_atomsent(self, p):
		'''
		atomsent : OPEN predicate termseq CLOSE
		'''
		pass

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
		'sentence : OPEN QUOTEDSTRING CLOSE'
		print("???")
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
		# parser = yacc.yacc(module=self)

		self.parser.parse(input_string)
		print("ok")

"""
HARD-CODED TESTS
"""

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

"""
MAIN FUN
"""

# temporarily commented out so it's not running too many tests

'''def main(file, lexer_parser = True):
	lex = ClifLexer()

	with open(file, 'r') as clif_file:
		lines = clif_file.readlines()
		for line in lines:
			print('\nLexing ' + line)
			lex.lex(line)	

main(sys.argv[1])	# TODO: modify this and main() to include the boolean arg'''