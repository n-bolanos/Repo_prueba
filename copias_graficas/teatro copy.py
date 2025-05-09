from random import random
import math
from openpyxl import Workbook
class Teatro:

    def __init__(self):

        '''Constantes globales'''
        self.IDLE:int = 1
        self.BUSY:int = 0
        self.LIMITE_RELOJ = 480

        '''Inicializar las variables de estado'''
        self.reloj: float = 0.0
        self.num_cl_q_P: int = 0
        self.num_cl_q_T: int = 0
        self.disp_servidor: int = self.IDLE
        self.next_evento: int = 0

        self.arrival_q_P: list[float] = []
        self.arrival_q_T: list[float] = []
        self.eventos: list[float] = [None, 2, 3, 10**30, self.LIMITE_RELOJ]

        '''Inicializar los estadísiticos'''
        self.acm_q_P: int = 0
        self.acm_q_T: int = 0
        self.total_delay_P: float = 0.0
        self.total_delay_T: float = 0.0

    def generador_llegada_P(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(12)
        '''
        u = random()
        l = 1/12
        return (math.log(1-u))/(-l)
    
    def generador_llegada_T(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(10)
        '''
        u = random()
        l = 1/10
        return (math.log(1-u))/(-l)
    
    def generador_servicio_P(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(6)
        '''
        u = random()
        l = 1/6
        return (math.log(1-u))/(-l)

    def generador_servicio_T(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(5)
        '''
        u = random()
        l = 1/5
        return (math.log(1-u))/(-l)
    
    def timing(self):
        '''
        Esta función se encarga del manejo del reloj de la simulación
        '''
        
        self.next_evento = 0
        min_tiempo_next = 10**29

        #Buscar el evento mas cercano
        for i in range(1,5):
            t_potencial = self.eventos[i]
            if t_potencial < min_tiempo_next:
                min_tiempo_next = t_potencial
                self.next_evento = i
        
        self.reloj = min_tiempo_next    #Actualizar el reloj de la simulación
        return

    def report(self):
        '''
        Esta función genera el reporte de la simulación
        '''
        print('-------------END OF SIMULATION--------------')
        return [self.total_delay_P/self.acm_q_P,self.total_delay_T/self.acm_q_T,self.acm_q_P,self.acm_q_T,self.reloj]

    def llegada_P(self):
        '''
        Esta función simula la llegada en persona de un nuevo cliente al sistema
        '''

        self.eventos[1] = self.reloj + self.generador_llegada_P() #Programar la siguiente llegada

        if self.disp_servidor == self.IDLE: #Verifica si el servidor esta disponible
            self.acm_q_P += 1
            self.disp_servidor = self.BUSY  #Cambia estado del servidor
            self.eventos[3] = self.reloj+ self.generador_servicio_P() #Programa la salida
        else:
            self.num_cl_q_P += 1 #Se agrega una persona a al fila
            self.arrival_q_P.append(self.reloj) #se guarda su tiempo de llegada
        return
    
    def llegada_T(self):
        '''
        Esta función simula la llegada de una llamada al sistema
        '''

        self.eventos[2] = self.reloj + self.generador_llegada_T() #Programar la siguiente llegada

        if self.disp_servidor == self.IDLE: #Verifica si el servidor esta disponible
            self.acm_q_T += 1
            self.disp_servidor = self.BUSY  #Cambia estado del servidor
            self.eventos[3] = self.reloj+ self.generador_servicio_P() #Programa la salida
        else:
            self.num_cl_q_T += 1 #Se agrega una persona a al fila
            self.arrival_q_T.append(self.reloj) #se guarda su tiempo de llegada
        return

    def salida(self):
        '''
        Esta función simula la salida de un cliente de cualquier tipo del sistema
        '''

        if self.num_cl_q_P > 0: #Verifica si hay clientes en persona
            #Actualiza estadisticos
            self.acm_q_P += 1
            self.total_delay_P += self.reloj - self.arrival_q_P[0]

            self.arrival_q_P.pop(0) #Quitar registro de llegada de cliente que sale
            self.num_cl_q_P -=1 #Quitar el cliente de la fila
            self.eventos[3] = self.reloj + self.generador_servicio_P()  #Programa la siguiente salida

        elif self.num_cl_q_T > 0: #Verifica si hay clientes en linea telefonica
            #Actualiza estadisticos
            self.acm_q_T += 1
            self.total_delay_T += self.reloj - self.arrival_q_T[0]

            self.arrival_q_T.pop(0) #Quitar registro de llegada de cliente que sale
            self.num_cl_q_T -=1 #Quitar el cliente de la fila
            self.eventos[3] = self.reloj + self.generador_servicio_T()  #Programa la siguiente salida
        
        else:

            self.eventos[3] = 10**30 #Programa la siguiente salida a futuro
            self.disp_servidor = self.IDLE  #Actualizar el estado del servidor
        
        return
            
    def main(self):
        '''
        Esta función se encarga de iniciar, ejecutar la simulación, y devolver el reporte sobre la misma.
        '''
        subrutina = [None, self.llegada_P, self.llegada_T, self.salida]
        
        while True:
            self.timing()    #Determina el siguiente tipo de evento a ejecutar
            if self.next_evento == 4:
                break

            subrutina[self.next_evento]()   #Ejecuta la subrutina del evento correspondiente

        
        
            
        return self.report()
    
nueva_sim = Teatro()
lista = nueva_sim.main()
n = 15
work = Workbook()
worksheet = work.active
for _ in range(n):
    print("it",_)
    nueva_sim = Teatro()
    lista = nueva_sim.main()
    worksheet.append(lista)


work.save('Modelos_SIM_data_output.xlsx')