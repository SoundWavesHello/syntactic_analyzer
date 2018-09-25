Author: Kevin Lane
Syntactic Analysis RD LL(1) Parser


The following program has a function for each of the following processes:

Program --> type main ( ) {Declarations Statements}
Declarations --> {Declaration}
Declaration --> type id (, id)*
Statements --> {Statement}
Statement --> Assignment | printStatement | ifStatement | whileStatement |
              returnStatement
printStatement --> print Expression;
ifStatement --> if (Expression) Statement [else Statement]
whileStatement --> while (Expression) Statement
returnStatement --> return Expression;
Assignment --> id assignOp Expression;
Expression --> Conjunction {|| Conjunction}
Conjunction --> Equality {&& Equality}
Equality --> Relation [equOp Relation]
Relation --> Addition [relOp Addition]
Addition --> Term {addOp Term}
Term --> Factor {multOp Factor}
Factor --> id | intLiteral | boolLiteral | floatLiteral | (Expression)


Notes: The program parses through a list of tokens by starting at the program
       function and consuming tokens that are in the program process, making
       appropriate function calls for declarations and statements.  The same
       process occurs at those functions and so on until all of the tokens are
       parsed through (meaning the program is syntactically correct) or there
       are tokens left.  The latter case means that some tokens were not 
       consumed because they syntactically should be in a different place.
       That triggers the error function.  It was written in Python 3.0 through
       Wing IDE.
