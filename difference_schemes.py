import numpy as np
import math
from planets import Planet
import numpy.typing as ntp

G = 6.67e-11

def _calculate_a(planets : list[Planet], i : int, j : int) -> ntp.NDArray[np.float64]:
    m = len(planets)
    dim = planets[0].dim
    cur_movement = planets[i].movement
    sum_a = np.zeros([dim])
    for k in range(0, m):
        if k != i:
            movement = planets[k].movement
            direction = movement.get_r(j) - cur_movement.get_r(j)
            r2 = np.sum(direction**2)
            a = planets[k].m*G/r2
            cos_angle = direction / math.sqrt(r2)
            sum_a += a * cos_angle
    return sum_a

def calculate_euler(planets : list[Planet], start_pos : int, size : int, ht : int):
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            movement.set_a(j, _calculate_a(planets, i, j))
            movement.set_v(j+1, movement.get_v(j) + movement.get_a(j) * ht)
            movement.set_r(j+1, movement.get_r(j) + movement.get_v(j) * ht)

def calculate_eulkram(planets : list[Planet], start_pos : int, size : int, ht : int):
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            movement.set_a(j, _calculate_a(planets, i, j))
            movement.set_v(j+1, movement.get_v(j) + movement.get_a(j) * ht)
            movement.set_r(j+1, movement.get_r(j) + movement.get_v(j+1) * ht)

def _init_biman(calculate_biman):
    def wraper(planets : list[Planet], start_pos : int, size : int, ht : int):
        if start_pos == 0:
            m = len(planets)
            for i in range(0, m):
                movement = planets[i].movement
                movement.set_a(0, _calculate_a(planets, i, 0))
                movement.set_v(1, movement.get_v(0) + movement.get_a(0) * ht)
                movement.set_r(1, movement.get_r(0) + movement.get_v(1) * ht)
            for i in range(0, m):
                movement = planets[i].movement
                movement.set_a(1, _calculate_a(planets, i, 1))
                movement.set_r(2, movement.get_r(1) + movement.get_v(1)*ht - 1/6*(4*movement.get_a(1) - movement.get_a(0))*(ht**2))
            return calculate_biman(planets, 2, size-2, ht)
        else:
            return calculate_biman(planets, start_pos, size, ht)
    return wraper

@_init_biman
def calculate_biman(planets : list[Planet], start_pos : int, size : int, ht : int):
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            movement.set_a(j, _calculate_a(planets, i, j))
            movement.set_v(j, movement.get_v(j-1) + 1/6*(2*movement.get_a(j) + 5*movement.get_a(j-1) - movement.get_a(j-2))*ht)
            movement.set_r(j+1, movement.get_r(j) + movement.get_v(j)*ht - 1/6*(4*movement.get_a(j) - movement.get_a(j-1))*(ht**2))

def _init_vernel(calculate_vernel):
    def wraper(planets : list[Planet], start_pos : int, size : int, ht : int):
        if start_pos == 0:
            m = len(planets)
            for i in range(0, m):
                movement = planets[i].movement
                movement.set_a(0, _calculate_a(planets, i, 0))
                movement.set_v(1, movement.get_v(0) + movement.get_a(0) * ht)
                movement.set_r(1, movement.get_r(0) + movement.get_v(1) * ht)
            return calculate_vernel(planets, 1, size-1, ht)
        else:
            return calculate_vernel(planets, start_pos, size, ht)
    return wraper

@_init_vernel
def calculate_vernel(planets : list[Planet], start_pos : int, size : int, ht : int):
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            movement.set_a(j, _calculate_a(planets, i, j))
            movement.set_r(j+1, 2*movement.get_r(j) - movement.get_r(j-1) + movement.get_a(j)*(ht**2))
            movement.set_v(j, (movement.get_r(j+1) - movement.get_r(j-1))/(2*ht))