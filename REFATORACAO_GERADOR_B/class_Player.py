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
VALOR_MIDI_MAX = 127

class Player:
    def __init__(self,musica):
        self.musica = musica

    def play(self):
        for nota in self.musica:
            if nota.valorMIDI is not None:
                base_mais_oitava = nota.valorMIDI + (DISTANCIA_OITAVA * nota.oitava)
                if base_mais_oitava <= VALOR_MIDI_MAX:
                    notaMIDI = base_mais_oitava
                else:
                    notaMIDI = nota.valorMIDI
                valor_instrumento = ValoresInstrumentos[nota.instrumento].value
                midi_out.set_instrument(valor_instrumento)
                midi_out.note_on(notaMIDI,nota.volume)
                time.sleep(Utilidades.bpmParaMilisegundos(nota.bpm))
                midi_out.note_off(notaMIDI,nota.volume)
            else:
                pass
