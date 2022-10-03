# In this document, some inspiration was taken from the simpleArith.py example in Pyparsing
# github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py

import re
from pyparsing import Regex, infixNotation, Literal, oneOf, OpAssoc, common

# All characters allowed in an attribute of a PyTango device. Letters a to z, A to Z, number 0 to 9 and the '-' character.
allowed_characters_regex = "a-zA-Z0-9-"

# The attribute cannot contain an empty space, the '/' character or brackets (brackets need be escaped with '\').
forbidden_characters_regex = " /\(\)"

# According to the Tango naming system. 
# 3 times any amount of characters, followed by a '/'. This specifies the device.
# Then any amount of characters to specify the attribute.
# For example: r3-a110311cab01/mag/psia-01/current
attribute_regex = f"[{allowed_characters_regex}][^{forbidden_characters_regex}]*/" * 3 + f"[{allowed_characters_regex}][^{forbidden_characters_regex}]*" 

re_compiled = re.compile(attribute_regex)

exponent = Literal('^')
multiplication_division = oneOf('* /')
plus_minus = oneOf('+ -')

operands = Regex(attribute_regex) | common.number

infix_parser = infixNotation(operands,
    [
        # (Operator, number of operands, associativity)
        (exponent, 2, OpAssoc.RIGHT),
        (multiplication_division, 2, OpAssoc.LEFT),
        (plus_minus, 2, OpAssoc.LEFT)
    ]
)

def parse_expression(expression: str): 
    """
    Take an expression and return a list of [variable, operation, variable, operation,...variable].
    Lists inside this list have priority (like paranthesis in mathematical operations), and should be evaluated first.
    Order of operation matters.
    The operands, operators and brackets should be seperated by a space.
    For example, the expression "( x + 2 ) - 4 * 27" will return [[x, '+', 2], '-', [4, '*', 27]]
    where x is some string in the form of a valid PyTango attribute according to the attribute_regex constant.
    """
    
    # ERROR HANDLING 
    
    # split expression into words.
    words = expression.split()
    next_word_is_variable = True # We expect the first word to be a variable, then an operator, then a variable, etc.
    for word in words:
      # Remove opening and closing bracket for words where the bracket is written directly attached. e.g. '(r3/ps/mag/current)'
      if len(word) > 1 and word.startswith('('):
        word = word[1:] 
      if len(word) > 1 and word.endswith(')'):
        word = word[:-1] 

      # Check if the word is valid
      attribute_match = re_compiled.fullmatch(word) # it is a valid attribute
      operator_match = word in "^*/+-" # it is a valid operator. (This is a bit of an hidden dependency, as the operators are seperately defined for the infix notation class above)
      closing_bracket_match = word == ")"
      opening_bracket_match = word == "("

      # it is a valid number
      try:
        float(word)
        number_match = True
      except ValueError:
        number_match = False

      if not (attribute_match or operator_match or number_match or closing_bracket_match or opening_bracket_match): # If it matches none of these, panic!
        raise SyntaxError(f"Invalid input in {word}")
   
      # Check if the word is an operator or variable, as we expect
      if next_word_is_variable and operator_match: # The next word is supposed to be a variable, but it is an operator. Panic!
        raise SyntaxError(f"{word} was expected to be a variable, but is an operator.")
      elif not next_word_is_variable and (number_match or attribute_match): # Expected an operator, but found a variable. Panic!
        raise SyntaxError(f"{word} was expected to be an operator, but is a variable.") 
      elif opening_bracket_match: # opening brackets have to be followed by a variable
        next_word_is_variable = True
      elif closing_bracket_match: # closing brackets have to be followed by an operator
        next_word_is_variable = False
      else: # switch the expectation
        next_word_is_variable = not next_word_is_variable
    
    # last word always has to be a variable. This check happens outside the loop, since the loop only checks with respect to the pervious character.
    # That is, the expression '2+' is valid according to the loop above, but it shouldn't be.
    if operator_match: # last character not allowed to be an operator
      raise SyntaxError(f"Final character of expression is an operator: {word}")

    # Check if all opening brackets are closed.
    rest_of_expression = expression
    next_opening_bracket = rest_of_expression.find('(')
    next_closing_bracket = rest_of_expression.find(')')
    
    while next_opening_bracket != -1 or next_closing_bracket != -1:
      no_closing_bracket = next_opening_bracket != -1 and next_closing_bracket == -1
      no_opening_bracket = next_opening_bracket == -1 and next_closing_bracket != -1
      closing_before_opening = next_closing_bracket < next_opening_bracket
      if no_closing_bracket: # no closing bracket
        raise SyntaxError(f"opening bracket at position {next_opening_bracket} is opened but never closed.")
      if no_opening_bracket or closing_before_opening: # no opening bracket
        raise SyntaxError(f"closing bracket at position {next_closing_bracket} is closed but never opened.")
    
      # this only happens if next_opening_bracket and next_closing_bracket are both != -1
      # Remove the brackets that we just checked from the expression
      rest_of_expression = rest_of_expression[:next_opening_bracket] + rest_of_expression[next_opening_bracket+1:next_closing_bracket] + rest_of_expression[next_closing_bracket+1:]
      next_opening_bracket = rest_of_expression.find('(')
      next_closing_bracket = rest_of_expression.find(')')
    
    # If everything is ok, we parse it.
    return infix_parser.parse_string(expression).asList()[0]
