import numpy as np
import numpy.typing as ntp

class PlanetMovement:
    """
    Класс для хранения изменений в положении, скорости и ускорении планеты в заданном временном промежутке.
    """
    def __init__(self, dim : int, n : int, r0 : np.ndarray, v0 : np.ndarray):
        """
        Принимаемые значения:
        dim - размерность пространства;
        n - число узлов временного промежутка;
        r0 - начальное положение планеты;
        v0 - начальная скорость.
        """
        self._r = np.zeros([dim, n+1])
        self._v = np.zeros([dim, n+1])
        self._a = np.zeros([dim, n+1])
        self.set_r(0, r0)
        self.set_v(0, v0)

    def get_r(self, index : int) -> ntp.NDArray[np.float64]:
        return self._r[:, index]
    
    def get_v(self, index : int) -> ntp.NDArray[np.float64]:
        return self._v[:, index]
    
    def get_a(self, index : int) -> ntp.NDArray[np.float64]:
        return self._a[:, index]
    
    def set_r(self, index : int, r : ntp.NDArray[np.float64]):
        self._r[:, index] = r

    def set_v(self, index : int, v : ntp.NDArray[np.float64]):
        self._v[:, index] = v

    def set_a(self, index : int, a : ntp.NDArray[np.float64]):
        self._a[:, index] = a

class PlanetEnergy:
    """
    Класс для хранения изменений кинетической и потенциальной энергии планет.
    """
    def __init__(self, n : int):
        """
        Принимаемые значения:
        n - число узлов временного промежутка.
        """
        self._uk = np.zeros([n+1])
        self._up = np.zeros([n+1])

    def get_uk(self, index):
        return self._uk[index]
    
    def get_up(self, index):
        return self._up[index]

    def set_uk(self, index, uk):
        self._uk[index] = uk

    def set_up(self, index, up):
        self._up[index] = up

    def get_u(self, index):
        return self.get_uk(index) + self.get_up(index)

class Planet:
    """
    Класс для хранения параметров планеты.
    """
    def __init__(self, m : float, dim : int, n : int, r0 : list[float] = None, v0 : list[float] = None):
        """
        Принимаемые значения:
        m - масса планеты;
        dim - размерность пространства;
        n - число узлов временного промежутка;
        r0 - начальное положение планеты;
        v0 - начальная скорость.
        """
        if r0 is None:
            r0 = np.zeros([dim])
        else:
            r0 = np.array(r0)
        if v0 is None:
            v0 = np.zeros([dim])
        else:
            v0 = np.array(v0)
        self.m = m
        self._dim = dim
        self._n = n
        self._movement = PlanetMovement(dim, n, r0, v0)
        self._energy = PlanetEnergy(n)

    @property
    def movement(self) -> PlanetMovement:
        return self._movement
    
    @property
    def energy(self) -> PlanetEnergy:
        return self._energy
    
    @property
    def dim(self) -> int:
        return self._dim
    
    @property
    def n(self) -> int:
        return self._n
