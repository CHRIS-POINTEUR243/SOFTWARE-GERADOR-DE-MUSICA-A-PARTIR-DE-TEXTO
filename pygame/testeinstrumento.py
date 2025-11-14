import pygame
import pygame.midi
import os
import time

#tem que ter um delay suficiente para o som tocar!

pygame.init()
pygame.mixer.init()
pygame.midi.init()
port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)

GRAND_PIANO = 0
CHURCH_ORGAN = 19
midi_out.set_instrument(GRAND_PIANO)
#valor correspondente a um instrumento no General MIDI

midi_out.note_on(76, 127)
time.sleep(1)
midi_out.note_off(76, 127)
midi_out.note_on(88, 127)
time.sleep(1)
midi_out.note_off(88, 127)
midi_out.note_on(88, 64)
time.sleep(1)
midi_out.note_off(88, 64)

#valor correspondente a uma nota e oitava no General MIDI
