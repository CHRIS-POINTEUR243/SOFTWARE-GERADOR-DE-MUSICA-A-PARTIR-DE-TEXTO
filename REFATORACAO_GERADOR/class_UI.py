#TESTE DE CLASSE UI CHAMANDO MUSIC SERVICES

#ESTÁ DANDO ERRO POIS O STREAMLIT NÃO TEM PORTA MIDI, ENTÃO PYGAME.MIDI NÃO FUNCIONA PRA SAIR SOM DIRETO NO STREAMLIT
#PELO QUE EU LI, TEM QUE TRANSFORMAR O ARQUIVO MIDI PARA WAV OU MP3 E TOCAR NA INTERFACE POR ST.AUDIO()
#BIBLIOTECAS FLUIDSYNTH, MIDO CONSEGUEM FAZER ISSO, APARENTEMENTE

import streamlit as st
from class_MusicServices import MusicServices
from enum_Valores import ValoresInstrumentos

NOTA_DEFAULT = 'C'
OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 127  # máximo
BPM_DEFAULT = 120
INSTRUMENTO_DEFAULT = 'ACOUSTIC_GRAND_PIANO'
VALOR_INSTRUMENTO_DEFAULT = ValoresInstrumentos.ACOUSTIC_GRAND_PIANO.name

opcoes_oitava = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
opcoes_instrumentos = [inst.name for inst in ValoresInstrumentos]

class UI:
    def __init__(self):
        self.inicializaCabecalho()
        self.inicializaInterface()

    def inicializaCabecalho(self):
        st.set_page_config(page_title="Gerador de Música", page_icon="🎵")

        # Título central
        st.markdown(
            "<h1 style='text-align:center;'>Gerador de Música</h1>",
            unsafe_allow_html=True,
        )

        st.write("")

    def inicializaInterface(self):
        st.write("Transforma texto em música!")

        if "volume" not in st.session_state:
            st.session_state.volume = VOLUME_DEFAULT
        if "oitava" not in st.session_state:
            st.session_state.oitava = OITAVA_DEFAULT
        if "bpm" not in st.session_state:
            st.session_state.bpm = BPM_DEFAULT

        st.write("")

        with st.form(key="gerar_musica"):

            texto = st.text_input("Insira o texto:", placeholder="Ex: ABRA A GAIOLA DE H ...")

            st.write("")
            arquivo_texto = st.file_uploader("Ou carregue um arquivo texto:",type=["txt"])

            self.volume = st.slider("Volume",0,127,127)
            self.oitava = st.selectbox("Oitava:",opcoes_oitava,OITAVA_DEFAULT)
            self.bpm = st.number_input("Bpm:",10,280,120,10)
            self.instrumento = st.selectbox("Instrumento:",opcoes_instrumentos,index=opcoes_instrumentos.index(VALOR_INSTRUMENTO_DEFAULT))

            submit_button = st.form_submit_button(label="Gerar Música")
            if submit_button:
                if texto and arquivo_texto:
                    st.warning("Insira um texto OU carregue um arquivo!")
                    return
                
                elif texto and not arquivo_texto:
                    texto_converter = texto

                elif arquivo_texto and not texto:
                    texto_converter = arquivo_texto

                music_services = MusicServices(texto_converter,INSTRUMENTO_DEFAULT,self.oitava,self.volume,self.bpm)


if __name__ == "__main__":

    ui = UI()
