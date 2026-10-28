"""Página principal do dashboard em Streamlit."""

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from f1.api import APIError, OpenF1Client
from f1.models import Driver, Lap, Meeting, SessionInfo
from f1.processing import classificar_voltas


@st.cache_data(ttl=3600, show_spinner=False)
def carregar_meetings(ano: int) -> list[Meeting]:
    return OpenF1Client().meetings(ano)


@st.cache_data(ttl=3600, show_spinner=False)
def carregar_sessoes(meeting_key: int) -> list[SessionInfo]:
    return OpenF1Client().sessions(meeting_key)


@st.cache_data(ttl=3600, show_spinner=False)
def carregar_pilotos(session_key: int) -> list[Driver]:
    return OpenF1Client().drivers(session_key)


@st.cache_data(ttl=3600, show_spinner=False)
def carregar_voltas(session_key: int) -> list[Lap]:
    return OpenF1Client().laps(session_key)


def main() -> None:
    st.set_page_config(page_title="F1 | Engenharia de Dados Júnior", page_icon="🏎️", layout="wide")
    st.title("🏎️ Dashboard de Fórmula 1")
    st.caption("Projeto educacional de Engenharia de Dados Júnior • API OpenF1")
    st.write("Selecione o Grande Prêmio e a sessão para consultar as voltas mais rápidas.")

    with st.sidebar:
        st.header("Filtros")
        anos = list(range(date.today().year, 2022, -1))
        ano_padrao = date.today().year - 1
        ano = st.selectbox(
            "Temporada",
            anos,
            index=anos.index(ano_padrao) if ano_padrao in anos else 0,
        )
        st.caption("A API gratuita fornece dados históricos a partir de 2023.")

    try:
        with st.spinner("Carregando Grandes Prêmios..."):
            meetings = carregar_meetings(ano)
        if not meetings:
            st.info("Nenhum Grande Prêmio encontrado para esse ano. Tente outro.")
            return

        meetings = sorted(meetings, key=lambda m: (m.date_start or "", m.meeting_key))
        meeting = st.selectbox(
            "Grande Prêmio",
            options=meetings,
            format_func=lambda m: f"{m.meeting_name} — {m.country_name or 'País não informado'}",
        )
        if meeting is None:
            return

        with st.spinner("Carregando sessões..."):
            sessoes = carregar_sessoes(meeting.meeting_key)
        if not sessoes:
            st.info("Não foram encontradas sessões para este Grande Prêmio.")
            return
        sessoes = sorted(sessoes, key=lambda s: (s.date_start or "", s.session_key))
        sessao = st.selectbox(
            "Sessão",
            options=sessoes,
            index=next((i for i, s in enumerate(sessoes) if s.session_name == "Race"), 0),
            format_func=lambda s: s.session_name,
        )
        if sessao is None:
            return

        unico = st.checkbox("Mostrar somente a melhor volta de cada piloto", value=True)
        assinatura = (ano, meeting.meeting_key, sessao.session_key, unico)
        if st.button("Consultar voltas", type="primary"):
            st.session_state["consulta_f1"] = assinatura

        if st.session_state.get("consulta_f1") != assinatura:
            st.info("Clique em **Consultar voltas** para carregar o ranking.")
            return

        with st.spinner("Consultando voltas e pilotos..."):
            voltas = carregar_voltas(sessao.session_key)
            pilotos = carregar_pilotos(sessao.session_key)
        dados = classificar_voltas(
            voltas,
            pilotos,
            limite=5,
            apenas_melhor_por_piloto=unico,
        )
        if not dados:
            st.warning("Não há voltas válidas para esta sessão. Ela pode ainda não ter ocorrido.")
            return

        tabela = pd.DataFrame(dados)
        st.subheader("As 5 voltas mais rápidas")
        col1, col2, col3 = st.columns(3)
        col1.metric("Voltas classificadas", len(tabela))
        col2.metric("Melhor tempo", tabela.iloc[0]["Tempo"])
        col3.metric("Piloto mais rápido", tabela.iloc[0]["Piloto"])

        st.dataframe(tabela, hide_index=True, width="stretch")
        figura = px.bar(
            tabela,
            x="Posição",
            y="Tempo (s)",
            color="Piloto",
            text="Tempo",
            hover_data=["Equipe", "Volta"],
            title="Tempos das cinco voltas mais rápidas",
        )
        figura.update_layout(xaxis=dict(tickmode="linear", dtick=1))
        st.plotly_chart(figura, width="stretch")
        st.download_button(
            "Baixar resultados em CSV",
            data=tabela.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"f1_voltas_{ano}_{sessao.session_key}.csv",
            mime="text/csv",
        )
    except APIError as erro:
        st.error(f"Não foi possível consultar a OpenF1. Detalhes: {erro}")
        st.info("Tente novamente mais tarde ou selecione uma sessão histórica.")

    st.caption("Fonte: https://openf1.org/ • Projeto didático, não oficial da Fórmula 1.")
