from random import random
from openpyxl import Workbook
import numpy
from matplotlib import pyplot

def grafica(times,states,color='blue'):
    fig,axis = pyplot.subplots()
    axis = pyplot.plot(times,states,color=color,linewidth=0.5)
    pyplot.show()

states_cc = []
states_s = []
states_t = []
tiempos = []

class Cafeteria:
    def __init__(self):
        
        '''Constantes globales'''
        self.TIEMPO_CC = 60
        self.TIEMPO_S = 30
        self.LIMITE_CL_ATENDIDOS = 1000


        '''Inicializar las variables de estado'''
        
        self.reloj: float = 0.0
        self.last_time: float = 0.0
        self.num_cl_q_CC: int = 0
        self.num_cl_q_S: int = 0
        self.num_ser_disp_CC: int = 6
        self.num_ser_disp_S: int = 1
        self.num_cl_q_T: int = 0
        self.num_disp_T: int = 200
        self.next_evento: int = 0

        self.arrival_q_CC: list[float] = []
        self.arrival_q_S: list[float] = []
        self.tipo_q_T: list[str] = []
        self.arr_dep_T: list[tuple[float, float]] = []
        self.eventos: list = [None, 10**30, 10**30, [10**30], (10**30, 10**30)]

        '''Inicializar los estadísiticos'''
        self.num_cl_atendidos: int = 0
        self.acm_q_CC: int = 0
        self.acm_q_S: int = 0
        self.area_numq_CC: float = 0.0
        self.area_numq_S: float = 0.0
        self.total_delay_CC: float = 0.0
        self.total_delay_S: float = 0.0
        self.total_time_T: float = 0.0

    def generador_llegadas(self):
        '''
        Esta función genera un valor bajo una distribución ~U(5, 15)
        '''
        a = 5
        b = 15
        
        u = random()    
        return round(u*(b-a)+a,3)

    def esc_fila(self):
        '''
        Esta función simula la decisión de qué fila escoger
        '''
        u = random()
        if u < 0.8:
            return 'CC'
        return 'S'

    def generador_consumo_CC(self):
        '''
        Esta función genera un valor bajo una distribución ~U(1200, 2400)
        '''
        a = 1200
        b = 2400
        
        u = random()    
        return round(u*(b-a)+a,3)

    def generador_consumo_S(self):
        '''
        Esta función genera un valor bajo una distribución ~U(600, 1200)
        '''
        a = 600
        b = 1200
        
        u = random()    
        return round(u*(b-a)+a,3)
        
    def timing(self):
        '''
        Esta función se encarga del manejo del reloj de la simulación
        '''
        
        self.next_evento = 0
        min_tiempo_next = 10**29
        
        for i in range(1,5):
            if i == 3:
                t_potencial = min(self.eventos[3])  #Para obetener la primera salida_CC dentro de las programadas
            elif i == 4:
                t_potencial = self.eventos[4][1]   #Para obtener la salida de la tupla. Estas son de la forma (llegada, salida)
            else:
                t_potencial = self.eventos[i]
                
            if t_potencial < min_tiempo_next:
                min_tiempo_next = t_potencial
                self.next_evento = i
                
        self.last_time = self.reloj
        
        self.reloj = min_tiempo_next    #Actualizar el reloj de la simulación
        return
    
    def update_stats(self):
        '''
        Esta función actualiza los estadísticos del sistema
        '''
        delta = self.reloj - self.last_time
        if delta < 0:
            print(self.next_evento)
        self.area_numq_CC += delta * self.num_cl_q_CC
        self.area_numq_S += delta * self.num_cl_q_S
        
        return

    def report(self):
        '''
        Esta función genera el reporte de la simulación
        '''
        print('-------------END OF SIMULATION--------------')
        return ["Average delay in queue 'Comida Caliente'",self.total_delay_CC/self.acm_q_CC,"Average number in queue 'Comida Caliente'",self.area_numq_CC/self.reloj,"Average delay in queue 'Sandwiches'",self.total_delay_S/self.acm_q_S,"Average number in queue 'Sandwiches'",self.area_numq_S/self.reloj,"Average time in table",self.total_time_T/self.num_cl_atendidos,"equivalent to",self.total_time_T/self.num_cl_atendidos/60,"Time simulation ended",self.reloj/60]
        
    def llegada(self):
        '''
        Esta función simula la rutina cuando llega un nuevo cliente al sistema
        '''
        self.eventos[1] = self.reloj + self.generador_llegadas() #Programar la siguiente llegada
        
        fila = self.esc_fila()  #Escoger a qué fila va a ir
        
        if fila == 'CC':
            if self.num_ser_disp_CC > 0:
                self.acm_q_CC += 1
                self.num_ser_disp_CC -= 1   #Desmarcar un servidor como disponible
                
                if self.eventos[3][0] == 10**30:
                    self.eventos[3].pop(0)
                    
                self.eventos[3].append(self.reloj + self.TIEMPO_CC) #Programar la salida de la fila
            else:
                self.num_cl_q_CC += 1   #Se suma la persona a la fila
                self.arrival_q_CC.append(self.reloj)
                
        elif fila == 'S':
            if self.num_ser_disp_S > 0:
                self.acm_q_S += 1
                self.num_ser_disp_S -= 1   #Desmarcar un servidor como disponible
                self.eventos[2] = self.reloj + self.TIEMPO_S #Programar la salida de la fila
            else:
                self.num_cl_q_S += 1    #Ponerlo en la fila
                self.arrival_q_S.append(self.reloj) #Guardar su tiempo de llegada
            
        return
    
    def salida_S(self):
        '''
        Esta función simula la rutina cuando un cliente termina de ser atendido en la fila de Sandwiches
        '''
        if self.num_cl_q_S > 0: #Verifica si hay personas en cola
            self.num_cl_q_S -= 1    #Se quita una persona de la cola
            self.total_delay_S += self.reloj - self.arrival_q_S[0]  #Actualizar estadísticos
            self.acm_q_S += 1
            self.eventos[2] = self.reloj + self.TIEMPO_S    #Programar siguiente salida
            self.arrival_q_S.pop(0) #Actualizar los tiempos de llegada
        else:
            self.num_ser_disp_S += 1    #Liberar un servidor
            self.eventos[2] = 10**30    #Se deja a futuro la siguiente salida
        
        self.tipo_q_T.append('S')   #El cliente pasa a la fila de las mesas
        self.asignar_mesa() #Se trata de asignarle una mesa
        
        return
    
    def salida_CC(self):
        '''
        Esta función simula la rutina cuando un cliente termina de ser atendido en la fila de Sandwiches
        '''
        if self.num_cl_q_CC > 0: #Verifica si hay personas en cola
            self.num_cl_q_CC -= 1    #Se quita una persona de la cola
            self.total_delay_CC += self.reloj - self.arrival_q_CC[0]  #Actualizar estadísticos
            self.acm_q_CC += 1
            
            #Programar siguiente salida
            self.eventos[3].pop(0)  #Quitar evento actual 
            self.eventos[3].append(self.reloj + self.TIEMPO_CC)   #Añadir próximo evento
            
            self.arrival_q_CC.pop(0) #Actualizar los tiempos de llegada
        else:
            self.num_ser_disp_CC += 1    #Liberar un servidor
            
            self.eventos[3].pop(0) #Quitar el evento actual
            if not self.eventos[3]:
                self.eventos[3].append(10**30) #Se deja al futuro la próxima salida
        
        self.tipo_q_T.append('CC')   #El cliente pasa a la fila de las mesas
        self.asignar_mesa() #Se trata de asignarle una mesa
        
        return
        
    def asignar_mesa(self):
        '''
        Esta función simula el intento de asignar una mesa a los clientes que salen de ser atendidos
        '''
        if self.num_disp_T > 0: #Verifica si hay mesas disponibles
            cliente = self.tipo_q_T.pop(0)  #Elimina el cliente de la fila
            
            # Programa la salida de la mesa y se guarda su tiempo de llegada           
            if cliente == 'S':
                self.arr_dep_T.append((self.reloj, self.reloj + self.generador_consumo_S()))
            elif cliente == 'CC':
                self.arr_dep_T.append((self.reloj, self.reloj + self.generador_consumo_CC()))
            
            # Se busca cual será la siguiente salida
            next_dep = self.arr_dep_T[0]  
            index = 0
            for i, ele in enumerate(self.arr_dep_T):
                if ele[1] < next_dep[1]:
                    next_dep = ele
                    index = i
                    
            self.eventos[4] = (next_dep[0], next_dep[1], index) # Se programa formalmente la siguiente salida
            self.num_disp_T -= 1
        return
      
    def salida(self):
        '''
        Esta función simula el evento de la salida de un cliente del sistema
        '''
        self.num_cl_atendidos += 1  # Actualiza estadísticos
        self.total_time_T += self.eventos[4][1] - self.eventos[4][0]   
        
        # Se libera una mesa
        self.num_disp_T += 1    
        self.arr_dep_T.pop(self.eventos[4][2]) 
        
        if self.tipo_q_T:   #Si hay personas esperando por una mesa, las asigna
            self.asignar_mesa()
        else:
            #Programar la siguiente salida
            if self.arr_dep_T:  #Verifica si hay mesas ocupadas aún
                next_dep = self.arr_dep_T[0]  
                index = 0
                
                for i, ele in enumerate(self.arr_dep_T):
                    if ele[1] < next_dep[1]:
                        next_dep = ele
                        index = i
                        
                self.eventos[4] = (next_dep[0], next_dep[1], index) # Se programa formalmente la siguiente salida
            else:
                self.eventos[4] = (10**30, 10**30, 0) #Dejar abierta la proxima salida al futuro
        
        return
        
    def main(self):
        '''
        Esta función se encarga de iniciar, ejecutar la simulación, y devolver el reporte sobre la misma.
        '''
        subrutina = [None, self.llegada, self.salida_S, self.salida_CC, self.salida]
        self.eventos[1] = self.generador_llegadas() #Programa el primer evento que sucederá: una llegada
        
        while self.num_cl_atendidos <= self.LIMITE_CL_ATENDIDOS:
            
            tiempos.append(self.reloj)
            states_cc.append(6-self.num_ser_disp_CC)
            states_s.append(1-self.num_ser_disp_S)
            states_t.append(self.num_disp_T)
            self.timing()    #Determina el siguiente tipo de evento a ejecutar
            
            self.update_stats() #Actualizar estadísticos
            
            subrutina[self.next_evento]()   #Ejecuta la subrutina del evento correspondiente
        
        
            
        return self.report()
    
nueva_sim = Cafeteria()
lista = nueva_sim.main()
grafica(tiempos,states_cc,color='blue')
grafica(tiempos,states_s,color='red')
grafica(tiempos,states_t,color='green')
# work = Workbook()
# worksheet = work.active
# worksheet['A1'] = "Iteración"
# worksheet['B1'] = lista[0]
# worksheet['C1'] = lista[2]
# worksheet['D1'] = lista[4]
# worksheet['E1'] = lista[6]
# worksheet['F1'] = lista[8]
# worksheet['G1'] = lista[10]
# worksheet['H1'] = lista[12]


# n = 15
# for _ in range(n):
#     print("it",_)
#     nueva_sim = Cafeteria()
#     lista = nueva_sim.main()
#     print(lista[1])
#     print(lista[3])
#     print(lista[5])
#     print(lista[7])
#     print(lista[9])
#     worksheet.append([_,lista[1],lista[3],lista[5],lista[7],lista[9],lista[11],lista[13]])


# work.save('Modelos_SIM_data_output.xlsx')
