# 🎮 Steam Games Analysis - Projeto Final Fase 2

Este projeto realiza uma análise exploratória completa de um dataset contendo mais de 72 mil jogos da Steam. O trabalho foi desenvolvido como requisito para a Fase 2 da disciplina de Programação para Dados.

## 👤 Identificação

* **Instituição:** Pontifícia Universidade Católica do Rio Grande do Sul (PUCRS)
* **Curso:** Tecnólogo em Banco de Dados
* **Disciplina:** Programação para Dados
* **Aluno:** Jeferson Gomes da Silva

## 📋 Sobre o Projeto

O objetivo principal é transformar dados brutos em insights sobre a indústria de games, validando os resultados através de testes automatizados e amostragens.

### Diferenciais Técnicos:

* **Modularização:** Código dividido em responsabilidades claras (Loader, Preprocessing, Analysis, Visualizations).
* **Robustez:** Cobertura de testes com `pytest`.
* **Performance:** Uso de operações vetorizadas com `NumPy` e `Pandas`.
* **Portabilidade:** Suporte total para execução em ambiente local ou Google Colab.

## 📚 Conteúdo Acadêmico Aplicado

| Aula | Tópico | Aplicação Prática |
| :--- | :--- | :--- |
| **06** | Configuração de Ambiente | Estrutura de pastas, argumentos CLI e gerenciamento de arquivos. |
| **07** | NumPy | Cálculos estatísticos, correlações e operações vetorizadas. |
| **08/09**| Matplotlib | Visualizações customizadas (Linha, Pizza, Histograma) e rcParams. |
| **10** | Pandas | Manipulação de DataFrames, tratamento de missings e agregações. |

## 📂 Estrutura do Projeto

```text
programacaoparadados2/
├── 📁 data/                  # Dataset compactado (steam_games.zip)
├── 📁 src/                   # Código fonte modular (Core do projeto)
│   ├── config.py             # Estilos de gráficos e caminhos
│   ├── data_loader.py        # Extração e leitura de ZIP
│   ├── preprocessing.py      # Limpeza e transformação de dados
│   ├── analysis.py           # Lógica das perguntas de negócio
│   └── visualizations.py     # Funções de geração de gráficos
├── 📁 tests/                 # Testes unitários com pytest
├── 📁 outputs/               # Gráficos (PNG) e Tabelas (CSV) gerados
├── main.py                   # Ponto de entrada principal da análise
├── gerar_graficos.py         # Script focado apenas em gerar e exibir os gráficos na tela
├── run_tests.py              # Atalho para execução de testes unitários
├── validate_analysis.py      # Atalho para validação e conferência dos dados
└── requirements.txt          # Lista de dependências (pip)
```

## 🚀 Como Executar Localmente

Abra o terminal na pasta raiz do projeto e siga os passos abaixo:

**1. Instalar as dependências:**
```bash
!pip install -r requirements.txt
```

**2. Executar a análise completa:** (Puxa os dados, cria as tabelas CSV, exibe os resumos e gera os gráficos silenciosamente)
```bash
!python main.py
```

**3. Gerar os Gráficos:**
```bash
!python gerar_graficos.py
```

**4. Visualizar os Gráficos na Tela:**
```python
from IPython.display import Image, display
import os

FIGURES_PATH = '/content/programacaoparadados2/outputs/figures'

print(f'Exibindo gráficos da pasta: {FIGURES_PATH}')

display(Image(os.path.join(FIGURES_PATH, 'grafico1_os_support.png')))
display(Image(os.path.join(FIGURES_PATH, 'grafico2_indie_strategy.png')))
display(Image(os.path.join(FIGURES_PATH, 'grafico3_price_distribution.png')))
```

**5. Executar os testes automatizados (pytest):**
```bash
!python run_tests.py
```

**6. Validar os resultados (sanity check):**
```bash
!python validate_analysis.py
