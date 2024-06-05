########################################################################################
# PROYECTO FINAL DE PYTHON "PIENSA RAPIDO"           FECHA DE INICIO: 10/05/2024       #
# PROGRAMADORES:                                     FECHA DE FINALIZACION: 03/06/2024 #
# 1.- LESLY GALLARDO GONZALEZ      MATRICULA: 370027                                   #
# 2.- RAUL ARAM VAZQUEZ FIGUEROA   MATRICULA: 370132                                   #
# DESCRIPCION: Juego tipo cuestionario sobre preguntas basicas de matematicas para     #
# niños de entre 8 a 10 años de edad.                                                  #
# El juego inicia al presionar "iniciar" en el menu, seguido de esto apareceran las    # 
# instrucciones del juego y despues el contador comenzara. El participante tiene 1     #
# minuto para contestar  20 preguntas correctamente. Es un 1 punto por pregunta        #
# correcta. Trata de hacer la mayor cantidad de puntos posibles                        #
########################################################################################

# ---------- LIBRERIAS ---------- #
import tkinter as tk 
import pygame #importar desde el CMD
import time 
import threading 
from tkinter import messagebox
from PIL import ImageTk, Image #importar desde el CMD

# ---------- ESTRUCTURA DE PAGINAS ---------- #
class Mi_Juego(tk.Tk):
    def __init__(self):
        super().__init__()
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.geometry("1000x630")
        self.resizable(0, 0)
        self.pages = {}
        self.current_page = None
        self.limite_tiempo = 60
        self.cronometro_label = tk.Label(self.container, text="Tiempo: 0 s", font = ("Helvetica", 12))
        self.cronometro_label.pack()
        self.puntaje = 0
        self.after_id = None
        self.cronometro_en_ejecucion = False
        pygame.mixer.init()  
        self.musica_menu()
        
        self.mostrar_pag(pag1)
        
    def iniciar_cronometro(self, iniciar=False):
        if iniciar:
            self.tiempo = 0
            self.cronometro_en_ejecucion = True  # Marcar el cronómetro como en ejecución
            self.actualizar_cronometro ()
        else:
            self.tiempo = -1
            self.cronometro_en_ejecucion = False 
            self.actualizar_cronometro ()
        
    def detener_cronometro(self):
        self.cronometro_en_ejecucion = False # Detener el cronometro
        
    def actualizar_cronometro(self):
        self.tiempo += 1
        #print(f"Tiempo actualizado: {self.tiempo}")  # línea para imprimir el tiempo
        self.cronometro_label.config(text=f"Tiempo: {self.tiempo} s")

        if self.tiempo < self.limite_tiempo and self.cronometro_en_ejecucion:
            self.after_id = self.after(1000, self.actualizar_cronometro)

        if self.tiempo >= self.limite_tiempo:
            self.avanzar_a_pagina_final()
        
    def reiniciar_cronometro(self):
        self.detener_cronometro()  # Detener cualquier instancia anterior del cronómetro
        #print("Cronómetro detenido")
        self.tiempo = 0  # Restablecer el tiempo a cero
        #print("Tiempo reiniciado")
        if self.after_id:
            self.after_cancel(self.after_id)  # Cancelar cualquier evento pendiente de actualización del cronómetro
            #print("Evento de actualización cancelado")

    def mostrar_pag(self, pagina):
        if pagina not in self.pages:
            self.pages[pagina] = pagina(self.container, self)
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[pagina]
        self.current_page.pack(expand=True, fill="both")

        if hasattr(self.current_page, "on_show"):
            self.current_page.on_show()
            
    def avanzar_a_pagina_final(self):
        self.detener_cronometro()
        pygame.mixer.music.stop()
        messagebox.showwarning ("TIEMPO", "SE ACABO EL TIEMPO!!!")
        self.mostrar_pag(pag28)
        
    def aumentar_puntaje (self):
        self.puntaje = self.puntaje + 1
        
    def obtener_puntaje (self):
        return self.puntaje
    
    def reiniciar_puntaje (self):
        self.puntaje = 0
        
    def musica_menu(self):
        pygame.mixer.music.load("IMGS_proyecto/MainMenu.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.6)
        
    def musica_preparacion (self):
        pygame.mixer.music.load ("IMGS_proyecto/Preparados.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.95)
        
    def musica_juego (self):
        pygame.mixer.music.load ("IMGS_proyecto/TLT.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.95)
                
# ---------- MENU PRINCIPAL (PAG 1) ---------- #
class pag1 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
    
        def salir (): #funcion que cierra la aplicacion
            resp = tk.messagebox.askquestion ("CONFIRMACION", "Seguro que quieres salir?")
            if resp == "yes":
                self.controller.destroy ()
            
        def iniciar (): #funcion que inicia el juego 
                self.controller.mostrar_pag (pag2)
        
        self.img_menu = ImageTk.PhotoImage(Image.open("IMGS_proyecto/Menu_Principal.jpg").resize((980, 590), Image.LANCZOS)) #imagen del menu
        lbl_img = tk.Label (self, image = self.img_menu)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton_jugar = ImageTk.PhotoImage(Image.open("IMGS_boton/B_jugar.png").resize((340, 35), Image.LANCZOS)) #imagen del boton iniciar
        self.boton1 = tk.Button (self, image = self.img_boton_jugar, command = iniciar, bd = 0, highlightthickness= 0)
        self.boton1.place (x = 332, y = 370)
    
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))

        self.img_boton_salida = ImageTk.PhotoImage(Image.open("IMGS_boton/B_fuera.jpg").resize((110, 100), Image.LANCZOS)) #imagen del boton salir
        self.boton2 = tk.Button (self, image = self.img_boton_salida, command = salir, bd = 0, borderwidth= 0, highlightthickness = 0)        
        self.boton2.place (x = 860, y = 15)
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))
        
    def reproducir_sonido (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/boton parcial.mp3")  
            sonido.play()
            
    def on_show(self):
        self.controller.musica_menu()
            
# ---------- INSTRUCCIONES (PAG 2) ---------- #
class pag2 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        
        def regresar ():
            self.controller.mostrar_pag (pag1)
            
        def avanzar ():
            self.controller.mostrar_pag (pag3)
        
        self.img_instrucciones = ImageTk.PhotoImage(Image.open("IMGS_proyecto/Instrucciones.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_instrucciones)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton_regresar = ImageTk.PhotoImage(Image.open("IMGS_boton/B_regresar.jpg").resize((110, 55), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton_regresar, command = regresar, bd = 0, borderwidth= 0, highlightthickness = 0)        
        self.boton2.place (x = 35, y = 14)
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))
        
        self.img_boton_continuar = ImageTk.PhotoImage(Image.open("IMGS_boton/B_continuar.jpg").resize((215, 30), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton_continuar, command = avanzar, bd = 0, highlightthickness= 0)
        self.boton1.place (x = 380, y = 545)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))
        
    def reproducir_sonido (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/boton parcial.mp3")  
            sonido.play()
            
# ---------- PREPARACION (PAG 3) ---------- #
class pag3 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        
        def regresar ():
            self.controller.mostrar_pag (pag2)
            
        def avanzar ():
            self.controller.mostrar_pag (pag4)
        
        self.img_listo1 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/Listo.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_listo1)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton_regresar = ImageTk.PhotoImage(Image.open("IMGS_boton/B_regresar.jpg").resize((100, 55), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton_regresar, command = regresar, bd = 0, borderwidth= 0, highlightthickness = 0)        
        self.boton2.place (x = 35, y = 14)
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))
        
        self.img_boton_continuar = ImageTk.PhotoImage(Image.open("IMGS_boton/B_continuar.jpg").resize((215, 30), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton_continuar, command = avanzar, bd = 0, highlightthickness= 0)
        self.boton1.place (x = 375, y = 423)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido(self.controller))
        
    def reproducir_sonido (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/boton parcial.mp3")  
            sonido.play()
        
# ---------- PREPARACION (PAG 4) ---------- #
class pag4 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        pygame.mixer.music.stop()
        
        self.img_listo2 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/n3.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_listo2)
        lbl_img.place (x = 7, y = 0)
        
    def on_show(self):
        self.timer = self.after(1000, lambda: self.controller.mostrar_pag(pag5))
        self.controller.musica_preparacion()

    def on_hide(self):
        self.after_cancel(self.timer)
        
