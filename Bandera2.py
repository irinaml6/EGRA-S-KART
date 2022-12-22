# PROJECTE EGRA: Grup 2
import numpy as np
import glm

from codi_objectes.SuperclassObjecte import Objecte

class Bandera2(Objecte):
    def __init__(self, app, ubi):
        super().__init__(app)
        self.ubi = ubi
    
    def update(self):
        self.texture.use(location=0)
        t = glm.translate(self.m_model, self.ubi)
        self.shader_program['m_model'].write(t*self.m_model)
    
    def get_model_matrix(self):
        return super().get_model_matrix()
    def on_init(self):
        string = 'bandera'
        super().on_init(string)
    def render(self):
        super().render()
    def destroy(self):
        super().destroy()
    def get_vao(self):
        return super().get_vao()
    def get_vaoa(self):
        return super().get_vaoa()      
    def get_vaop(self):
        return super().get_vaop()
        
    def get_vertex_data(self, color):
        vertices = [(-8, 25, 0), (-8, 30, 0), (0, 25, 0), (0, 30, 0)]
        indices = [(0,3,1),(0,2,3)]
        vertex_data = self.get_data(vertices, indices, color)        
        tex_coord = [(0,0), (1,0), (1,1), (0,1)]        
        tex_coord_indices = [(3,1,0), (3,2,1)]                        
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices, color)        
        vertex_data = np.hstack([tex_coord_data, vertex_data])        
        return vertex_data
    
    def get_data(self, vertices, indices, color):
        return super().get_data(vertices, indices, color)
    def get_vbo(self, color):
        return super().get_vbo(color)
    def get_shader_program(self):
        return super().get_shader_program()