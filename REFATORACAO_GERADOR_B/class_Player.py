#RECEBE LISTA DE NOTAS vinda de GeradorNotas e RETORNA SONS

import pygame
import pygame.midi
import time

pygame.init()
pygame.mixer.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)

from class_Utilidades import Utilidades,DISTANCIA_OITAVA
from enum_Valores import ValoresInstrumentos

class Player:
    def __init__(self,musica):
        self.musica = musica

    def play(self):
        for nota in self.musica:
            if nota.valorMIDI is not None:
                valor_instrumento = ValoresInstrumentos[nota.instrumento].value
                midi_out.set_instrument(valor_instrumento)
                midi_out.note_on(nota.valorMIDI,nota.volume)
                time.sleep(Utilidades.bpmParaMilisegundos(nota.bpm))
                midi_out.note_off(nota.valorMIDI,nota.volume)
            else:
                pass
