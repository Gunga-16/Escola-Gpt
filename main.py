from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from app.config import SETTINGS
from app.openai_service import stream_answer
from app.ui import apply_page_config, render_sidebar

load_dotenv()
apply_page_config()
page = render_sidebar()


def home() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>Aprenda com o EscolaGPT</h1>
          <p>Um assistente educacional criado para apoiar pesquisas, estudos e compreensão de conteúdos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-card"><h3>💬 Tire dúvidas</h3><p>Faça perguntas e peça explicações adequadas ao seu nível de estudo.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><h3>🧠 Aprenda por etapas</h3><p>Solicite exemplos, exercícios, pistas e revisões de conteúdo.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="info-card"><h3>🔎 Use com responsabilidade</h3><p>Confirme informações importantes em fontes confiáveis e com professores.</p></div>', unsafe_allow_html=True)
    st.subheader("Sugestões para começar")
    st.markdown(
        "- Explique fotossíntese para um aluno do 8º ano.\n"
        "- Crie cinco exercícios de sub-rede IPv4 sem mostrar as respostas.\n"
        "- Ajude-me a revisar este parágrafo e explique as correções.\n"
        "- Monte um plano de estudos de uma semana para uma prova."
    )


def chat() -> None:
    st.title("💬 Chat educacional")
    st.caption(f"Modelo configurado: `{SETTINGS.model}`")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Olá! Sou o EscolaGPT. Qual conteúdo você está estudando hoje?",
            }
        ]

    top_col, _ = st.columns([1, 4])
    with top_col:
        if st.button("Nova conversa", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "Nova conversa iniciada. Como posso ajudar?"}
            ]
            st.rerun()

    for message in st.session_state.messages:
        avatar = "🧑‍🎓" if message["role"] == "user" else "🎓"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("Escreva sua pergunta...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎓"):
        try:
            answer = st.write_stream(stream_answer(st.session_state.messages))
        except RuntimeError as exc:
            answer = f"Não foi possível gerar a resposta. {exc}"
            st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


def contents() -> None:
    st.title("📚 Conteúdos")
    st.subheader("Engenharia de prompt")
    st.write(
        "Engenharia de prompt é a prática de formular instruções claras, contextualizadas "
        "e verificáveis para obter respostas mais úteis de modelos de linguagem."
    )
    st.markdown(
        """
        **Estrutura recomendada de um bom pedido:**

        1. informe o objetivo;
        2. forneça o contexto necessário;
        3. determine o formato da resposta;
        4. estabeleça limites ou critérios;
        5. revise e refine o pedido.
        """
    )
    st.info("Exemplo: “Explique ligações químicas para o 9º ano, usando uma analogia e três perguntas de revisão.”")


def about() -> None:
    st.title("ℹ️ Sobre o projeto")
    st.write(
        "O EscolaGPT surgiu em 2024 como um trabalho escolar em HTML e CSS. "
        "Nesta versão, o protótipo foi reconstruído como aplicação Python com Streamlit "
        "e integração real com a API da OpenAI."
    )
    st.subheader("Evolução técnica")
    st.markdown(
        "- interface estática → aplicação interativa;\n"
        "- mensagens demonstrativas → respostas reais por API;\n"
        "- páginas e estilos repetidos → componentes Python reutilizáveis;\n"
        "- chave no código → variável de ambiente;\n"
        "- projeto escolar → projeto de portfólio documentado."
    )
    st.subheader("Autor")
    st.write("Sérgio Henrique da Cunha Calazans — acadêmico de Ciência da Computação.")


pages = {
    "Início": home,
    "Chat": chat,
    "Conteúdos": contents,
    "Sobre o projeto": about,
}
pages[page]()
