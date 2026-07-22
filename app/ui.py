from __future__ import annotations

import streamlit as st


CSS = """
<style>
:root { --brand: #2563eb; --surface: #0f172a; }
.block-container { max-width: 1050px; padding-top: 2rem; padding-bottom: 3rem; }
.hero { padding: 2.2rem; border-radius: 24px; background: linear-gradient(135deg,#0f172a,#1d4ed8); color:white; margin-bottom:1.5rem; }
.hero h1 { margin:0 0 .6rem 0; font-size:2.6rem; }
.hero p { margin:0; font-size:1.08rem; opacity:.92; }
.info-card { border:1px solid rgba(128,128,128,.25); border-radius:18px; padding:1.25rem; height:100%; }
.small-muted { opacity:.72; font-size:.92rem; }
[data-testid="stChatMessage"] { border-radius: 16px; padding: .25rem .5rem; }
</style>
"""


def apply_page_config() -> None:
    st.set_page_config(
        page_title="EscolaGPT",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar() -> str:
    with st.sidebar:
        st.title("🎓 EscolaGPT")
        st.caption("Projeto educacional atualizado")
        page = st.radio(
            "Navegação",
            ["Início", "Chat", "Conteúdos", "Sobre o projeto"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**Boas práticas**")
        st.caption("Confira informações importantes e não compartilhe dados pessoais.")
    return page
