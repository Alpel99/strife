import math

def point_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def circle_triangle_collision(circle_center, circle_radius, triangle_vertices):
    closest_point = None
    min_distance = float('inf')

    # create midpoints to check dist, aswell!
    for vertex in triangle_vertices:
        distance = point_distance(circle_center, vertex)
        if distance < min_distance:
            min_distance = distance
            closest_point = vertex

    print(min_distance, circle_radius)
    if min_distance <= circle_radius or isInside(*triangle_vertices, circle_center):
        return True
    else:
        return False

def area(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def isInside(point1, point2, point3, point):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    x, y = point
    
    # Calculate area of triangle ABC
    A = area(point1, point2, point3)

    # Calculate area of triangle PBC
    A1 = area(point, point2, point3)

    # Calculate area of triangle PAC
    A2 = area(point1, point, point3)

    # Calculate area of triangle PAB
    A3 = area(point1, point2, point)

    # Check if sum of A1, A2, and A3 is the same as A
    return A == A1 + A2 + A3
