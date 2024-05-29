''' Compiler template for COSC261 Assignment
    ## WARNING ## Your code should be derived from this template 
                  by modifying only the parts mentioned in the requirements; 
                  other changes are at your own risk. 
                  Feel free, however, to experiment during the development.
'''

import re
import sys

# Restrictions:
# Integer constants must be short.
# Stack size must not exceed 1024.
# Integer is the only type.
# Logical operators cannot be nested.

class Scanner:
    '''The interface comprises the methods lookahead and consume.
       Other methods should not be called from outside of this class.
    '''

    def __init__(self, input_file):
        '''Reads the whole input_file to input_string, which remains constant.
           current_char_index counts how many characters of input_string have
           been consumed.
           next_token holds the most recently found token and the
           corresponding part of input_string.
        '''
        # source code of the program to be compiled
        self.input_string = input_file.read()
        # index where the unprocessed part of input_string starts
        self.current_char_index = 0
        # a pair (most recently read token, matched substring of input_string)
        self.next_token = self.get_token()
    #Author Samuel Beattie
    def skip_white_space(self):
        '''Consumes white-space characters in input_string up to the 
           next non-white-space character.
        '''
        current_token = self.input_string[self.current_char_index]
        while current_token.isspace():
            self.current_char_index += 1
            if self.current_char_index < len(self.input_string):
                current_token = self.input_string[self.current_char_index]
            else:
                self.current_char_index -= 1
                return
        return
  #Author Samuel Beattie
    def no_token(self):
        '''Stop execution if the input cannot be matched to a token.'''
        print('lexical error: no token found at the start of ' +
              self.input_string[self.current_char_index:])
        sys.exit()
  #Author Samuel Beattie
    def get_token(self):
        '''Returns the next token and the part of input_string it matched.
           The returned token is None if there is no next token.
           The characters up to the end of the token are consumed.
           TODO:
           Call no_token() if the input contains extra characters that 
           do not match any token (and are not white-space).
        '''
        if self.current_char_index < len(self.input_string):
            self.skip_white_space()
            token, longest = None, ''
            for (t, r) in Token.token_regexp:
                match = re.match(r, self.input_string[self.current_char_index:])
                if match and match.end() > len(longest):
                    token, longest = t, match.group()
            # check if there is a token
            if token is not None:
                # consume the token by moving the index to the end of the matched part
                self.current_char_index += len(longest)
                return (token, longest)
            else:
                if not self.input_string[self.current_char_index].isspace():
                    self.no_token()
                return None, ''
        else:
            return None, ''


    def lookahead(self):
        '''Returns the next token without consuming it.
           Returns None if there is no next token.
        '''
        return self.next_token[0]

    def unexpected_token(self, found_token, expected_tokens):
        '''Stop execution because an unexpected token was found.
           found_token contains just the token, not its value.
           expected_tokens is a sequence of tokens.
        '''
        print('syntax error: token in ' + repr(sorted(expected_tokens)) +
              ' expected but ' + repr(found_token) + ' found')
        sys.exit()
#Author Samuel Beattie
    def consume(self, *expected_tokens):
        '''Returns the next token and consumes it, if it is in
           expected_tokens. Calls unexpected_token(...) otherwise.
           If the token is a number or an identifier, not just the
           token but a pair of the token and its value is returned.
        '''
        current_value = self.next_token[1]
        self.next_token = self.lookahead()
        if self.next_token in expected_tokens:
            if self.next_token in Token.ID:
                current_token = self.next_token
                self.next_token = self.get_token()
                return current_token, current_value
            elif self.next_token in Token.NUM:
                current_token = self.next_token
                self.next_token = self.get_token()
                return current_token, current_value
            else:
                current_token = self.next_token
                self.next_token = self.get_token()
                return current_token
        else:
            self.unexpected_token(self.next_token,expected_tokens)

