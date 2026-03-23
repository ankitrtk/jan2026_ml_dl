import random


def random_int(num):
    print(random.randrange(1, 10))


def coin_toss():
    print(random.choice(['Heads', 'Tails']))


def closer_point(p, a, b):
    distance_p_to_a = abs(p[0] - a[0] ) + abs(p[1] - a[1])
    distance_p_to_b = abs(p[0] - b[0] ) + abs(p[1] - b[1])
    if distance_p_to_a < distance_p_to_b:
        print('A is Closer to P')
    elif distance_p_to_a > distance_p_to_b:
        print('B is Closer to P')
    else:
        print('A,B both are at equal distance from P')


def is_point_on_line_1d(a, b, p):
    small, large = (a, b) if a <= b else (b, a)

    if p >= small and p <= large:
        print("Point P -> {} is on line ({}, {}) : True".format(p, small, large))
    else:
        print("Point P -> {} is not on line ({}, {}) : False".format(p, small, large))


def are_lines_touching_or_overlapping(start1, end1, start2, end2):
    start1, end1 = (start1,end1) if start1 <= end1 else (end1, start1)
    if start2 in range(start1, end1+1) or end2 in range(start1, end1+1):
        print('True')
    else:
        print('False')


def is_point_inside_rectangle(x1, y1, x2, y2, px, py):
    if px in range(x1, x2+1) and py in range(y1, y2+1):
        print('True')
    else:
        print('False')


def are_rectangles_intersecting(rect1: tuple, rect2: tuple) -> bool:
    rect1_x1 = rect1[0][0]
    rect1_x2 = rect1[1][0]
    rect1_y1 = rect1[0][1]
    rect1_y2 = rect1[1][1]

    rect2_x1 = rect2[0][0]
    rect2_y1 = rect2[0][1]

    if rect2_x1 in range(rect1_x1, rect1_x2+1) and rect2_y1 in range(rect1_y1, rect1_y2+1):
        print('True')
    else:
        print('False')


def my_impurity(c1, c2):
    # your formula here
    impurity = 1 - abs(c1-c2)/(c1+c2)
    print('impurity is', impurity)

random_int(10)
coin_toss()
closer_point((1, 2), (0, 0), (5, 5))     # Output: 'A'
closer_point((4, 4), (0, 0), (8, 8))     # Output: 'Equal'
closer_point((7, 3), (2, 3), (10, 3))    # Output: 'B'
is_point_on_line_1d(2, 5, 3)      # Output: True
is_point_on_line_1d(5, 2, 3)      # Output: True
is_point_on_line_1d(2, 5, 6)      # Output: False
is_point_on_line_1d(4, 4, 4)      # Output: True  (A single point segment)
is_point_on_line_1d(4, 4, 5)      # Output: False
is_point_on_line_1d(-5, -2, -3)   # Output: True
is_point_on_line_1d(-5, -2, -6)   # Output: False
is_point_on_line_1d(-2, -5, -4)   # Output: True
is_point_on_line_1d(-1, 3, 0)     # Output: True
are_lines_touching_or_overlapping(1, 4, 3, 6)        # Output: True   (Overlap from 3 to 4)
are_lines_touching_or_overlapping(1, 3, 3, 5)        # Output: True   (Touch at point 3)
are_lines_touching_or_overlapping(1, 2, 3, 4)        # Output: False  (Completely separate)
are_lines_touching_or_overlapping(-3, 1, 0, 4)       # Output: True   (Overlap from 0 to 1)
are_lines_touching_or_overlapping(-5, -2, -2, 3)     # Output: True   (Touch at point -2)
are_lines_touching_or_overlapping(-10, -6, -5, -1)   # Output: False  (No touch or overlap)
are_lines_touching_or_overlapping(-2, -7, -4, -3)    # Output: True   (Overlap from -4 to -3, even with reversed inputs)
is_point_inside_rectangle(0, 0, 10, 5, 3, 2)   # Output: True
is_point_inside_rectangle(0, 0, 10, 5, 10, 5)  # Output: True  (point on the corner)
is_point_inside_rectangle(0, 0, 10, 5, 11, 5)  # Output: False (outside the rectangle)
is_point_inside_rectangle(-5, -5, 5, 5, 0, 0)  # Output: True  (inside a rectangle with negative coordinates)
are_rectangles_intersecting(((0, 0), (3, 3)), ((2, 2), (5, 5)))
# Output: True
are_rectangles_intersecting(((0, 0), (1, 1)), ((2, 2), (3, 3)))
# Output: False
are_rectangles_intersecting(((0, 0), (2, 2)), ((2, 2), (4, 4)))
# Output: True
are_rectangles_intersecting(((0, 0), (5, 5)), ((1, 1), (2, 2)))
# Output: True
my_impurity(0, 5)     # Output: 0.0 because it pure having only c2.
my_impurity(4, 0)     # Output: 0.0 because it pure having only c2.
my_impurity(8, 8)     # Output: 1.0 because it is total impure, having equal numbers from both classes
my_impurity(7, 3)     # Output: 0.6
my_impurity(9, 1)     # Output: 0.2