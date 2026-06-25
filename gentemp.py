import random
def generatetemp(templa: list, matrix: list, bias: float, debug=False, maxlen=100):
    '''
    Generates an RNA secondary structure template using given parameters.
    Parameters:
    templa (list): The template to append to
    matrix (list): A matrix of probabilities for appending characters based on the previous one
    bias (float): The bias towards ")" (subtracts from matrix[0])
    '''
    tempsum = 1
    while tempsum > 0 and len(templa) <= maxlen:

        if debug:
            print("Before:", templa, tempsum)

        choice = random.random()
        prev = templa[-1]
        p_open = matrix[0] if prev == "(" else matrix[1]
        p_open = max(0, p_open - bias * tempsum)

        if choice < p_open:
            templa.append("(")
            tempsum += 1
        else:
            if prev == "(":
                templa.append("*")
            templa.append(")")
            tempsum -= 1

        if debug:
            print("After:", templa, tempsum)