#Author Samuel Beattie
class Token:
    # The following enumerates all tokens.
    AND   = 'AND'
    NOT   = 'NOT'
    OR    = 'OR'
    READ  = 'READ'
    WRITE = 'WRITE'
    DO    = 'DO'
    ELSE  = 'ELSE'
    END   = 'END'
    IF    = 'IF'
    THEN  = 'THEN'
    WHILE = 'WHILE'
    SEM   = 'SEM'
    BEC   = 'BEC'
    LESS  = 'LESS'
    EQ    = 'EQ'
    GRTR  = 'GRTR'
    LEQ   = 'LEQ'
    NEQ   = 'NEQ'
    GEQ   = 'GEQ'
    ADD   = 'ADD'
    SUB   = 'SUB'
    MUL   = 'MUL'
    DIV   = 'DIV'
    LPAR  = 'LPAR'
    RPAR  = 'RPAR'
    NUM   = 'NUM'
    ID    = 'ID'

    # The following list gives the regular expression to match a token.
    # The order in the list matters for mimicking Flex behaviour.
    # Longer matches are preferred over shorter ones.
    # For same-length matches, the first in the list is preferred.
    token_regexp = [
        (AND,   'and'),
        (NOT,   'not'),
        (OR,    'or'),
        (READ,  'read'),
        (WRITE, 'write'),
        (DO,    'do'),
        (ELSE,  'else'),
        (END,   'end'),
        (IF,    'if'),
        (THEN,  'then'),
        (WHILE, 'while'),
        (SEM,   ';'),
        (BEC,   ':='),
        (LESS,  '<'),
        (EQ,    '='),
        (GRTR,  '>'),
        (LEQ,   '<='),
        (NEQ,   '!='),
        (GEQ,   '>='),
        (ADD,   '\\+'), # + is special in regular expressions
        (SUB,   '-'),
        (MUL,   '\\*'),
        (DIV,   '/'),
        (LPAR,  '\\('), # ( is special in regular expressions
        (RPAR,  '\\)'), # ) is special in regular expressions
        (NUM,   '[0-9]+'),
        (ID,    '[a-z]+'),
    ]

class Symbol_Table:
    '''A symbol table maps identifiers to locations.'''
    def __init__(self):
        self.symbol_table = {}
    def size(self):
        '''Returns the number of entries in the symbol table.'''
        return len(self.symbol_table)
    def location(self, identifier):
        '''Returns the location of an identifier. If the identifier is not in
           the symbol table, it is entered with a new location. 
           Locations are numbered sequentially starting with 0.
        '''
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        index = len(self.symbol_table)
        self.symbol_table[identifier] = index
        return index

class Label:
    def __init__(self):
        self.current_label = 0
    def next(self):
        '''Returns a new, unique label.'''
        self.current_label += 1
        return 'l' + str(self.current_label)

def indent(s, level):
    return '    '*level + s + '\n'

# Each of the following classes is a kind of node in the abstract syntax tree.
# indented(level) returns a string that shows the tree levels by indentation.
# code() returns a string with JVM bytecode implementing the tree fragment.
# true_code/false_code(label) jumps to label if the condition is/is not true.
# Execution of the generated code leaves the value of expressions on the stack.

class Program_AST:
    def __init__(self, program):
        self.program = program
    def __repr__(self):
        return repr(self.program)
    def indented(self, level):
        return self.program.indented(level)
    def code(self):
        program = self.program.code()
        local = symbol_table.size()
        java_scanner = symbol_table.location('Java Scanner')
        return '.class public Program\n' + \
               '.super java/lang/Object\n' + \
               '.method public <init>()V\n' + \
               'aload_0\n' + \
               'invokenonvirtual java/lang/Object/<init>()V\n' + \
               'return\n' + \
               '.end method\n' + \
               '.method public static main([Ljava/lang/String;)V\n' + \
               '.limit locals ' + str(local) + '\n' + \
               '.limit stack 1024\n' + \
               'new java/util/Scanner\n' + \
               'dup\n' + \
               'getstatic java/lang/System.in Ljava/io/InputStream;\n' + \
               'invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V\n' + \
               'astore ' + str(java_scanner) + '\n' + \
               program + \
               'return\n' + \
               '.end method\n'

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result
    def indented(self, level):
        result = indent('Statements', level)
        for st in self.statements:
            result += st.indented(level+1)
        return result
    def code(self):
        result = ''
        for st in self.statements:
            result += st.code()
        return result

class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
                       repr(self.then) + ' end'
    def indented(self, level):
        return indent('If', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               l1 + ':\n'
#Author Samuel Beattie    
class If_Else_AST:  
    def __init__(self, condition, then, else_then_condition,):
        self.condition = condition
        self.then = then
        self.else_then_condition = else_then_condition
    def __repr__(self):
        return 'if-else ' + repr(self.condition) + ' then ' + \
                       repr(self.then) + \
                    ' else ' + repr(self.else_then) + ' end'
    def indented(self, level):
        return indent('If-Else', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1) + \
               self.else_then_condition.indented(level+1)
    def code(self):
        l1 = label_generator.next() # use goto to skip to the else statement
        l2 = label_generator.next()
        return self.condition.false_code(l1) + self.then.code() + \
                'goto ' + l2 + '\n' + \
                l1 + ':\n' + self.else_then_condition.code() + \
                l2 + ':\n' #output l2 and then leave a newline for the code after the if statement
                    # goes to l1 (the if statement code) if the condition is true, otherwise,
                    # runs the else code underneath and then goes to l2 (code following the statement)
#Author Samuel Beattie
class While_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return 'while ' + repr(self.condition) + ' do ' + \
                          repr(self.body) + ' end'
    def indented(self, level):
        return indent('While', level) + \
               self.condition.indented(level+1) + \
               self.body.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next() #goto skips/goes back to l1 if the false_code is false (statement is true?)
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'
#Author Samuel Beattie
class BooleanExpression_AST:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self): # not necessary
        return 'BooleanTerm (or BooleanTerm)*' #multiple expressions
    def true_code(self, label):
        expressions = "" #string containing the true_code of each expression
        for expr in self.expression:
            expressions += expr.true_code(label)
        return expressions
    def false_code(self, label):
        l1 = label_generator.next()
        expressions = "" #string containing the true_code of each expression
        for expr in self.expression:
            expressions += expr.true_code(l1)
        return expressions + 'goto ' + \
               label + '\n' + \
               l1 + ':\n'
