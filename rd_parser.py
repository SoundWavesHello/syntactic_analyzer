"""
Author: Kevin Lane
Syntactic Analysis - RD LL(1) parser
Last Modified: 10/19/17


Input: A text file where each line has a token and the corresponding lexeme
Output: True if and only if no syntax errors; otherwise returns error and
        error location
        
"""




def main():
    
    # get the filename
    filename = input("Please type in a filename: ")
    
    iNextToken = 0 #Next token index
    tokenStream = [] # creates a stream of tokens to parse
    lexemeStream = [] # creates a stream of lexemes

    # Read in the file to fill in token and lexeme streams
    infile = open(filename, "r")
    myStr = infile.read() # a string of the whole file
    myList = myStr.split() # splits the string into tokens and lexemes
    tokenStream = myList[0::2] # list of tokens (even elements from myList)
    lexemeStream = myList[1::2] # list of lexemes (odd elements from myList)

    print("Tokens:", tokenStream)
    print("Lexemes:", lexemeStream)
    
    
    #Start at the start symbol Program
    result = program(iNextToken, tokenStream)
    
    iNextToken = result[0]
    errorPresent = result[1]
    
    if iNextToken < len(tokenStream) or errorPresent:
        error(iNextToken, tokenStream, lexemeStream) 
        # program should go through everything that is syntactically 
        #correct, if there's anything left, then it is an error
        # iNextToken will also stop where it can no longer consume
        # any more tokens, so iNextToken will point to the error location
    else:
        print("Syntactically correct!")


def program(iNextToken, tokenStream):
    
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "type"):
        iNextToken += 1 #consume the 'type'
    
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "main"):
        iNextToken += 1 #consume the 'main'
    
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "("):
        iNextToken += 1 #consume the '('

    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ")"):
        iNextToken += 1 #consume the ')'
        
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "{"):
        iNextToken += 1 #consume the '{'
    else:
        # if any of the above 5 tokens are not present in this order
        # then, not syntactically correct; prematurely return iNextToken
        # to avoid unecessarily checking declarations and statements
        return iNextToken
    
    iNextToken = declarations(iNextToken, tokenStream) #consume the declarations
    result = statements(iNextToken, tokenStream) # consume the statements
    iNextToken = result[0]
    errorPresent = result[1]
    
    # This is the only token that can be syntactically wrong without being 
    # caught by just looking at if iNextToken < len(tokenStream); if it is
    # missing, then iNextToken wouldn't be less than len(tokenStream).  For all
    # other tokens, this doesn't matter, as the parser would get stopped at the
    # next token and register as an error
    
    if errorPresent:
        return (iNextToken, errorPresent)
    
    elif iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "}"):
        iNextToken += 1 #consume the '}'
    
    else:
        errorPresent = True
        
    return (iNextToken, errorPresent)
    

def declarations(iNextToken, tokenStream):

    # check if the current token starts a declaration, keeping in mind that 
    # declarations start with 'type'; if that's the case then keep looking for
    # more declarations
    while iNextToken < len(tokenStream) and \
          tokenStream[iNextToken] == "type":
        iNextToken = declaration(iNextToken, tokenStream)
    return iNextToken # allows higher functions to keep track of NextToken index


def declaration(iNextToken, tokenStream):
    # consume 'type'
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "type"):
        iNextToken += 1
    
    # consume 'id'
    if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id"):
        iNextToken += 1    
    
    # while there are still more ids to follow (indicated by a comma)
    while iNextToken < len(tokenStream) and (tokenStream[iNextToken] == ","):
        iNextToken += 1 #consume the comma
        
        if iNextToken < len(tokenStream) and (tokenStream[iNextToken] == "id"):
            iNextToken += 1 #consume the 'id'        
    
    # consume the following semi-colon
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == ";":
        iNextToken += 1
    
    return iNextToken # allow functions to keep track of nextToken index


