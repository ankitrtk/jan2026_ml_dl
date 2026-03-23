import math

def calculate_intrest(principal, rate, time):
    simple_intreset = principal*rate*time*.001
    print("Simple Intrest for Principle: {}, ROI: {}, Time: {} is: {}".format(principal, rate, time, simple_intreset))


def calculate_hypotense(base, height):
    hypotense = (base ** 2 + height ** 2) ** 0.5
    print("\nHypotense for base: {} and Height: {} is : {}".format(base, height, hypotense))


def calculate_distance_2d(x1, y1, x2, y2, caller=None):
    distance_2d = ((x2-x1)**2 + (y2-y1)**2) ** 0.5
    if caller:
        print("\n2D distance Between ({}, {}) & ({}, {}) is: {}".format(x1, y1, x2, y2, distance_2d))
    return distance_2d


def calculate_distance_3d(x1, y1, z1, x2, y2, z2):
    distance_3d = math.sqrt(calculate_distance_2d(x1, y1, x2, y2)**2 + (z2-z1)**2)
    print("\n3d_distance for ({}, {}, {}, {}, {}, {}) is: {}".format(x1,y1,z1,x2,y2,z2,distance_3d))


def manhattan_distance(x1, y1, x2, y2):
    manhattan_distance = abs(x1-x2) + abs(y1-y2)
    print("\nManhattan Distance between ({}, {}, {}, {}) is: {}".format(x1,y1,x2,y2,manhattan_distance))


def predict_y_on_straight_line(m, c, x, caller=None):
    y = m*x + c
    if caller:
        print("\nValue of y when m={}, c={}, and x={} is: {}".format(m, c, x, y))
    return y


def fit(x1, y1, x2, y2):
    slope = (y2-y1)/(x2-x1)
    intercept = y1 - (slope*x1)
    print("\nFor ({}, {}, {}, {}) the Slope and Intercept is: {} {}".format(x1, y1, x2, y2, slope, intercept))


def my_square(x):
    return x**2


def my_cube(x):
    return x**3

def approx_derivative(func, x, h):
    output = (func(x+h) - func(x)) / h
    print(output)





calculate_intrest(1000,8, 5)
calculate_hypotense(4, 3)
calculate_distance_2d(0, 0, 3, 4, 'caller')
calculate_distance_2d(1, 2, 4, 6, 'caller')
calculate_distance_3d(0, 0, 0, 1, 1, 1)  # Output: 1.7320508075688772
calculate_distance_3d(2, 3, 5, 2, 3, 5)  # Output: 0.0
calculate_distance_3d(1, 2, 3, 4, 6, 9)  # Output: 7.810249675906654
manhattan_distance(2, 3, 5, 1)  # Output: 5
manhattan_distance(0, 0, 0, 0)  # Output: 0
manhattan_distance(-1, -1, 1, 1)  # Output: 4
predict_y_on_straight_line(2, 3, 4, 'caller')     # Output: 11
predict_y_on_straight_line(-1, 5, 2, 'caller')    # Output: 3
fit(1, 2, 3, 6)       # Output: (2.0, 0.0)
fit(0, 5, 2, 9)       # Output: (2.0, 5.0)
approx_derivative(my_square, 3, 0.0001)
approx_derivative(my_cube, 2, 0.0001)