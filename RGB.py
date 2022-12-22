# PROJECTE EGRA: Grup 2
# RGB: en aquesta classe creem els pickles que contenen matrius de les posicions, 
#      on cada posicio és una tupla del color del píxel de la textura corresponent.

from skimage import io
import numpy as np
import cv2
import pickle

class Colors:
    def __init__(self, app):
        self.app = app
        #self.matriu = self.get_matriu('textures/arco_colors.jpg') #afegir tambe dir_path com a parametre
        self.matriu = self.get_matriu()
        
        
    def get_pos(self,x,z):        
        j = int((z+30.316)*(1024/(476.622+30.316)))
        i = int((x-214.154)*(1024/(-292.784-214.154)))
        
        return i,j

    def get_matriu(self):        
        if self.app.num_circuit == '1':
            nom_fitxer = "pickles/circuit1.pickle"
        elif self.app.num_circuit == '2':
            nom_fitxer = "pickles/circuit2.pickle"
        elif self.app.num_circuit == '3':
            nom_fitxer = "pickles/circuit3.pickle"
            
        ### CREACIÓ PICKLES ###
            
        # img = io.imread(dir_path)
        # r,g,b = cv2.split (img)
        
        # imatge = np.empty((1024,1024), tuple)
        
        # for i in range(len(imatge)):
        #     for j in range(len(imatge)):
        #         tupla = (round(r[i,j]/255,3),round(g[i,j]/255,3),round(b[i,j]/255,3))
        #         imatge[i,j] = tupla
        
        # with open(nom_fitxer, "wb") as f1:
        #     pickle.dump(imatge, f1)
        
        with open(nom_fitxer, "rb") as f1:
            imatge = pickle.load(f1)
    
        return imatge
    
    def get_color(self,x,z):
        xx, zz = self.get_pos(x,z)        
        color = self.matriu[xx, zz]
        
        return color
    
    


        

        


