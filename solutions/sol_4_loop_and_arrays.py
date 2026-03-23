from functools import reduce
from sol_3_recursion import *

def find_min_max(arr):
    min_val = reduce(lambda x,y:x if x < y else y, arr)
    max_val = reduce(lambda x,y:x if x > y else y, arr)
    return min_val, max_val


def min_max_normalize(value, data):
    min_val, max_val = find_min_max(data)
    return (value-min_val)/(max_val-min_val)


def compute_mean(data):
    if len(data) == 0:
        return 0
    return reduce(lambda x,y:x+y, data)/len(data)


def compute_sd(data):
    if len(data) == 0:
        return 0

    mean = compute_mean(data)
    new_data = list(map(lambda x: (x - mean)**2, data))
    new_mean = compute_mean(new_data)
    sd = new_mean ** 0.5
    return sd


def find_outliers(data, threshold):
    mean = compute_mean(data)
    sd = compute_sd(data)

    outliers = list(filter(lambda x: ((x-mean)/sd) > threshold, data))
    return outliers


def compute_iqr(data):
    percentile_25 = int(len(data)*0.25)
    percentile_75= int(len(data)*0.75)

    iqr = data[percentile_75] - data[percentile_25]
    return iqr


def standardize(data):
    mean = compute_mean(data)
    sd = compute_sd(data)
    print(mean, sd)

    stand_data = list(map(lambda x:(x-mean)/sd if sd != 0 else 0, data))
    return stand_data


def compute_rmse(actual, predicted):
    new_data = list(map(lambda x,y:(x-y)**2, actual, predicted))
    mean = compute_mean(new_data)
    rmse = mean ** 0.5
    return rmse


def compute_mae(actual, predicted):
    if isinstance(actual[0],(int, float)):
        new_data = list(map(lambda x,y:abs(x-y), actual, predicted))
        mean = compute_mean(new_data)
        return(mean)
    else:
        mean = 0
        for p_actual, p_predicted in zip(actual, predicted):
            new_data = list(map(lambda x,y:abs(x-y), p_actual, p_predicted))
            mean += compute_mean(new_data)

        return mean/len(actual)


def compute_huber_loss(actual, predicted, delta):
    new_data = list(map(lambda x,y:abs(x-y)**2 * 0.5 if abs(x-y) <= delta else (delta * abs(x-y) - (0.5 * delta**2)), actual, predicted))
    mean = compute_mean(new_data)
    return mean


def closer_point(p, a, b):
    distance_p_a = sum(map(lambda x,y:(x-y)**2, p, a))
    distance_p_b = sum(map(lambda x, y: (x - y) ** 2, p, b))

    if distance_p_a < distance_p_b:
        return 'A'
    elif distance_p_b < distance_p_a:
        return 'B'
    else:
        return 'Equal'


def find_nearest_neighbour(data, point):
    #can Be done using reduce
    #new_data = reduce(lambda a,b: a if abs(a-point) < abs(b-point) else b, data)
    new_data = list(map(lambda x:abs(x-point), data))
    nearest_nb = new_data.index(min(new_data))
    return data[nearest_nb]


def find_nearest_neighbour(data, point):
    new_data = []
    for p in data:
        new_data.append(sum(map(lambda x,y:(x-y)**2, p, point)))

    return data[new_data.index(min(new_data))]


def multiply_polynomial(equation, multiplier):
    return list(map(lambda x:x*multiplier, equation))


def add_polynomials(eq1, eq2):
    # #[2, 0, 3, 10, 0]
    #       +
    #    [4, 0, 6, 20]
    large, small = (eq1, eq2) if len(eq1) >= len(eq2) else (eq2, eq1)
    delta = abs(len(eq1)-len(eq2)) # How smaller the shorter equation

    for i in range(len(small)):
        large[i+delta] += small[i]

    return large


def subtract_polynomials(eq1, eq2, pos=None):
    #If we want to remove the eliminated variable
    return [x-y for i, (x, y) in enumerate(zip(eq1, eq2)) if i != pos]
    #return [x - y for x, y in zip(eq1, eq2)]

# [2, 3], [1, 4] -> (2x + 3) * (x + 4) = [2, 11, 12]
# [2, 0, 3, 10], [1, 2])) -> (2x^3 + 3x + 10) * (x + 2) = 2x^4 + 4x^3 + 3x^2 + 16x + 20
# # Output: [2, 4, 3, 16, 20]
def multiply_polynomials(eq1, eq2):
    result = []
    for num in eq1:
        # [2, 0, 3, 10] * 1 = [2, 0, 3, 10]
        # [2, 0, 3, 10] * 2 = [4, 0, 6, 20]
        new_result = multiply_polynomial(eq2, num)
        if len(result) == 0:
            result = new_result
        else:
            #[2, 0, 3, 10, 0] #Appending 0 for shiftting it to right
            result = result + [0]
            #[2, 0, 3, 10, 0]
            #        +
            #   [4, 0, 6, 20]
            result = add_polynomials(result, new_result)
    return result


