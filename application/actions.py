from application.params import AppPapams
from interface.windows import UiMainWindow, TimerMainWindow
import interface.widgets as widgets
import gravity.difference_schemes as ds

def update_window(window : UiMainWindow):
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

def update_axes(num : int, graphic : widgets.Graphic3D):
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

def update_lines(num : int, time_sec : widgets.TextLine, time_day : widgets.TextLine, energy : widgets.TextLine):
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

def reset_timer(window : TimerMainWindow):
    def wraper():
        update_window.num = 0
    return wraper