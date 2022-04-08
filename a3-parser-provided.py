import sys

import ply.yacc as yacc
import ply.lex as lex

from ply.lex import TOKEN

class ClifLexer():

	# CONSTRUCTOR
	def __init__(self):
		print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		print('Lexer destructor called.')

	reserved_bool = {
		'and' : 'AND',
		'or' : 'OR',
		'iff' : 'IFF',
		'if' : 'IF',
		'not' : 'NOT',
		'cl:comment' : 'COMMENT'
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

	def t_NEWLINE(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	def t_error(self,t):
		print("Lexing error: Unknown character \"{}\" at line {}".format(t.value[0], t.lexer.lineno))
		t.lexer.skip(1)

	t_ignore = ' \t\r\n\f\v'

	# regular expressions used to build decorators for function tokens

	digit = r'([0-9])'
	numeral = r'(' + digit + r')+'
	character = r'(' + digit + r'|[^0-9\)\(\'\"])' # gross - currently necessary because t_CHAR has higher priority than other rules

	stringquote = r'\''
	namequote = r'\"'
	quotedstring = stringquote + r'(' + character + r'|' + namequote + r')*' + stringquote

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

	# updated version in main.py for writing to file
	def lex(self, input_string):
		self.lexer.input(input_string)
		# list_of_str = []
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)
		# 	list_of_str.append(str(tok) + '\n')
		# return(list_of_str)


class ClifParser(object):

	tokens = ClifLexer.tokens

	# CONSTRUCTOR
	def __init__(self):
		print('Parser constructor called.')
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)

	start = 'starter'

	def p_starter(self, p):
		"""
		starter : sentence
				| sentence starter
		"""
		print("Starting the parsing process.")
		pass

	# def p_sentence(self, p): # TODO add boolsent once it's defined
	# 	"""
	# 	sentence : OPEN AND QUOTEDSTRING QUOTEDSTRING CLOSE
	# 	"""
	# 	# should actually be: sentence : atomsent
	# 	#							   | boolsent

	# 	# **rm note that the rule above is INCORRECT: it is just an example of how to specify a rule
	# 	#'sentence : OPEN QUOTEDSTRING CLOSE'
	# 	print("???")
	# 	print("Found a sentence: {} {} {} ".format(p[2], p[3], p[4]))
	# 	if p[3] == p[4]:
	# 		no_quotedstrings = 1
	# 	else:
	# 		no_quotedstrings = 2

	# 	print("Number of distinct quoted strings: " + str(no_quotedstrings))

	def p_sentence_atom(self, p):
		"""
		sentence : atomsent
		"""

		p[0] = p[1]
		print("Found a sentence: {}".format(p[0]))


	def p_sentence_bool(self, p):
		"""
		sentence : boolsent
		"""

		p[0] = p[1]
		print("Found a sentence: {}".format(p[0]))


	def p_atomsent(self, p):
		'''
		atomsent : OPEN predicate CLOSE
		'''
		# temporarily removed termseq b/c an error is being caught
		p[0] = p[2]

	def p_predicate(self, p):
		'''
		predicate : interpretedname
		'''
		p[0] = p[1]

	def p_termseq(self, p):
		'''
		termseq : interpretedname
				| interpretedname termseq
		'''
		p[0] = p[1:]

	# commenting out (for now?) since its claiming duplicate rule
	# def p_interpretedname(self, p): #neither of these are actually terminals... hmm
	# 	"""
	# 	interpretedname : NUMERAL
	# 					| QUOTEDSTRING
	# 	"""
	# 	pass

	def p_interpretedname_num(self, p):
		"""
		interpretedname : NUMERAL
		"""
		p[0] = p[1]

	def p_interpretedname_quote(self, p):
		"""
		interpretedname : QUOTEDSTRING
		"""
		p[0] = p[1]

	def p_boolsent_and(self, p):
		'''
		boolsent : OPEN AND sentence CLOSE
		'''
		p[0] = ('AND', p[3])

	def p_boolsent_or(self, p):
		'''
		boolsent : OPEN OR sentence CLOSE
		'''
		# how to write the grammar for { sentence } cause idk
		p[0] = ('OR', p[3])

	def p_boolsent_if(self, p):
		'''
		boolsent : OPEN IF sentence sentence CLOSE
					| OPEN IFF sentence sentence CLOSE
		'''
		# for now only handling IF, not IFF for testing:
		p[0] = ('IF', p[3], p[4])

	def p_boolsent_not(self, p):
		'''
		boolsent : OPEN NOT sentence CLOSE
		'''
		p[0] = ('NOT', p[3])

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

"""
HARD-CODED TESTS
"""

# # using only the lexer
# lexer = ClifLexer()
# s = "(and ('B' 'C') (or ('C' 'D'))))"
# print('\nLexing '+s)
# lexer.lex(s)

# parser = ClifParser()
# s = "(and 'Func')"
# #s = "(and ('max' 1 2 15) (or  ('Func' 'D')))"
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# parser = ClifParser()
# s = "(or 'Func')"
# #s = "(and ('max' 1 2 15) (or  ('Func' 'D')))"
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# # the following is currently not working but should be accepted because ? is in the set char
# parser = ClifParser()
# s = "('who' 'is' '?')" # there was a space between the last ' and )
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# parser.parse(s)

# ash's test
parser = ClifParser()
s = "(not ('hi'))"
print('\nLexing '+s)
parser.lexer.lex(s)
print('\nParsing '+s)
result = parser.parse(s)

# temporarily commented out so it's not running too many tests

"""
MAIN FUNCTION
Parameter file: relative path to a CLIF file
Parameter lexer_parser: run the lexer only (False) or run both the lexer and parser (True)
Preconditon: lexer_parser is a Boolean
"""

# def main(file, lexer_parser):
# 	lex = ClifLexer()

# 	if lexer_parser == "False":
# 		with open(file, 'r') as clif_file, open("q1_results.txt", "w") as lexer_results:
# 			lines = clif_file.readlines()
# 			for line in lines:
# 				lex_lines = lex.lex(line)
# 				lexer_results.write('\nLexing ' + line)
				
# 				for lex_token in lex_lines: 
# 					lexer_results.write(lex_token)

# 			lexer_results.close()
# 	elif lexer_parser == "True":
# 		pass
# 	else:
# 		print("Error.")

# main(sys.argv[1], sys.argv[2])