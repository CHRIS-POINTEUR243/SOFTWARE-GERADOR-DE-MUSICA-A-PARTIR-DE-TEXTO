from enum import Enum

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
    NOVA_LINHA = '\n'  
#Relaciona tokens parseados e nomes na tabela de métodos existente em GeradorNotas

MAX_LEN_TOKEN = max(len(token.value) for token in Tokens)
#Automaticamente alterado se forem definidos tokens de tamanho maior

class ValoresNotas(Enum):
    A = 69 
    B = 71 
    C = 60 
    D = 62 
    E = 64 
    F = 65 
    G = 67 
    H = 70 
#Valores referentes à oitava central (Dó do meio = C4)

class ValoresInstrumentos(Enum):
#Alguns timbres de piano:
    ACOUSTIC_GRAND_PIANO = 0
    BRIGHT_ACOUSTIC_PIANO = 1
    ELECTRIC_GRAND_PIANO = 2
    HONKY_TONK_PIANO = 3
    RHODES_PIANO = 4
    CHORUSED_PIANO = 5
    HARPSICHORD = 6
    CLAVINET = 7
#Alguns timbres de guitarra:
    ACOUSTIC_NYLON_GUITAR = 24
    ACOUSTIC_STEEL_GUITAR = 25
    ELECTRIC_JAZZ_GUITAR = 26
    ELECTRIC_CLEAN_GUITAR = 27
    ELECTRIC_MUTED_GUITAR = 28
    OVERDRIVEN_GUITAR = 29
    DISTORTION_GUITAR = 30
    GUITAR_HARMONICS = 31
#Alguns timbres de baixo:
    ACOUSTIC_BASS = 32 
    FINGERED_ELECTRIC_BASS = 33
    PLUCKED_ELECTRIC_BASS = 34
    FRETLESS_BASS = 35
    SLAP_BASS_1 = 36
    SLAP_BASS_2 = 37
    SYNTH_BASS_1 = 38
    SYNTH_BASS_2 = 39
#Alguns timbres étnicos:
    SITAR = 104
    BANJO = 105
    SHAMISEN = 106
    KOTO = 107
    KALIMBA = 108
    BAGPIPE = 109
    FIDDLE = 110
    SHANAI = 111
#Alguns efeitos sonoros:
    TINKLE_BELL = 112
    AGOGO = 113
    STEEL_DRUMS = 114
    WOOD_BLOCK = 115
    TAIKO_DRUM = 116
    MELODIC_TOM = 117
    SYNTH_DRUM = 118
    REVERSE_CYMBAL = 119
    GUITAR_FRET_NOISE = 120
    BREATH_NOISE = 121
    SEASHORE = 122
    BIRD_TWEET = 123
    TELEPHONE_RING = 124 
    HELICOPTER = 125
    APPLAUSE = 126
    GUN_SHOT = 127