# ---------- PREPARACION (PAG 5) ---------- #
class pag5 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        
        self.img_listo3 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/n2.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_listo3)
        lbl_img.place (x = 7, y = 0)
        
    def on_show(self):
        self.timer = self.after(1000, lambda: self.controller.mostrar_pag(pag6))

    def on_hide(self):
        self.after_cancel(self.timer)

# ---------- PREPARACION (PAG 6) ---------- #
class pag6 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        
        self.img_listo4 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/n1.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_listo4)
        lbl_img.place (x = 7, y = 0)
        
    def on_show(self):
        self.timer = self.after(1000, lambda: self.controller.mostrar_pag(pag7))

    def on_hide(self):
        self.after_cancel(self.timer)
        
# ---------- PREPARACION (PAG 7) ---------- #
class pag7 (tk.Frame):
    def __init__ (self, parent, controller):
        super().__init__ (parent)
        self.controller = controller
        
        self.img_listo5 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/Go.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_listo5)
        lbl_img.place (x = 7, y = 0)
        
    def on_show(self):
        self.timer = self.after(1000, lambda: self.controller.mostrar_pag(pag8))

    def on_hide(self):
        self.after_cancel(self.timer)

# ---------- PREGUNTA 1 (PAG 8) ---------- #
class pag8 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        pygame.mixer.music.stop()
        self.controller.musica_juego ()
        
        self.img_p1 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p1.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p1)
        lbl_img.place (x = 7, y = 0)
            
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b1.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b16.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b18.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag(self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje()
        self.controller.mostrar_pag(pag9)
        
    def on_show(self):
        self.controller.tiempo = 0
        self.controller.iniciar_cronometro(iniciar=True)  # Inicia el cronómetro solo cuando esta página se muestra
        self.controller.musica_juego()
        #if self.controller.cronometro_en_ejecucion:  # Verifica si el cronómetro se ha iniciado correctamente
         #   print("Cronometro iniciado")
         
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
              
# ---------- PREGUNTA 2 (PAG 9) ---------- #
class pag9 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p2 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p2.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p2)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b11.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b10.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b15.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b11.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton2":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag10)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 3 (PAG 10) ---------- #
class pag10 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p3 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p3.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p3)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b1.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b3.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b2.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b4.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag11)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 4 (PAG 11) ---------- #
class pag11 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller

        self.img_p4 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p4.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p4)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b3.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b6.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b16.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag12)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 5 (PAG 12) ---------- #
