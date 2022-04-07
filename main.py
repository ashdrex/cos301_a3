"""
COS301 Assignment 3:

This program contains a modified lexer and parser.
Pass a CLIF file as an input and the program will
output the results into a separate textfile.

Example:
'python main.py a3-valid-clif1-v2.txt True'

Authors: Nicole Cortez (Dydomio), Ashley Drexler (ashdrex)
Version: April 8, 2022
"""

import sys

import ply.yacc as yacc
import ply.lex as lex

from ply.lex import TOKEN


"""
LEXER
"""

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

	# t_DIGIT= r'([0-9])'
	def t_DIGIT(self, t):
		r'\b\d\b'
		return t

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

	def lex(self, input_string):
		self.lexer.input(input_string)
		list_of_str = []
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)
			list_of_str.append(str(tok) + '\n')
		return(list_of_str)

"""
PARSER
"""

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
		'sentence : OPEN QUOTEDSTRING CLOSE'
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

"""
MAIN FUNCTION

Parameter file: relative path to a CLIF file

Parameter lexer_parser: run the lexer only (False) or run both the lexer and parser (True)
Preconditon: lexer_parser is a Boolean
"""

def main(file, lexer_parser):
	# TODO: remove set boolean value from lexer_parser arg
	lex = ClifLexer()

	if lexer_parser == "False":
		with open(file, 'r') as clif_file, open("q1_results.txt", "w") as lexer_results:
			lines = clif_file.readlines()
			for line in lines:
				lex_lines = lex.lex(line)
				lexer_results.write('\nLexing ' + line)
				
				for lex_token in lex_lines: 
					lexer_results.write(lex_token)

			lexer_results.close()
	elif lexer_parser == "True":
		pass
	else:
		print("Error.")

main(sys.argv[1], sys.argv[2])	# TODO: modify this and main() to include the boolean arg