#Author Samuel Beattie
class BooleanTerm_AST:
    def __init__(self, term):
        self.term = term
    def __repr__(self):
        return 'BooleanFactor (and BooleanFactor)*' #multiple terms
    def true_code(self, label):
        l1 = label_generator.next()
        terms = "" #string containing the false_code of each term
        for ind_term in self.term:
            terms += ind_term.false_code(l1)
        return terms + 'goto ' + \
               label + '\n' + \
               l1 + ':\n'
    def false_code(self, label):
        terms = "" #string containing the false_code of each term
        for ind_term in self.term:
            terms += ind_term.false_code(label)
        return terms
#Author Samuel Beattie
class  BooleanFactor_AST:
    def __init__(self, factor):
        self.factor = factor
    def __repr__(self):
        return 'not BooleanFactor | Comparison'
    def true_code(self, label):
        return self.factor.false_code(label)
    def false_code(self, label):
        return self.factor.true_code(label) 

class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return repr(self.identifier) + ':=' + repr(self.expression)
    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level+1) + \
               self.expression.indented(level+1)
    def code(self):
        loc = symbol_table.location(self.identifier.identifier)
        return self.expression.code() + \
               'istore ' + str(loc) + '\n'
#Author Samuel Beattie
class Write_AST:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return 'write ' + repr(self.expression)
    def indented(self, level):
        return indent('Write', level) + self.expression.indented(level+1)
    def code(self):
        return 'getstatic java/lang/System/out Ljava/io/PrintStream;\n' + \
               self.expression.code() + \
               'invokestatic java/lang/String/valueOf(I)Ljava/lang/String;\n' + \
               'invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n'
#Author Samuel Beattie
class Read_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return 'read ' + repr(self.identifier)
    def indented(self, level):
        return indent('Read', level) + self.identifier.indented(level+1)
    def code(self):
        java_scanner = symbol_table.location('Java Scanner')
        loc = symbol_table.location(self.identifier.identifier)
        return 'aload ' + str(java_scanner) + '\n' + \
               'invokevirtual java/util/Scanner.nextInt()I\n' + \
               'istore ' + str(loc) + '\n'