class pag12 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p5 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p5.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p5)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b21.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b18.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b27.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b1.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton1":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag13)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 6 (PAG 13) ---------- #
class pag13 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p6 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p6.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p6)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b21.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b18.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b29.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton2":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag14)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 7 (PAG 14) ---------- #
class pag14 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p7 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p7.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p7)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b15.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b17.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b16.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton4":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag15)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 8 (PAG 15) ---------- #
class pag15 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p8 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p8.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p8)
        lbl_img.place (x = 7, y = 0)
    
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b15.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b17.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b20.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
    
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton4":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag16)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 9  (PAG 16) ---------- #
class pag16 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p9 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p9.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p9)
        lbl_img.place (x = 7, y = 0)
    
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b22.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b26.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b28.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b30.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag17)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 10 (PAG 17) ---------- #
class pag17 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p10 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p10.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p10)
        lbl_img.place (x = 7, y = 0)
    
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b10.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b15.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b2.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b5.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton1":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag18)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 11 (PAG 18) ---------- #
class pag18 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p11 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p11.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p11)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b11.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b25.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b20.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b10.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag19)
    
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 12 (PAG 19) ---------- #
class pag19 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p12 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p12.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p12)
        lbl_img.place (x = 7, y = 0)

        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b30.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b40.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b25.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b35.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton4":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag20)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
    
# ---------- PREGUNTA 13 (PAG 20) ---------- #
class pag20 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p13 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p13.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p13)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b12.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b16.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b18.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b14.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag21)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 14 (PAG 21) ---------- #
class pag21 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p14 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p14.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p14)
        lbl_img.place (x = 7, y = 0)
    
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b36.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b39.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b28.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b29.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton1":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag22)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 15 (PAG 22) ---------- #
class pag22 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p15 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p15.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p15)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b36.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b40.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b42.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b45.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag23)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()
        