def statements(iNextToken, tokenStream):

    # while there are are more statements left; excecute
    # look if there are more statements left by looking for "print", "if", 
    # "while", "return", or "id"
    while iNextToken < len(tokenStream) and (\
        tokenStream[iNextToken] == "print" or\
        tokenStream[iNextToken] == "if" or\
        tokenStream[iNextToken] == "while" or\
        tokenStream[iNextToken] == "return" or\
        tokenStream[iNextToken] == "id"):
        result = statement(iNextToken, tokenStream)
        iNextToken = result[0]
        errorPresent = result[1]
    return (iNextToken, errorPresent)


def statement(iNextToken, tokenStream):

    # only want to check one statement at a time, so use conditional
    # if it is 
    
    # check if it is an assignment statement
    if tokenStream[iNextToken] == "id":
        return assignment(iNextToken, tokenStream)
    # check if print statement
    elif tokenStream[iNextToken] == "print":
        return printStatement(iNextToken, tokenStream)
    # check if if statement
    elif tokenStream[iNextToken] == "if":
        return ifStatement(iNextToken, tokenStream)
    # check if while statement
    elif tokenStream[iNextToken] == "while":
        return whileStatement(iNextToken, tokenStream)
    # check if return statement
    elif tokenStream[iNextToken] == "return":
        return returnStatement(iNextToken, tokenStream)
    
    errorPresent = False
    # if it is not a statement, don't consume the token
    return (iNextToken, errorPresent)
    

def printStatement(iNextToken, tokenStream):

    # consume the 'print' token
    if iNextToken < len(tokenStream) and tokenStream[iNextToken] == "print":
        iNextToken += 1
    
    # check the expression statement
    iNextToken = expression(iNextToken, tokenStream)    
    
    # consume the semicolon
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == ";":
        iNextToken += 1    
    
    errorPresent = False    
    return (iNextToken, errorPresent)


def ifStatement(iNextToken, tokenStream):

    # consume the 'if' token
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == "if":
        iNextToken += 1    
    
    # consume the '('
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == "(":
        iNextToken += 1    

    # check for an expresion
    iNextToken = expression(iNextToken, tokenStream)
    
    # consume the ')'
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == ")":
        iNextToken += 1
        
    # check for a statement
    iNextToken = statement(iNextToken, tokenStream)
    
    # check to see if there is an else; if so, there's another statement
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == "else":
        iNextToken += 1 # consume the 'else' token
        # check the next statement
        iNextToken = statement(iNextToken, tokenStream)
        
    errorPresent = False    
    return (iNextToken, errorPresent)


def whileStatement(iNextToken, tokenStream):
    
    # consume the 'while' token
    if iNextToken < len(tokenStream) and \
           tokenStream[iNextToken] == "while":
            iNextToken += 1    
    # consume the '('
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == "(":
        iNextToken += 1    
            
    # check the expression
    iNextToken = expression(iNextToken, tokenStream)
                
    # consume the ')'
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == ")":
        iNextToken += 1
        
    # check the statement
    iNextToken = statement(iNextToken, tokenStream)
        
    errorPresent = False    
    return (iNextToken, errorPresent)


def returnStatement(iNextToken, tokenStream):
    
    # consume the "return" token
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == "return":
        iNextToken += 1        
    
    #check the expression
    iNextToken = expression(iNextToken, tokenStream)
    
    # consume the semicolon
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == ";":
        iNextToken += 1        
    else:
        errorPresent = True
    return (iNextToken, errorPresent)


def assignment(iNextToken, tokenStream):
    
    # check the id
    if iNextToken < len(tokenStream) and \
       (tokenStream[iNextToken] == "id"):
        iNextToken += 1    
    
    # check the assignOp
    if iNextToken < len(tokenStream) and \
       (tokenStream[iNextToken] == "assignOp"):
        iNextToken += 1    
    
    # check the expression
    iNextToken = expression(iNextToken, tokenStream)
    
    # consume the semicolon
    if iNextToken < len(tokenStream) and \
       tokenStream[iNextToken] == ";":
        iNextToken += 1    
        
    return iNextToken



