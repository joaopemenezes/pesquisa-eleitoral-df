
import pandas as pd 
def ranking_candidatos(df,cargo):
    dados = df[df["DS_CARGO"]== cargo].copy()
    ranking = (dados.groupby(
        [
            
            "NM_CANDIDATO",
            "NM_URNA_CANDIDATO",
            "SG_PARTIDO"
        ], 
        as_index = False
        )["QT_VOTOS_NOMINAIS_VALIDOS"].sum().sort_values("QT_VOTOS_NOMINAIS_VALIDOS", ascending = False)
               
               )
    return ranking
""" Retorna quantidades de votos por partido """
def votos_partido(df):
    votos_par  = df.copy() 
    ranking_votos =(votos_par.groupby(["SG_PARTIDO", "NR_PARTIDO"], as_index = False)["QT_VOTOS_NOMINAIS_VALIDOS"].sum().sort_values("QT_VOTOS_NOMINAIS_VALIDOS",ascending = False))
    total_votos = ranking_votos["QT_VOTOS_NOMINAIS_VALIDOS"].sum()
    """ Percentual por partido"""
    ranking_votos["percentual"] = (ranking_votos["QT_VOTOS_NOMINAIS_VALIDOS"] / total_votos * 100).round(2)

    return ranking_votos


""""
Partidos com mais votos segundo vaga disputada
"""
def votos_partido_cargo(df,cargo):
    votos_par  = df[df["DS_CARGO"] == cargo].copy()  
    ranking_votos_cargo =(votos_par.groupby(["SG_PARTIDO", "NR_PARTIDO"])["QT_VOTOS_NOMINAIS_VALIDOS"].sum().sort_values(ascending = False))
  
    return ranking_votos_cargo
""" Quantidades votos por zona """
def votos_por_zona(df):
    df = df.copy()
    resultado_zona = df.groupby(["NR_ZONA"], as_index = False)["QT_VOTOS_NOMINAIS_VALIDOS"].sum().sort_values("QT_VOTOS_NOMINAIS_VALIDOS", ascending = False)
    return resultado_zona

def vencedores_por_zona(df):
    df = df.copy()
    vencedor_zona = df.groupby(["NR_ZONA","NM_CANDIDATO"], as_index = False)["QT_VOTOS_NOMINAIS_VALIDOS"].sum()
    maior_voto = vencedor_zona.groupby(["NR_ZONA"], as_index = False)["QT_VOTOS_NOMINAIS_VALIDOS"].transform(max)
    vencedor = vencedor_zona[vencedor_zona["QT_VOTOS_NOMINAIS_VALIDOS"] == maior_voto]
    return vencedor


def quantidade_zonas_vencido_candidato(df):
    df = df.copy()
    votozona = (
        df.groupby([
            "NM_CANDIDATO",
            "NR_ZONA"
        ], as_index = False)["QT_VOTOS_NOMINAIS_VALIDOS"].sum()

    )
    maior_voto = (
        votozona.groupby("NR_ZONA")["QT_VOTOS_NOMINAIS_VALIDOS"].transform(max))
    vencedores = votozona[votozona["QT_VOTOS_NOMINAIS_VALIDOS"] == maior_voto]
    zonas_vencidas = (
        vencedores.groupby(["NM_CANDIDATO"]).size()
    )
    return zonas_vencidas

if __name__ == "__main__":
    # Rode da raiz do projeto: python -m src.analises
    from src.carregamento import carregar_dados, preparar_dados

    df = preparar_dados(carregar_dados())

    print(ranking_candidatos(df, "Governador").head(10))
    print(votos_partido_cargo(df, "Deputado Distrital"))
    print(votos_partido(df))
    print(votos_por_zona(df))
    print(vencedores_por_zona(df))
    print(quantidade_zonas_vencido_candidato(df))