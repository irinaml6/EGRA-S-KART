# PROJECTE EGRA: Grup 2
# GraphicsEngine: Classe principal del videojoc.
    
import pygame as pg
import moderngl as mgl
import time
import sys
from pygame import mixer
import glm

from Cotxe import Cotxe
from SkyBox import SkyBox
from Camera import Camera 
from Textures import Texture
from Circuit import Circuit
from Musica import Musica
from Minimapa import Camera_m

from codi_objectes.Fantasma import Fantasma
from codi_objectes.Meta import Meta
from codi_objectes.Cartell import Cartell
from codi_objectes.Cubitos import Cubitos
from codi_objectes.Pregunta import Pregunta
from codi_objectes.Tronco1 import Tronco1
from codi_objectes.Fulles1 import Fulles1
from codi_objectes.Escales import Escales
from codi_objectes.Pal import Pal
from codi_objectes.Pal2 import Pal2
from codi_objectes.Bandera import Bandera
from codi_objectes.Bandera2 import Bandera2
from codi_objectes.Pancarta import Pancarta
from codi_objectes.Pancarta2 import Pancarta2
from codi_objectes.Pancarta3 import Pancarta3
from codi_objectes.GameOver import GameOver
from codi_objectes.Roca import Roca
from codi_objectes.Fletxa import Fletxa2
from codi_objectes.Fletxa1 import Fletxa1
from codi_objectes.Nitro import Nitro
from codi_objectes.Nitro2 import Nitro2


