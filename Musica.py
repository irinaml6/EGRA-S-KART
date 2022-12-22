# PROJECTE EGRA: Grup 2
# MUSICA: en aquesta classe carreguem tots els audios que utilitzem.

from pygame import mixer

class Musica:
    def __init__(self,app):
        self.app = app
        
        self.musiques = {}
        self.musiques['fondo'] = 'musiquita/musica d fondo.wav'
        self.musiques['arrencada'] = 'musiquita/Arrencar cotxe.wav'
        self.musiques['motor'] = 'musiquita/Motor corriendo.wav'
        self.musiques['inici'] = 'musiquita/soroll inici (3s).wav'
        self.musiques['ult_volta'] = 'musiquita/SE_RC_LAP_FINAL.wav'
        self.musiques['volta'] = 'musiquita/SE_RC_LAP.wav'
        self.musiques['fin_volta'] = 'musiquita/SE_RC_GOAL.wav'
        self.musiques['col_metall'] = 'musiquita/SE_VCL_COL_METAL.wav'
        self.musiques['col_cubitos'] = 'musiquita/SE_ITM_BOX_BRK.wav'
        self.musiques['final'] = 'musiquita/SE_RC_GOAL.wav'
        self.musiques['colisio'] = 'musiquita/SE_VCL_COL_CAR.wav'
        self.musiques['col_roca'] = 'musiquita/SE_VCL_COL_GAKE.wav'
        self.musiques['fondo2'] = 'musiquita/fondo2.wav'
        self.musiques['fondo3'] = 'musiquita/fondo3.wav'
        self.musiques['nop'] = 'musiquita/SE_UI_CTRL_REJECT.wav'
        self.musiques['fondo_rapid'] = 'musiquita/musica d fondo_rapid.wav'
        self.musiques['fondo2_rapid'] = 'musiquita/fondo2_rapid.wav'
        self.musiques['fondo3_rapid'] = 'musiquita/fondo3_rapid.wav'
        self.musiques['inici2'] = 'musiquita/inici2.wav'
        self.musiques['tinta'] = 'musiquita/SE_ITM_GESO_START.wav'
        self.musiques['nitro'] = 'musiquita/SE_ITM_BANANA_FLY.wav'
        
        mixer.init()
        
        
    def load(self,song):
        m = mixer.Sound(self.musiques[song])
        return m
    
