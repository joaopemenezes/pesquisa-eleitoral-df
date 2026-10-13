from pathlib import Path

import pandas as pd

from src.carregamento import carregar_dados, preparar_dados
from src.analises import (
    ranking_candidatos,
    votos_partido,
    votos_por_zona,
    vencedores_por_zona,
    quantidade_zonas_vencido_candidato,
)

CARGOS = [
    "Governador",
    "Senador",
    "Deputado Federal",
    "Deputado Distrital",
]

RAIZ = Path(__file__).resolve().parent
PASTA_RESULTADOS = RAIZ / "resultados"
COL_VOTOS = "QT_VOTOS_NOMINAIS_VALIDOS"
COLUNAS_NECESSARIAS = [
    "DS_CARGO",
    "NM_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "SG_PARTIDO",
    "NR_PARTIDO",
    "NR_ZONA",
    COL_VOTOS,
]


def salvar_resultado(resultado, nome):
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_RESULTADOS / nome
    resultado.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Salvo: {caminho}")


def nome_arquivo(cargo):
    return cargo.lower().replace(" ", "_")


def preparar(df):
    df = preparar_dados(df)

    faltando = [c for c in COLUNAS_NECESSARIAS if c not in df.columns]
    if faltando:
        raise SystemExit(f"Colunas ausentes na planilha: {faltando}")

    df[COL_VOTOS] = pd.to_numeric(df[COL_VOTOS], errors="coerce").fillna(0)
    return df


def cargos_disponiveis(df):
    """Casa CARGOS com os nomes reais da planilha, ignorando maiúsculas/minúsculas."""
    presentes = {str(c).strip().upper(): c for c in df["DS_CARGO"].dropna().unique()}
    encontrados = []

    for cargo in CARGOS:
        original = presentes.get(cargo.upper())
        if original is None:
            print(f"Aviso: cargo '{cargo}' não encontrado nos dados.")
        else:
            encontrados.append(original)

    return encontrados


def analisar_cargo(df, cargo):
    nome = nome_arquivo(cargo)
    print(f"\nAnalisando: {cargo}")

    # As funções de partido, zona e vencedores não recebem "cargo",
    # então entregamos a elas o DataFrame já filtrado
    df_cargo = df[df["DS_CARGO"] == cargo]

    ranking = ranking_candidatos(df, cargo)
    print(ranking.head(10).to_string(index=False))

    zonas_vencidas = (
        quantidade_zonas_vencido_candidato(df_cargo)
        .reset_index(name="zonas_vencidas")
        .sort_values("zonas_vencidas", ascending=False)
    )

    salvar_resultado(ranking, f"ranking_{nome}.csv")
    salvar_resultado(votos_partido(df_cargo), f"partidos_{nome}.csv")
    salvar_resultado(votos_por_zona(df_cargo), f"zonas_{nome}.csv")
    salvar_resultado(vencedores_por_zona(df_cargo), f"vencedores_por_zona_{nome}.csv")
    salvar_resultado(zonas_vencidas, f"zonas_vencidas_{nome}.csv")


def executar():
    df = preparar(carregar_dados())
    print(f"Registros carregados: {len(df):,}")

    salvar_resultado(votos_partido(df), "votos_por_partido_geral.csv")
    salvar_resultado(votos_por_zona(df), "votos_por_zona_geral.csv")

    cargos = cargos_disponiveis(df)
    if not cargos:
        print("Nenhum cargo da lista foi encontrado. Cargos nos dados:")
        print(sorted(df["DS_CARGO"].dropna().unique()))
        return

    for cargo in cargos:
        analisar_cargo(df, cargo)

    print("\nAnálises concluídas.")


if __name__ == "__main__":
    executar()