class GraphicsEngine:
    def __init__(self, num_circuit,mode_joc, nom, musica, efectes_so, win_size=(1000,800)): #(800,600)
        #dades jugador/partida
        self.num_circuit = num_circuit
        self.nom = nom
        self.efectes_so = efectes_so
        self.melodia = musica
        self.mode_joc = mode_joc    
        self.dades_partida = [self.nom, self.mode_joc, self.num_circuit]
               
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # creatopengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # detect and use exixting opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        self.ctx.point_size = 5
        self.clock = pg.time.Clock()
        self.time = 0
        self.deltaTime = 0
        self.lastFrame = 0
        
        self.camera = Camera(self)
        self.camera_m = Camera_m(self)
        self.texture = Texture(self)
        self.cotxe = Cotxe(self)
        self.cotxe_m = Cotxe(self, True)
        self.skybox = SkyBox(self)
        self.cartell = Cartell(self)
        self.pregunta1 = Pregunta(self,(80,0,5))
        self.pregunta2 = Pregunta(self,(-30,0,254))
        self.pregunta3 = Pregunta(self,(-125,0,15))
        self.cubitos = Cubitos(self)
        
        if self.num_circuit == "1":
            valor_inici1 = -37
            valor_inici2 = 98
            self.pancarta1 = Pancarta(self,(-37,-2,9))  
            self.pancarta2 = Pancarta2(self,(-37,-2,9))  
            self.pancarta3 = Pancarta3(self,(-37,-2,9)) 
            self.game_over = GameOver(self,(-37,-2,9))  
        elif self.num_circuit == "2":
            valor_inici1 = 15
            valor_inici2 = 214
            self.pancarta1 = Pancarta(self,(13,0,34))  
            self.pancarta2 = Pancarta2(self,(13,0,34))  
            self.pancarta3 = Pancarta3(self,(13,0,34))  
            self.game_over = GameOver(self,(13,0,34))  
        elif self.num_circuit == "3":
            valor_inici1 = -16
            valor_inici2 = 118
            self.pancarta1 = Pancarta(self,(-50,0,16))  
            self.pancarta2 = Pancarta2(self,(-50,0,16))  
            self.pancarta3 = Pancarta3(self,(-50,0,16))  
            self.game_over = GameOver(self,(-50,0,16))  

        if self.mode_joc == '2':
            self.cotxe_fantasma = Fantasma(self)
            
        self.meta1 = Meta(self, valor_inici1)
        self.meta2 = Meta(self, valor_inici2)
        self.circuit = Circuit(self)
        self.circuit_m = Circuit(self)
        self.musica = Musica(self)
        
        #decoracions
        self.roca1 = Roca(self,(152,0,37))
        self.roca2 = Roca(self,(-256,0,277))
        self.tronco1 = Tronco1(self,(0,0,60))
        self.fulles1 = Fulles1(self,(0,0,60))
        self.tronco2 = Tronco1(self,(47,0,40))
        self.fulles2 = Fulles1(self,(47,0,40))
        self.tronco3 = Tronco1(self,(20,0,50))
        self.fulles3 = Fulles1(self,(20,0,50))
        self.tronco4 = Tronco1(self,(64,0,51))
        self.fulles4 = Fulles1(self,(64,0,51))
        self.tronco5 = Tronco1(self,(82,0,58))
        self.fulles5 = Fulles1(self,(82,0,58))
        self.tronco6 = Tronco1(self,(97,0,48))
        self.fulles6 = Fulles1(self,(97,0,48))
        self.tronco7 = Tronco1(self,(111,0,60))
        self.fulles7 = Fulles1(self,(111,0,60))
        self.tronco8 = Tronco1(self,(128,0,49))
        self.fulles8 = Fulles1(self,(128,0,49))
        self.tronco9 = Tronco1(self,(-12,0,48))
        self.fulles9 = Fulles1(self,(-12,0,48))
        self.tronco10 = Tronco1(self,(-28,0,50))
        self.fulles10 = Fulles1(self,(-28,0,50))
        self.tronco11 = Tronco1(self,(-43,0,48))
        self.fulles11 = Fulles1(self,(-43,0,48))
        self.tronco12 = Tronco1(self,(-56,0,53))
        self.fulles12 = Fulles1(self,(-56,0,53))
        self.tronco13 = Tronco1(self,(-71,0,43))
        self.fulles13 = Fulles1(self,(-71,0,43))
        self.tronco14 = Tronco1(self,(-84,0,59))
        self.fulles14 = Fulles1(self,(-84,0,59))
        self.fulles15 = Fulles1(self,(155,0,175))
        self.tronco15 = Tronco1(self,(155,0,175))
        self.fulles16 = Fulles1(self,(124,0,184))
        self.tronco16 = Tronco1(self,(124,0,184))
        self.fulles17 = Fulles1(self,(33,0,178))
        self.tronco17 = Tronco1(self,(33,0,178))
        self.fulles18 = Fulles1(self,(26,0,160))
        self.tronco18 = Tronco1(self,(26,0,160))
        self.nitro = Nitro(self,(105,0,425))
        self.nitro2 = Nitro2(self,(-144,0,8))
        self.fletxa1 = Fletxa1(self,(-192,0,304))
        self.fletxa2 = Fletxa2(self,(-140,0,362))
        self.bandera = Bandera(self,(-170,0,74))
        self.bandera2 = Bandera(self,(-112.252,-20,120.47))
        self.bandera3 = Bandera2(self,(-226.04,-20,390.96))
        self.pal = Pal(self,(-555,0,240))
        self.pal2 = Pal2(self,(-112.752,0,118.476))
        self.pal3 = Pal2(self,(-234.79,0,390.96))
        self.escales = Escales(self,(-180,0,90))
        
        
        self.canvi = False
        self.panoramica = False
        self.final_partida  = False
        self.inici_partida = False
        self.final_volta = False
        self.temps_partida = 0.0
        self.temps_volta = 0.0
        self.llista_temps = []
        self.start = 0
        self.start2 = 0
        self.end = 0
        self.entrat = False
        self.segueix = False
        self.fi = True
        self.acabar = False
        self.inici2 = True
        self.inici_2 = 0.0 
        self.end_2 = 0.0
        self.time_inici_partida = 0.0
        self.com = False              
        self.inici = True
        self.ha_frenat = True
        self.num_voltes = 1
        if self.mode_joc == '2':
            self.num_voltes = 3
            
        
        #canals musica
        mixer.set_num_channels(20)
        self.channel0 = mixer.Channel(0) #inici + fons
        self.channel1 = mixer.Channel(1) # nomes fondo
        self.channel2 = mixer.Channel(2) # choque limits
        self.channel3 = mixer.Channel(3) # motor
        self.channel4 = mixer.Channel(4) # final partida
        self.channel5 = mixer.Channel(5) # choque cubitos
        self.channel6 = mixer.Channel(6) # volta
        self.channel7 = mixer.Channel(7) # ultima volta
        self.channel8 = mixer.Channel(8) # musica rapida
        self.channel11 = mixer.Channel(11) # choque arbres/escales
        self.channel12 = mixer.Channel(12) # choque roques
        self.channel13 = mixer.Channel(13) # no trampas 
        
        if self.efectes_so == True and self.melodia == False:
            self.channel0.set_volume(0.2)
            self.channel2.set_volume(0.6)
            self.channel4.set_volume(0.6)
            self.channel5.set_volume(0.6)
            self.channel6.set_volume(0.5)
            self.channel7.set_volume(0.6)
            self.channel11.set_volume(0.6)
            self.channel12.set_volume(0.6)
            self.channel13.set_volume(0.6)
            #melodia desactivada
            self.channel1.set_volume(0)
            self.channel3.set_volume(0)
            self.channel8.set_volume(0)
            
        elif self.melodia == True and self.efectes_so == False:
            self.channel0.set_volume(0.2) 
            self.channel1.set_volume(0.2)
            self.channel3.set_volume(0.005) 
            self.channel8.set_volume(0.2)
            #efectes so desactivats
            self.channel2.set_volume(0)
            self.channel4.set_volume(0)
            self.channel5.set_volume(0)
            self.channel6.set_volume(0)
            self.channel7.set_volume(0)
            self.channel11.set_volume(0)
            self.channel12.set_volume(0)
            self.channel13.set_volume(0)
            
        elif self.melodia == True and self.efectes_so == True:
            self.channel0.set_volume(0.2) 
            self.channel1.set_volume(0.2)
            self.channel2.set_volume(0.6)
            self.channel3.set_volume(0.005) 
            self.channel4.set_volume(0.6)
            self.channel5.set_volume(0.6)
            self.channel6.set_volume(0.5)
            self.channel7.set_volume(0.6)
            self.channel8.set_volume(0.2)
            self.channel11.set_volume(0.6)
            self.channel12.set_volume(0.6)
            self.channel13.set_volume(0.6)
        
        else:
            self.channel0.set_volume(0) 
            self.channel1.set_volume(0)
            self.channel2.set_volume(0) 
            self.channel3.set_volume(0)
            self.channel4.set_volume(0)           
            self.channel5.set_volume(0)
            self.channel6.set_volume(0)
            self.channel7.set_volume(0)
            self.channel8.set_volume(0)
            self.channel11.set_volume(0)
            self.channel12.set_volume(0)
            self.channel13.set_volume(0)
               
    
    def check_events(self):           
        for event in pg.event.get():
            pressed = pg.key.get_pressed()
            
            if pressed[pg.K_w]:
                if self.ha_frenat == True:
                    self.channel3.play(self.musica.load('motor'),-1)
                    self.ha_frenat = False
                
                self.cotxe.forward(self.deltaTime)
                self.camera.forward(self.deltaTime)
                self.cotxe_m.forward(self.deltaTime)
                self.cotxe.direccio = 1
            
            elif pressed[pg.K_s]:
                self.cotxe.backward(self.deltaTime)                
                self.cotxe_m.backward(self.deltaTime)
                self.cotxe.direccio = -1

            elif pressed[pg.K_SPACE]: 
                self.cotxe.frenada(self.deltaTime)
                self.cotxe_m.frenada(self.deltaTime)
                
            if pressed[pg.K_d]:
                self.cotxe.turn("right", self.deltaTime)
                self.cotxe_m.turn("right", self.deltaTime)
                self.camera.turn("right", self.deltaTime)
                
            elif pressed[pg.K_a]:
                self.cotxe.turn("left", self.deltaTime)
                self.cotxe_m.turn("left", self.deltaTime)
                self.camera.turn("left", self.deltaTime)
            
            elif pressed[pg.K_q]:
                self.panoramica  = True
                
            elif pressed[pg.K_e]:
                self.canvi= True
            
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.cotxe.destroy()
            
                pg.quit()
                sys.exit()
                

                
    def render(self):
        # clear framebuffer        
        if self.com == False:
            self.inici_2 = time.time()
        self.com = True
        self.ctx.clear(color=(0,0,0))
        if self.camera.perspectiva:
            self.ctx.viewport = (0,0,self.WIN_SIZE[0],self.WIN_SIZE[1])
            self.cotxe.update(self.deltaTime) 
            self.camera.update(self.deltaTime, self.canvi, self.panoramica)
            self.meta1.update()
            self.meta2.update()
            self.circuit.update()
            self.cotxe_m.update(self.deltaTime)
            self.cotxe.render()
            if self.mode_joc == '2':
                self.cotxe_fantasma.render()
            self.cartell.render()
            self.meta1.render()
            self.meta2.render()
            self.circuit.render()
            self.circuit_m.update()
           
            #321 inici partida
            if 5 < self.time_inici_partida < 6:
                    self.pancarta3.render()
            if 6 < self.time_inici_partida < 7:
                    
                    self.pancarta2.render()
            if 7< self.time_inici_partida < 8.3:
                    self.pancarta1.render()
                    
            if self.num_voltes == 4:
                self.game_over.render()
            
            if self.num_circuit == '1':                     
                self.skybox.render()
                self.cubitos.update()
                self.cubitos.render()
                self.tronco1.render()
                self.fulles1.render()
                self.tronco2.render()
                self.fulles2.render()
                self.tronco3.render()
                self.fulles3.render()
                self.tronco4.render()
                self.fulles4.render()
                self.tronco5.render()
                self.fulles5.render()
                self.tronco6.render()
                self.fulles6.render()
                self.tronco7.render()
                self.fulles7.render()
                self.tronco8.render()
                self.fulles8.render()
                self.tronco9.render()
                self.fulles9.render()
                self.tronco10.render()
                self.fulles10.render()
                self.tronco11.render()
                self.fulles11.render()
                self.tronco12.render()
                self.fulles12.render()
                self.tronco13.render()
                self.fulles13.render()
                self.tronco14.render()
                self.fulles14.render()
                self.tronco15.render()
                self.fulles15.render()
                self.tronco16.render()
                self.fulles16.render()
                self.tronco17.render()
                self.fulles17.render()
                self.tronco18.render()
                self.fulles18.render()
                self.escales.render()
                self.pal.render()
                self.bandera.render()
                self.pregunta1.render()
                self.pregunta2.render()
                self.pregunta3.render()
                self.nitro2.render()
                
            elif self.num_circuit == "2":
                self.skybox.update()
                self.skybox.render()
                self.cubitos.update()
                self.cubitos.render()
                self.roca1.update()
                self.roca2.update()
                self.roca1.render()
                self.roca2.render()
                self.fletxa1.render()
                self.fletxa2.render()
                self.nitro.render()
                
            elif self.num_circuit == "3":
                self.bandera2.render()
                self.bandera3.render()
                self.pal2.render()
                self.pal3.render()
                
            # MUSICA INICI (3,2,1) + FONDO          
            if self.inici == True:
                self.channel0.play(self.musica.load('inici2'))
                self.inici = False
                
            if self.channel0.get_busy() == False:
                if self.num_circuit == '1' and self.inici2 == True:
                    self.inici2 = False
                    self.channel1.play(self.musica.load('fondo'),-1)
                elif self.num_circuit == '2' and self.inici2 == True:
                    self.inici2 = False
                    self.channel1.play(self.musica.load('fondo2'),-1)
                elif self.num_circuit == '3' and self.inici2 == True:
                    self.inici2 = False
                    self.channel1.play(self.musica.load('fondo3'),-1)

            # SI FRENA EL COTXE APAGAR POC A POC EL MOTOR
            if self.cotxe.velocity <= 0:
                self.channel3.fadeout(1000)
                self.ha_frenat = True
            
            # COLISIONS
            if self.cotxe.col_metall == True and self.num_circuit=='1':
                self.channel2.play(self.musica.load('col_metall'))
                self.cotxe.col_metall = False
            elif self.cotxe.col_metall == True and self.num_circuit=='2':
                self.channel2.play(self.musica.load('col_roca'))
                self.cotxe.col_metall = False
            elif self.cotxe.col_cubitos == True:
                self.channel5.play(self.musica.load('col_cubitos'))
                self.cotxe.col_cubitos = False   
            elif self.cotxe.colisio == True:
                self.channel11.play(self.musica.load('colisio'))
                self.cotxe.colisio = False
            elif self.cotxe.col_roca == True:
                self.channel12.play(self.musica.load('col_roca'))
                self.cotxe.col_roca = False     
            elif self.cotxe.col_nop == True:
                self.channel13.play(self.musica.load('nop'))
                self.cotxe.col_nop = False 
            elif self.cotxe.col_tinta == True:
                self.channel13.play(self.musica.load('tinta'))
                self.cotxe.col_tinta = False 
            elif self.cotxe.col_nitro == True:
                self.channel13.play(self.musica.load('nitro'))
                self.cotxe.col_nitro = False
                
            # Incrementar el número de voltes
            pos_actual = self.cotxe.position_frontal
            if self.num_circuit == "1":
                pos_meta_x = 0 #x
                pos_meta_z = 30
            elif  self.num_circuit == "2":
                pos_meta_x = 60
                pos_meta_z = 65
            elif  self.num_circuit == "3":
                pos_meta_x = -5
                pos_meta_z = 65

            if self.num_voltes < 4 and (pos_actual[0] > pos_meta_x and pos_actual[2] < pos_meta_z) and self.cotxe.direccio == 1 and self.entrat != True:
                self.inici_partida = True
                self.entrat = True

            if self.entrat and self.cotxe.direccio == 1  and (pos_actual[0] < pos_meta_x and pos_actual[2] < pos_meta_z):
               self.segueix = True
               self.fi = True

            if self.fi == True and self.segueix and self.cotxe.direccio == 1  and (pos_actual[0] > pos_meta_x and pos_actual[2] < pos_meta_z):
                self.final_volta = True

            #Perque el cotxe freni al final
            if self.num_voltes == 4 and (pos_actual[0] > pos_meta_x+25 and pos_actual[2] < pos_meta_z):
                self.acabar = True
                self.channel1.fadeout(1000)
                self.channel8.fadeout(1000)
                self.channel3.fadeout(1000)
                self.final_partida = True
                
           
        if self.num_voltes == 4:
            volta = 3
        else:
            volta = self.num_voltes
       
        if self.mode_joc =='2':
            info = 'VOLTA : 1/1  |   TEMPS : ' + str(self.temps_partida)
        else:
            info = 'VOLTA : ' + str(volta) + '/3   |   TEMPS : ' + str(self.temps_partida)
            
        pg.display.set_caption(info)
        
        #MINIMAPA
        self.ctx.disable(flags=mgl.DEPTH_TEST)
        self.ctx.viewport = (self.WIN_SIZE[0]-self.WIN_SIZE[0]//3,0,self.WIN_SIZE[0]//3, self.WIN_SIZE[1]//3)
        self.camera_m.setCamera(glm.vec3(-40,450,223.269), glm.vec3(-40,0,223.269), glm.vec3(1,0,0), 0)
        self.circuit_m.render()
        self.cotxe_m.render() 
        self.nitro2.render()
        self.nitro.render()            
        # swap buffers 
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        # swap buffers
        pg.display.flip()
    
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001 # 0.001
        
        # INICI PARTIDA
        if self.inici_partida:
            self.start = time.time()
            self.start2 = time.time()
            self.inici_partida = False

        # CÀLCUL A CADA INSTANT DE TEMPS
        if self.entrat:
            self.end = time.time()
            self.temps_partida = round(self.end - self.start, 2)
            self.temps_volta = round(self.end - self.start2, 2)

        # TEMPS PER VOLTA
        if self.temps_volta < 20:
            self.final_volta=False
            
        if self.final_volta:           
            self.llista_temps.append([self.num_voltes,self.temps_volta])
            self.fi = False
            self.final_volta = False
            self.num_voltes += 1

            if self.num_voltes == 2:
                self.channel6.play(self.musica.load('volta'))

            elif self.num_voltes == 3:
                 self.channel7.play(self.musica.load('ult_volta'))
                 
                 if self.num_circuit == '1':
                     self.channel1.stop()
                     self.channel8.play(self.musica.load('fondo_rapid'),-1)
                 elif self.num_circuit == '2':
                     self.channel1.stop()
                     self.channel8.play(self.musica.load('fondo2_rapid'),-1)
                 elif self.num_circuit == '3':
                     self.channel1.stop()
                     self.channel8.play(self.musica.load('fondo3_rapid'),-1)

            self.start2 = time.time()

            if self.num_voltes == 4:
                self.entrat = False
                self.channel4.play(self.musica.load('fin_volta'))
                self.channel0.stop()
                self.channel1.fadeout(1000)
                self.channel8.fadeout(1000)
                self.channel3.fadeout(1000)
                self.ha_frenat = True
                self.final_partida = True

        if self.acabar:
            self.cotxe.velocity = 0
            self.cotxe.acceleration = 0
            self.camera.velocity = 0
            self.camera.acceleration = 0
            self.cotxe_m.velocity = 0
            self.cotxe_m.acceleration = 0
           
        self.deltaTime = self.time - self.lastFrame
        self.lastFrame = self.time
        
        return self.time

        
    def run(self):
         while not self.final_partida:
             self.get_time()
             self.end_2 = time.time()
             self.time_inici_partida = self.end_2 - self.inici_2
             if self.time_inici_partida > 8.3: #321 no mouret  
                self.check_events()
             self.render()
             self.clock.tick(60)                     
        
         self.dades_partida.append(self.temps_partida)
         self.dades_partida.append(self.llista_temps)
         
         
         time.sleep(3)
         return (self.dades_partida)
         
         pg.quit()
         sys.exit()

    
    
 

    