class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return repr(self.left) + self.op + repr(self.right)
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def true_code(self, label):
        op = { '<':'if_icmplt', '=':'if_icmpeq', '>':'if_icmpgt',
               '<=':'if_icmple', '!=':'if_icmpne', '>=':'if_icmpge' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    def false_code(self, label):
        # Negate each comparison because of jump to "false" label.
        op = { '<':'if_icmpge', '=':'if_icmpne', '>':'if_icmple',
               '<=':'if_icmpgt', '!=':'if_icmpeq', '>=':'if_icmplt' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'

class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return '(' + repr(self.left) + self.op + repr(self.right) + ')'
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def code(self):
        op = { '+':'iadd', '-':'isub', '*':'imul', '/':'idiv' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + '\n'

class Number_AST:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return self.number
    def indented(self, level):
        return indent(self.number, level)
    def code(self): # works only for short numbers
        return 'sipush ' + self.number + '\n'

class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return self.identifier
    def indented(self, level):
        return indent(self.identifier, level)
    def code(self):
        loc = symbol_table.location(self.identifier)
        return 'iload ' + str(loc) + '\n'

# The following functions comprise the recursive-descent parser.

def program():
    sts = statements()
    return Program_AST(sts)

def statements():
    result = [statement()]
    while scanner.lookahead() == Token.SEM:
        scanner.consume(Token.SEM)
        st = statement()
        result.append(st)
    return Statements_AST(result)

def statement():
    if scanner.lookahead() == Token.IF:
        return if_statement()
    elif scanner.lookahead() == Token.WHILE:
        return while_statement()
    elif scanner.lookahead() == Token.ID:
        return assignment()
    elif scanner.lookahead() == Token.READ:
        return read()
    elif scanner.lookahead() == Token.WRITE:
        return write()
    else: # error
        return scanner.consume(Token.IF, Token.WHILE, Token.ID, Token.READ, Token.WRITE)
      
def if_statement():
    scanner.consume(Token.IF)
    condition = boolean_expression() #if statement condition composes of boolean expression(s)
    scanner.consume(Token.THEN)
    then = statements()
#Author Samuel Beattie
    if scanner.lookahead() == Token.ELSE: # check if an else statement follows the if
        scanner.consume(Token.ELSE)
        else_then = statements()
        scanner.consume(Token.END)
        return If_Else_AST(condition, then, else_then)
    scanner.consume(Token.END)
    return If_AST(condition, then)
#Author Samuel Beattie
def while_statement():
    scanner.consume(Token.WHILE)
    condition = boolean_expression() #while statement composes of boolean expression(s)
    scanner.consume(Token.DO)
    body = statements()
    scanner.consume(Token.END)
    return While_AST(condition, body)

def assignment():
    ident = identifier()
    scanner.consume(Token.BEC)
    expr = expression()
    return Assign_AST(ident, expr)
#Author Samuel Beattie
def read():
    scanner.consume(Token.READ)
    ident = identifier()
    return Read_AST(ident)
#Author Samuel Beattie
def write():
    scanner.consume(Token.WRITE)
    expr = expression()
    return Write_AST(expr)
#Author Samuel Beattie
def boolean_expression(): # use statements code
    expr = [boolean_term()] #can be multiple terms in an expression 
    while scanner.lookahead() == Token.OR:
        scanner.consume(Token.OR) 
        expr.append(boolean_term())
    return BooleanExpression_AST(expr)
#Author Samuel Beattie
def boolean_term():
    term = [boolean_factor()] #can be multiple factors in a term
    while scanner.lookahead()== Token.AND:
        scanner.consume(Token.AND)
        term.append(boolean_factor()) 
    return BooleanTerm_AST(term)
#Author Samuel Beattie
def boolean_factor():
    if scanner.lookahead() == Token.NOT: # not BooleanFactor | Comparison
        scanner.consume(Token.NOT)
        return BooleanFactor_AST(boolean_factor())
    else:
        return comparison() # not a not, must give a comp

operator = { Token.LESS:'<', Token.EQ:'=', Token.GRTR:'>',
             Token.LEQ:'<=', Token.NEQ:'!=', Token.GEQ:'>=',
             Token.ADD:'+', Token.SUB:'-', Token.MUL:'*', Token.DIV:'/' }

def comparison():
    left = expression()
    op = scanner.consume(Token.LESS, Token.EQ, Token.GRTR,
                         Token.LEQ, Token.NEQ, Token.GEQ)
    right = expression()
    return Comparison_AST(left, operator[op], right)

def expression():
    result = term()
    while scanner.lookahead() in [Token.ADD, Token.SUB]:
        op = scanner.consume(Token.ADD, Token.SUB)
        tree = term()
        result = Expression_AST(result, operator[op], tree)
    return result

def term():
    result = factor()
    while scanner.lookahead() in [Token.MUL, Token.DIV]:
        op = scanner.consume(Token.MUL, Token.DIV)
        tree = factor()
        result = Expression_AST(result, operator[op], tree)
    return result

def factor():
    if scanner.lookahead() == Token.LPAR:
        scanner.consume(Token.LPAR)
        result = expression()
        scanner.consume(Token.RPAR)
        return result
    elif scanner.lookahead() == Token.NUM:
        value = scanner.consume(Token.NUM)[1]
        return Number_AST(value)
    elif scanner.lookahead() == Token.ID:
        return identifier()
    else: # error
        return scanner.consume(Token.LPAR, Token.NUM, Token.ID)

def identifier():
    value = scanner.consume(Token.ID)[1]
    return Identifier_AST(value)

# Initialise scanner, symbol table and label generator.

scanner = Scanner(sys.stdin)
symbol_table = Symbol_Table()
symbol_table.location('Java Scanner') # fix a location for the Java Scanner
label_generator = Label()

# Uncomment the following to test the scanner without the parser.
# Show all tokens in the input.
#
# token = scanner.lookahead()
# while token != None:
#     if token in [Token.NUM, Token.ID]:
#         token, value = scanner.consume(token)
#         print(token, value)
#     else:
#         print(scanner.consume(token))
#     token = scanner.lookahead()
# sys.exit()

# Call the parser.

ast = program()
if scanner.lookahead() != None:
    print('syntax error: end of input expected but token ' +
          repr(scanner.lookahead()) + ' found')
    sys.exit()

# Uncomment the following to test the parser without the code generator.
# Show the syntax tree with levels indicated by indentation.
#
# print(ast.indented(0), end='')
# sys.exit()

# Call the code generator.

# Translate the abstract syntax tree to JVM bytecode.
# It can be assembled to a class file by Jasmin: http://jasmin.sourceforge.net/

print(ast.code(), end='')

