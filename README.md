# SBML
SBML description:

SBML Datatypes:
Numbers: Integers and Reals – implement as Python integers and floats.

Booleans: True and False – implement as Python Booleans.

Strings: Sequences of characters enclosed within matching single or double quotes in a single line. Strings should be implemented using the equivalent Python String type.

List: Finite, ordered sequence of elements separated by commas and enclosed within matching square brackets. Elements of the list need not be of the same type. Implement as Python list.

Tuple: Finite, ordered sequence of elements separated by commas and enclosed within matching parentheses. Elements of the tuple need not be of the same type. SBML Literal Representation of Data Types:

Integer: Positive (no sign) or negative (unary -) whole numbers in base-10 representation (decimal representation). An integer literal is one or more digits, 0-9. Examples: 57, -18, 235

Real: A real value is represented by 0 or more digits (0-9), followed by a decimal point, ".", followed by 0 or more digits (0-9), except that a decimal point by itself with no leading or trailing digit is not a real. Examples: 3.14159, 0.7, .892, 32787. A real can also contain exponents as in scientific notation. In this case, a real value, as defined above, is followed by an "e" character and then a positive or negative integer, as defined above. Examples: 6.02e-23, 17.0e4

Boolean: True, False (just as in Python)

String: A string literal begins with a single or double quote, followed by zero or more non-quote characters, and ends with a matching quote. The value of the string literal does not include the starting and ending quotes. Examples: "Hello World!", "867-5309"

List: A list literal is composed by a left square bracket, followed by a comma-separated sequence of zero or more expressions, followed by a right square bracket. Examples: ["a", "b"], [1, 2], [307, "307", 304+3]



SBML Operators:

Operator precedence and associativity is given below.

01. ( expression ) – A parenthesized expression
02. ( expression1, expression2, … ) – Tuple constructor A singleton tuple can be constructed by including a comma after the expression. E.g., ( expression1, ) There are no empty tuples
03. #i(tuple) – returns the argument at index i in the tuple. Indices start at 1 as in SML.
04. a[b] – Indexing Operation. b can be any expression.
05. a ** b – Exponentiation. base a raised to the power b. right associative: 2\**3\**4 == 2\**(3\**4)
06. a * b – Multiplication. Overloaded for integers and reals.
07. a / b – Division. Overloaded for integers and reals, but result is always a real value. 
08. a div b – Integer Division. Returns just the quotient. a and b are integers.
09. a mod b – Modulus. Divides a by b and returns just the remainder. a and b are integers.
10. a + b – Addition. Overloaded for integers, reals, strings, and lists.
11. a – b – Subtraction. Overloaded for integers and reals.
12. a in b – Membership. Evaluates to True if it finds the value of a inside the string or list represented by b.
13. a::b – Cons. Adds operand a to the front of the list referred to by operand b.
14. not a – Boolean negation.
15. a andalso b – Boolean Conjunction (AND)
16. a orelse b – Boolean Disjunction (OR)
17. a < b – Less than. Comparison.
18. a <= b – Less than or equal to. Comparison.
19. a == b – Equal to. Comparison.
20. a <> b – Not equal to. Comparison.
21. a >= b – Greater than or equal to. Comparison.
22. a > b – Greater than. Comparison. 

SBML Operator Precedence: 
Operator Precedence for SBML (ordered from lowest to highest): All operators are left-associative, except for exponentiation (\**) and cons (::), which are right associative Operators on the same line have the same precedence. 

01. orelse Boolean Disjunction
02. andalso Boolean Conjunction
03. not Boolean Negation
04. <, <=, ==, <>, >=, > Comparison Operators (for numbers and strings)
05. h::t Cons operator
06. in Membership test
07. +, - Addition and Subtraction(Overloaded for numbers, strings, lists)
08. *, /, div, mod Multiplication, Division, Integer Division, Modulus
09. ** Exponentiation
10. a[b] Indexing
11. #i(tuple) Tuple Indexing
12. (exp1, exp2,...) Tuple Creation
13. (exp) Parenthetical Expression

SMBL Operator Semantics:

Indexing: Operand a must be either a string or a list. Operand b must be an integer. If a is a string, then return the b-th character as a string. If a is a list, then return the b-th element as an instance of whatever type it is. The index is 0-based. If the index is out of bounds, then this is a semantic error.

