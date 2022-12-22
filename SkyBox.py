# PROJECTE EGRA: Grup 2
#SKYBOX: En aquesta classe creem els 3 skybox que utilitzem

import numpy as np
import glm
       
class SkyBox:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.shader_program = self.get_shader_program()
        self.m_model = self.get_model_matrix()
        self.on_init()
        self.time = 0.1
        self.vbo = self.get_vbo((1,1,0))
        self.vboa = self.get_vbo((1,0,1))
        self.vbop = self.get_vbo((0.5,1,1))
        self.vao = self.get_vao() #cares

    def update(self):
        self.texture.use(location=0)
        self.shader_program['m_view'].write(glm.mat4(glm.mat3(self.app.camera.m_view)))
        
    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
        
    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(glm.mat4(glm.mat3(self.app.camera.m_view)))
        if self.app.num_circuit == '1':
            string = 'skybox'
            self.texture = self.app.texture.textures[string]
            self.shader_program['u_texture_0'] = 0
            self.texture.use(location=0)
            
        elif self.app.num_circuit == '2':
            string = 'skybox2' 		 
            self.texture = self.app.texture.textures[string]
            self.shader_program['u_texture_0'] = 0
            self.texture.use(location=0)
        # elif self.app.num_circuit == '3':
        # 		string = 'skybox3'
        
        
    def render(self):
        self.update()
        self.vao.render()
        
    def destroy (self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao
    
    def get_vaoa(self):
        vaoa = self.ctx.vertex_array(self.shader_program, [(self.vboa, '3f 3f', 'in_color','in_position')])
        return vaoa
    
    def get_vaop(self):
        vaop = self.ctx.vertex_array(self.shader_program, [(self.vbop, '3f 3f', 'in_color','in_position')])
        return vaop
    
    def get_vertex_data(self, color):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
                
        vertex_data = self.get_data(vertices, indices, color)
        
        #ho invertim perque volem pintar el cub per dins, agulles del rellotge
        vertex_data = np.flip(vertex_data, 1).copy(order='C')
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
                layout (location = 0) in vec3 in_position;
                
                out vec3 texCubeCoords;
                
                uniform mat4 m_proj;
                uniform mat4 m_view;

                
                void main() {
                    texCubeCoords = in_position;
                    vec4 pos = m_proj * m_view * vec4(in_position, 1.0);
                    gl_Position = pos.xyww;
                    gl_Position.z -= 0.0001; 
                }
            ''',
            fragment_shader='''
                #version 330
                out vec4 fragColor;
                
                in vec3 texCubeCoords;
                
                uniform samplerCube u_texture_0;
  
                void main() { 
                    fragColor = texture(u_texture_0, texCubeCoords);
                }
            ''',
        )
        return program


