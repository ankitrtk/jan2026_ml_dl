def factorial_recursive(n):
    if n==1 or n==0:
        return 1
    else:
        return n*factorial_recursive(n-1)


def multiply_recursive(a, b):
    if b == 0:
        return 0
    else:
        if (a < 0 and b > 0) or (a > 0 and b < 0):
            a = abs(a)
            b = abs(b)
            return - (a + multiply_recursive(a, b-1))
        else:
            a = abs(a)
            b = abs(b)
            return a + multiply_recursive(a, b-1)


def power(a, b):
    if b == 0:
        return 1
    else:
        return a * power(a, b-1)


def compute_power(a, b):
    if b == 0:
        return 1
    else:
        if b < 0:
            return 1/(a * compute_power(a, abs(b)-1))
        else:
            return a * compute_power(a, b-1)


def recursive_divide(a, b):
    if b == a:
        return (1, 0)
    elif b > a:
        return (0, a)
    else:
        return tuple(a + b for a, b in zip([1, 0], recursive_divide(a-b, b)))



def compute_hcf(a, b):
    if b == 0:
        return a
    else:
        return compute_hcf(b, a%b)



def print_move(start, end):
    tower_list = ['A', 'B', 'C']
    print("Moving from {} -> {}".format(tower_list[start-1], tower_list[end-1]))


def solve_hanoi(n, start=1, end=3):
    if n == 1:
        #print_move(start, end)
        print("Moving from {} -> {}".format(start, end))
    else:
        other = 6 - (start + end)
        solve_hanoi(n-1, start, other)
        #print_move(start, end)
        print("Moving from {} -> {}".format(start, end))
        solve_hanoi(n-1, other, end)



if __name__ == "__main__":
    # print(factorial_recursive(5))  # Output: 120
    # print(factorial_recursive(3))  # Output: 6
    # print(factorial_recursive(0)) # Output: 1
    # print(factorial_recursive(1)) # Output: 1
    # print(multiply_recursive(-4, -5))
    # print(multiply_recursive(4, 3))   # Output: 12
    # print(multiply_recursive(5, 0))     # Output: 0
    # print(multiply_recursive(7, -2))    # Output: -14
    # print(multiply_recursive(-3, -3))   # Output: 9
    # print(power(9, 3))
    # print(power(2, 3))   # Output: 8
    # print(power(5, 2))   # Output: 25
    # print(compute_power(2, 3))   # Output: 8
    # print(compute_power(2, -3))  # Output: 0.125
    # print(compute_power(3, -3))
    # print(compute_power(5, 0))   # Output: 1
    # print(recursive_divide(17, 5))   # Output: (3, 2)
    # print(recursive_divide(20, 4))   # Output: (5, 0)
    # print(recursive_divide(7, 3))    # Output: (2, 1)
    # print(recursive_divide(0, 1))    # Output: (0, 0)
    # print(compute_hcf(12, 18))     # Output: 6
    # print(compute_hcf(100, 25))    # Output: 25
    # print(compute_hcf(17, 13))     # Output: 1
    # print(compute_hcf(0, 5))       # Output: 5
    solve_hanoi(3)