# PROJECTE EGRA: Grup 2
# CÀMERA MINIMAPA: Càmera que mostra una vista sencera del circuit des de dalt que utilitzem com a minimapa.

import glm

class Camera_m:
    def __init__(self, app):
        self.app = app
        self.aspec_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position = glm.vec3(-40,450,223.269)
        self.up = glm.vec3(1,0,0)
        self.at = glm.vec3(-40,0,223.269)
        self.angle = 0
        self.perspectiva = True
        # view_matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        
        
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.at, self.up)
    
    def get_projection_matrix(self):
        return glm.ortho(-3,3,-3,3,0.1,100)
        
    
    def setCamera(self,position, at, up, angle):
        self.position = position
        self.at = at
        self.up = up
        self.angle = angle
        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()
        self.app.circuit_m.shader_program['m_view'].write(self.m_view)
        if self.app.num_circuit == '1':
            self.app.nitro2.shader_program['m_view'].write(self.m_view)
        elif self.app.num_circuit == '2':
            self.app.nitro.shader_program['m_view'].write(self.m_view)
        self.app.cotxe_m.shader_program['m_view'].write(self.m_view)

        
        