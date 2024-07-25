import random
import math

matrix = [[0, 1072, 1555, 3327, 10214, 10042, 6764, 3913, 9152, 4489, 18140, 8614, 7967],
[6660, 0, 6711, 7979, 11776, 14694, 8296, 2910, 8149, 6021, 17137, 7611, 9499],
[1282, 1219, 0, 3474, 10361, 10189, 6911, 4060, 9299, 4636, 18287, 8761, 8114],
[3405, 3044, 2157, 0, 7044, 7094, 4767, 5872, 10272, 3656, 18133, 10540, 6398],
[9961, 9600, 8713, 7160, 0, 11692, 4824, 8388, 6343, 5743, 14204, 6755, 3123],
[6847, 6486, 5599, 4046, 9864, 0, 7587, 9121, 13092, 6476, 20953, 13504, 9218],
[5292, 4931, 4044, 2491, 9378, 7023, 0, 7759, 12606, 5990, 20467, 12427, 8732],
[4096, 3724, 3801, 5069, 8866, 11784, 5386, 0, 5613, 3111, 14601, 5075, 6589],
[7426, 7054, 7477, 8696, 7998, 15199, 8331, 3676, 0, 6056, 11678, 2152, 9407],
[4444, 4083, 3196, 3619, 5907, 9295, 2427, 2797, 7745, 0, 15606, 7213, 3630],
[11811, 11439, 11862, 11771, 7947, 16303, 9435, 8061, 4768, 10354, 0, 5427, 9356],
[9936, 9564, 9987, 9702, 5878, 14234, 7366, 6186, 2893, 8285, 9630, 0, 7287],
[8014, 7653, 6766, 7189, 8575, 11963, 5095, 6367, 4355, 3722, 12216, 4767, 0]]

def f(points, matrix): # point - list of numbers from 0 to n-1
    dist = 0
    for i in range(len(points) - 1):
        dist += matrix[points[i]][points[i + 1]]
    dist += matrix[points[-1]][points[0]]  # return to the starting point
    return dist


def anneal(matrix, cars_n):
    all_points = list(range(len(matrix)))
    state = []
    for i in range(cars_n):
        state.append([0])
    all_points.pop(0)
    while all_points:
        for i in range(len(state)):
            print(state)
            point = all_points.pop(random.randint(0, len(all_points) - 1))
            state[i].append(point)
    temp = 1
    n = 1e6
    i = 0
    while i < n:
        temp *= 0.99
        i+=1
        seed = random.randint(1, 10)
        if cars_n == 1:
            seed = 10
        if seed == 1:  # change between cars
            pass
        else:
            car = random.randint(0, len(state) - 1)
            x = random.randint(1, len(state[car]) - 2)
            y = random.randint(1, len(state[car]) - 2)
            while x == y:
                y = random.randint(1, len(state[car]) - 2)
            new_state = state.copy()
            new_state[car][x], new_state[car][y] = new_state[car][y], new_state[car][x]
            f_old = f(state, matrix)
            f_new = f(new_state, matrix)
        if f_old == f_new:
            continue
        if f_old > f_new:
            state = new_state
            continue
        if (random.uniform(0, 1) < math.exp((f_old - f_new) / temp)):
            state = new_state
            continue
    return state

# points = [0, 1, 7, 8, 11, 10, 4 , 12, 9, 6, 5, 3, 2, 0]
# min_path = 100000000000000000000
# for i in range(10):
#     print(i)
#     path = anneal(matrix, points)
#     ln = f(path, matrix)
#     if ln < min_path:
#         min_path = ln

# print(min_path)

path = anneal(matrix, 3)
print(path, f(path, matrix))
        