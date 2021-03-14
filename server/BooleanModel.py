from main import importFromFile ,list_repetition

operators = 'and or not ( )'.split()
proiority = {
    'not' : 3 ,
    'and' : 2 ,
    'or' : 1 ,
    '(' : 0
}

def tokenizeQuery(query :str) :
    return query.replace('(',' ( ').replace(')',' ) ').split()


def toPostfix(tokenized_query):
    stack = []
    postfix = []

    for token in tokenized_query:
        if token not in operators:
            postfix.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')': # right
            operator = stack.pop()
            while operator != '(':
                postfix.append(operator)
                operator = stack.pop()             
        else:
            while (len(stack) != 0) and (proiority[token] <= proiority[stack[-1]]):
                postfix.append(stack.pop())
            stack.append(token)

    while (len(stack) != 0):
        postfix.append(stack.pop())
    return postfix


def answareQuery(query , doc_index):
    tokenized_query = tokenizeQuery(query)
    postfixed_query = toPostfix(tokenized_query) 
    op_size = 2 
    stack = [] 

    for token in postfixed_query:
        if token not in operators:
            stack.append(token)
        else :
            operand1 = stack.pop() if type(stack[-1]) == set else set(doc_index[stack.pop()])
            operand2 = {}
            if token not in ('not') :
                operand2 = stack.pop() if type(stack[-1]) == set else set(doc_index[stack.pop()])
            if token == 'and' :
                stack.append(operand1 & operand2)
            elif token == 'or' :
                stack.append(operand1 | operand2)
            elif token == 'not' :
                # TODO REMOVE HARDCODED 3204 MAX VALUE OF DOCS
                stack.append(set(list(range(1,3204+1))) - operand1)
    return stack.pop()




if __name__ == '__main__':
    # x = tokenizeQuery('A and B or not C and B')

    invertedfile : dict = importFromFile('data/invertedFile.pkl')
    doc_index : dict = importFromFile('data/repetitionList.pkl')
  
    print(sorted(answareQuery('(preliminary or (report and time))' , doc_index)))