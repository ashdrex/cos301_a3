import sys

import ply.yacc as yacc
import ply.lex as lex

from ply.lex import TOKEN

class ClifLexer():

	# CONSTRUCTOR
	def __init__(self):
		# print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		pass
		# print('Lexer destructor called.')

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
	character = r'(' + digit + r'|[^0-9\)\(\'\"])' # exclude OPEN, CLOSE, STRINGQUOTE, and NAMEQUOTE

	stringquote = r'\''
	namequote = r'\"'
	quotedstring = stringquote + r'(' + character + r'|' + namequote + r')*' + stringquote

	# token specification as a string (no regular expression)

	t_OPEN= '\('
	t_CLOSE= '\)'

	# token specification as a regular expression

	t_DIGIT= r'([0-9])'

	# token specification as a function

	def t_RESERVEDELEMENT(self, t):
		r'[a-zA-Z]+(?::[a-zA-Z]+)*'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			return t
		else:
			pass

	@TOKEN(quotedstring)
	def t_QUOTEDSTRING(self, t):
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
		list_of_str = []
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)
			list_of_str.append(str(tok) + '\n')
		return(list_of_str)

# method to turn a tuple into a string of its elements
def stringifyTuple(tup):
	# don't do anything if it's not a tuple
	if (isinstance(tup, tuple)):
		tupString = ""
		for i in range (0, len(tup)):
			if(tup[i] == ')' or tup[i-1] == "(" or tup[i] == " "):
				tupString = tupString + str(tup[i])
			else:
				tupString = tupString + " " + str(tup[i])
		return tupString.strip()
	else:
		return tup