# ---------- PREGUNTA 16 (PAG 23) ---------- #
class pag23 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p16 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p16.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p16)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b25.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b21.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b20.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b28.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton4":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag24)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 17 (PAG 24) ---------- #
class pag24 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p17 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p17.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p17)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b49.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b56.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b47.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b50.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton1":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag25)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 18 (PAG 25) ---------- #
class pag25 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p18 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p18.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p18)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b16.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b8.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b24.jpg").resize((200, 35), Image.LANCZOS)) #correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b32.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag26)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 19 (PAG 26) ---------- #
class pag26 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p19 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p19.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p19)
        lbl_img.place (x = 7, y = 0)

        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b56.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b64.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b60.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b50.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton1":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag27)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PREGUNTA 20 (PAG 27) ---------- #
class pag27 (tk.Frame):
    def __init__ (self, parent, controller):
        super(). __init__ (parent)
        self.controller = controller
        
        self.img_p20 = ImageTk.PhotoImage (Image.open("IMGS_proyecto/p20.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image = self.img_p20)
        lbl_img.place (x = 7, y = 0)
        
        self.img_boton1 = ImageTk.PhotoImage(Image.open("IMGS_boton/b84.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton1 = tk.Button (self, image = self.img_boton1, command = lambda: self.siguiente_pag ("boton1"), bd = 0, highlightthickness= 0)
        self.boton1.place (x = 535, y = 310)
        
        self.img_boton2 = ImageTk.PhotoImage(Image.open("IMGS_boton/b76.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton2 = tk.Button (self, image = self.img_boton2, command = lambda: self.siguiente_pag ("boton2"), bd = 0, highlightthickness= 0)
        self.boton2.place (x = 535, y = 405)
        
        self.img_boton3 = ImageTk.PhotoImage(Image.open("IMGS_boton/b81.jpg").resize((200, 35), Image.LANCZOS)) # correcta
        self.boton3 = tk.Button (self, image = self.img_boton3, command = lambda: self.siguiente_pag ("boton3"), bd = 0, highlightthickness= 0)
        self.boton3.place (x = 265, y = 310)
        
        self.img_boton4 = ImageTk.PhotoImage(Image.open("IMGS_boton/b74.jpg").resize((200, 35), Image.LANCZOS)) 
        self.boton4 = tk.Button (self, image = self.img_boton4, command = lambda: self.siguiente_pag ("boton4"), bd = 0, highlightthickness= 0)
        self.boton4.place (x = 265, y = 405)
        
        self.boton1.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton2.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
        self.boton3.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido1(self.controller))
        
        self.boton4.bind("<ButtonRelease-1>", lambda event: self.reproducir_sonido2(self.controller))
        
    def siguiente_pag (self, boton_presionado):
        if boton_presionado == "boton3":
            self.controller.aumentar_puntaje ()
        self.controller.mostrar_pag (pag28)
        
    def reproducir_sonido1 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Correcto.mp3")  
            sonido.play()
            
    def reproducir_sonido2 (self, controller):
            pygame.mixer.init()
            sonido = pygame.mixer.Sound("IMGS_proyecto/Incorrecto.mp3")  
            sonido.play()

# ---------- PANTALLA FINAL (PAG 28) ---------- #
class pag28(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        pygame.mixer.music.stop()
        self.controller.iniciar_cronometro (iniciar = False)
        self.img_gracias = ImageTk.PhotoImage(Image.open("IMGS_proyecto/Gracias.jpg").resize((980, 590), Image.LANCZOS))
        lbl_img = tk.Label(self, image=self.img_gracias)
        lbl_img.place(x=7, y=0)
        
    def on_show(self):
        pygame.mixer.music.stop()
        self.controller.reiniciar_cronometro()  # Reinicia el cronómetro al mostrar esta página
        puntos = self.controller.obtener_puntaje()
        if puntos < 20:
            messagebox.showinfo("PUNTUACION", f"TOTAL: {puntos} puntos !!! \nBuen intento  :)")
        else:
            messagebox.showinfo("PUNTUACION", f"TOTAL: {puntos} puntos !!! \nExcelente :)")
        self.timer = self.after(3000, lambda: self.controller.mostrar_pag(pag1))
        self.controller.reiniciar_puntaje()
        
    def on_hide(self):
        self.after_cancel(self.timer)

if __name__ == "__main__":
    ventana = Mi_Juego ()
    ventana.mainloop ()