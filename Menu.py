# PROJECTE EGRA: Grup 2
# MENU: Classe amb la qual l'usuari interacciona, on tria el circuit i el mode de joc,
#       i on es guarden les dades de la partida per fer un ranking i mostrar les estadístiques de l'ultima partida

import pygame as pg
import pygame_menu
from GraphicsEngine import GraphicsEngine
import pickle

class Menu:
    def __init__(self):
        self.GraphicsEngine = GraphicsEngine
     
        self.img2 = pygame_menu.baseimage.BaseImage("textures/mario.png")
        self.img2.scale(0.2,0.2)
        self.font = pygame_menu.font.FONT_MUNRO
        
        #variables graphicengine
        self.CIRCUIT = ['1']
        self.MODE = ['1']
        self.MUSICA = [True]
        self.EFECTES_SO = [True]
        
        self.CREDITS = [ "Videojoc creat per: Irina Moreno, Gerard Perales,","Nuria Hernandez, Oleguer Gregori i Ariadna De Vicente", "GRAU EN ENGINYERIA DE DADES","Entorns grafics de realitat augmentada, 2022"]
        self.INSTRUCCIONS = ["MODE LLIURE: El jugador realitza 3 voltes a contra rellotge al circuit escollit",
                            "MODE FANTASMA: El jugador podra competir contra el FINAL BOSS EGRA al circuit que elegeixis",
                            "Tecla W: Accelerar endevant",
                            "Tecla S: Accelerar enrere", 
                            "Barra Espaiadora: Frenar", 
                            "Tecla A: Girar cap a la dreta",  
                            "Tecla D: Girar cap a l'esquerra", 
                            "Tecla E: Canviar vista del joc a frontal/del darrere del cotxe", 
                            "Tecla Q: Canviar la camera del joc a una vista aerea"]
        
        #ranking i estadistiques
        self.ultima = []
        self.estadistiques = []
        self.ranking = []
        self.ll_1=[] 
        self.ll_2 = []
        self.ll_3 = []        
        self.top5_1 = []
        self.top5_2 = []
        self.top5_3 = []
        
    #funcions x guardar les tries de l'usuari
    def set_circuit(self, value, circuit):
        self.CIRCUIT[0] = circuit
        
    def set_mode(self, value, mode):
        self.MODE[0] = mode       
        
    def set_musica(self, value):
        if value:
            self.MUSICA = [True]
        else:
            self.MUSICA = [False]
    
    def set_efectes_so(self, value):
        if value:
            self.EFECTES_SO = [True]
        else:
            self.EFECTES_SO = [False]
             
    def start_the_game(self):
        #funció crida el fitxer principal del videojoc
        
        circuit = self.CIRCUIT[0]  
        musica = self.MUSICA[0]  
        mode = self.MODE[0]
            
        efectes_so = self.EFECTES_SO[0]
        self.nom = self.nom.get_value() #passem a string
        app = self.GraphicsEngine(circuit, mode, self.nom, musica, efectes_so)
        dades_partida = app.run()
        
        #actualitzem el ranking amb les dades obtingudes de la partida
        self.ranking.append(dades_partida)
        with open("pickles/ranking.pickle", "wb") as f1:
            pickle.dump(self.ranking, f1)
            
        #tornem a obrir el menu
        mm = Menu()
        mm.menu()
        
    def menu(self):        
        #carregar pickle  ranking
        with open("pickles/ranking.pickle", "rb") as f1:
            self.ranking = pickle.load(f1)
       
        #ESTADISTIQUES ÚLTIMA PARTIDA
        self.ultima = self.ranking[-1]        
        if self.ultima[1] == '1':
            mode_ = "MODE CONTRARELLOTGE"
        else:
            mode_ = "MODE FANTASMA"
            
        if self.ultima[2] == '1':
            circuit_ = "STAR CUP'S"
        elif self.ultima[2] == '2':
            circuit_ = "BROWSER CASTLE"
        else:
            circuit_ = "SENDA ARCOIRIS"
        nickname = self.ultima[0] 
        temps = self.ultima[3]
        self.estadistiques.append(["Jugador: " + nickname])
        self.estadistiques.append(["Mode de Joc: " + mode_])
        self.estadistiques.append(["Circuit: " + circuit_])          
        self.ultima = self.ultima[-1]
        for dada in self.ultima:             
            self.estadistiques.append(["Volta: " + str(dada[0]), "Temps: " + str(dada[1])])
        self.estadistiques.append(["Temps total: " + str(temps)])
            
        #RANKING
        for resultat in self.ranking:  
            if resultat[1] == '1': #mode_joc == contrarellotge
                if resultat[2] == '1': #num cricuit
                    self.ll_1.append([resultat[0],resultat[3]])                                                     
                elif resultat[2] == '2':
                    self.ll_2.append([resultat[0],resultat[3]])                    
                else:
                   self.ll_3.append([resultat[0],resultat[3]])                  
                
        self.ll_1 = sorted(self.ll_1, key = lambda x:x[1])   
        self.ll_2 = sorted(self.ll_2, key = lambda x:x[1])   
        self.ll_3 = sorted(self.ll_3, key = lambda x:x[1])   
        
        self.top5_1 = self.ll_1[0:5]
        self.top5_2 = self.ll_2[0:5]
        self.top5_3 = self.ll_3[0:5]
     
        # INIT MENU    
        pg.init()
        self.pantalla = pg.display.set_mode((800, 600))
        
        #creacio theme        
        MY_THEME = pygame_menu.themes.Theme(background_color=(0,0,0,0), # transparent background
                                            title_background_color=(111, 47, 175), #color linea sota titol
                                            title_font_shadow=True,
                                            title_font = self.font,
                                            title_font_size = 50,
                                            widget_font= self.font, 
                                            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE,   
                                            )
        
        self.menu = pygame_menu.Menu("EGRA'S KART", 800, 600,
                                onclose=pygame_menu.events.EXIT, 
                                theme = MY_THEME).translate(280,90)
     
        #foto mario
        image_widget2 = self.menu.add.image(image_path=self.img2.copy())
        image_widget2.set_float(origin_position=True)
        image_widget2.translate(250, 250)
                
        #pantalla jugar
        self.jugar = pygame_menu.Menu('Jugar', 800, 600, theme=MY_THEME)
        self.nom = self.jugar.add.text_input('Nom jugador :', default='',
                                             maxchar=15,
                                             input_underline='_') 
        
        self.jugar.add.selector('Circuit :', [("1 - Star Cup's ", '1'), ("2 - Bowser Castle", '2'), ("3 - Senda Arcoiris", '3')], 
                          onchange = self.set_circuit, selector_id = 'select_circuit')
        self.jugar.add.selector('Mode Joc:', [("Carrera Lliure ", '1'), ("Mode Fantasma", '2')], 
                          onchange = self.set_mode, selector_id = 'select_mode')
        self.jugar.add.button('START', self.start_the_game)
        self.jugar.add.button('Return to menu', pygame_menu.events.BACK).translate(0,100)     
                
        #pantalla instruccions
        self.instruccions = pygame_menu.Menu('INSTRUCCIONS', 800, 600, theme=MY_THEME)
        for m in self.INSTRUCCIONS:
            self.instruccions.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
            self.instruccions.add.vertical_margin(10)
        self.instruccions.add.button('Return to menu', pygame_menu.events.BACK).translate(0,90) 
        
        #pantalla RANKING CONTRARELLOTGE CIRCUIT 1
        self.circuit1 = pygame_menu.Menu("Star Cup's", 800, 600, theme=MY_THEME) 
        for c1 in self.top5_1:
            self.circuit1.add.label(c1, align=pygame_menu.locals.ALIGN_CENTER, font_size=50)
            self.circuit1.add.vertical_margin(10)
        self.circuit1.add.button('Return to RANKINGS', pygame_menu.events.BACK).translate(0,60) 
        
        #pantalla RANKING CONTRARELLOTGE CIRCUIT 2
        self.circuit2 = pygame_menu.Menu(" Bowser Castle", 800, 600, theme=MY_THEME)
        for c2 in self.top5_2:
            self.circuit2.add.label(c2, align=pygame_menu.locals.ALIGN_CENTER, font_size=50)
            self.circuit2.add.vertical_margin(10)
        self.circuit2.add.button('Return to RANKINGS', pygame_menu.events.BACK).translate(0,60) 
        
        #pantalla RANKING CONTRARELLOTGE CIRCUIT 3
        self.circuit3 = pygame_menu.Menu('Senda Arcoiris', 800, 600, theme=MY_THEME)
        for c3 in self.top5_3:
            self.circuit3.add.label(c3, align=pygame_menu.locals.ALIGN_CENTER, font_size=50)
            self.circuit3.add.vertical_margin(10)
        self.circuit3.add.button('Return to RANKINGS', pygame_menu.events.BACK).translate(0,60) 
                
        #pantalla RANKING
        self.ranking_ = pygame_menu.Menu('RANKINGS', 800, 600, theme=MY_THEME)
        self.ranking_.add.button("Star Cup's", self.circuit1)
        self.ranking_.add.button(" Bowser Castle", self.circuit2)
        self.ranking_.add.button('Senda Arcoiris', self.circuit3)
        self.ranking_.add.button('Return to menu', pygame_menu.events.BACK).translate(0,100) 
        
        
        #pantalla ESTADÍSTIQUES
        self.estadistiques_ = pygame_menu.Menu('ESTADISTIQUES', 800, 600, theme=MY_THEME)
        for m in self.estadistiques:
            self.estadistiques_.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
            self.estadistiques_.add.vertical_margin(10)
        self.estadistiques_.add.button('Return to menu', pygame_menu.events.BACK).translate(0,90) 
        
        
        #pantalla credits
        self.credit = pygame_menu.Menu('CREDITS', 800, 600, theme=MY_THEME)        
        for m in self.CREDITS:
            self.credit.add.label(m, align=pygame_menu.locals.ALIGN_CENTER, font_size=20)
            self.credit.add.vertical_margin(10)
        self.credit.add.button('Return to menu', pygame_menu.events.BACK).translate(0,90) 
        
        #botons menu
        self.menu.add.button('JUGAR', self.jugar).translate(-280,-70) 
        self.menu.add.button('INSTRUCCIONS', self.instruccions).translate(-280,-70)     
        self.menu.add.toggle_switch('MUSICA', True,
                                            toggleswitch_id='musica',
                                            state_text=('OFF', 'ON'),
                                            onchange  = self.set_musica, 
                                            switch_border_width = 1).translate(-240,-70)         
        self.menu.add.toggle_switch('EFECTES SO', True,
                                            toggleswitch_id='efectes_so',
                                            state_text=('OFF', 'ON'),
                                            onchange  = self.set_efectes_so, 
                                            switch_border_width = 1).translate(-220,-70)                                            
        self.menu.add.button('RANKING', self.ranking_).translate(-280,-70) 
        self.menu.add.button('ESTADISTIQUES', self.estadistiques_).translate(-280,-70) 
        self.menu.add.button('CREDITS', self.credit).translate(-280,-70) 
        self.menu.add.button('SORTIR', pygame_menu.events.EXIT).translate(-280,-70)         
        self.menu.mainloop(self.pantalla)



if __name__ == '__main__':
    m = Menu()
    m.menu()


