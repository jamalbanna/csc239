import re

#list to keep track of ids 
identifiers_list = []

#error logs list
errors_list = []

#Classifies a given token into its category (keyword, operator, separator, numeric, boolean, string, identifier)
#Preconditions: token is a string 
#Postconditions: returns a string of (keyword, operator, separator, numeric, boolean, string, identifier)
def classifyToken(token):

    keywords = ['if', 'else', 'return', 'int', 'float', 'String' , 'Boolean']
    operators = ['+','-', '*', '/', '=', '==', '!=', '>','<','%']
    separators = ['(',')', '{', '}', ',' , ';']
    boolea = ['True', 'False']
    
    #Token classification
    if token in keywords:
        return 'keyword'
    elif token in operators:
        return 'operator'
    elif token in separators:
        return 'seperator'
    elif bool(re.fullmatch(r'[+-]?(\d+(\.\d*)?|\.\d+)', token)):
        return 'numeric'
    elif token in boolea:
        return 'boolean'
    elif (token.startswith('"') and token.endswith('"')):
        return 'string' 
    else:
        identifiers_list.append(token)
        return 'identifier'

#Checks for unmatched parentheses 
#Preconditions: code is in string format and read corrrectly
#Postconditions: adds error to error_list if unmatched brackets are found
def hasUnmatchedParentheses(s):
    stack = []

    # Parentheses matching logic
    for char in s:
        if char == '{' or char == '(':
            stack.append(char)
        elif char == '}' or char == ')':
            if len(stack) == 0:
                errors_list.append("Unmatched parantheses.")
            top_element = stack.pop() 
            if top_element == '{' and char != '}':
                errors_list.append("Unmatched parantheses.")
            elif top_element == '(' and char != ')':
                errors_list.append("Unmatched parantheses.")
    if len(stack) != 0:
        errors_list.append("Unmatched parantheses.")

# Get the filepath and read code content
filepath = input('Enter file path with extension (filepath.txt): ')
file = open(filepath, "r")
code = file.read()

# Reference: https://www.w3schools.com/python/python_regex.asp
# Finding strings based on the regex
strings = re.findall(r'"(.*?)"', code)
#adding quotations
for i in range(len(strings)):
    strings[i] = '"' + strings[i] + '"'

specialCharacters = ['{','}', ';', ',' , '(', ')' ,'+', '-', '*', '/', '==', '!=','>','<', '%', '=']
openedQuotation = False
filteredInput = ''

# Parsing and filtering input
for ch in code:
    if ch == '"':
        openedQuotation = not openedQuotation
        continue
    if openedQuotation:
        continue
    else:
        if ch in specialCharacters:
            filteredInput += ' ' + ch + ' '
        else:
            filteredInput += ch   

# Tokenize and classify tokens
tokens = filteredInput.split() + strings
tokensDict = {}
for token in tokens:
    temp = classifyToken(token)
    tokensDict[token] = classifyToken(token)

# Read lines for further processing 
lines = []
with open(filepath, 'r') as file:
    for line in file:
        lines.append(line.strip())

filteredLines = []
openedQuotation = False
for line in lines:
    tempLine = ''
    for ch in line:
        #if opening quotation add space before it, else if closing add space after it
        if ch == '"':
            openedQuotation = not openedQuotation
            if openedQuotation:
                tempLine += ' ' + ch
            else:
                tempLine += ch + ' ' 
        elif openedQuotation:
            tempLine += ch
        else:
            #add space before and after special characters
            if ch in specialCharacters:
                tempLine += ' ' + ch + ' '
            else:
                tempLine += ch  
    filteredLines.append(tempLine) 

# Keep unique ids only
identifiersDict = set(identifiers_list)

# Lists to categorize variable types
int_ids_list = []
float_ids_list = []
string_ids_list = []
boolean_ids_list = []

# Extracts and returns the first identifier found in a line of code.
# Preconditions:line is a string
# Postconditions: Returns the first identifier found in the line if present; otherwise, returns None.
def getId(line):
    tempTokens = line.split()
    for token in tempTokens:
        if classifyToken(token) == 'identifier':
            return token



