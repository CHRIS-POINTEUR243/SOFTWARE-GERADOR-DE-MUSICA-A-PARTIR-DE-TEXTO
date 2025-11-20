import streamlit as st
from mainVer1 import GeradorMusical, ProcessaTexto, OITAVA_DEFAULT, VOLUME_DEFAULT, BPM_DEFAULT

st.set_page_config(page_title="Gerador Music", page_icon="🎵")

# Título central
st.markdown(
    "<h1 style='text-align:center;'>Gerador Music</h1>",
    unsafe_allow_html=True,
)
## core button
st.markdown(
    """
    <style>
    /* Deixa TODOS os botões vermelhos */
    .stButton > button {
        background-color: red;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6em 1.2em;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: darkred;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.write("Write your word, or your phrase:")

# Caixa de texto
texto = st.text_input("", placeholder="Ex: ABRA A GAIOLA DE H ...")

# Estado inicial (volume, oitava, bpm)
if "volume" not in st.session_state:
    st.session_state.volume = VOLUME_DEFAULT
if "oitava" not in st.session_state:
    st.session_state.oitava = OITAVA_DEFAULT
if "bpm" not in st.session_state:
    st.session_state.bpm = BPM_DEFAULT

# Botão principal: Tocar
col_start, _ = st.columns([1, 3])
with col_start:
    tocar = st.button("Tocar", use_container_width=True)

st.write("")

# Linha de controles Som + / Som - / Pausar / Continuar
col_som_plus, col_som_minus, col_pause, col_continue = st.columns(4)

with col_som_plus:
    if st.button("Som +"):
        st.session_state.volume = min(127, st.session_state.volume + 10)

with col_som_minus:
    if st.button("Som -"):
        st.session_state.volume = max(0, st.session_state.volume - 10)

with col_pause:
    st.button("Pausar", disabled=True)  # visual, pausa real é mais complexa

with col_continue:
    st.button("Continuar", disabled=True)  # visual

st.write("")

# Botão Parar (também visual por enquanto)
st.button("Parar", disabled=True)

st.write(f"Volume atual: {st.session_state.volume}")

# --- Lógica: gerar e tocar usando suas classes ---
if tocar:
    if not texto.strip():
        st.warning("Digite algum texto primeiro.")
    else:
        gm = GeradorMusical()
        gm.bpm_atual = st.session_state.bpm
        gm.volume_atual = st.session_state.volume
        gm.oitava_atual = st.session_state.oitava

        # usa ProcessaTexto do seu código
        proc = ProcessaTexto(gm.tabelaFuncoes, gm.tabelaNotas, texto)
        tokens = proc.processaTextoEmLista()

        st.write("Tokens gerados:", tokens)

        gm.lista_notas = []
        gm.mapeiaTexto(tokens)

        st.write(f"{len(gm.lista_notas)} notas geradas. Tocando...")

        # Aqui realmente toca o MIDI usando a sua classe Nota
        for n in gm.lista_notas:
            n.tocar()
