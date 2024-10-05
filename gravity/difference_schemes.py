import numpy as np
import math
from gravity.planets import Planet
import numpy.typing as ntp

G = 6.67e-11

def _calculate_a(planets : list[Planet], i : int, j : int) -> ntp.NDArray[np.float64]:
    """
    Функция для вычисления ускорения планеты по расстояниям между ней и другими планетами.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    i - индекс планеты в списке, для которой ищется ускорение;
    j - индекс временного узла, в котором необходимо найти ускорение.

    Возвращаемое значение:
    Массив размерности dim хранящий компоненты ускорения.
    """
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

def _calculate_up(planets : list[Planet], i : int, j : int) -> float:
    """
    Функция для вычисления потенциальной энергии планеты по расстояниям между ней и другими планетами.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    i - индекс планеты в списке, для которой ищется потенциальная энергия;
    j - индекс временного узла, в котором необходимо найти потенциальную энергию.

    Возвращаемое значение:
    Значение потенциальной энергии.
    """
    m = len(planets)
    cur_movement = planets[i].movement
    sum_up = 0
    for k in range(i+1, m):
        movement = planets[k].movement
        direction = movement.get_r(j) - cur_movement.get_r(j)
        r = math.sqrt(np.sum(direction**2))
        sum_up = planets[k].m / r
    return -sum_up * G * planets[i].m

def _calculate_uk(planets : list[Planet], i : int, j : int) -> float:
    """
    Функция для вычисления кинетической энергии планеты по её скорости.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    i - индекс планеты в списке, для которой ищется кинетическая энергия;
    j - индекс временного узла, в котором необходимо найти кинетическую энергию.

    Возвращаемое значение:
    Значение кинетической энергии.
    """
    cur_movement = planets[i].movement
    v2 = np.sum(cur_movement.get_v(j)**2)
    return planets[i].m * v2 / 2

def _init_euler(calculate_euler):
    """
    Функция-декоратор для задания начальных значений перемещения планет для методов Эйлера и Эйлера-Крамера.
    """
    def wraper(planets : list[Planet], start_pos : int, size : int, ht : int):
        if start_pos == 0:
            m = len(planets)
            for i in range(0, m):
                movement = planets[i].movement
                energy = planets[i].energy
                energy.set_up(0, _calculate_up(planets, i, 0))
                energy.set_uk(0, _calculate_uk(planets, i, 0))
                movement.set_a(0,  _calculate_a(planets, i, 0))
            return calculate_euler(planets, 1, size-1, ht)
        else:
            return calculate_euler(planets, start_pos, size, ht)
    return wraper

@_init_euler
def calculate_euler(planets : list[Planet], start_pos : int, size : int, ht : int):
    """
    Функция для вычисления перемещения планет методом Эйлера.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    start_pos - индекс временного узла, с которого начнутся вычисления;
    size - число временных узлов, которые должны быть вычислены;
    ht - шаг дискретизации по времени.
    """
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            movement.set_v(j, movement.get_v(j-1) + movement.get_a(j-1) * ht)
            movement.set_r(j, movement.get_r(j-1) + movement.get_v(j-1) * ht)
            energy.set_uk(j, _calculate_uk(planets, i, j))
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            energy.set_up(j, _calculate_up(planets, i, j))
            movement.set_a(j, _calculate_a(planets, i, j))

@_init_euler
def calculate_eulkram(planets : list[Planet], start_pos : int, size : int, ht : int):
    """
    Функция для вычисления перемещения планет методом Эйлера-Крамера.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    start_pos - индекс временного узла, с которого начнутся вычисления;
    size - число временных узлов, которые должны быть вычислены;
    ht - шаг дискретизации по времени.
    """
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            movement.set_v(j, movement.get_v(j-1) + movement.get_a(j-1) * ht)
            movement.set_r(j, movement.get_r(j-1) + movement.get_v(j) * ht)
            energy.set_uk(j, _calculate_uk(planets, i, j))
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            energy.set_up(j, _calculate_up(planets, i, j))
            movement.set_a(j, _calculate_a(planets, i, j))

def _init_biman(calculate_biman):
    """
    Функция-декоратор для задания начальных значений перемещения планет для метода Бимана.
    """
    def wraper(planets : list[Planet], start_pos : int, size : int, ht : int):
        if start_pos == 0:
            m = len(planets)
            for i in range(0, m):
                energy = planets[i].energy
                movement = planets[i].movement
                energy.set_up(0, _calculate_up(planets, i, 0))
                energy.set_uk(0, _calculate_uk(planets, i, 0))
                movement.set_a(0, _calculate_a(planets, i, 0))
            for i in range(0, m):
                movement = planets[i].movement
                energy = planets[i].energy
                movement.set_v(1, movement.get_v(0) + movement.get_a(0) * ht)
                movement.set_r(1, movement.get_r(0) + movement.get_v(1) * ht)
            for i in range(0, m):
                energy = planets[i].energy
                movement = planets[i].movement
                energy.set_up(1, _calculate_up(planets, i, 1))
                energy.set_uk(1, _calculate_uk(planets, i, 1))
                movement.set_a(1, _calculate_a(planets, i, 1))
            return calculate_biman(planets, 2, size-2, ht)
        else:
            return calculate_biman(planets, start_pos, size, ht)
    return wraper

@_init_biman
def calculate_biman(planets : list[Planet], start_pos : int, size : int, ht : int):
    """
    Функция для вычисления перемещения планет методом Бимана.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    start_pos - индекс временного узла, с которого начнутся вычисления;
    size - число временных узлов, которые должны быть вычислены;
    ht - шаг дискретизации по времени.
    """
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            movement.set_r(j, movement.get_r(j-1) + movement.get_v(j-1)*ht - 1/6*(4*movement.get_a(j-1) - movement.get_a(j-2))*(ht**2))
        for i in range(0, m):
            energy = planets[i].energy
            movement = planets[i].movement
            energy.set_up(j, _calculate_up(planets, i, j))
            movement.set_a(j, _calculate_a(planets, i, j))
        for i in range(0, m):
            energy = planets[i].energy
            movement = planets[i].movement
            movement.set_v(j, movement.get_v(j-1) + 1/6*(2*movement.get_a(j) + 5*movement.get_a(j-1) - movement.get_a(j-2))*ht)
            energy.set_uk(j, _calculate_uk(planets, i, j))

def _init_vernel(calculate_vernel):
    """
    Функция-декоратор для задания начальных значений перемещения планет для метода Вернеле.
    """
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
    """
    Функция для вычисления перемещения планет методом Вернеле.

    Принимаемые значения:
    planets - список планет, имеющих одинаковые dim и n;
    start_pos - индекс временного узла, с которого начнутся вычисления;
    size - число временных узлов, которые должны быть вычислены;
    ht - шаг дискретизации по времени.
    """
    m = len(planets)
    size = min(size, planets[0].n-start_pos)
    for j in range(start_pos, start_pos+size):
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            energy.set_up(j, _calculate_up(planets, i, j))
            movement.set_a(j, _calculate_a(planets, i, j))
        for i in range(0, m):
            movement = planets[i].movement
            energy = planets[i].energy
            movement.set_r(j+1, 2*movement.get_r(j) - movement.get_r(j-1) + movement.get_a(j)*(ht**2))
            movement.set_v(j, (movement.get_r(j+1) - movement.get_r(j-1))/(2*ht))
            energy.set_uk(j, _calculate_uk(planets, i, j))