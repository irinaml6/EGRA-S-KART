# PROJECTE EGRA: Grup 2
# En aquesta classe carreguem la textura dels 3 cirucuits.
import numpy as np
import glm

class Circuit:
    def __init__(self,app):
        self.app = app
        self.ctx = app.ctx
        self.shader_program = self.get_shader_program()
        self.m_model = self.get_model_matrix()
        self.on_init()
        self.time = 0.1
        self.vbo = self.get_vbo((1,1,0)) 
        self.vao = self.get_vao() #cares
       
    def update(self):
        self.texture.use(location=0)
        self.shader_program['m_model'].write(glm.mat4())

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
        
    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)
        if self.app.num_circuit == '1':
            self.texture = self.app.texture.textures['circuit1']  
        elif self.app.num_circuit == '2':
            self.texture = self.app.texture.textures['circuit2']  
        elif self.app.num_circuit == '3':
            self.texture = self.app.texture.textures['circuit3']  
        self.shader_program['u_texture_0'] = 0
        self.texture.use(location=0)

    def render(self):
        self.update()
        self.vao.render()

    def destroy (self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
    
    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position_circuit')])
        return vao
    
    def get_vaoa(self):
        vaoa = self.ctx.vertex_array(self.shader_program, [(self.vboa, '3f 3f', 'in_color','in_position_circuit')])
        return vaoa
    
    def get_vaop(self):
        vaop = self.ctx.vertex_array(self.shader_program, [(self.vbop, '3f 3f', 'in_color','in_position_circuit')])
        return vaop
    
    def get_vertex_data(self, color):
        vertices = [(214.154,0,-30.316), (214.154,0,476.622), (-292.784,0,476.622), (-292.784,0,-30.316)]
        indices = [(0,2,3),(0,1,2)]
        vertex_data = self.get_data(vertices, indices, color)
        tex_coord = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [(0,2,3), (0,1,2)]
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
                layout (location = 1) in vec3 in_position_circuit;
                
                out vec2 uv_0;
                
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                
                void main() {
                    uv_0 = in_texcoord_0;
                    gl_Position = m_proj * m_view * m_model * vec4(in_position_circuit, 1.0);
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