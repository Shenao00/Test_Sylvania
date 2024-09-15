import math
fs=float(0.3) #30% del factor de seguridad
HSP=float(4.5) #Horas sol pico
horas_uso=float(12)
Dod_Litio=0.8
Dod_Gel=0.5
class Panel:

    def __init__(self,potencia, tension):
        self.potencia= potencia
        self.tension= tension
        print("Se ha ingresado un panel solar de potencia {} W".format(self.potencia))

    def __str__(self):
        return 'Panel solar {} W'.format(self.potencia)

    def parameters(self):
        return {
            'Potencia': self.potencia,
            'tension': self.tension,
        }

    
class Bateria:

    def __init__(self,tipo, capacidad, tension):
        self.tipo=tipo
        self.capacidad= capacidad
        self.tension=tension
        self.energia=float(self.tension)*float(self.capacidad)
        if self.tipo=='Litio':
            self.E_Disponible=self.energia*Dod_Litio
        else:
            self.E_Disponible=self.energia*Dod_Gel
        print("Se ha ingresado una batería tipo {} de {} Ah a {} V y {} Wh de energía".format(self.tipo,self.capacidad,self.tension,self.energia))

    def __str__(self):
        return 'Bateria tipo {} de {} Ah a {} V y {} Wh de energía'.format(self.tipo,self.capacidad,self.tension,self.energia)
    def parameters(self):
        return {
            'tipo': self.tipo,
            'capacidad': self.capacidad,
            'tension': self.tension,
            'energia': self.energia,
            'E_Disponible' : self.E_Disponible
        }


class MPPT:

    def __init__(self,ref,PV_input12V,PV_input24V,P_Output12V,P_Output24V):
        self.ref=ref
        self.PV_input12V=PV_input12V
        self.PV_input24V= PV_input24V
        self.P_Output12V=P_Output12V
        self.P_Output24V=P_Output24V
        
        print("Se ha ingresado un MPPT con PV input {}W/12V, {}W/24V  y P output {}W/12V, {}W/24V ".format(self.PV_input12V,self.PV_input24V,self.P_Output12V,self.P_Output24V))

    def __str__(self):
        return 'MPPT con PV input {}W/12, {}W/24  y P output {}W/12V, {}W/24V'.format(self.PV_input12V,self.PV_input24V,self.P_Output12V,self.P_Output24V)
    def parameters(self):
        return {
            'Referencia': self.ref,
            'PV input W@12V': self.PV_input12V,
            'PV input W@24V': self.PV_input24V,
            'P output W@12V': self.P_Output12V,
            'P output W@24V': self.P_Output24V,
            
        }

#P23495=Panel(165,19.21)
#P26376=Panel(450,41.65)
#P26377=Panel(540,41.65)
#P40353=Panel(580,42.71)
#P40143=Panel(610,39.73)

#P25450=Bateria("Litio",36,12.8)
#P25451=Bateria("Litio",50,12.8)
#P29946=Bateria("Litio",75,12.8)

#P37578=Bateria("Gel",150,12)
#P25446=Bateria("Gel",200,12)
#P23235=Bateria("Gel",250,12)

#SC160=MPPT("SC160",200,400,80,160)
#SC200=MPPT("SC200",260,520,100,200)
#SC260=MPPT("SC260",400,800,130,260)
#SC300=MPPT("SC300",550,1100,150,300)


class Productos:

    def __init__(self):
        self.Bat_stock=[]
        self.Panel_stock=[]
        self.MPPT_stock=[]

    def agregar_bateria(self,b): #b será una batería
        self.Bat_stock.append(b.parameters())

    def agregar_panel(self,p): #p será un panel solar
        self.Panel_stock.append(p.parameters())

    def agregar_MPPT(self,m): #p será un panel solar
        self.MPPT_stock.append(m.parameters())
    
    def mostrar(self):
        for b in self.Bat_stock:
            print (b)
        for p in self.Panel_stock:
            print(p)
        for m in self.MPPT_stock:
            print(m)
    def mostrar_Baterias(self):
        for b in self.Bat_stock:
            print (b)
    def mostrar_Paneles(self):
        for p in self.Panel_stock:
            print(p)
    def mostrar_MPPT(self):
        for m in self.MPPT_stock:
            print(m)
    
    def calcular_energia_total(self):
        energia_total = sum(b['energia'] for b in self.Bat_stock)
        return energia_total





#P.mostrar()
    
