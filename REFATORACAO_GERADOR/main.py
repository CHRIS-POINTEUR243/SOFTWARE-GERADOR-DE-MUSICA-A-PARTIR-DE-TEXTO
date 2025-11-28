#FUNCIONA PELO PYGAME MIDI USANDO ESTE ARQUIVO MAIN

from class_MusicServices import MusicServices

NOTA_DEFAULT = 'C'
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  # máximo
BPM_DEFAULT = 120
INSTRUMENTO_DEFAULT = 'ACOUSTIC_GRAND_PIANO'

if __name__ == "__main__":
    def roda_teste(texto,descricao):
        music_services = MusicServices(texto,INSTRUMENTO_DEFAULT,OITAVA_DEFAULT,VOLUME_DEFAULT,BPM_DEFAULT)
        print(descricao)

#Testes
    roda_teste("AA++AA---AA", "BPM+")






