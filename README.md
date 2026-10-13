# 🗳️ Análise Eleitoral do Distrito Federal

Análise dos resultados das **Eleições Gerais de 2026 no Distrito Federal**, feita a partir de dados públicos do TSE.

O projeto pega uma planilha com milhares de linhas e a transforma em tabelas objetivas: quem foi mais votado, em quais zonas eleitorais e como os votos se distribuíram pelo território.

## O que o projeto faz

- Localiza e carrega automaticamente a planilha do TSE
- Limpa e prepara os dados para análise
- Executa as análises e salva os resultados em arquivos CSV
- Permite abrir os resultados no Excel, no Google Planilhas ou em qualquer ferramenta de dados

## Requisitos

- Python 3.9 ou superior
- As bibliotecas listadas em `requirements.txt`

## Como executar

1. Coloque a planilha original do TSE na pasta `dados/`.
2. Instale as dependências:

```bash
   pip install -r requirements.txt
```

3. Rode o projeto:

```bash
   python main.py
```

Ao final, os arquivos CSV estarão na pasta `resultados/`.

## Estrutura do projeto

```
.
├── main.py              # Ponto de entrada: executa todas as análises
├── requirements.txt     # Dependências do projeto
├── src/
│   ├── carregamento.py  # Localiza, carrega e prepara a planilha
│   └── analises.py      # Funções de análise (uma pergunta por função)
├── dados/               # Planilha original do TSE
└── resultados/          # CSVs gerados pelas análises
```

## Fonte dos dados

Os dados vêm do **Tribunal Superior Eleitoral (TSE)**, do portal de dados abertos.
A aba utilizada é `votacao_candidato_munzona_2026_`, que traz a votação de cada candidato por município e zona eleitoral.

## Como adicionar uma nova análise

1. Crie uma função em `src/analises.py` que receba o DataFrame e retorne o resultado.
2. Chame essa função em main.py e salve o retorno em `resultados/.

## Observações

- Os números refletem exatamente o que consta na planilha do TSE; o projeto não altera os votos.
- Se o TSE atualizar o arquivo, basta substituir a planilha em `dados/` e rodar novamente.

## Contribuições

Encontrou um erro ou tem uma ideia de análise? Abra uma issue ou envie um pull request. Toda ajuda é bem-vinda.

## Licença
