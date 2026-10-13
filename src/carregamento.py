import pandas as pd
from pathlib import Path
NOME_ABA_OFICIAL = "votacao_candidato_munzona_2026_"
def carregar_dados():
   
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_arquivo = (
        raiz_projeto 
        / "dados"
        / "votacao_candidato_munzona_2026_DF.xlsx"
    )
    df = pd.read_excel(caminho_arquivo, sheet_name= NOME_ABA_OFICIAL)
    return df


def preparar_dados(df):
        df  = df.copy()
        df["QT_VOTOS_NOMINAIS"] = pd.to_numeric(df["QT_VOTOS_NOMINAIS"], errors= "coerce").fillna(0).astype(int)
        return df


if __name__ == "__main__":
      df = carregar_dados()
      df = preparar_dados(df)
      print(df.head())