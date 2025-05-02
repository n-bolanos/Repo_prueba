from random import random
import matplotlib.pyplot as plt
import math

def graphic(x,y):
    fig,ax = plt.subplots() #Se crea la figura y ejes
    ax.scatter(x,y) #Se Crea el grafico de puntos
    plt.show() #Muestra la figura

def grafica_densidad(fun,iteraciones=1000000,param=None,redondeo=2):
    dictionary = {} #Diccionario para acumular las frecuencias de los valores
    for i in range(iteraciones):
        if param is None: #Se revisa si la funcion tiene o no parametros
            value = round(fun(),redondeo) #Se redondea a tantas cifras decimales com se desee
        else:
            value = round(fun(param),redondeo)
        # Se agrega cada valor al diccionario y se va llevando registro de sus frecuencias
        if value in dictionary:
                dictionary[value] += 1
        else:
                dictionary[value] = 0

    prop = [] #Lista para guardar las proporciones de aparición
    for i in dictionary.values():
        #Se guardan las proporciones
        prop.append( (i/iteraciones)*10**redondeo)
    graphic(dictionary.keys(),prop) #Se grafican los resultados
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


#Punto 2 b
def r_acum_inv_b(u):
     return (3/2)*u

def metodo_ar_b():
    while True:
     u1 = random()
     x = r_acum_inv_b(u1)
     tx=7/4

     if x <= 1:
            fx=1/4
     else:
            fx = 3*x - 11/4

     px= fx/tx
     u2 = random()

     if u2 <= px:
          return x


#Punto 3a
def tr_inv_a():
   
    u = random()

    base = 2*u - 1 
    if base < 0:
         inv = -abs(base)**(1/3)
    else:
        inv = (base)**(1/3)

    return inv



def ar_a():
     while True:
        u1 = random()
        x = 2*u1-1
        
        fx = 3*x**2 /2
        tx = 3/2
        px = fx/tx
        
        u2 = random()
        if u2 <= px:
            return x
        
# Punto 3 b
def tr_inv_b(a:float):
    if a>=0.5 or a<=0:
          print("No se puede hacer uso del algoritmo - 0<=a<=0.5")
          return None
    u:float = random()
    
    if u <= a/(2-2*a):
        ans = math.sqrt(2*a*(1-a)*u)
    
        
    elif u<= (2-3*a)/(2-2*a):
        ans= ((2*(1-a)*u)+a)/2
        
    else:
        k = (u+(a/(2*(1-a)))+((a+1)/(2*a))-1)*(2*a*(1-a))
        ans = 1-((1-k)**(1/2))
        
    return ans
    
def ar_b(a:float):
    while True:
        u0 = random()
        t = 1/(1-a)
        if u0 <= a/(2-2*a):
            f = u0/(a*(1-a))
        elif u0< (2-3*a)/(2-2*a):
            f = 1/(1-a)
        else:
            f= (1-u0)/(a*(1-a))
        px = f/t
        u1 = random()
        if u1 <= px:
            return u0


#5
def trans_inv_5():
    u = random()
    inversa = (16*u)**(1/4)
    return inversa

#6 
def trans_inv_6():
     u = random()
     inversa = (27*u)**(1/3)
     return inversa

