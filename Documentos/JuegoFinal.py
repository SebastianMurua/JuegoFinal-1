import pilas
pilas.iniciar()
from pilas.escena import Normal
import random
import ConfigParser

class EscenaDeMenu(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        Fondo= pilas.imagenes.cargar("personajes/fotomenu.jpg")
        fondo1= pilas.fondos.Fondo(Fondo)
        self.crear_menu()

    def crear_menu(self):

        def comienza_juego():
            pilas.cambiar_escena(EscenaDeJuego())

        def creditos():
            pilas.cambiar_escena(EscenaDeCredito())
    
        def ayuda():
            pilas.cambiar_escena(EscenaDeAyuda())

        def salir():
            import sys
            sys.exit(0)

        menu = pilas.actores.Menu([('Comenzar a jugar', comienza_juego),
                                        ('ayuda', ayuda),
                                        ('creditos', creditos),
                                        ('Salir', salir)
                                        ])

#______________________________________AYUDA___________________________________________________________#
class EscenaDeAyuda(pilas.escena.Base): 

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        Fondo=pilas.imagenes.cargar("personajes/bob marley.jpg")
        fondo1= pilas.fondos.Fondo(Fondo)
        texto=pilas.actores.Texto("""
Este juego es muy facil de jugar y divertido 
solo tenes que esquivar los autos que vienen
en sentido contrario, no podes tocar el pasto
y solo podes ir para adelante sino perdes
suerteeeeee !!! 
        """)
        texto.x= 30 
        texto.y = 250

        pilas.avisar("Presiona 'P' para regresar al menu")    
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'p':
            pilas.cambiar_escena(EscenaDeMenu())

pilas.cambiar_escena(EscenaDeAyuda())  
    
#______________________________________CREDITOS_______________________________________________________#
class EscenaDeCredito(pilas.escena.Base): 

    def __init__(self):
        pilas.escena.Base.__init__(self)
            
    def iniciar (self):
        Fondo=pilas.imagenes.cargar("personajes/bob marley.jpg")
        fondo1= pilas.fondos.Fondo(Fondo)
        texto=pilas.actores.Texto("creado por: Flores Matias, Ceballos Luciano")
        pilas.avisar("Presiona 'P' para regresar al menu")       

        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'p':
            pilas.cambiar_escena(EscenaDeMenu())

pilas.cambiar_escena(EscenaDeCredito())    
#_________________________________________JUEGO_____________________________________________________#
class EscenaDeJuego(pilas.escena.Base): 

    def __init__(self,puntaje="0"):
        pilas.escena.Base.__init__(self)
        self.puntos = puntaje
        self.autitosmalos= []
    
    def iniciar(self):
        Fondo2=pilas.imagenes.cargar("personajes/fotojuego.png")
        fondo3= pilas.fondos.Fondo(Fondo2)
        self.puntaje=pilas.actores.Puntaje(x=280, y=200)
        self.puntaje.color = pilas.colores.blanco

        def aumentar(puntaje):
            puntaje.aumentar(10)
            return True
        self.aumentar = pilas.mundo.agregar_tarea(5, aumentar, self.puntaje)

#______auto que esquiba a los otros autos_________________________________________________________________#
        protagonista = pilas.imagenes.cargar("personajes/ferrary.png") 
        autobueno= pilas.actores.Actor(protagonista)#este es el auto numero 1
        autobueno.x=0
        autobueno.y=-20
        autobueno.aprender(pilas.habilidades.MoverseConElTeclado)
        autobueno.aprender(pilas.habilidades.SeMantieneEnPantalla)
        autobueno.aprender(pilas.habilidades.PuedeExplotar)
        autobueno.radio_de_colision =30
  
#_____________________funcion para que salgan los autos__________________________________________#        
        def salir() :
            carril= random.choice((116,0,-116))
            y=240
            duracion=random.choice((1.5 , 2 , 2.2 , 2.5, 2.7 , 3 ))
            auto=random.choice(("personajes/autito.png","personajes/cinqaaue.png"))   
            nombre=pilas.imagenes.cargar(auto)               
            autito=pilas.actores.Actor(nombre,x=carril,y=y)
            autito.y = pilas.utils.interpolar(-400, duracion=duracion)
            autito.aprender(pilas.habilidades.PuedeExplotar)
            autito.radio_de_colision = 30
            self.autitosmalos.append(autito)
#__________________________________________________Colision__________________________________________#
            def cuando_colisionan(autobueno,autito):
                for i in range(len(self.autitosmalos)):
                    self.autitosmalos[i].eliminar()
                autobueno.eliminar()
                pilas.escena_actual().tareas.eliminar_todas()
                Fondo= pilas.imagenes.cargar("personajes/autos.jpg")
                fondo_perdedor= pilas.fondos.Fondo(Fondo)
                texto3=pilas.actores.Texto("Tu ultimo puntaje es : " + self.puntaje.obtener_texto())
                texto3.y=70
                texto3.color = pilas.colores.verde 
                textoo=pilas.actores.Texto("Termino el juego mas suerte para la proxima ")
                textoo.y=130
                textoo.color = pilas.colores.amarillo
 #___________________________________menu de colision_____________________________________________#
                
                def iniciar_juego_de_nuevo(): #Inicia de nuevo el juego
                    pilas.cambiar_escena(EscenaDeJuego())
                def volver_menu(): #Vuelve al menu principal
                    pilas.mundo.motor.mostrar_puntero_del_mouse()
                    pilas.cambiar_escena(EscenaDeMenu())
                def salir_del_juego(): #sale del juego
                    pilas.terminar()
                def guarda_puntaje():
                    pilas.mundo.motor.mostrar_puntero_del_mouse()
                    puntaje = self.puntaje.obtener_texto()
                    pilas.cambiar_escena(GuardarPuntaje(puntaje))
               
                menu = pilas.actores.Menu([("Reiniciar juego", iniciar_juego_de_nuevo),
                                           ("Volver al menu principal", volver_menu),
                                           ("Guardar puntaje", guarda_puntaje),
                                           ("Salir", salir_del_juego),
                                          ]) 
               
            pilas.escena_actual().colisiones.agregar(autobueno, autito, cuando_colisionan)  
            return True     
        self.salir = pilas.mundo.agregar_tarea(1, salir) 
#_______________Guarda el puntaje_________________________________________________________________#

class GuardarPuntaje(pilas.escena.Base):
    def __init__(self, puntaje):
        pilas.escena.Base.__init__(self)
        self.puntaje = puntaje        
    def iniciar(self):        
        Fondo= pilas.imagenes.cargar("personajes/fotomenu.jpg")
        fondo1= pilas.fondos.Fondo(Fondo)
        titulo = pilas.actores.Texto("Ingresa tu  nombre." + "Tu puntaje es: " + str(self.puntaje))        
        ingreso = pilas.interfaz.IngresoDeTexto()  
        ingreso.y = -50
        boton = pilas.interfaz.Boton("Enviar")
        boton.y = -100

        def crear():
            try:
                ar = open("puntajes.ini", 'r')
                cosas = ar.read()
                ar.close()
                arch = open("puntajes.ini", 'r+')
                arch.write(cosas + "\n" + str(ingreso.texto) + "," +str(self.puntaje))
                arch.close
                pilas.cambiar_escena(EscenaDeMenu())

            except:
                arch = open("puntajes.ini", 'r+')
                arch.write(str(ingreso.texto) + "," +str(self.puntaje))
                arch.close()
                pilas.cambiar_escena(EscenaDeMenu())

            
        boton.conectar(crear)
#______________________________________________volver al menu______________________________________________________#
        
        pilas.eventos.pulsa_tecla.conectar(self.cuando_pulsa_tecla)
    def cuando_pulsa_tecla(self, evento):
        if evento.texto == u'p':
            pilas.cambiar_escena(EscenaDeMenu())
#__________________________________________________________________________________________________________________#
# Carga la nueva escena
pilas.cambiar_escena(EscenaDeMenu())

pilas.ejecutar()
