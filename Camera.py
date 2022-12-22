# PROJECTE EGRA: Grup 2
# CÀMERA: En aquesta classse creem 3 objectes càmera que seguiexen el cotxe des de diferents punts de vista.

import math
import glm
from pygame.math import Vector3


class Camera:
    def __init__(self, app):
        self.app = app
        self.aspec_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        
        #defienir paràmetres per després canviar de càmera
        self.camares = [Vector3(-20,10,-20), Vector3(25,10,5), Vector3(85,100,0)] #vector que conté les posicions de les 3 càmeres
        self.actual = 0
        self.anterior = 0
        self.x = self.camares[self.actual][0]
        self.y = self.camares[self.actual][1]
        self.z = self.camares[self.actual][2] 
        
        self.position = Vector3(self.x,self.y,self.z)
        self.center = glm.vec3(0,0,0)
        self.up = glm.vec3(0,1,0)
        self.graus = 60
        self.perspectiva = True
        self.velocity = 0
        self.acceleration = 0.0
        
        # view_matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        
        #físiquies càmera
        self.a = 0.1
        self.length = 4
        self.max_acceleration = 5.0
        self.max_steering = 30
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.rotation_matrix = glm.mat4()
        self.rotation_matrix_forward = glm.mat4()
        self.acceleration = 0.0
        self.steering = 0.0
        self.angle = 0


    def get_view_matrix(self):
        l = [self.position[0], self.position[1], self.position[2]]
        return glm.lookAt(glm.vec3(l), self.center, self.up)
    
    def get_projection_matrix(self):
        if self.graus != 0:
            return glm.perspective(glm.radians(self.graus), self.aspec_ratio, 0.1, 1000)
        else:
            return glm.ortho(-2,2,-2,2, 0.1, 100)
        
    def forward(self, dt):
        if self.velocity < 0:
            self.acceleration = 0 
        else:
            self.acceleration += 1 * dt

        self.velocity += self.acceleration * dt
        if self.velocity >= self.max_velocity:
            self.velocity = self.max_velocity

   
    def turn(self, side, deltaTime):
        
        if side == "right":
            self.steering += 110 * deltaTime
            self.b = glm.rotate(glm.mat4(), glm.radians(self.a-1), glm.vec3(0,1,0))           
            self.a-= 0.5
            
        elif side == "left":
            self.steering -= 110 * deltaTime           
            self.b = glm.rotate(glm.mat4(), glm.radians(self.a+1), glm.vec3(0,1,0))
            self.a+= 0.5
            
    def update(self, dt, canvi, panoramica):
        if self.velocity >= self.max_velocity:
            self.velocity = self.max_velocity

        l = [self.app.cotxe.position[0], self.app.cotxe.position[1], self.app.cotxe.position[2]]
        self.center = glm.vec3(l) + glm.vec3(0,4,0)
        
        vx = math.cos(glm.radians(self.steering) )
        vz = math.sin(glm.radians(self.steering) )
        
        if self.actual == 0:
            p2 = self.center + self.length*glm.vec3((-3*vx,1,-3*vz))
        elif self.actual == 1:
            p2 = self.center + self.length*glm.vec3((-3*vx,1,-3*vz)) + glm.vec3(0,90,0)
        elif self.actual == 2:
            p2 = self.center + self.length*glm.vec3((+6*vx,1,+6*vz)) # + glm.vec3(50,0,0)
       
        m_view = glm.lookAt(glm.vec3(p2), self.center, self.up)
        
        #canvi de càmera
        if canvi:
            if self.actual == 0:
                self.actual = 1
                self.anterior = 0
                self.position[0] = self.position[0] + 50
            elif self.actual == 1:
                self.actual = 0
                self.anterior = 1
                self.position[0] = self.position[0] - 50
            elif self.actual == 2:
                self.actual = self.anterior
                self.position = glm.vec3(self.position[0]+40, self.position[1]-90, self.position[2]+5)
            self.app.canvi = False
        
        if panoramica:
            if self.actual == 2:
                self.actual = self.anterior
                self.position = glm.vec3(self.position[0]+40, self.position[1]-90, self.position[2]+5)
                
            else: 
                self.anterior = self.actual
                self.actual = 2
                self.position = glm.vec3(self.position[0]-40, self.position[1]+90, self.position[2]-5)
            self.app.panoramica = False
            
            self.x = self.position[0] 
            self.y = self.position[1]
            self.z = self.position[2]
        
        self.app.cotxe.shader_program['m_view'].write(m_view)
        self.app.circuit.shader_program['m_view'].write(m_view)
        self.app.cartell.shader_program['m_view'].write(m_view)
        self.app.cubitos.shader_program['m_view'].write(m_view) 
        self.app.meta1.shader_program['m_view'].write(m_view) 
        self.app.meta2.shader_program['m_view'].write(m_view)  
        if self.app.mode_joc == '2':
            self.app.cotxe_fantasma.shader_program['m_view'].write(m_view)
        
        #321 inici partida
        if 5 < self.app.time_inici_partida < 6:
            self.app.pancarta3.shader_program['m_view'].write(m_view) 
        if 6 < self.app.time_inici_partida < 7:
            self.app.pancarta2.shader_program['m_view'].write(m_view) 
        if 7 < self.app.time_inici_partida < 8.3:
            self.app.pancarta1.shader_program['m_view'].write(m_view) 
            
        if self.app.num_voltes == 4:
            self.app.game_over.shader_program['m_view'].write(m_view)
            
        #shader_program depenent del circuit
        if self.app.num_circuit == '1':
            self.app.pregunta1.shader_program['m_view'].write(m_view) 
            self.app.pregunta2.shader_program['m_view'].write(m_view) 
            self.app.pregunta3.shader_program['m_view'].write(m_view) 
            self.app.tronco1.shader_program['m_view'].write(m_view)
            self.app.fulles1.shader_program['m_view'].write(m_view)
            self.app.tronco2.shader_program['m_view'].write(m_view)
            self.app.fulles2.shader_program['m_view'].write(m_view)
            self.app.tronco3.shader_program['m_view'].write(m_view)
            self.app.fulles3.shader_program['m_view'].write(m_view)
            self.app.tronco4.shader_program['m_view'].write(m_view)
            self.app.fulles4.shader_program['m_view'].write(m_view)
            self.app.tronco5.shader_program['m_view'].write(m_view)
            self.app.fulles5.shader_program['m_view'].write(m_view)
            self.app.tronco6.shader_program['m_view'].write(m_view)
            self.app.fulles6.shader_program['m_view'].write(m_view)
            self.app.tronco7.shader_program['m_view'].write(m_view)
            self.app.fulles7.shader_program['m_view'].write(m_view)
            self.app.tronco8.shader_program['m_view'].write(m_view)
            self.app.fulles8.shader_program['m_view'].write(m_view)
            self.app.tronco9.shader_program['m_view'].write(m_view)
            self.app.fulles9.shader_program['m_view'].write(m_view)
            self.app.tronco10.shader_program['m_view'].write(m_view)
            self.app.fulles10.shader_program['m_view'].write(m_view)
            self.app.tronco11.shader_program['m_view'].write(m_view)
            self.app.fulles11.shader_program['m_view'].write(m_view)
            self.app.tronco12.shader_program['m_view'].write(m_view)
            self.app.fulles12.shader_program['m_view'].write(m_view)
            self.app.tronco13.shader_program['m_view'].write(m_view)
            self.app.fulles13.shader_program['m_view'].write(m_view)
            self.app.tronco14.shader_program['m_view'].write(m_view)
            self.app.fulles14.shader_program['m_view'].write(m_view)
            self.app.tronco15.shader_program['m_view'].write(m_view)
            self.app.fulles15.shader_program['m_view'].write(m_view)
            self.app.tronco16.shader_program['m_view'].write(m_view)
            self.app.fulles16.shader_program['m_view'].write(m_view)
            self.app.tronco17.shader_program['m_view'].write(m_view)
            self.app.fulles17.shader_program['m_view'].write(m_view)
            self.app.tronco18.shader_program['m_view'].write(m_view)
            self.app.fulles18.shader_program['m_view'].write(m_view)
            self.app.nitro2.shader_program['m_view'].write(m_view)
            self.app.escales.shader_program['m_view'].write(m_view)
            self.app.pal.shader_program['m_view'].write(m_view)
            self.app.bandera.shader_program['m_view'].write(m_view)
            
        elif self.app.num_circuit == '2':
            self.app.roca1.shader_program['m_view'].write(m_view)
            self.app.roca2.shader_program['m_view'].write(m_view)
            self.app.fletxa1.shader_program['m_view'].write(m_view)
            self.app.fletxa2.shader_program['m_view'].write(m_view)
            self.app.nitro.shader_program['m_view'].write(m_view)
            self.app.game_over.shader_program['m_view'].write(m_view)  

        elif self.app.num_circuit == '3':
            self.app.skybox.shader_program['m_view'].write(m_view)
            self.app.bandera2.shader_program['m_view'].write(m_view)
            self.app.bandera3.shader_program['m_view'].write(m_view)
            self.app.pal2.shader_program['m_view'].write(m_view)
            self.app.pal3.shader_program['m_view'].write(m_view)
