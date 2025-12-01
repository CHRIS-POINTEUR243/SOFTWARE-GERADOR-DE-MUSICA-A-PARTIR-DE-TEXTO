#Usada em Player, GeradorNotas e Nota

MINUTO = 60
DISTANCIA_OITAVA = 12
UNIDADE_BPM = 80

class Utilidades:
    def bpmParaMilisegundos(bpm):
        tempo = 1 / (bpm / MINUTO)
        return tempo