class Carga:
    def __init__(self, p_luminaria, eficacia, autonomia, BaTip, Productos):
        self.p_luminaria = p_luminaria
        self.eficacia = eficacia
        self.autonomia = autonomia
        self.BaTip = BaTip
        self.Productos = Productos
        self.Panel = Productos.Panel_stock
        self.Bateria = [b for b in Productos.Bat_stock if b['tipo'] == BaTip]  # Filtra baterías según el tipo
        self.MPPT_stock = Productos.MPPT_stock
        self.energia_usada = int(self.p_luminaria) * horas_uso
        self.Pot_req = (self.energia_usada * (1 + fs) / HSP)
        self.mejor_bateria = None
        self.mejor_panel = None
        self.mejor_MPPT = None
        
        print ("El flujo luminoso es {} lm".format(int(self.p_luminaria)*int(self.eficacia)))

    def calculo_Panel(self, criterio='Potencia'):
        if not self.Panel:
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        Panel_seleccionado = []
    
        for modulo in self.Panel:
            actual = modulo.get(criterio)
            if actual >= self.Pot_req:
                Panel_seleccionado.append([modulo, 'Cantidad: ', 1, modulo['Potencia'] * 1])
            elif actual * 2 >= self.Pot_req:
                Panel_seleccionado.append([modulo, 'Cantidad: ', 2, modulo['Potencia'] * 2])
            elif actual * 3 >= self.Pot_req:
                Panel_seleccionado.append([modulo, 'Cantidad: ', 3, modulo['Potencia'] * 3])
            elif actual * 4 >= self.Pot_req:
                Panel_seleccionado.append([modulo, 'Cantidad: ', 4, modulo['Potencia'] * 4])
    
        if not Panel_seleccionado:
            print("No se encontraron opciones adecuadas de paneles.")
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        # Selecciona la mejor opción basada en tu criterio (cantidad mínima, etc.)
        mejor_panel = min(Panel_seleccionado, key=lambda x: (x[2], x[1])) if Panel_seleccionado else None
        self.mejor_panel=mejor_panel
    
        # Devuelve todas las opciones y la mejor opción
        return {'todas_opciones': Panel_seleccionado, 'mejor_opcion': mejor_panel}

    
    def calculo_Bateria(self, criterio1='energia'):
        if self.BaTip == "Litio" and float(horas_uso) / float(self.autonomia) >= Dod_Litio:
            criterio1 = 'E_Disponible'
        elif self.BaTip == "Gel" and float(horas_uso) / float(self.autonomia) >= Dod_Gel:
            criterio1 = 'E_Disponible'
    
        if not self.Bateria:
            print("No hay baterías del tipo especificado en el stock.")
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        Bateria_seleccionada = []
    
        for Celda in self.Bateria:
            relative = Celda.get(criterio1)
            if self.BaTip == 'Litio':
                if relative >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 1, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 1))])
                elif relative * 2 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 2, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 2))])
                elif relative * 4 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 4, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 4))])
                elif relative * 6 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 6, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 6))])
                elif relative * 8 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 8, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 8))])
            elif self.BaTip == 'Gel':
                if relative >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 1, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 1))])
                elif relative * 2 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 2, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 2))])
                elif relative * 4 >= (int(self.p_luminaria) * int(self.autonomia)):
                    Bateria_seleccionada.append([Celda, 'Cantidad: ', 4, 'DOD:{:.0%}'.format(self.energia_usada / (Celda['energia'] * 4))])
    
        if not Bateria_seleccionada:
            print("No se encontraron opciones adecuadas de baterías.")
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        # Selecciona la mejor opción basada en tu criterio (cantidad mínima, etc.)
        mejor_bateria = min(Bateria_seleccionada, key=lambda x: (x[2])) if Bateria_seleccionada else None
        self.mejor_bateria=mejor_bateria
        # Devuelve todas las opciones y la mejor opción
        return {'todas_opciones': Bateria_seleccionada, 'mejor_opcion': mejor_bateria}



    def calculo_MPPT(self):
        if not self.mejor_panel or not self.mejor_bateria:
            print("Primero debe calcular y seleccionar la mejor opción de panel y batería.")
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        cantidad_baterias = self.mejor_bateria[2]  # Cantidad de baterías seleccionadas
        if cantidad_baterias == 1:
            tension_sistema = 12
            potencia_panel = self.mejor_panel[3]  # Potencia total de los paneles seleccionados
            potencia_salida_requerida = self.p_luminaria  # Potencia de salida basada en la potencia de la luminaria
        else:
            tension_sistema = 24
            potencia_panel = self.mejor_panel[3]  # Potencia total de los paneles seleccionados
            potencia_salida_requerida = self.p_luminaria  # Potencia de salida basada en la potencia de la luminaria
    
        MPPT_seleccionado = []
    
        for mppt in self.MPPT_stock:
            if tension_sistema == 12:
                if mppt['PV input W@12V'] >= potencia_panel and mppt['P output W@12V'] >= int(potencia_salida_requerida):
                    MPPT_seleccionado.append(mppt)
            elif tension_sistema == 24:
                if mppt['PV input W@24V'] >= potencia_panel and mppt['P output W@24V'] >= int(potencia_salida_requerida):
                    MPPT_seleccionado.append(mppt)
    
        if not MPPT_seleccionado:
            print("No se encontraron MPPT adecuados para la configuración seleccionada.")
            return {'todas_opciones': [], 'mejor_opcion': None}
    
        # Selecciona la mejor opción basada en tu criterio
        mejor_mppt = min(MPPT_seleccionado, key=lambda x: (x['PV input W@12V'] if tension_sistema == 12 else x['PV input W@24V'])) if MPPT_seleccionado else None
        self.mejor_MPPT = mejor_mppt    
        # Devuelve todas las opciones y la mejor opción
        return {'todas_opciones': MPPT_seleccionado, 'mejor_opcion': mejor_mppt}