class ClifParser(object):

	tokens = ClifLexer.tokens

	# CONSTRUCTOR
	def __init__(self):
		# print('Parser constructor called.')
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)
		self.is_atomic = False
		self.is_bool = False
		self.ops = 0
		self.names = {}

	start = 'starter'

	def p_starter(self, p):
		"""
		starter : sentence
				| sentence starter
		"""
		# print("Starting the parsing process.")

	def p_sentence_atom(self, p):
		"""
		sentence : atomsent
		"""

		p[0] = stringifyTuple(p[1])

		# print("Found a sentence: {}".format(p[0]))
		self.is_atomic = True
		self.is_bool = False


	def p_sentence_bool(self, p):
		"""
		sentence : boolsent
		"""

		p[0] = stringifyTuple(p[1])

		# print("Found a sentence: {}".format(p[0]))
		self.is_atomic = False
		self.is_bool = True

	# special sentence case for multiple occurrences of sentence
	# only used with and/or boolsent
	def p_multisent(self, p):
		"""
		multisent : sentence
				  | sentence multisent
				  | empty
		"""

		if(p[1] != None):
			if(len(p) == 2):
				p[0] = p[1]
			elif(len(p) == 3):
				p[0] = "{} {}".format(p[1], p[2])
		else:
			p[0] = p[1]
			

	def p_atomsent(self, p):
		'''
		atomsent : OPEN predicate termseq CLOSE
		'''

		# don't return termseq if it's empty
		if (p[3] == None):
			p[0] = (p[1], p[2], p[4])
		else:
			p[0] = (p[1], p[2], p[3], p[4])

	def p_predicate(self, p):
		'''
		predicate : interpretedname
		'''
		p[0] = p[1]

	def p_termseq(self, p):
		'''
		termseq : interpretedname
				| interpretedname termseq
				| empty
		'''

		# TODO fix this conditional, the logic is weird (if if -> same result as "else")
		# return termseq as a format string if it's a sequence of two or more terms
		if(p[1] != None):
			if(len(p) == 2):
				p[0] = p[1]
			elif(len(p) == 3):
				p[0] = "{} {}".format(p[1], p[2])
		else:
			p[0] = p[1]

	def p_interpretedname(self, p):
		"""
		interpretedname : NUMERAL
						| QUOTEDSTRING
		"""
		p[0] = p[1]
		if p[1][0] == ("'" or "\""): # lol there's gotta be a better way of recognizing a quotedstring, this way a quick way off the top of my head
			self.names[p[1]] = p[1]

	def p_boolsent_and(self, p):
		'''
		boolsent : OPEN AND multisent CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'AND', p[3], p[4]))
		self.ops += 1

	def p_boolsent_or(self, p):
		'''
		boolsent : OPEN OR multisent CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'OR', p[3], p[4]))
		self.ops += 1

	# covers both IF and IFF
	def p_boolsent_if(self, p):
		'''
		boolsent : OPEN IF sentence sentence CLOSE
				 | OPEN IFF sentence sentence CLOSE
		'''
		p[0] = stringifyTuple((p[1], p[2], p[3], p[4], p[5]))
		self.ops += 1


	def p_boolsent_not(self, p):
		'''
		boolsent : OPEN NOT sentence CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'NOT', p[3], p[4]))
		self.ops += 1

	# empty production rule to support rules with repetition
	def p_empty(self, p):
		'empty :'
		pass

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
		print(self.get_output(input_string))

	def get_output(self, input_string):
		if self.is_atomic:
			atom_str = "atomic: {}: ops={}, names={}".format(input_string.strip(), self.ops, len(self.names))
			return atom_str
		elif self.is_bool:
			bool_str = "Boolean: {}: ops={}, names={}".format(input_string.strip(), self.ops, len(self.names))
			return bool_str

"""
HARD-CODED TESTS
"""

# atomsent + termseq test
# parser = ClifParser()
# s = "('max' 1 2 15)"
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# result = parser.parse(s)

# boolsent + multisent test
# parser = ClifParser()
# s = "(and ('max' 1 2 15) ('words') ('foo'))"
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# result = parser.parse(s)

# iff + if test
# parser = ClifParser()
# s = "(iff ('min' 4 8 16 'maybe') (if ('yes') (and ('max' 1 2 15) ('words') ('foo'))))"
# print('\nLexing '+s)
# parser.lexer.lex(s)
# print('\nParsing '+s)
# result = parser.parse(s)
# print(str(parser.get_count()) + " sentences")

# print test/mocking a file input
# arr = ["('FuncA' 'a' 100)", "(and ('B' 'C') (or ('C' 'D')))", "(or ('FuncB' ('Func' 100 'A')) 'Func1')"]	# the example in the pdf has an extra paren for the second sent?
# print(str(len(arr)) + " sentences")    
# for s in arr:
# 	parser = ClifParser()
# 	result = parser.parse(s)

"""
MAIN FUNCTION
Parameter file: relative path to a CLIF file
Parameter lexer_parser: run the lexer only (False) or run both the lexer and parser (True)
Preconditon: lexer_parser is a Boolean
"""

def main(file, lexer_parser):
	lex = ClifLexer()

	if lexer_parser == "False":
		with open(file, 'r') as clif_file, open("lexer_results.txt", "a") as lexer_results:
			lines = clif_file.readlines()
			for line in lines:
				lex_lines = lex.lex(line)
				lexer_results.write('\nLexing ' + line)
				
				for lex_token in lex_lines: 
					lexer_results.write(lex_token)

			lexer_results.close()
	elif lexer_parser == "True":
		with open(file, 'r') as clif_file, open("lexer_results.txt", "a") as lexer_results,  open("parser_results.txt", "a") as parser_results:
			lines = clif_file.readlines()

			num_sentences = str(len(lines)) + " sentences\n"
			print(num_sentences)    
			parser_results.write(num_sentences)
			for line in lines:
				parser = ClifParser()

				lex_lines = lex.lex(line)
				
				result = parser.parse(line)
				parser_results.write(parser.get_output(line) + "\n")

				lexer_results.write('\n\nLexing ' + line)				
				for lex_token in lex_lines: 
					lexer_results.write(lex_token)

			lexer_results.close()	
	else:
		print("Error.")

main(sys.argv[1], sys.argv[2])