# solve_for_first_variable([3, 4, 6, 20], [5, 6])  #  3x + 4y + 6z = 20 y=5, Z=6
# Output: -12
# solve_for_first_variable([2, 5, 7], [4])  # Equation: 2x + 5y = 7, y=4
# # (7 - (5*4)) / 2 = (7 - 20) / 2 = -13/2 = -6.5
def solve_for_first_variable(equation, values):
    #[3, 4, 6, 20], [5, 6]
    last_val = equation[-1] # 20
    x_cofficent = equation[0] # 3
    eq_except_first_last = equation[1:-1] #[4, 6]
    if not isinstance(values, list):
        values = [values]
    sum_multiply_cofficient = sum([x*y for x, y in zip(eq_except_first_last, values)]) # 4*5 + 6*6 = 56
    result = (last_val - sum_multiply_cofficient)/x_cofficent #(20 - 56)/3 = -12
    return result


def eliminate_variable(eqns, pos=0):
    if eqns[0][0] == 0:
        eqns[0], eqns[1] = eqns[1], eqns[0]
    base = eqns[0]
    reduced = []
    for eq in eqns[1:]:
        if eq[0] == 0:
            reduced.append(eq[1::])
        else:
            mult_factor = base[pos]/eq[pos]
            new_eq = multiply_polynomial(eq, mult_factor)
            result = subtract_polynomials(base, new_eq, pos)
            reduced.append(result)
    return reduced


def solve_equations_recursively(eqns):
    if len(eqns[0]) == 2:
        return eqns[0][1]/eqns[0][0]
    else:
        reduced = eliminate_variable(eqns, 0)
        remaining = solve_equations_recursively(reduced)
        x0 = solve_for_first_variable(eqns[0], remaining)
        if not isinstance(remaining, list):
            remaining = [remaining]
        return [x0] + remaining



# Example 1
# 2x +3y = 5
# x - y = 10
equations = [[2, 3, 5], [1, -1, 10]]
print(solve_equations_recursively(equations))

# Example 2
# x + y + z = 6
# 2y + 5z = -4
# 2x + 5y - z = 27
equations = [
    [1, 1, 1, 6],    # x + y + z = 6
    [0, 2, 5, -4],   # 2y + 5z = -4
    [2, 5, -1, 27]   # 2x + 5y - z = 27
]
print(solve_equations_recursively(equations))

# Example 3
# x + y + z + u = 10
# 2x - y + 3z + u = 5
# -x + 4y + z - 2u = 8
# 3x + y - z + 2u = 7
equations = [
    [1, 1, 1, 1, 10],
    [2, -1, 3, 1, 5],
    [-1, 4, 1, -2, 8],
    [3, 1, -1, 2, 7]
]
print(solve_equations_recursively(equations))

equations = [
    [1, 1, 1, 1, 1, 15],
    [2, -1, 3, 1, -1, 4],
    [-1, 4, 1, -2, 1, 10],
    [3, 1, -1, 2, 4, 20],
    [1, -2, 4, 1, 3, 8]
]

print(solve_equations_recursively(equations))


# Expected Output: [5.0, 3.0, -2.0]
# Meaning: x = 5, y = 3, z = -2

