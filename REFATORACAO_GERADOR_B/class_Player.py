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
                notaMIDI = nota.valorMIDI + (DISTANCIA_OITAVA * nota.oitava)
                valor_instrumento = ValoresInstrumentos[nota.instrumento].value
                midi_out.set_instrument(valor_instrumento)
                midi_out.note_on(notaMIDI,nota.volume)
                time.sleep(Utilidades.bpmParaMilisegundos(nota.bpm))
                midi_out.note_off(notaMIDI,nota.volume)
            else:
                pass