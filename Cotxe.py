# PROJECTE EGRA: Grup 2
#COTXE: En aquesta classe creem l'objecte cotxe del videojoc.

import numpy as np
import glm
import math
from pygame.math import Vector3
from RGB import Colors


class Cotxe:
    def __init__(self,app, minimapa = False):
        self.app = app
        self.ctx = app.ctx
        self.shader_program = self.get_shader_program()
        self.minimapa = minimapa
        
        #posició inicial del cotxe i velocitat màxima x circuit
        if self.app.num_circuit == "1":
            self.position = Vector3(-37,-2,9)
            self.max_velocity = 0.63
        elif self.app.num_circuit == "2":
            self.position = Vector3(13,0,34)
            self.max_velocity = 0.63
        elif self.app.num_circuit == "3":
            self.position = Vector3(-50,0,16)
            self.max_velocity = 0.47
            
        #físiques
        self.velocity = 0
        self.position_frontal = self.position[0]+4.5
        self.position_back = self.position[0]-4.5
        self.direccio = 0 # 1 endavant  -1 enrere 
        self.length = 4
        self.max_acceleration = 3.5
        self.max_steering = 30
        self.acceleration = 0.0
        self.steering = 0.0
        self.b = glm.mat4()
        self.out_vel = 0.1
        self.C_drag = 0.4257
        self.C_rr = 12.8
        self.EngineForce = 1000
        self.f = 0
        self.Mass = 1200
        self.vel = 0
        self.a = 0
                      
        self.T0 = glm.mat4()
        self.R = glm.mat4()
        self.T = glm.mat4() 
        self.S = glm.mat4()
        
        #per controlar trampes
        self.alerta = False
        self.superat = False

        self.upward = 0
        self.side = 0
        self.m_model = self.get_model_matrix()
        self.on_init()
        self.fix()
        self.time = 0.1
        
        self.vbo = self.get_vbo((1,1,0))
        self.vao = self.get_vao() #cares
        
        self.color = Colors(app)
        #colisions
        self.col_metall = False
        self.col_cubitos = False
        self.colisio = False
        self.peligro = False
        self.col_roca = False
        self.col_nop = False
        self.col_tinta = False
        self.col_nitro = False
        self.passa_nitro = False
        self.temps_nitro = 0
        
    
    #anar endavant
    def forward(self, dt):
        self.f = 1

    #anar enrere
    def backward(self, dt):
        self.f = -1
            
    def frenada(self, deltaTime):
        self.f = 2
        if 0.075 > self.velocity > 0:
            self.velocity = 0
            self.acceleration = 0
        elif self.velocity > 0: 
            self.velocity -= 0.02
        else:
            self.velocity = 0
            self.acceleration = 0
            
    #girar        
    def turn(self, side, deltaTime):
        if side == "right":
            self.steering += 110 * deltaTime
            self.a-= 5
        elif side == "left":
   
            self.steering -= 110 * deltaTime
            self.a+= 5
            
    #colocar cotxe
    def fix(self):
        self.R = glm.rotate(glm.mat4(), glm.radians(-90), (1,0,0))
        self.R = glm.rotate(self.R, glm.radians(271), (0,0,1))
        self.T = glm.translate(self.T, (0,4,0))
        self.corrected = self.T*self.R
        self.shader_program['m_model'].write(self.T*self.R*self.m_model)
    
    def update(self, dt):
        self.texture.use(location=0)
        
        if self.steering:
              self.b = glm.rotate(glm.mat4(), glm.radians(-self.steering), glm.vec3(0,0,1))

        vx = math.cos(glm.radians(self.steering) )
        vz = math.sin(glm.radians(self.steering) )
        if self.f == 1: # Accelera
            F_traction = 1 * self.EngineForce
            F_drag = -self.C_drag * self.velocity * self.velocity
            F_rr = -self.C_rr * self.velocity
            F_long = F_traction + F_drag + F_rr
            self.acceleration = ( F_long/self.Mass ) * 0.5
            self.velocity = self.velocity + dt * self.acceleration
            if self.velocity >= self.max_velocity:
                self.velocity = self.max_velocity
            
            self.f = 0
        elif self.f == 0 or self.f == 2: # deixa d'accelerar, vel constant
            self.velocity = self.velocity
        else: #Endarrere
            F_traction = - 1 * (self.EngineForce/5) 
            F_drag = -self.C_drag * self.velocity * self.velocity
            F_rr = -self.C_rr * self.velocity
            F_long = F_traction + F_drag + F_rr
            self.acceleration = F_long/self.Mass
            self.velocity = self.velocity + dt * self.acceleration 
            
            if self.velocity <= -0.1:
                self.velocity = -0.1
        
        self.position += glm.vec3((vx, 0, vz))*self.velocity
        self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
        self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
        
        #RGB, CONTROLAR VELOCITAT DEPENENT DE LA POSICIÓ
        color = self.color.get_color(self.position[0], self.position[2])        
        if self.app.num_circuit == "1" or self.app.num_circuit == "2":
            
            #vermell
            if color == (0.996,0.0,0.0):
                if self.velocity > self.out_vel:
                    self.velocity -= 0.02

                if self.velocity > 0:
                    self.forward(dt)
            #negre
            elif color == (0.0, 0.0, 0.0) or color == (0.004, 0.004, 0.004) or color == (0.008, 0.008, 0.008):
                self.col_tinta = True
                self.max_velocity = 0.1
            #groc
            elif color == (1.0, 0.965, 0.0) or color == (1.0, 0.969, 0.0) or color == (1.0, 0.965, 0.004) or color == (1.0, 0.961, 0.012) or color == (0.992, 0.973, 0.0):
                if not self.passa_nitro:
                    self.col_nitro = True
                    self.temps_nitro = self.app.temps_partida
                    self.velocity += 0.25
                
                self.passa_nitro = True
                if self.velocity > self.max_velocity:
                    self.max_velocity = self.velocity
            else:
                if self.app.num_circuit == "1":
                    self.max_velocity = 0.63
                elif self.app.num_circuit == "2":
                    self.max_velocity = 0.63
                elif self.app.num_circuit == "3":
                    self.max_velocity = 0.47
                
            if self.passa_nitro:
                if self.app.temps_partida > self.temps_nitro + 2:
                    self.velocity -= 0.25
                    self.temps_nitro = 0
                    self.max_velocity = 0.47
                    self.passa_nitro = False
        
        #caiguda cotxe circuit 3 --------------------------------------
        elif self.app.num_circuit == "3":
            if color == (0.996,0.0,0.0):
                self.velocity = 0.0
                self.b = glm.mat4()
                if self.position[0] >= -50:
                    self.steering = 0.0
                    self.app.camera.steering = 0.0
                    self.position = Vector3(-5,0,16)
                elif -218.217 < self.position[0] <= -50 and self.position[2]>46:
                    self.steering = 180.0
                    self.app.camera.steering = 180.0
                    self.position = Vector3(-50,0,135.174)
                    self.b = glm.rotate(glm.mat4(),glm.radians(180),glm.vec3(0,0,1))
                elif self.position[0] <= -218.217 or -218.217 < self.position[0] <= -50 and self.position[2]<46:
                    self.steering = 270.0
                    self.app.camera.steering = 270.0
                    self.position = Vector3(-243.703,0,431.974)
                    self.b = glm.rotate(glm.mat4(),glm.radians(180),glm.vec3(1,0,0))
                    
                                    
        self.position += glm.vec3((vx, 0, vz))*self.velocity
        self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
        self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
        
        #limits circuit --------------------------------------            
        if self.position_frontal[2] <= -19.316 or self.position_back[2] <= -19.316 or self.position_frontal[2] >= 467.622 or self.position_back[2] >= 467.622 or  self.position_frontal[0] >= 205.155 or self.position_back[0] >= 205.155 or self.position_frontal[0] <= -286.784 or self.position_back[0] <= -286.784:
            self.f=0
            self.velocity = 0
            self.acceleration = 0
            self.app.camera.velocity = 0
            self.app.camera.acceleration = 0
                
            if self.position_frontal[2] <= -19.316 or self.position_back[2] <= -19.316:
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.col_metall = True
                    
            elif self.position_frontal[2] >= 467.622 or self.position_back[2] >= 467.622:             
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                self.col_metall = True
                
            elif self.position_frontal[0] >= 205.155 or self.position_back[0] >= 205.155:
                self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                self.col_metall = True
            
            elif self.position_frontal[0] <= -286.784 or self.position_back[0] <= -286.784:    
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2])
                self.col_metall = True
                
            self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
            self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
           
    
        #limit1_pregunta --------------------------------------
        if (self.app.num_circuit == "1" and 80 >= self.position_frontal[0] >= 70 and 10 >= self.position_frontal[2] >= 4) or (self.app.num_circuit == "1" and self.app.num_circuit == "1" and -30 >= self.position_frontal[0] >= -40 and 259 >= self.position_frontal[2] >= 252) or (self.app.num_circuit == "1" and self.app.num_circuit == "1" and -124 >= self.position_frontal[0] >= -135 and 20 >= self.position_frontal[2] >= 14):
            self.f = 0
            self.velocity = 0
            self.acceleration = 0
            self.app.camera.velocity = 0
            self.app.camera.acceleration = 0
            #CUBITO1
            #dreta
            if ((81 >= self.position_frontal[0] >= 69) and(11 >= self.position_frontal[2] >= 9)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.col_cubitos = True
            #frontal    
            if ((11 >= self.position_frontal[2] >= 3) and (71 >=self.position_frontal[0] >= 69)):
                self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                self.col_cubitos = True
            #back
            if ((11 >= self.position_frontal[2] >= 3) and (79 <=self.position_frontal[0] <= 81)):
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                self.col_cubitos = True
            #left    
            if ((81 >= self.position_frontal[0] >= 69) and(9 <= self.position_frontal[2] <= 11)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                self.col_cubitos = True
                
            
            #CUBITO2
            #dreta
            if ((-29 >= self.position_frontal[0] >= -41) and (260 >= self.position_frontal[2] >= 258)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.col_cubitos = True
            #frontal    
            if ((260 >= self.position_frontal[2] >= 252) and (-39 >=self.position_frontal[0] >= -41)):
                self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                self.col_cubitos = True
            #back
            if ((260 >= self.position_frontal[2] >= 252) and (-30 >=self.position_frontal[0] >= -32)):
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                self.col_cubitos = True
            #left    
            if ((-29 >= self.position_frontal[0] >= -41) and(251 <= self.position_frontal[2] <= 253)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                self.col_cubitos = True
                
            self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
            self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
           
            
            #CUBITO3
            #dreta
            if ((-124 >= self.position_frontal[0] >= -130) and(22 >= self.position_frontal[2] >= 18)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.col_cubitos = True
            #frontal    
            if ((21 >= self.position_frontal[2] >= 14) and (-134 >=self.position_frontal[0] >= -136)):
                self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                self.col_cubitos = True
            #back
            if ((21 >= self.position_frontal[2] >= 13) and (-125 <=self.position_frontal[0] <= -123)):
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                self.col_cubitos = True
            #left    
            if ((-124 >= self.position_frontal[0] >= -129) and(13 <= self.position_frontal[2] <= 15)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                self.col_cubitos = True
                
            self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
            self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
           
        
        #limits arbres + bandera
        elif (self.app.num_circuit == "1" and 145 >= self.position_frontal[0]>= -79 and 38 <= self.position_frontal[2] <= 89) or (self.app.num_circuit == "1" and -132 >= self.position_frontal[0]>= -189 and 67 <= self.position_frontal[2] <= 134) or (self.app.num_circuit == "1" and 164 >= self.position_frontal[0] >= 125 and 206 >= self.position_frontal[2] >= 171) or (self.app.num_circuit == "1" and 43 >= self.position_frontal[0] >= 29 and 200 >= self.position_frontal[2] >= 145):
            self.f = 0
            self.velocity = 0
            self.acceleration = 0
            self.app.camera.velocity = 0
            self.app.camera.acceleration = 0
            #ARBRES1
            #dreta
            if ((145 >= self.position_frontal[0] >= -79) and(90 >= self.position_frontal[2] >= 87)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+5)
                self.colisio = True
            #frontal    
            if ((90 >= self.position_frontal[2] >= 36) and (-75 >=self.position_frontal[0] >= -79)):
                self.position = glm.vec3(self.position[0]-5, self.position[1], self.position[2])
                self.colisio = True
            #back
            if ((90 >= self.position_frontal[2] >= 36) and (143 <=self.position_frontal[0] <= 145)):
                self.position = glm.vec3(self.position[0]+5, self.position[1], self.position[2]) 
                self.colisio = True
            #left    
            if ((145 >= self.position_frontal[0] >= -79) and(36 <= self.position_frontal[2] <= 40)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-5)
                self.colisio = True
                
            #ARBRES2
            #dreta
            if ((165 >= self.position_frontal[0] >= 124) and(207 >= self.position_frontal[2] >= 204)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.colisio = True
            #frontal    
            if ((207 >= self.position_frontal[2] >= 170) and (127 >=self.position_frontal[0] >= 123)):
                self.position = glm.vec3(self.position[0]-5, self.position[1], self.position[2])
                self.colisio = True
            #back
            if ((207 >= self.position_frontal[2] >= 170) and (162 <=self.position_frontal[0] <= 165)):
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                self.colisio = True
            #left    
            if ((165 >= self.position_frontal[0] >= 124) and(170 <= self.position_frontal[2] <= 173)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-4)
                self.colisio = True
                
            #ARBRES3
            #dreta
            if ((44 >= self.position_frontal[0] >= 28) and(201 >= self.position_frontal[2] >= 198)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                self.colisio = True
            #frontal    
            if ((201 >= self.position_frontal[2] >= 147) and (32 >=self.position_frontal[0] >= 29)):
                self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                self.colisio = True
            #back
            if ((201 >= self.position_frontal[2] >= 147) and (41 <=self.position_frontal[0] <= 44)):
                self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                self.colisio = True
            #left    
            if ((44 >= self.position_frontal[0] >= 22) and(147 <= self.position_frontal[2] <= 150)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                self.colisio = True
                
            #BANDERA
            #dreta
            if ((-130 >= self.position_frontal[0] >= -190) and(135 >= self.position_frontal[2] >= 132)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+5)
                self.colisio = True
            #frontal    
            if ((135 >= self.position_frontal[2] >= 64) and (-187 >=self.position_frontal[0] >= -190)):
                self.position = glm.vec3(self.position[0]-5, self.position[1], self.position[2])
                self.colisio = True
            #back
            if ((135 >= self.position_frontal[2] >= 64) and (-133 <=self.position_frontal[0] <= -130)):
                self.position = glm.vec3(self.position[0]+5, self.position[1], self.position[2]) 
                self.colisio = True
            #left    
            if ((-130 >= self.position_frontal[0] >= -190) and(65 <= self.position_frontal[2] <= 70)):
                self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-6)
                self.colisio = True
            
            self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
            self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
            
            
            
        #limit roca
        elif self.app.num_circuit == "2":
            if self.app.roca1.ubi[1] < 5 or self.app.roca2.ubi[1] < 5:
                if (161 >= self.position_frontal[0] >= 142 and 49 >= self.position_frontal[2] >=31) or (self.app.num_circuit == "2" and self.app.num_circuit == "2" and -253 >= self.position_frontal[0] >= -266 and 289 >= self.position_frontal[2] >= 276):
                    self.f = 0
                    self.velocity = 0
                    self.acceleration = 0
                    self.app.camera.velocity = 0
                    self.app.camera.acceleration = 0
                    #ROCA1
                    #dreta
                    if ((161 >= self.position_frontal[0] >= 142) and(49 >= self.position_frontal[2] >= 48)):
                        self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                        self.col_roca = True
                    #frontal    
                    if ((49 >= self.position_frontal[2] >= 31) and (143 >=self.position_frontal[0] >= 142)):
                        self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                        self.col_roca = True
                    #back
                    if ((49 >= self.position_frontal[2] >= 31) and (160 <=self.position_frontal[0] <= 161)):
                        self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2])
                        self.col_roca = True
                    #left    
                    if ((161 >= self.position_frontal[0] >= 142) and(31 <= self.position_frontal[2] <= 32)):
                        self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                        self.col_roca = True
                        
                    #ROCA2
                    #dreta
                    if ((-253 >= self.position_frontal[0] >= -266) and(289 >= self.position_frontal[2] >= 288)):
                        self.position = glm.vec3(self.position[0], self.position[1], self.position[2]+2)
                        self.col_roca = True
                    #frontal    
                    if ((289 >= self.position_frontal[2] >= 277) and (-265 >=self.position_frontal[0] >= -266)):
                        self.position = glm.vec3(self.position[0]-2, self.position[1], self.position[2])
                        self.col_roca = True
                    #back
                    if ((289 >= self.position_frontal[2] >= 277) and (-257 <=self.position_frontal[0] <= -256)):
                        self.position = glm.vec3(self.position[0]+2, self.position[1], self.position[2]) 
                        self.col_roca = True
                    #left    
                    if ((-253 >= self.position_frontal[0] >= -266) and(276 <= self.position_frontal[2] <= 277)):
                        self.position = glm.vec3(self.position[0], self.position[1], self.position[2]-2)
                        self.col_roca = True
                        
                    self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
                    self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
                
            # SENSE TRAMPES CIRCUIT 2
            if self.position[2] > 350:
                self.superat = False

            if self.superat == False and (-175 < self.position[0] < -126 and 250 < self.position[2] < 367):
                self.alerta = True
                
            if self.alerta:
                if self.position_frontal[0] >= -133:
                    self.col_nop = True
                    self.f = 0
                    self.velocity = 0
                    self.acceleration = 0
                    self.app.camera.velocity = 0
                    self.app.camera.acceleration = 0
                    self.position = glm.vec3(self.position[0]-4, self.position[1], self.position[2])
                    self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
                    self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
                                       
                elif -162 >= self.position_frontal[0]:
                    self.col_nop = True
                    self.f = 0
                    self.velocity = 0
                    self.acceleration = 0
                    self.app.camera.velocity = 0
                    self.app.camera.acceleration = 0
                    self.position = glm.vec3(self.position[0]+4, self.position[1], self.position[2])
                    self.position_frontal = glm.vec3(self.position[0]+4.5, self.position[1],self.position[2])
                    self.position_back = glm.vec3(self.position[0]-4.5, self.position[1],self.position[2])
                    
                if self.position[2]  <= 250:
                    self.alerta = False
                    self.superat = True   
                    
       
        l = [self.position[0], self.position[1], self.position[2]]
        a = glm.translate(glm.mat4(), glm.vec3(l))
        
        self.shader_program['m_model'].write(a*self.corrected * self.b * self.centered) 

    def get_model_matrix(self):
        if self.minimapa:
            self.S = glm.scale(glm.mat4(), (4,4,4))            
        m_model = glm.mat4()
        self.T0 = glm.translate(self.T0, (-1.75,-5,-1.75 ))
        self.centered = self.T*self.R*self.S * self.T0
        m_model = self.T*self.R*self.S * self.T0 * m_model # La matriu del model està centrada al 0, aixi les rotacions les apliquem en aquesta
        return m_model
    
        
    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
        self.texture = self.app.texture.textures["cotxe"]
        self.texture.use(location=0)

    def render(self):
        self.texture.use(location=0)
        self.vao.render()
                
    def destroy (self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])
        return vao
    
    
    def get_vertex_data(self, color):
        #tots els vertex que formen el cotxe
        vertices = [(0,-1,1),(3.5,-1,1),(3.5,-1,2.5),(0,-1,2.5),(3.5,0.6,2.5),(0,0.5,2.5),
        (3.5,1.4,3.5),(0,1.4,3.5),(3.5,5.2,3.5),(0,5.2,3.5),(3.5,6,2.5),(0,6,2.5),
        (3.5,9,2.5),(0,9,2.5),(3.5,9,1),(0,9,1),(0,1.6,1),(3.5,5,1),
        
        (0,0.8,0.8),(0.5,0.8,0.8),(3,0.8,0.8),(3.5,0.8,0.8),(0,5.8,0.8),(0.5,5.8,0.8),(3,5.8,0.8),(3.5,5.8,0.8),
        
        (0,0,1),(0,0,0.6),(0,0.2,0.2),(0,0.6,0),(0,1,0),(0,1.4,0.2),(0,1.6,0.6),(0,1.6,1),(0,1.4,1.4),(0,1,1.6),(0,0.6,1.6),(0,0.2,1.4),
        (0.5,0,1),(0.5,0,0.6),(0.5,0.6,0),(0.5,1,0),(0.5,1.4,0.2),(0.5,1.6,0.6),(0.5,1.6,1),(0.5,1.4,1.4),(0.5,1,1.6),(0.5,0.6,1.6),(0.5,0.6,1.6),(0.5,0.2,1.4),
        
        (3,0,1),(3,0,0.6),(3,0.2,0.2),(3,0.6,0),(3,1,0),(3,1.4,0.2),(3,1.6,0.6),(3,1.6,1),(3,1.4,1.4),(3,1,1.6),(3,0.6,1.6),(3,0.2,1.4),
        (3.5,0,1),(3.5,0,0.6),(3.5,0.2,0.2),(3.5,0.6,0),(3.5,1,0),(3.5,1.4,0.2),(3.5,1.6,0.6),(3.5,1.6,1),(3.5,1.4,1.4),(3.5,1,1.6),(3.5,0.6,1.6),(3.5,0.2,1.4),
        
        (0,5,1),(0,5,0.6),(0,5.2,0.2),(0,5.6,0),(0,6,0),(0,6.4,0.2),(0,6.6,0.6),(0,6.6,1),(0,6.4,1.4),(0,6,1.6),(0,5.6,1.6),(0,5.2,1.4),
        (0.5,5,1),(0.5,5,0.6),(0.5,5.2,0.2),(0.5,5.6,0),(0.5,6,0),(0.5,6.4,0.2),(0.5,6.6,0.6),(0.5,6.6,1),(0.5,6.4,1.4),(0.5,6,1.6),(0.5,5.6,1.6),(0.5,5.2,1.4),
        
        (3,5,1),(3,5,0.6),(3,5.2,0.2),(3,5.6,0),(3,6,0),(3,6.4,0.2),(3,6.6,0.6),(3,6.6,1),(3,6.4,1.4),(3,6,1.6),(3,5.6,1.6),(3,5.2,1.4),
        (3.5,5,1),(3.5,5,0.6),(3.5,5.2,0.2),(3.5,5.6,0),(3.5,6,0),(3.5,6.4,0.2),(3.5,6.6,0.6),(3.5,6.6,1),(3.5,6.4,1.4),(3.5,6,1.6),(3.5,5.6,1.6),(3.5,5.2,1.4),
        
        ]
        
        indices = [(0,1,2),(0,2,3),(3,2,4),(3,4,5),(5,4,6),(5,6,7),(7,6,8),(7,8,9),(9,8,10),
                  (9,10,11),(11,10,12),(11,12,13),(13,12,14),(13,14,15),(0,3,5),(0,5,16),
                  (16,5,7),(16,7,9),(16,9,11),(11,13,15),(16,11,15),(1,4,2),(1,17,4),(17,6,4),
                  (17,8,6),(17,10,8),(17,14,10),(14,12,10),(14,15,0),(14,0,1), 
                
                  (26,37,18),(37,36,18),(36,35,18),(35,34,18),(34,33,18),(33,32,18),(32,31,18),(31,30,18),(30,29,18),(29,28,18),(28,27,18),(27,26,18),
                  (49,38,19),(48,49,19),(47,48,19),(46,47,19),(45,46,19),(44,45,19),(43,44,19),(42,43,19),(41,42,19),(40,41,19),(39,40,19),(38,39,19),
                  (26,38,49),(26,49,37),(37,49,48),(37,48,36),(36,48,47),(36,47,35),(35,47,46),(35,46,34),(34,46,45),(34,45,33),(33,45,44),(33,44,32),
                  (32,44,43),(32,43,31),(31,43,42),(31,42,30),(30,42,41),(30,41,29),(29,41,40),(29,40,28),(28,40,39),(28,39,27),(27,39,38),(27,38,26),
                  
                  (50,61,20),(61,60,20),(60,59,20),(59,58,20),(58,57,20),(57,56,20),(56,55,20),(55,54,20),(54,53,20),(53,52,20),(52,51,20),(51,50,20),
                  (73,62,21),(72,73,21),(71,72,21),(70,71,21),(69,70,21),(68,69,21),(67,68,21),(66,67,21),(65,66,21),(64,65,21),(63,64,21),(62,63,21),
                  (50,62,73),(50,73,61),(61,73,72),(61,72,60),(60,72,71),(60,71,59),(59,71,70),(59, 70,58),(58,70,69),(58,69,57),(57,69,68),(57,68,56),
                  (56,68,67),(56,67,55),(55,67,66),(55,66,54),(54,66,65),(54,65,53),(53,65,64),(53,64,52),(52,64,63),(52,63,51),(51,63,62),(51,62,50),
                  
                  (74,85,22),(85,84,22),(84,83,22),(83,82,22),(82,81,22),(81,80,22),(80,79,22),(79,78,22),(78,77,22),(77,76,22),(76,75,22),(75,74,22),
                  (97,86,23),(96,97,23),(95,96,23),(94,95,23),(93,94,23),(92,93,23),(91,92,23),(90,91,23),(89,90,23),(88,89,23),(87,88,23),(86,87,23),
                  (74,86,97),(74,97,85),(85,97,96),(85,96,84),(84,96,95),(84,95,83),(83,95,94),(83,94,82),(82,94,93),(82,93,81),(81,93,92),(81,92,80),
                  (80,92,91),(80,91,79),(79,91,90),(79,90,78),(78,90,89),(78,89,77),(77,89,88),(77,88,76),(76,88,87),(76,87,75),(75,87,86),(75,86,74),
                
                  (109,98,24),(108,109,24),(107,108,24),(106,107,24),(105,106,24),(104,105,24),(103,104,24),(102,103,24),(101,102,24),(100,101,24),(99,100,24),(98,99,24),
                  (121,110,25),(120,121,25),(119,120,25),(118,119,25),(117,118,25),(116,117,25),(115,116,25),(114,115,25),(113,114,25),(112,113,25),(111,112,25),(110,111,25),
                  (98,110,121),(98,121,109),(109,121,120),(109,120,108),(108,120,119),(108,119,107),(107,119,118),(107,118,106),(106,118,117),(106,117,105),(105,117,116),(105,116,104),
                  (104,116,115),(104,115,103),(103,115,114),(103,114,102),(102,114,113),(102,113,101),(101,113,112),(101,112,100),(100,112,111),(100,111,99),(99,111,110),(99,110,98) 
              ]

        vertex_data = self.get_data(vertices, indices, color)
        
        #textura del cotxe
        tex_coord = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),                             
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),
                             (3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0),(3, 2, 1),(3, 1, 0)]
                         

        tex_coord_data = self.get_data(tex_coord, tex_coord_indices, color)
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
    
    @staticmethod
    def get_data(vertices, indices, color): 
       data = [vertices[ind] for triangle in indices for ind in triangle]
       return np.array(data, dtype='f4')

    def get_vbo(self,color):
        vertex_data = self.get_vertex_data(color)
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self):
       program = self.ctx.program(    
           vertex_shader='''
               #version 330
               layout (location = 0) in vec2 in_texcoord_0;
               layout (location = 1) in vec3 in_position;
               
               out vec2 uv_0;
               
               uniform mat4 m_proj;
               uniform mat4 m_view;
               uniform mat4 m_model;
               
               void main() {
                   uv_0 = in_texcoord_0;
                   gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
               }
           ''',
           fragment_shader='''
               #version 330
               layout (location = 0) out vec4 fragColor;
               in vec2 uv_0;
               
               uniform sampler2D u_texture_0;
               
               void main() { 
                   vec3 color = texture(u_texture_0, uv_0).rgb;
                   fragColor = vec4(color,1.0);
               }
           ''',
       )
       return program