def expression (iNextToken, tokenStream):
    # check the conjunction
    iNextToken = conjunction(iNextToken, tokenStream)
    
    # check if there are more conjunctions left by looking at the '||' token
    while(iNextToken < len(tokenStream) and tokenStream[iNextToken] == "||"):
        iNextToken += 1 # consume the or token
        
        #check the next conjunction
        iNextToken = conjunction(iNextToken, tokenStream)
        
    return iNextToken


def conjunction(iNextToken, tokenStream):
    # check the equality
    iNextToken = equality(iNextToken, tokenStream)
    
    # check for more equalities by looking at the '&&' token
    while(iNextToken < len(tokenStream) and tokenStream[iNextToken] == "&&"):
        iNextToken += 1 # consume the && token
        
        # check the next equality
        iNextToken = equality(iNextToken, tokenStream)
    return iNextToken


def equality(iNextToken, tokenStream):
    # check the first relation
    iNextToken = relation(iNextToken, tokenStream)
    
    # check if there is another relation
    if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "equOp"):
        iNextToken += 1 # consume the 'equOp'
        iNextToken = relation(iNextToken, tokenStream) # consume the relation
        
    return iNextToken


def relation(iNextToken, tokenStream):
    # check the first addition
    iNextToken = addition(iNextToken, tokenStream)
    
    # check if there is another addition
    if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == "relOp"):
        iNextToken += 1 # consume the 'addOp'
        iNextToken = addition(iNextToken, tokenStream) # consume the relation
        
    return iNextToken



def addition(iNextToken, tokenStream):
    # check the first term
    iNextToken = term(iNextToken, tokenStream)
    
    # check if there are more terms by looking for a "addOp"
    while(iNextToken < len(tokenStream) and tokenStream[iNextToken] == "addOp"):
        iNextToken += 1 # consume the "addOp"
        
        # check the next term
        iNextToken = term(iNextToken, tokenStream)
    return iNextToken


def term(iNextToken, tokenStream):
    # check the first factor
    iNextToken = factor(iNextToken, tokenStream)
    
    # check if there are more factors by looking for a "multOp"
    while(iNextToken < len(tokenStream) and \
          tokenStream[iNextToken] == "multOp"):
        iNextToken += 1 # consume the "multOp"
        
        # check the next factor
        iNextToken = factor(iNextToken, tokenStream)

    return iNextToken


def factor(iNextToken, tokenStream):
    
    # check if the factor is an id, int, bool, float, or id
    if iNextToken < len(tokenStream) and \
       (tokenStream[iNextToken] == "id" or 
        tokenStream[iNextToken] == "intLiteral" or \
        tokenStream[iNextToken] == "boolLiteral" or \
        tokenStream[iNextToken] == "floatLiteral" or \
        tokenStream[iNextToken] == "charLiteral"):
        iNextToken += 1
    # check if the factor is an expression enclosed by parantheses
    elif iNextToken < len(tokenStream) and tokenStream[iNextToken] == "(":
        iNextToken += 1 # consume the parantheses
        
        # check if the next token is an expression
        if (iNextToken < len(tokenStream) and \
            expression(iNextToken, tokenStream) - iNextToken != 0):
            iNextToken = expression(iNextToken, tokenStream)
        
        # consume the ')'
        if (iNextToken < len(tokenStream) and tokenStream[iNextToken] == ")"):
            iNextToken += 1
        
    return iNextToken
     
        
def error(iNextToken, tokenStream, lexemeStream):
    # if there are any tokens left, then point to error location
    if iNextToken < len(tokenStream):
        print("Error: Invalid expression. Error location: <",\
            tokenStream[iNextToken], ",", lexemeStream[iNextToken], ">.")
    # if there are no tokens left, it must be expecting more terms
    else:
        print("Error: Incomplete expression. Expecting more terms.")

main()