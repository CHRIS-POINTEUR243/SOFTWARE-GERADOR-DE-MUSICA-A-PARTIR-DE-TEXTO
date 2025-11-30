from enum_Valores import ValoresNotas
from class_Utilidades import DISTANCIA_OITAVA

NOTA_DEFAULT = 'C'

class Nota:
    def __init__(self, caractere, oitava, bpm, volume, instrumento):
        self.caractere = caractere
        self.oitava = oitava
        self.bpm = bpm
        self.volume = volume
        self.instrumento = instrumento

        if caractere in ValoresNotas.__members__:
            self.valorMIDI = ValoresNotas[caractere].value
        else:
            self.valorMIDI = None

        base_mais_oitava = self.valorMIDI + (DISTANCIA_OITAVA * self.oitava)

        if base_mais_oitava <= 127:
            self.valorMIDI = base_mais_oitava
        else:
            pass