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
        st.set_page_config(page_title="Gerador de Música", page_icon="🎵")

        if "screen" not in st.session_state:
            st.session_state.screen = "tela_input" 

        self.music_services = None
        self.texto_converter = None

        self.inicializaCabecalho()

        if st.session_state.screen == "tela_input":
            self.telaGerador()
        elif st.session_state.screen == "tela_player":
            self.telaPlayer()

    def inicializaCabecalho(self):
        st.markdown(
            "<h1 style='text-align:center;'>Gerador de Música</h1>",
            unsafe_allow_html=True,
        )
        st.write("")

    def mudaTela(self,nome_tela):
        st.session_state.screen = nome_tela
        st.rerun()

    def telaGerador(self):
        st.write("Transforma texto em música!")

        if "volume" not in st.session_state:
            st.session_state.volume = VOLUME_DEFAULT
        if "oitava" not in st.session_state:
            st.session_state.oitava = OITAVA_DEFAULT
        if "bpm" not in st.session_state:
            st.session_state.bpm = BPM_DEFAULT

        st.write("")

        with st.form(key="gerar_musica"):

            placeholder_texto = st.empty()
            texto_digitado = placeholder_texto.text_input("Insira o texto:",placeholder="Ex: ABRA A GAIOLA DE H ...")

            st.write("")

            arquivo_texto = st.file_uploader("Ou carregue um arquivo texto:",type=["txt"])
            conteudo_arquivo = None

            if arquivo_texto is not None:
                conteudo_arquivo = arquivo_texto.read().decode("utf-8")
                placeholder_texto.text_input("Insira o texto:",value=conteudo_arquivo)
                texto_digitado = conteudo_arquivo

            self.volume = st.slider("Volume",0,127,127)
            self.oitava = st.selectbox("Oitava:",opcoes_oitava,index=opcoes_oitava.index(OITAVA_DEFAULT))
            self.bpm = st.number_input("Bpm:",10,280,120,10)
            self.instrumento = st.selectbox("Instrumento:",opcoes_instrumentos,index=opcoes_instrumentos.index(VALOR_INSTRUMENTO_DEFAULT))

            botao_gerar = st.form_submit_button(label="Gerar Música")

            if botao_gerar:
                if texto_digitado and arquivo_texto:
                    st.warning("Insira um texto OU carregue um arquivo!")
                    return
                
                if not texto_digitado:
                    st.warning("Insira um texto OU carregue um arquivo!")
                    return
         
                self.texto_converter = texto_digitado

                self.music_services = MusicServices(texto_digitado,self.instrumento,self.oitava,self.volume,self.bpm)

                #salva a música no buffer de estado
                st.session_state.music_services = self.music_services

                if self.music_services.isMusicaPronta:
                    self.inicializaCabecalho
                    self.mudaTela("tela_player")

    def telaPlayer(self):
        st.write("Música gerada!")

        #busca a música do buffer de estado
        self.music_services = st.session_state.get("music_services", None)


        if self.music_services is None:
            st.warning("Música não encontrada!")
            return
        
        if st.button("Gerar arquivo MIDI"):
            self.music_services.gerarMidi()
            st.toast("Arquivo MIDI 'musica_gerada.mid' gerado com sucesso!")

        col1,col2,col3 = st.columns([1,1,1])

        with col1:
            if st.button("▶️ Play"):        
                self.music_services.play()

        with col2:
            if st.button("⏸️ Pause"):
                pass
                
        with col3:
            if st.button("⏹️ Voltar"):
                self.mudaTela("tela_input")



if __name__ == "__main__":
    ui = UI()
