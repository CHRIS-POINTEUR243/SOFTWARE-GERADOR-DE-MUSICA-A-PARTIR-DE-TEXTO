import pygame
import numpy as np

SAMPLE_RATE = 44100  # Hz

pygame.init()
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)

def gerar_tom(freq, duracao=0.4, volume=0.5):
    t = np.linspace(0, duracao, int(SAMPLE_RATE * duracao), False)
    
    onda = (
    1.0 * np.sin(2 * np.pi * freq * t) +       # fundamental
    0.5 * np.sin(2 * np.pi * 2*freq* t) +     # 2º harmônico
    0.3 * np.sin(2 * np.pi * 3*freq * t)       # 3º harmônico...
)
    #onda = np.sin(2 * np.pi * freq * t)
    onda = (onda * 32767 * volume).astype(np.int16)
    onda_stereo = np.column_stack((onda, onda))  # 2 canais
    return pygame.sndarray.make_sound(onda_stereo)

notas_freq = {
    "A": 440.00,   # Lá
    "B": 493.88,   # Si
    "C": 261.63,   # Dó
    "D": 293.66,   # Ré
    "E": 329.63,   # Mi
    "F": 349.23,   # Fá
    "G": 392.00,   # Sol
    "H": 466.16,   # Si♭
}

def tocar_texto(texto):
    for ch in texto:
        if ch in notas_freq:          # só A–H maiúsculo
            som = gerar_tom(notas_freq[ch])
            som.play()
        # se não for nota, é pausa
        pygame.time.wait(450)

# exemplo de uso:
if __name__ == "__main__":

    texto = input("Digite texto Majuscula:") # só letras A–H vão virar soms
    tocar_texto(texto)
    pygame.quit()

