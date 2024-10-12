from application.params import AppPapams
from interface.windows import UiMainWindow
import interface.widgets as widgets

from gravity.planets import Planet
import gravity.difference_schemes as ds

def update_window(window : UiMainWindow):
    """
    Функция обновления окна.

    Args:
        window: окно с визуальными элементами.
    """
    app = AppPapams()
    update_window.num = 0
    graphic = window.graphic_box
    time_sec = window.time_sec_line
    time_day = window.time_day_line
    energy = window.energy_line

    def wraper():
        if update_window.num == app.n // app.step:
            return

        planets = AppPapams().planets
        ht = AppPapams().ht
        step = AppPapams().step
        ds.calculate_vernel(planets, update_window.num*step, step, ht)

        update_axes(update_window.num, graphic)
        update_lines(update_window.num, time_sec, time_day, energy)

        update_window.num += 1
        graphic.draw()
    return wraper

def update_axes(num : int, 
                graphic : widgets.Graphic3D):
    """
    Функция обновления графика на окне.

    Args:
        num: номер временного узла.
        graphic: окно графика.
    """
    planets = AppPapams().planets
    step = AppPapams().step

    ax = graphic.axes
    ax.clear()
    u = 0
    for planet in planets:
        r = planet.movement._r
        m = planet.m
        ax.plot3D(r[0, :(num+1)*step], r[1, :(num+1)*step], r[2, :(num+1)*step])
        if m > 1e29:
            ax.scatter(r[0, (num+1)*step-1], r[1, (num+1)*step-1], r[2, (num+1)*step-1], s=60)
        else:
            ax.scatter(r[0, (num+1)*step-1], r[1, (num+1)*step-1], r[2, (num+1)*step-1], s=20)
        u += planet.energy.get_u(num*step)

    # ax.set_title(f'Time = {ht*(num+1)*step-1} sec\nEnergy = {u}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

def update_lines(num : int, 
                 time_sec : widgets.TextLine, 
                 time_day : widgets.TextLine, 
                 energy : widgets.TextLine):
    """
    Функция обновления текстовых полей окна.

    Args:
        num: номер временного узла.
        time_sec: текстовое поле со значением времени в секундах.
        time_day: текстовое поле со значением времени в днях.
        energy: текстовое поле со значением энергии.
    """
    planets = AppPapams().planets
    ht = AppPapams().ht
    step = AppPapams().step

    u = 0
    for planet in planets:
        u += planet.energy.get_u(num*step)
    time = ht*(num+1)*step-1

    energy.setText(str(u))
    time_sec.setText(str(time))
    time_day.setText(str(time // (3600*24)))

def reset_timer(window : UiMainWindow):
    """
    Функция обновления данных о системе с элементов окна.

    Args:
        window: окно с визуальными элементами.
    """
    def wraper():
        update_window.num = 0
        AppPapams().t = int(window.time_edit_line.text())
        AppPapams().ht = int(window.ht_edit_line.text())
        window.time_max_sec_line.setText(str(AppPapams().t))
        window.time_max_day_line.setText(str(AppPapams().t // (3600*24)))

        table = window.table
        AppPapams().planets = []
        planets = AppPapams().planets
        for i in range(0, table.rowCount()):
            x = float(table.item(i, 0).text())
            y = float(table.item(i, 1).text())
            z = float(table.item(i, 2).text())
            vx = float(table.item(i, 3).text())
            vy = float(table.item(i, 4).text())
            vz = float(table.item(i, 5).text())
            m = float(table.item(i, 6).text())
            planets.append(Planet(m, 3, AppPapams().n, r0=[x, y, z], v0=[vx, vy, vz]))

        AppPapams().calculate = AppPapams().methods[window.method_list.currentText()]
    return wraper

def add_row(window : UiMainWindow):
    """
    Функция добавления строки в таблице окна.

    Args:
        window: окно с визуальными элементами.
    """
    table = window.table
    def wraper():
        table.insertRow(table.rowCount())
    return wraper

def delete_row(window : UiMainWindow):
    """
    Функция удаления строки в таблице окна.

    Args:
        window: окно с визуальными элементами.
    """
    table = window.table
    def wraper():
        if len(table.selectedIndexes()) != 1:
            table.removeRow(table.rowCount()-1)
        else:
            table.removeRow(table.selectedIndexes()[0].row())
    return wraper