# PROJECTE EGRA: Grup 2
# TEXTURE: en aquesta classe carreguem totes les textures que utilitzem.


import pygame as pg

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures['cotxe'] = self.get_texture(path='textures/cotxe1.jpg')
        self.textures['cubitos1'] = self.get_texture(path='textures/cubitos.png')
        self.textures['cubitos2'] = self.get_texture(path='textures/circuit2_bo.jpg')
        self.textures['meta'] = self.get_texture(path='textures/blanco.jpg')
        self.textures['pregunta'] = self.get_texture(path='textures/cubo_pregunta.jpg')
        self.textures['circuit1'] = self.get_texture(path='textures/circuit1.jpg')
        self.textures['circuit2'] = self.get_texture(path='textures/circuit2_bo.png')
        self.textures['circuit3'] = self.get_texture(path='textures/arco.jpg')
        self.textures['cartell1'] = self.get_texture(path='textures/cartell.png')
        self.textures['cartell3'] = self.get_texture(path='textures/cartell3.png')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/SkyBox_circuit1/', ext='png')
        self.textures['skybox2'] = self.get_texture_cube(dir_path='textures/SkyBox_circuit2/', ext='png')
        self.textures['skybox3'] = self.get_texture_cube(dir_path='textures/SkyBox_circuit3/', ext='png')
        self.textures['tronco'] = self.get_texture(path='textures/tronco.jpeg')
        self.textures['fulles'] = self.get_texture(path='textures/fulles.jpeg')
        self.textures['escales'] = self.get_texture(path='textures/escales.png')
        self.textures['bandera'] = self.get_texture(path='textures/bandera.png')
        self.textures['roca'] = self.get_texture(path='textures/roca2.png')
        self.textures['fletxa'] = self.get_texture(path='textures/fletxa.jpg')
        self.textures['nitro'] = self.get_texture(path='textures/nitro.png')
        self.textures['fantasma'] = self.get_texture(path='textures/cotxe_fantasma.jpg')
        self.textures['1_temps'] = self.get_texture(path='textures/1_temps.jpg')
        self.textures['2_temps'] = self.get_texture(path='textures/2_temps.jpg')
        self.textures['3_temps'] = self.get_texture(path='textures/3_temps.jpg')
        self.textures['game_over'] = self.get_texture(path='textures/game_over.png')
       
        
    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom','front', 'back']
        textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]    
        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)
        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube
 
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture,'RGB'))
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]