# # Example 1
# equations = [[2, 3, 5], [1, -1, 10]]
# print(eliminate_variable(equations, 0))
# # Output: [[0, 1, -15]]
# # Explanation: After eliminating x, we get 0x + 1y = -15 → y = -15
#
# # Example 2
# equations = [[1, 1, 4], [2, -1, 1]]
# print(eliminate_variable(equations, 1))
# # Output: [[1, 0, 5]]
# # Explanation: After eliminating y, we get 1x + 0y = 5 → x = 5
#
# print(eliminate_variable([[2, 3, 8], [4, -1, 2]], 0)) # Output: [7, 14]   # Represents 7y = 14
# print(eliminate_variable([[1, 2, 3], [3, 1, 7]], 1)) # Output: [-5, -11]   # Represents -5x = -11
# print(solve_for_first_variable([3, 4, 6, 20], [5, 6]))  # Output: -12
# print(solve_for_first_variable([2, 5, 7], [4]))  # Equation: 2x + 5y = 7, y=4
# # (7 - (5*4)) / 2 = (7 - 20) / 2 = -13/2 = -6.5
# # Output: -6.5
# print(multiply_polynomials([2, 3], [1, 4])) # (2x + 3) * (x + 4) = [2, 11, 12]
# print(multiply_polynomials([2, 0, 3, 10], [1, 2])) # (2x^3 + 3x + 10) * (x + 2) = 2x^4 + 4x^3 + 3x^2 + 16x + 20
# # Output: [2, 4, 3, 16, 20]
# print(add_polynomials([2, 0, 3, 10], [1, 4, 0, 6]))  # Output: [3, 4, 3, 16]
# # Explanation: (2x^3 + 3x + 10) + (1x^3 + 4x^2 + 6) = 3x^3 + 4x^2 + 3x + 16
# print(add_polynomials([5, 2], [3])) # Output: [5, 2+3] = [5, 5]
# # Explanation: (5x + 2) + (3) = 5x + 5
# print(multiply_polynomial([2, 0, 3, 10], 5))   # Output: [10, 0, 15, 50]
# print(multiply_polynomial([1, -2, 4], 3))     # Output: [3, -6, 12]
# print(find_nearest_neighbour([(1, 2), (3, 4), (6, 1)], (2, 3))) # Output: (1, 2)
# print(find_nearest_neighbour([(0, 0), (5, 5), (2, 1)], (3, 3))) # Output: (2, 1)
# print(find_nearest_neighbour([[3, 4], [2, 1], [0, 0]], [1, 2])) # Output: [2, 1])
# print(find_nearest_neighbour([[1, 1, 1], [2, 2, 2], [-1, -1, -1]], [0, 0, 0])) # Output: [1, 1, 1]
# print(find_nearest_neighbour([2, 5, 8, 12], 6))   # Output: 5
# print(find_nearest_neighbour([1, 4, 10, 20], 15)) # Output: 10
# print(find_min_max([5, 8, 2, 10, 3]))  # Output: (2, 10)
# print(find_min_max([7, 7, 7, 7]))  # Output: (7, 7)
# print(min_max_normalize(20, [10, 20, 30]))  # Output: 0.5
# print(min_max_normalize(10, [10, 20, 30]))  # Output: 0.0
# print(compute_mean([2, 4, 6, 8]))      # Output: 5.0
# print(compute_mean([10, 20, 30]))      # Output: 20.0
# print(compute_mean([]))                # Output: 0
# print(compute_sd([2, 4, 4, 4, 5, 5, 7, 9]))   # Output: 2.0
# print(compute_sd([10, 10, 10, 10]))           # Output: 0.0
# print(find_outliers([10, 12, 12, 13, 12, 11, 90], 2)) # Output: [90]
# print(find_outliers([5, 6, 7, 8, 9, 10, 100], 2)) # Output: [100]
# print(compute_iqr([1, 2, 3, 4, 5, 6, 7, 8, 9]))  # Q1 = 3, Q3 = 7 → IQR = 7 - 3 = 4
# print(compute_iqr([10, 20, 30, 40, 50, 60])) # Q1 = 20, Q3 = 50 → IQR = 50 - 20 = 30
# print(standardize([1, 2, 3, 4, 5])) # Output: [-1.2649, -0.6325, 0.0, 0.6325, 1.2649]
# print(standardize([10, 10, 10])) # Output: [0.0, 0.0, 0.0]   (because all values are the same)
# print(compute_rmse([2, 3, 4], [3, 2, 5]))  # Output: 1.0
# print(compute_rmse([1, 2, 3], [1, 2, 3]))  # Output: 0.0
# print(compute_rmse([2, 3, 4], [3, 1, 7]))
# Example 1: 1-D
# actual = [3, 5, 2]
# predicted = [2, 5, 4]
# print(compute_mae(actual, predicted))  # Output: 1.0
# print(compute_mae([1.5, 3.5, 5.5], [2, 3.5, 6]))
# Example 2: 2-D
# actual = [[1, 2], [3, 4], [5, 6]]
# predicted = [[2, 2], [2, 5], [5, 7]]
# compute_mae(actual, predicted) # Output: 0.8888888888888888
# print(compute_huber_loss([5, 2, 7], [4.8, 2.5, 10], 1))
# # For (5, 4.8): 0.5*(0.2^2) = 0.02
# # For (2, 2.5): 0.5*(0.5^2) = 0.125
# # For (7, 10): 1*3 - 0.5*1^2 = 2.5
# # Average = (0.02 + 0.125 + 2.5) / 3 = 0.8817
# # Output: 0.8817 (approximately)
#
# print(compute_huber_loss([1, 2, 3], [1, 2, 3], 1))
# # All predictions are exact → loss = 0
# # Output: 0
# print(closer_point([1, 2], [0, 0], [5, 5]))  # Output: "A"  (because P is closer to A)
# print(closer_point([3, 3, 3], [0, 0, 0], [6, 6, 6]))  # Output: "Equal"  (distances are the same)
# print(closer_point([10, 10], [2, 2], [20, 20])) # Output: "B"  (P is closer to B)