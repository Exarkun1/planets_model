import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from planets import Planet
import difference_schemes as ds

t = 315360000
ht = 3600

n = t // ht
step = 100

planets = [
    Planet(1.21e30, 3, n, v0=[0,0,10000]),
    Planet(6.08e24, 3, n, r0=[149500000000, 0, 0], v0=[0, 23000, 0]),
    Planet(1.21e29, 3, n, r0=[490000000000, 0, 0], v0=[0, 10000, 0])
]

def animate_system(num):
    ax.clear()
    ds.calculate_vernel(planets, num*step, step, ht)
    u = 0
    for planet in planets:
        r = planet.movement._r
        m = planet.m
        ax.plot3D(r[0, :(num+1)*step], r[1, :(num+1)*step], r[2, :(num+1)*step])
        if m > 1e29:
            ax.scatter(r[0, (num+1)*step], r[1, (num+1)*step], r[2, (num+1)*step], s=60)
        else:
            ax.scatter(r[0, (num+1)*step], r[1, (num+1)*step], r[2, (num+1)*step], s=20)
        u += planet.energy.get_u(num*step)

    ax.set_title(f'Time = {ht*(num+1)*step} sec\nEnergy = {u}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

fig = plt.figure()
ax = plt.axes([0.3, 0.1, 0.5, 0.8], projection='3d')
ani = animation.FuncAnimation(fig, animate_system, interval=10, frames=n//step, repeat=False)

axButn1 = plt.axes([0.1, 0.2, 0.1, 0.05]) 
btn1 = plt.Button(axButn1, label="pause", color='pink', hovercolor='tomato')
btn1.on_clicked(lambda event: ani.pause())
axButn2 = plt.axes([0.1, 0.3, 0.1, 0.05]) 
btn2 = plt.Button(axButn2, label="resume", color='pink', hovercolor='tomato')
btn2.on_clicked(lambda event: ani.resume())

plt.show()

# f = f'anumate.gif'
# writergif = animation.PillowWriter(fps=n//step//100)
# line_ani.save(f, writer=writergif)