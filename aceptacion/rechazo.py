from random import random
import matplotlib.pyplot as plt

def graphic(x,y):
    fig,ax = plt.subplots()
    ax.scatter(x,y)
    plt.show()
x = 0

def r_acum_inversa(u:float):
    return (5/3) * u

def metodo_ar():
    while True:
        a1:float = random()
        x = r_acum_inversa(a1)

        if x <= 1:
            return x
        else:
            f2 = ((-9/8)*x)+(15/8)
            t = 3/4
            px = f2 / t
            u = random()
            if u <= px:
                return x


dictionary = {}
for i in range(100000000):
    value = round(metodo_ar(),2)
    if value in dictionary:
            dictionary[value] += 1
    else:
            dictionary[value] = 0

graphic(dictionary.keys(),dictionary.values())