#Checks for common syntax errors in code lines
# Preconditions: filteredLines is a list of strings of code lines
# Postconditions: Errors detected are appended to errors_list
def hasInvalidSyntax():

    ifStatementPattern = r'^\s*if\s*\(.+\)\s*\{'
    elseStatementPattern =  r'^\s*\}?\s*else\s*\{'
    returnPattern = r'^\s*return\s+([a-zA-Z_]\w*|\d+|".?"|\'.?\')\s*;?\s*$'
    intPattern = r'\s*int\s+([a-zA-Z_]\w*)\s*(=\s*([a-zA-Z_]\w*|[-+]?\d+))?\s*;'
    floatPattern = r'\s*float\s+([a-zA-Z_]\w*)\s*(=\s*([a-zA-Z_]\w*|[-+]?\d*\.\d+f?))?\s*;'
    booleanPattern = r'\s*boolean\s+([a-zA-Z_]\w*)\s*(=\s*([a-zA-Z_]\w*|true|false))?\s*;'
    stringPattern = r'\s*String\s+([a-zA-Z_]\w*)\s*(=\s*([a-zA-Z_]\w*|"(?:\\.|[^"\\])*"))?\s*;'

    for line in filteredLines:
        intCounter = 0
        stringCounter = 0
        booleanCounter = 0
        floatCounter = 0
        tempTokens = line.split()

        # Syntax checking for if, else, return, and variable declarations
        if 'if' in line:
            if re.match(ifStatementPattern, line):
                pass
            else:
                errors_list.append( 'Incorrect if statement syntax: ' + line)
                continue
            
        elif 'else' in line:
            if re.match(elseStatementPattern, line):
                pass
            else:
                errors_list.append('Incorrect else statement syntax: ' + line)
                continue
        
        elif 'return' in line:
            if re.match(returnPattern, line):
                pass
            else:
                errors_list.append('Incorrect return statement syntax: ' + line)
                continue
            
        elif 'int ' in line:
            int_ids_list.append(getId(line))
            if re.match(intPattern, line):
                pass
            else:
                errors_list.append('Incorrect int syntax: ' + line)
                continue
              
        elif 'float ' in line:
            float_ids_list.append(getId(line))
            if re.match(floatPattern, line):
                pass
            else:
                errors_list.append('Incorrect float syntax: ' + line)
                continue    
            
        elif 'boolean ' in line:
            boolean_ids_list.append(getId(line))
            if re.match(booleanPattern, line):
                pass
            else:
                errors_list.append('Incorrect Boolean syntax: ' + line)
                continue
           
        elif 'String ' in line:
            string_ids_list.append(getId(line))
            if re.match(stringPattern, line):
                pass
            else:
                errors_list.append('Incorrect String syntax: ' + line)
                continue
           
        # Type mismatch checking 
        if '=' in line:
            words = line.split()
            for word in words:
                if word in int_ids_list:
                    intCounter += 1
                elif word in float_ids_list:
                    floatCounter += 1
                elif word in string_ids_list:
                    stringCounter += 1
                elif word in boolean_ids_list:
                    booleanCounter += 1
            if max(intCounter,floatCounter,stringCounter,booleanCounter) != (intCounter + floatCounter + stringCounter + booleanCounter):
                errors_list.append('Type mismatch: ' + line)


# Validates identifier names based on naming conventions (starts with a letter, '$', or '_').
# Preconditions: identifiersDict exists
# Postconditions: Invalid identifiers are appended to errors_list
def hasInvalidIdentifiers():
    for id in identifiersDict:
        if id[0] == '$' or id[0] == '_' or id[0].isalpha() : 
            continue
        else:
            errors_list.append('Invalid identifier: ' + id)

# Checks for unrecognized characters in identifiers.
# Preconditions: identifiersDict exists
# Postconditions: Invalid identifiers are appended to errors_list
def hasInvalidCharacters():
    for id in identifiersDict:
        if bool(re.fullmatch(r'^[\$a-zA-Z0-9_\.]+$', id)) : 
            continue
        else:
            errors_list.append('Invalid character ' + id)

# Validates operator usage to avoid consecutive operators or hanging operators before semicolons
# Preconditions: filteredLines is a list of strings 
# Postconditions:Lines with invalid operator usage are appended to errors_list
def hasInvalidOperatorUsage():
    for line in filteredLines:
        if has_incorrect_operator_usage(line):
            errors_list.append('Invalid operator usage ' + line)
    return False

# Identifies incorrect operator usage, such as consecutive operators or trailing operators before a semicolon.
# Preconditions: statement is a string representing a line
# Postconditions: Returns True if incorrect operator usage is found; otherwise, False
def has_incorrect_operator_usage(statement):
    # Regex patterns to catch common incorrect operator usage
    incorrect_patterns = [
        r'[+\-*/%]\s*[+\-*/%](?!=)',  # Two arithmetic operators in a row, like x + * y
        r'[+\-*/]\s*;',               # Hanging operator before semicolon, like x + ;
    ]
    for pattern in incorrect_patterns:
        if re.search(pattern, statement):
            return True  # Incorrect operator usage found
    return False  # No incorrect operator usage found

#print tokens in needed format
print("tokens:")
for key, value in tokensDict.items():
    print(f"('{key}', '{value}')")


# calls functions for checks
# Preconditions: functions exists
# Postconditions: Errors are appended to errors_list, prints errors if they exist
def checks():
    hasUnmatchedParentheses(code)
    hasInvalidSyntax()
    hasInvalidIdentifiers()
    hasInvalidCharacters()
    hasInvalidOperatorUsage()

    for error in errors_list:
        print(error)

checks()



    








