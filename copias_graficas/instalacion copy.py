from random import random
import math
from openpyxl import Workbook
class Instalacion:
    def __init__(self):
        '''Constantes globales'''
        self.LIMITE_RELOJ = 1000
        self.IDLE = 1
        self.BUSY = 0

        '''Inicializar las variables de estado'''
        self.reloj: float = 0.0
        self.last_time: float = 0.0
        self.num_cl_q_1: int = 0
        self.num_cl_q_2: int = 0
        self.est_s_A1: tuple[int, str|None] = (self.IDLE, None)
        self.est_s_A2: tuple[int, str|None] = (self.IDLE, None)
        self.est_s_B: tuple[int, str|None] = (self.IDLE, None)
        self.next_evento: int = 0

        self.arrival_q_1: list[float] = []
        self.arrival_q_2: list[float] = []
        self.salida_prog_1: list[tuple[float, str]] = []
        self.eventos: list = [None, 10**30, (10**30, None, None), (10**30, None), self.LIMITE_RELOJ]

        '''Inicializar los estadísiticos'''
        self.acm_cl_q_1: int = 0
        self.acm_cl_q_2: int = 0
        self.area_q_1: float = 0.0
        self.area_q_2: float = 0.0
        self.total_delay_1: float = 0.0
        self.total_delay_2: float = 0.0
        self.area_cl1_SA1: float = 0.0
        self.area_cl2_SA1: float = 0.0
        self.area_cl1_SA2: float = 0.0
        self.area_cl2_SA2: float = 0.0
        self.area_cl1_SB: float = 0.0
        self.area_cl2_SB: float = 0.0
    
    def generador_llegada(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(1)
        '''
        u = random()
        l = 1
        return (math.log(1-u))/(-l)
    
    def esc_tipo(self):
        '''
        Esta función simula la probabilidad de establecer el tipo de un nuevo cliente que llega al sistema
        '''
        u = random()
        
        if u < 0.7:
            return 1
        return 2
    
    def generador_salida_1(self):
        '''
        Esta función genera un valor bajo una distribución ~ exp(0.8)
        '''
        u = random()
        l = 1/0.8
        return (math.log(1-u))/(-l)
    
    def generador_salida_2(self):
        '''
        Esta función genera un valor bajo una distribución ~U(0.5, 0.7)
        '''
        a = 0.5
        b = 0.7
        
        u = random()    
        return round(u*(b-a)+a,3)
         
    def escoger_serA(self):
        '''
        Esta función asigna homogeneamente usarios al servidor A1 o A2
        '''
        u = random()
        
        if u < 0.5:
            eleccion = 'A1'
        else:
            eleccion = 'A2'
        
        return eleccion
                  
    def timing(self):
        '''
        Esta función se encarga del manejo del reloj de la simulación
        '''
        
        self.next_evento = 0
        min_tiempo_next = 10**29
        
        #Buscar el evento más próximo dentro de la lista de eventos
        for i in range(1,5):
            if i == 2 or i == 3:
                t_potencial = self.eventos[i][0]  #Para obtener el tiempo dentro de las tuplas programadas
            else:
                t_potencial = self.eventos[i]
                
            if t_potencial < min_tiempo_next:
                min_tiempo_next = t_potencial
                self.next_evento = i
        
        # Mantener la integridad de las salidas tipo 1 programadas
        if self.next_evento == 2:
            self.buscar_prox_salida_1()
            if self.salida_prog_1:  
                self.salida_prog_1.pop(self.eventos[2][2])
            
        self.last_time = self.reloj
        
        self.reloj = min_tiempo_next    #Actualizar el reloj de la simulación

        return
    
    def update_stats(self):
        '''
        Esta función actualiza los estadísticos de áreas cada vez que se realiza un evento
        '''
        delta = self.reloj - self.last_time
        
        self.area_q_1 += delta*self.num_cl_q_1
        self.area_q_2 += delta*self.num_cl_q_2
        
        if self.est_s_A1[0] == self.BUSY:
            customer = self.est_s_A1[1]
            
            if customer == 1:
                self.area_cl1_SA1 += delta
            elif customer == 2:
                self.area_cl2_SA1 += delta
                
        if self.est_s_A2[0] == self.BUSY:
            customer = self.est_s_A2[1]
            
            if customer == 1:
                self.area_cl1_SA2 += delta
            elif customer == 2:
                self.area_cl2_SA2 += delta
                
        if self.est_s_B[0] == self.BUSY:
            customer = self.est_s_B[1]
            
            if customer == 1:
                self.area_cl1_SB += delta
            elif customer == 2:
                self.area_cl2_SB += delta
            
        return
    
    def report(self):
        '''
        Esta función genera el reporte de la simulación
        '''
        print('Numero clientes 1 atendidos: ', self.acm_cl_q_1)
        print('Numero clientes 1 cola: ', self.num_cl_q_1)
        print('Numero clientes 2 atendidos: ', self.acm_cl_q_2)
        print('Numero clientes 2 cola: ', self.num_cl_q_2)

        print('-------------END OF SIMULATION--------------')
        list1 = [self.total_delay_1/self.acm_cl_q_1,self.area_q_1/self.reloj,self.total_delay_2/self.acm_cl_q_2,self.area_q_2/self.reloj,(self.area_cl1_SA1/(self.area_cl1_SA1 + self.area_cl2_SA1))*100,(self.area_cl2_SA1/(self.area_cl1_SA1 + self.area_cl2_SA1))*100,(1 -(self.area_cl1_SA1 + self.area_cl2_SA1)/(self.reloj))*100,self.area_cl1_SA2/(self.area_cl1_SA2 + self.area_cl2_SA2)*100,self.area_cl2_SA2/(self.area_cl1_SA2 + self.area_cl2_SA2)*100,(1 -(self.area_cl1_SA2 + self.area_cl2_SA2)/(self.reloj))*100,self.area_cl1_SB/(self.area_cl1_SB + self.area_cl2_SB)*100,self.area_cl2_SB/(self.area_cl1_SB + self.area_cl2_SB)*100,(1 -(self.area_cl1_SB + self.area_cl2_SB)/(self.reloj))*100,self.reloj]  
        return list1
    
    def buscar_prox_salida_1(self):
        '''
        Esta función busca la menor salida tipo 1 programada y la coloca como evento en la lista de eventos
        '''
        
        if self.salida_prog_1: # Verifica si hay salida de tipo 1 que deban ser programadas
            min_time = self.salida_prog_1[0][0]
            siguiente = self.salida_prog_1[0]
            index = 0
            
            # Dentro de las salidas que aún no sean programadas, busca la más próxima
            for i, elem in enumerate(self.salida_prog_1):
                if elem[0] < min_time:
                    min_time = elem[0]
                    siguiente = elem
                    index = i
                    
            self.eventos[2] = (siguiente[0], siguiente[1], index)
            
        else:
            self.salida_prog_1.append((10**30, None))
            
        return
            
    def llegada(self):
        '''
        Esta función simula la llegada de un nuevo cliente al sistema
        '''
        self.eventos[1] = self.reloj + self.generador_llegada() #Programar siguiente llegada
        
        if self.esc_tipo() == 1:    #Verifica si es cliente tipo 1
            
            if self.est_s_A1[0] == self.IDLE or self.est_s_A2[0] == self.IDLE: #Verifica si hay algun servidor tipo A libre
                eleccion = self.escoger_serA() #Escoge aleatoriamente una prioridad para revisar primero la disponibilidad entre A1 y A2
                
                if eleccion == 'A1':
                    if self.est_s_A1[0] == self.IDLE:   #Verifica si el servidor A1 está libre
                        self.acm_cl_q_1 += 1    #Actualiza estadístico
                        self.est_s_A1 = (self.BUSY, 1)  #Cambia estado del servidor
                        self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A1'))   #Programa su salida
                        self.buscar_prox_salida_1()
                        
                    elif self.est_s_A2[0] == self.IDLE:
                        self.acm_cl_q_1 += 1    #Actualiza estadístico
                        self.est_s_A2 = (self.BUSY, 1)  #Cambia estado del servidor
                        self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A2'))  #Programa su salida
                        self.buscar_prox_salida_1()
                        
                elif eleccion == 'A2':                    
                    if self.est_s_A2[0] == self.IDLE: # Verifica si el servidor A2 está libre
                        self.acm_cl_q_1 += 1    #Actualiza estadístico
                        self.est_s_A2 = (self.BUSY, 1)  #Cambia estado del servidor
                        self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A2'))   #Programa su salida
                        self.buscar_prox_salida_1()
                    
                    elif self.est_s_A1[0] == self.IDLE:
                        self.acm_cl_q_1 += 1    #Actualiza estadístico
                        self.est_s_A1 = (self.BUSY, 1)  #Cambia estado del servidor
                        self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A1'))   #Programa su salida
                        self.buscar_prox_salida_1()
                        
            elif self.est_s_B[0] == self.IDLE: # Si ningún servidor A está libre, revisa B
                self.acm_cl_q_1 += 1    #Actualiza estadístico
                self.est_s_B = (self.BUSY, 1)  #Cambia estado del servidor
                self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'B'))   #Programa su salida
                self.buscar_prox_salida_1()
                
            else:
                self.num_cl_q_1 += 1    #Añadir el cliente a la fila
                self.arrival_q_1.append(self.reloj) #Agregar su llegada a la lista de tiempos
                
        else:
            if self.est_s_B[0] == self.IDLE: # Verifica si el servidor B está libre
                if self.est_s_A1[0] == self.IDLE or self.est_s_A2[0] == self.IDLE: #Revisa si hay al menos un servidor A libre
                    eleccion = self.escoger_serA()
                    
                    if eleccion == 'A1':
                        if self.est_s_A1[0] == self.IDLE:
                            self.acm_cl_q_2 += 1    #Actualiza estadístico
                            
                            #Cambia estado de servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A1 = (self.BUSY, 2)
                            
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A1')    #Programa su salida
                            
                        elif self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_2 += 1    #Actualiza estadístico
                            
                            #Cambia estado de servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A2 = (self.BUSY, 2)
                            
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A2')    #Programa su salida
                            
                    elif eleccion == 'A2':
                        if self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_2 += 1    #Actualiza estadístico
                            
                            #Cambia estado de servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A2 = (self.BUSY, 2)
                            
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A2')    #Programa su salida
                            
                        elif self.est_s_A1[0] == self.IDLE:
                            self.acm_cl_q_2 += 1    #Actualiza estadístico
                            
                            #Cambia estado de servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A1 = (self.BUSY, 2)
                            
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A1')    #Programa su salida

                else:
                    self.num_cl_q_2 += 1 # Lo suma a la fila
                    self.arrival_q_2.append(self.reloj) # Guarda su tiempo de llegada
                    
            else:
                self.num_cl_q_2 += 1    # Lo suma a la fila
                self.arrival_q_2.append(self.reloj) #Guarda su tiempo de llegada
                
        return
    
    def salida_1(self):
        '''
        Esta función simula la salida de un cliente tipo 1 del sistema
        '''
                   
        server = self.eventos[2][1] # Recuperar el tipo de servidor que estaba ocupado
       
        # Liberar el servidor ocupado
        if server == 'A1':
            self.est_s_A1 = (self.IDLE, None)
        elif server == 'A2':
            self.est_s_A2 = (self.IDLE, None)
        elif server == 'B':
            self.est_s_B = (self.IDLE, None)
            
        self.asignar_servidor()
        
        #Programar siguiente salida
        self.buscar_prox_salida_1()
        
        return
    
    def salida_2(self):
        '''
        Esta función simula la salida de un cliente tipo 2 del sistema
        '''
                   
        server = self.eventos[3][1] # Recuperar el tipo de servidor que estaba ocupado
       
        # Liberar los servidores ocupados
        self.est_s_B = (self.IDLE, None)
       
        if server == 'A1':
            self.est_s_A1 = (self.IDLE, None)
        elif server == 'A2':
            self.est_s_A2 = (self.IDLE, None)

        self.asignar_servidor()
        
        # Programar salida al futuro si no se programaron nuevas salidas
        if self.eventos[3][0] == self.reloj:
            self.eventos[3] = (10**30, None)
        
        return
    
    def asignar_servidor(self):
        '''
        Esta función se encarga de revisar si hay fila de cualquier tipo y asignar un cliente a los servidores libres luego de una salida'''
        
        def revisar_fila_1():
            '''
            Esta función revisa si hay fila de clientes de tipo 1 y si es posible atenderlos
            '''
            
            if self.num_cl_q_1 > 0: #Se revisa si hay fila de tipo 1
                
                if self.est_s_A1[0] == self.IDLE or self.est_s_A2[0] == self.IDLE: # Verificar si algún servidor A está libre
                    elecccion = self.escoger_serA() # Escoge aleatoriamente cual servidor A revisar primero
                    
                    if elecccion == 'A1':
                
                        #Se revisa la dsiponibilidad de los servidores
                        if self.est_s_A1[0] == self.IDLE:   
                            self.acm_cl_q_1 += 1    #Actualizar estadístico
                            self.total_delay_1 += self.reloj - self.arrival_q_1[0]
                            
                            self.num_cl_q_1 -= 1    #Se quita un nuevo cliente de la fila
                            self.arrival_q_1.pop(0)
                            
                            self.est_s_A1 = (self.BUSY, 1)  #Se cambia el estado del servidor  
                            
                            self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A1')) #Se programa la respectiva salida
                            self.buscar_prox_salida_1()

                            
                        elif self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_1 += 1    #Actualizar estadístico
                            self.total_delay_1 += self.reloj - self.arrival_q_1[0]
                            
                            self.num_cl_q_1 -= 1    #Se quita un nuevo cliente de la fila
                            self.arrival_q_1.pop(0)
                            
                            self.est_s_A2 = (self.BUSY, 1)  #Se cambia el estado del servidor  
                            
                            self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A2')) #Se programa la respectiva salida
                            self.buscar_prox_salida_1()
                            
                    elif elecccion == 'A2':
                        if self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_1 += 1    #Actualizar estadístico
                            self.total_delay_1 += self.reloj - self.arrival_q_1[0]
                            
                            self.num_cl_q_1 -= 1    #Se quita un nuevo cliente de la fila
                            self.arrival_q_1.pop(0)
                            
                            self.est_s_A2 = (self.BUSY, 1)  #Se cambia el estado del servidor  
                            
                            self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A2')) #Se programa la respectiva salida
                            self.buscar_prox_salida_1()
                            
                        elif self.est_s_A1[0] == self.IDLE:   
                            self.acm_cl_q_1 += 1    #Actualizar estadístico
                            self.total_delay_1 += self.reloj - self.arrival_q_1[0]
                            
                            self.num_cl_q_1 -= 1    #Se quita un nuevo cliente de la fila
                            self.arrival_q_1.pop(0)
                            
                            self.est_s_A1 = (self.BUSY, 1)  #Se cambia el estado del servidor  
                            
                            self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'A1')) #Se programa la respectiva salida
                            self.buscar_prox_salida_1()
                
                elif self.est_s_B[0] == self.IDLE: # Si ningún A estaba libre, revisa si el B está libre
                    self.acm_cl_q_1 += 1    #Actualizar estadístico
                    self.total_delay_1 += self.reloj - self.arrival_q_1[0]
                    
                    self.num_cl_q_1 -= 1    #Se quita un nuevo cliente de la fila
                    self.arrival_q_1.pop(0)
                    
                    self.est_s_B = (self.BUSY, 1)  #Se cambia el estado del servidor  
                    
                    self.salida_prog_1.append((self.reloj + self.generador_salida_1(), 'B')) #Se programa la respectiva salida
                    self.buscar_prox_salida_1()
                
                else:
                    raise Exception('Error!!! No se ejecutó la simulación. No se logró asignar un servidor a un cliente tipo 1.')
            
            else:
                
                #Revisa si hay salidas tipo 1 pendientes por programar
                self.buscar_prox_salida_1()
                
                #Si no hay salida, se programa al futuro
                if not self.salida_prog_1:
                    self.eventos[2] = (10**30, None)    # Se deja abierto a futuro la siguiente salida
                
            return
    
        
        if self.num_cl_q_2 > 0: # Revisa si hay clientes de tipo 2, porque ellos tienen prioridad
            if self.est_s_B[0] == self.IDLE:# Revisa si el servidor B está libre
                
                if self.est_s_A1[0] == self.IDLE or self.est_s_A2[0] == self.IDLE: # Verifica si algún servidor A está libre
                    eleccion = self.escoger_serA() # Escoge aleatoriamente cual servidor A revisar primero
                    
                    if eleccion == 'A1':
                        if self.est_s_A1[0] == self.IDLE:
                            self.acm_cl_q_2 += 1 # Actualizar estadísticos
                            self.total_delay_2 += self.reloj - self.arrival_q_2[0]  
                            
                            # Se quita un cliente tipo 2 de la fila
                            self.num_cl_q_2 -= 1 
                            self.arrival_q_2.pop(0)
                            
                            # Se cambia el estado de los servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A1 = (self.BUSY, 2)
                            
                            # Se programa la siguiente salida
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A1')
                        
                        elif self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_2 += 1 # Actualizar estadístico
                            self.total_delay_2 += self.reloj - self.arrival_q_2[0]
                            
                            self.num_cl_q_2 -= 1 # Se quita un cliente tipo 2 de la fila
                            self.arrival_q_2.pop(0)
                            
                            # Se cambia el estado de los servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A2 = (self.BUSY, 2)
                            
                            # Se programa la siguiente salida
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A2')
                            
                    elif eleccion == 'A2':
                        if self.est_s_A2[0] == self.IDLE:
                            self.acm_cl_q_2 += 1 # Actualizar estadístico
                            self.total_delay_2 += self.reloj - self.arrival_q_2[0]
                            
                            self.num_cl_q_2 -= 1 # Se quita un cliente tipo 2 de la fila
                            self.arrival_q_2.pop(0)
                            
                            # Se cambia el estado de los servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A2 = (self.BUSY, 2)
                            
                            # Se programa la siguiente salida
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A2')
                            
                        elif self.est_s_A1[0] == self.IDLE:
                            self.acm_cl_q_2 += 1 # Actualizar estadísticos
                            self.total_delay_2 += self.reloj - self.arrival_q_2[0]  
                            
                            # Se quita un cliente tipo 2 de la fila
                            self.num_cl_q_2 -= 1 
                            self.arrival_q_2.pop(0)
                            
                            # Se cambia el estado de los servidores
                            self.est_s_B = (self.BUSY, 2)
                            self.est_s_A1 = (self.BUSY, 2)
                            
                            # Se programa la siguiente salida
                            self.eventos[3] = (self.reloj + self.generador_salida_2(), 'A1')
                                
                else:
                    revisar_fila_1()
                    
            else:
                revisar_fila_1()   
                
        else:
            revisar_fila_1()
        return   
        
    def main(self):
        '''
        Esta función se encarga de iniciar, ejecutar la simulación, y devolver el reporte sobre la misma.
        '''
        subrutina = [None, self.llegada, self.salida_1, self.salida_2]
        self.eventos[1] = self.generador_llegada() #Programa el primer evento que sucederá: una llegada
        
        while True:
            self.timing()    #Determina el siguiente tipo de evento a ejecutar
            
            self.update_stats() #Actualiza las estadísticos
            
            if self.next_evento == 4:
                break

            subrutina[self.next_evento]()   #Ejecuta la subrutina del evento correspondiente
            
        
            
        return self.report()   # Genera el reporte de la simulación
    
nueva_sim = Instalacion()
lista = nueva_sim.main()
work = Workbook()
worksheet = work.active
#worksheet.append(lista)
def asign_cell(count=1,lista=[]):
    cr1 = 65
    cr2 = ''
    for _ in lista:
        cell = (''.join([chr(cr1),cr2,str(count)]))
        print(cell)
        worksheet[cell] = _
        if cr1 < 89:
            cr1 += 2
        else:
            cr1 = 65
            cr2 = 'A'

n = 15
for i in range(n):
    nueva_sim = Instalacion()
    lista = nueva_sim.main()
    asign_cell(i+1,lista)


work.save('Modelos_SIM_data_output.xlsx')
