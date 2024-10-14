from gravity.planets import Planet
import gravity.difference_schemes as ds

class AppPapams:
    """
    Класс параметров системы.
    """
    instance = None

    def __new__(clc):
        if clc.instance is None:
            clc.instance = super(__class__, clc).__new__(clc)
            clc.instance._initialize()
        return clc.instance
    
    def _initialize(self):
        """
        Метод инициализации параметров системы.
        """
        self.t = 315360000
        self.ht = 3600
        self.step = 100
        
        self.planets = [
            Planet(1.21e30, 3, self.n, v0=[0,0,10000]),
            Planet(6.08e24, 3, self.n, r0=[149500000000, 0, 0], v0=[0, 23000, 0]),
            Planet(1.21e29, 3, self.n, r0=[490000000000, 0, 0], v0=[0, 10000, 0])
        ]

        self.calculate = ds.calculate_vernel

        self.methods = {
            "Euler": ds.calculate_euler,
            "Euler Kramer": ds.calculate_eulkram,
            "Biman": ds.calculate_biman,
            "Vernel": ds.calculate_vernel
        }

        self.reseted = False

    @property
    def n(self) -> int:
        """
        Свойство для числа временных узлов.

        Returns:
            Число временных узлов. 
        """
        return self.t // self.ht