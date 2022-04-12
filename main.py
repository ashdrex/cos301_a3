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

"""
PARSER
"""

class ClifParser(object):

	tokens = ClifLexer.tokens

	# CONSTRUCTOR
	def __init__(self):
		# print('Parser constructor called.')
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)
		self.is_valid = True
		self.is_atomic = False
		self.is_bool = False
		self.ops = 0
		self.names = {}
		self.elements = []

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

		self.elements.append("ParsedElement(TYPE: sentence, VALUE: {})".format(p[0]))


	def p_sentence_bool(self, p):
		"""
		sentence : boolsent
		"""

		p[0] = stringifyTuple(p[1])

		# print("Found a sentence: {}".format(p[0]))
		self.is_atomic = False
		self.is_bool = True

		self.elements.append("ParsedElement(TYPE: sentence, VALUE: {})".format(p[0]))

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

		self.elements.append("ParsedElement(TYPE: sentence, VALUE: {})".format(p[0]))
			

	def p_atomsent(self, p):
		'''
		atomsent : OPEN predicate termseq CLOSE
		'''

		# don't return termseq if it's empty
		if (p[3] == None):
			p[0] = stringifyTuple((p[1], p[2], p[4]))
		else:
			p[0] = stringifyTuple((p[1], p[2], p[3], p[4]))

		self.elements.append("ParsedElement(TYPE: atomsent, VALUE: {})".format(p[0]))

	def p_predicate(self, p):
		'''
		predicate : interpretedname
		'''
		p[0] = p[1]

		self.elements.append("ParsedElement(TYPE: predicate, VALUE: {})".format(p[0]))

	def p_termseq(self, p):
		'''
		termseq : interpretedname
				| interpretedname termseq
				| empty
		'''

		# return termseq as a format string if it's a sequence of two or more terms
		if(p[1] != None):
			if(len(p) == 2):
				p[0] = p[1]
			elif(len(p) == 3):
				p[0] = "{} {}".format(p[1], p[2])
		else:
			p[0] = p[1]

		self.elements.append("ParsedElement(TYPE: termseq, VALUE: {})".format(p[0]))

	def p_interpretedname(self, p):
		"""
		interpretedname : NUMERAL
						| QUOTEDSTRING
		"""
		p[0] = p[1]
		if p[1][0] == ("'" or "\""): # lol there's gotta be a better way of recognizing a quotedstring, this way a quick way off the top of my head
			self.names[p[1]] = p[1]
			self.elements.append("ParsedElement(TYPE: quotedstring, VALUE: {})".format(p[0]))
		else:
			self.elements.append("ParsedElement(TYPE: numeral, VALUE: {})".format(p[0]))

	def p_boolsent_and(self, p):
		'''
		boolsent : OPEN AND multisent CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'AND', p[3], p[4]))
		self.ops += 1

		self.elements.append("ParsedElement(TYPE: boolsent, VALUE: {})".format(p[0]))

	def p_boolsent_or(self, p):
		'''
		boolsent : OPEN OR multisent CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'OR', p[3], p[4]))
		self.ops += 1

		self.elements.append("ParsedElement(TYPE: boolsent, VALUE: {})".format(p[0]))

	# covers both IF and IFF
	def p_boolsent_if(self, p):
		'''
		boolsent : OPEN IF sentence sentence CLOSE
				 | OPEN IFF sentence sentence CLOSE
		'''
		p[0] = stringifyTuple((p[1], p[2], p[3], p[4], p[5]))
		self.ops += 1
		
		self.elements.append("ParsedElement(TYPE: boolsent, VALUE: {})".format(p[0]))

	def p_boolsent_not(self, p):
		'''
		boolsent : OPEN NOT sentence CLOSE
		'''
		p[0] = stringifyTuple((p[1], 'NOT', p[3], p[4]))
		self.ops += 1

		self.elements.append("ParsedElement(TYPE: boolsent, VALUE: {})".format(p[0]))

	# empty production rule to support rules with repetition
	def p_empty(self, p):
		'empty :'
		pass

	def p_error(self, p):

		if p is None:
			#print("Unexpectedly reached end of line input. Skipping...")
			self.elements.append("Unexpectedly reached end of line input. Skipping...")
		else:
			# Note the location of the error before trying to lookahead
			error_pos = p.lexpos

			# Reading the symbols from the Parser stack
			stack = [symbol for symbol in self.parser.symstack][1:]

			#print("Parsing error; current stack: " + str(stack))
			self.elements.append("Parsing error; current stack: " + str(stack))

		# not a valid sentence
		self.is_valid = False
		exit


	def parse(self, input_string):
		self.parser.parse(input_string)

		for element in self.elements:
			print(element)

		if self.is_atomic:
			atom_str = "atomic: {}: ops={}, names={}".format(input_string.strip(), self.ops, len(self.names))
			return atom_str
		elif self.is_bool:
			bool_str = "Boolean: {}: ops={}, names={}".format(input_string.strip(), self.ops, len(self.names))
			return bool_str

"""
MAIN FUNCTION

Parameter file: relative path to a CLIF file

Parameter lexer_parser: run the lexer only (False) or run both the lexer and parser (True)
Preconditon: lexer_parser is a Boolean
"""

def main(file, lexer_parser):
	lex = ClifLexer()

	if lexer_parser == "False":
		with open(file, 'r') as clif_file, open("results_file.txt", "a") as results_file:
			lines = clif_file.readlines()

			results_file.write("\n=== Lexing " + file + " ===\n")
			for line in lines:
				lex_lines = lex.lex(line)
				results_file.write('\nLexing ' + line)
				
				for lex_token in lex_lines: 
					results_file.write(lex_token)

			results_file.close()
	elif lexer_parser == "True":
		with open(file, 'r') as clif_file, open("results_file.txt", "a") as results_file:
			lines = clif_file.readlines()

			results_file.write("\n=== Lexing and parsing " + file + " ===\n")

			num_sentences = 0
			parsed_sentences = []
			for line in lines:
				parser = ClifParser()

				lex_lines = lex.lex(line)
				result = parser.parse(line)

				if (parser.is_valid == True):
					parsed_sentences.append(result)
					num_sentences += 1

				results_file.write('\nLexing ' + line)				
				for lex_token in lex_lines: 
					results_file.write(lex_token)

				#new
				results_file.write('\nParsing ' + line)
				for element in (parser.elements):
					results_file.write(element + '\n')

			results_file.write("\n\n{} sentences\n".format(num_sentences))
			for sents in parsed_sentences:
				results_file.write("{}\n".format(sents))

			results_file.close()
	else:
		print("Error.")

main(sys.argv[1], sys.argv[2])