from enum import Enum

class ValoresNotas(Enum):
    A = 69 
    B = 71 
    C = 60 
    D = 62 
    E = 64 
    F = 65 
    G = 67 
    H = 70 

class ValoresInstrumentos(Enum):
    ACOUSTIC_GRAND_PIANO = 0
    BRIGHT_ACOUSTIC_PIANO = 1
    ELECTRIC_GRAND_PIANO = 2
    HONKY_TONK_PIANO = 3
    RHODES_PIANO = 4
    CHORUSED_PIANO = 5
    HARPSICHORD = 6
    CLAVINET = 7
    ACOUSTIC_NYLON_GUITAR = 24
    ACOUSTIC_STEEL_GUITAR = 25
    ELECTRIC_JAZZ_GUITAR = 26
    ELECTRIC_CLEAN_GUITAR = 27
    ELECTRIC_MUTED_GUITAR = 28
    OVERDRIVEN_GUITAR = 29
    DISTORTION_GUITAR = 30
    GUITAR_HARMONICS = 31
    ACOUSTIC_BASS = 32 
    FINGERED_ELECTRIC_BASS = 33
    PLUCKED_ELECTRIC_BASS = 34
    FRETLESS_BASS = 35
    SLAP_BASS_1 = 36
    SLAP_BASS_2 = 37
    SYNTH_BASS_1 = 38
    SYNTH_BASS_2 = 39
    TELEPHONE_RING = 124 

class Tokens(Enum):
    ESPACO = ' '
    MAIS = '+'
    MENOS = '-'
    LETRA_O = 'O'
    LETRA_I = 'I'
    LETRA_U = 'U'
    INTERROGACAO = '?'
    BPM_MAIS = 'BPM+'
    BPM_MENOS = 'BPM-'
    PONTO_VIRGULA = ';'
    NOVA_LINHA = '\n'  # adicionei ENTER / quebra de linha (NL)

MAX_LEN_TOKEN = max(len(token.value) for token in Tokens)