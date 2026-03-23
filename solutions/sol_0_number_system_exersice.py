from math import remainder

valid_digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')


def choose_your_base(base=11):

    '''I Choose Base 11 and I put default value of Base to 11 
       but it will print digits for base 1 to 16'''
    print("Ans 1:")
    print("\tTotal Number of Digits in Base {} : {} ".format(base, valid_digits[0:base]))


def write_number_upto_digits(base=11, digits=3):
    num_list = []
    count = 1
    while count <= digits:
        if count == 1:
            num_list = list(valid_digits[0:base])
        else:
            index = base ** (count - 2)
            index2 = base ** (count - 1)
            for i in range(index, index2):
                for j in range(0, base):
                    num_list.append(str(num_list[i]) + str(num_list[j]))
        count += 1
    print("\nAns 2:")
    print("\tTotal Numbers Count: {} in Base: {} with Digits: {}".format(len(num_list), base, digits))
    print("\tList Of Numbers: {} ".format(num_list))


def convert_number_into_list(num1, num2):
    l1 = [d for d in str(num1)]
    l2 = [d for d in str(num2)]
    return l1, l2


def convert_number_of_equal_length(l1, l2):
    diff = abs(len(l1) - len(l2))
    if len(l1) > len(l2):
        l2 = ['0'] * diff + l2
    elif len(l2) > len(l1):
        l1 = ['0'] * diff + l1

    return l1, l2


def convert_numbers_a_to_f(l1, l2, base):
    for i in range(len(l1)-1,-1,-1):
        if l1[i] not in valid_digits[0:base]:
            print("Invalid Number", ''.join(l1))
            exit
        elif l2[i] not in valid_digits[0:base]:
            print("Invalid Number", ''.join(l2))
            exit

        # Convert A -> 10, B -> 11, C-> 12 and so on
        if valid_digits.index(l1[i]) > 9:
            l1[i] = valid_digits.index(l1[i])

        if valid_digits.index(l2[i]) > 9:
            l2[i] = valid_digits.index(l2[i])
    return l1, l2


def add_two_numbers_in_your_base(num1, num2, base=11, caller=None):
    l1, l2 = convert_number_into_list(num1, num2)
    l1, l2 = convert_number_of_equal_length(l1, l2)
    l1, l2 = convert_numbers_a_to_f(l1, l2, base)
    result = []

    carry = 0
    for i in range(len(l1)-1,-1,-1):
        sum = carry + int(l1[i]) + int(l2[i])
        carry = sum // base
        result = [valid_digits[sum % base]] + result

    if caller:
        return ''.join(result)
    print("\nAns 3:")
    print("\tSum of {} + {} in base {} is : {}".format(num1, num2, base, ''.join(result)))


def subtract_two_numbers_in_your_base(num1, num2, base=11):
    l1, l2 = convert_number_into_list(num1, num2)
    l1, l2 = convert_number_of_equal_length(l1, l2)
    l1, l2 = convert_numbers_a_to_f(l1, l2, base)
    result = []

    borrow = 0
    #Check if any digit is invalid then exit

    for i in range(len(l1)-1,-1,-1):
        if int(l1[i]) - borrow < int(l2[i]):
            sub = base + int(l1[i]) - int(l2[i]) - borrow
            borrow = 1
        else:
            sub = int(l1[i]) - int(l2[i]) - borrow
            borrow = 0
        result = [valid_digits[sub]] + result
    print("\nAns 4:")
    print("\tSubtraction of {} - {} in base {} is : {}".format(num1, num2, base, ''.join(result)))



def multiplication_table(base=11):
    base_digits = [i for i, _ in enumerate(valid_digits[0:base])]
    result = [[None for _ in range(base)] for _ in range(base)]

    for i in base_digits:
        for j in base_digits:
            mul = i * j
            quotient = mul // base
            remain = mul % base

            if quotient > 9:
                quotient = valid_digits[quotient]
            if remain > 9:
                remain = valid_digits[remain]
            result[i][j] = str(quotient) + str(remain)
    print("\nAns 5:")
    print("\tMultiplication Table of base {} is :\n".format(base))
    for row in result:
        print("\t", row)


def multiplication_two_digit_numbers(num1, num2, base=11):
    l1, l2 = convert_number_into_list(num1, num2)
    l1, l2 = convert_numbers_a_to_f(l1, l2, base)

    count = 0
    num = [0] * 5
    for x in l1[::-1]:
        result = ['0'] * count
        carry = 0
        for y in l2[::-1]:
            mul = int(x) * int(y) + carry
            carry = mul // base
            mod = mul % base
            result = [valid_digits[mod]] + result
        if carry > 0:
            result = [str(carry)] + result
        num[count] = ''.join(result)
        count += 1
    result = add_two_numbers_in_your_base(num[0], num[1], base, caller='mul')
    print("\nAns 5:")
    print("\t Multiplication of {} & {} in base {} is : {}".format(num1, num2, base, result))


def my_sqrt(num):
    low = 1
    high = (num/2) + 1

    guess = (high + low) / 2

    while round((guess*guess), 30) != num:
        print(low, high, guess, guess*guess, num)
        if guess*guess < num:
            low = guess
        else:
            high = guess
        guess = (high + low) / 2

    print(low, high, guess, guess*guess, num)



def my_cuberoot(num):
    low = 1
    high = (num/2) + 1

    guess = (high + low) / 2

    while round((guess**3), 30) != num:
        print(low, high, guess, guess**3, num)
        if guess**3 < num:
            low = guess
        else:
            high = guess
        guess = (high + low) / 2

    print(low, high, guess, guess**3, num)

# choose_your_base(base=11)
# write_number_upto_digits(base=11, digits=3)
# add_two_numbers_in_your_base('2A','7A', base=11)
# subtract_two_numbers_in_your_base('3AA', '2AA', base=11)
# multiplication_table(base=11)
# multiplication_two_digit_numbers('1A', '19', base=11)
# my_sqrt(67)
my_cuberoot(343)