Addition: Operands must either both be numbers, or both be strings, or both be lists. If they are integers or reals, then addition with standard (Python) semantics is performed. If a and b are both strings, then string concatenation is performed. If a and b are both lists, then list concatenation is performed.

Subtraction: Operands must both be integers or reals. Performed using standard subtraction semantics.

Multiplication: Operands must both be integers or reals. Performed using standard multiplication semantics. 

Division: Operands must both be integers or reals. Operand b cannot be 0. Performed using standard division semantics.

Booleans: Operands for Boolean operations (not, andalso, orelse) must be Boolean values.

Comparisons: Operands must either both be numbers or both be strings. Comparison of numbers (integers and strings) should follow standard semantics. Comparison of strings should follow the Python semantics. Returns True if comparison is true, and False if comparison is False. 


Variables and Assignment:

All variable names begin with an ASCII character, which may be followed by zero or more ASCII characters, digits, or underscores. A regular expression to match this definition of variable names is: "[a-zA-Z][a-zA-Z0-9_]*" Expressions from the previous homework (HW 03) must be extended in the following two ways:

1. Support for assignment to variables must be added. For example, "x = 1;". This will include assignment to indexed list variables. For example, if we have performed the assignment "array = [1, 2, 3];", and then perform the assignment "array[2] = 5", then the list stored in "array" should now contain [1, 2, 5].

2. Support must be added for variables used in expressions. For example, if x was assigned 1, then "print(x);" will print 1. Similarly, we should evaluate indexed variables if they occur in a place where their value is needed. For example, if array was assigned the list [1, 2, 5], then "print(array[0] + array[1] +
array[2]);" should print 8. 
Evaluating a variable for its value should have the following behavior. If the variable has had a value assigned to it, then the value should be returned. Otherwise, a "Semantic Error" should be reported and your program should stop. When an indexed list variable is used in an expression, then both the list and the index are evaluated to their value, and then the indexed list expression is evaluated. If the variable is not a list (or a string), or the index is not an integer, then a Semantic Error should be reported. If the index is outside the bounds of the list, then a Semantic Error should be reported.

New Statement Types:

1. Block: A block statement consists of zero or more statements enclosed in curly-braces, "{…}". When the block executes, each of the statements is executed in sequential order.

2. Assignment: an assignment statement consists of an expression, an equals sign, an expression, and a semicolon, "exp1 = exp2;". When the assignment statement executes the lefthand side expression is assigned the value evaluated for the right-hand side expression.

3. Print: a print statement consists of the "print" keyword, a left parenthesis, an expression, a right parenthesis, and then a semicolon. When the statement executes, the expression is evaluated for its value. The output displayed should be the same as that produced by Python for that value.

For example,
>>> print('a')
a
>>> print(['a'])
['a']
>>> print(1 < 2)
True 

4. Conditional Statements: 

A. If Statements: Consist of a keyword "if", a left parenthesis, an expression, a right parenthesis, and a block statement as the body of the If statement. When the If statement executes, if the expression evaluates to True, then the block statement composing the body is executed. 

B. If-Else Statements: Consist of a keyword "if", a left parenthesis, an expression, a right parenthesis, a block statement as the body of the If clause, the keyword "else", and a bloc statement as the body of the Else clause. When the IF-Else statement executes, if the expression is True, then execute the block statement that is the body of the If clause. Otherwise, execute the block statement that is the body of the Else clause.

5. Loop Statements:

A. While Loops: A While statement consists of the keyword "while", a left parenthesis, an expression, a right parenthesis, and a block statement that is the body of the While statement. Executing the while statement begins by evaluating the condition expression for its value. If the expression evaluates to False, then the While statement terminates. Otherwise, execute the block of statements that compose the body of the While statement, and then repeat the execution of the While statement from the evaluation of the condition expression. 


Function Definition: A function definition begins with the keyword "fun", followed by the name of the function, a left parenthesis, variables representing formal parameters separated by commas, a right parenthesis, an equal sign, a block, and then an expression. When the function is called, the block is executed first. Then
the expression is evaluated and the result of the expression evaluation is returned to the caller.

Function Call: A function call is an expression. The function name is followed by a left parenthesis, and then argument expressions, followed by a right parenthesis. The number of arguments passed to the call must match the number of parameters in the function definition. 
