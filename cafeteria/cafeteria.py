from random import random
import math

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
        self.eventos: list = [None, 10**30, 10**30, [10**30], 10**30]

        '''Inicializar los estadísiticos'''
        self.num_cl_atendidos: int = 0
        self.acm_q_CC: int = 0
        self.acm_q_S: int = 0
        self.area_numq_CC: float = 0.0
        self.area_numq_S: float = 0.0
        self.total_delay_CC: float = 0.0
        self.total_delay_S: float = 0.0
        self.total_time_T: float = 0.0


    def generador_llegadas():
        '''
        Esta función genera un valor bajo una distribución ~U(5, 15)
        '''
        a = 5
        b = 15
        
        u = random()    
        return round(u*(b-a)+a,3)

    def esc_fila():
        '''
        Esta función simula la decisión de qué fila escoger
        '''
        u = random()
        if u < 0.8:
            return 'CC'
        return 'S'

    def generador_consumo_CC():
        '''
        Esta función genera un valor bajo una distribución ~U(1200, 2400)
        '''
        a = 1200
        b = 2400
        
        u = random()    
        return round(u*(b-a)+a,3)

    def generador_consumo_S():
        '''
        Esta función genera un valor bajo una distribución ~U(600, 1200)
        '''
        a = 600
        b = 1200
        
        u = random()    
        return round(u*(b-a)+a,3)
        
    def timing(self):
        '''
        Esta función se encarga del manejo del reloj de la simulación'''
        
        self.next_evento = 0
        min_tiempo_next = 10**29
        
        for i in range(1,5):
            if i == 3:
                t_potencial = self.eventos[3][0]   #Para obetener la primera salida_CC dentro de las programadas
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
        delta = self.reloj - self.last_time
        self.area_numq_CC += delta * self.num_cl_q_CC
        self.area_numq_S += delta * self.num_cl_q_S
        
        return

    def report(self):
        print('-------------END OF SIMULATION--------------')
        print(f"\n\nAverage delay in queue 'Comida Caliente' {self.total_delay_CC/self.num_cl_q_CC} seconds, equivalent to {self.total_delay_CC/self.num_cl_q_CC/60} minutes\n\n")
        print(f"\n\nAverage number in queue 'Comida Caliente' {self.area_numq_CC/self.reloj} \n\n")
        print(f"\n\nAverage delay in queue 'Sandwiches' {self.total_delay_S/self.num_cl_q_S} seconds, equivalent to {self.total_delay_S/self.num_cl_q_S/60} minutes\n\n")
        print(f"\n\nAverage number in queue 'Sandwiches' {self.area_numq_S/self.reloj} \n\n")
        print(f"\n\nAverage time in table {self.total_time_T/self.num_cl_atendidos} seconds, equivalent to {self.total_time_T/self.num_cl_atendidos/60} minutes \n\n")
        print(f"\n\nTime simulation ended {self.reloj/3600} hours \n\n")
        
                
    def main(self):
        '''
        Esta función se encarga de iniciar, ejecutar la simulación, y devolver el reporte sobre la misma.
        '''
        subrutina = [None, self.llegada, self.salida_S, self.salida_CC, self.salida]
        self.eventos[1] = self.generador_llegadas() #Programa el primer evento que sucederá: una llegada
        
        while self.num_cl_atendidos <= self.LIMITE_CL_ATENDIDOS:
            self.timing()    #Determina el siguiente tipo de evento a ejecutar
            
            self.update_stats() #Actualizar estadísticos
            
            subrutina[self.next_evento]()   #Ejecuta la subrutina del evento correspondiente
        
        self.report()
            
        pass
        