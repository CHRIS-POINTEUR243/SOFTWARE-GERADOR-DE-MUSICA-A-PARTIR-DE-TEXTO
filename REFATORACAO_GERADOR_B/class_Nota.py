from enum_Valores import ValoresNotas

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