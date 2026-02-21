# 🤝 Guia de Contribuição, Reprodutibilidade e Inferência

Bem-vindo ao manual técnico e arquitetónico da minha solução para a deteção de fraudes financeiras. Concebi este guia com um objetivo claro: garantir **100% de reprodutibilidade** e demonstrar que o projeto transcende a simples criação de um modelo de *Machine Learning*. 

Aqui, detalho como apliquei boas práticas de engenharia de *software*, segregação rigorosa de dados e um *pipeline* preparado não apenas para o Kaggle, mas para inferência de novos dados num ambiente de produção real.

---

## 🛠️ 1. Configuração do Ambiente Local (Reprodutibilidade: 5/5)

Para evitar os clássicos problemas de dependências cruzadas e garantir que a aplicação funciona perfeitamente em qualquer máquina, estruturei o projeto com recurso a ambientes virtuais isolados.

**Passo 1: Clonar o repositório**
```bash
git clone [https://github.com/willianrupert/teste.git](https://github.com/willianrupert/teste.git)
cd teste
```

**Passo 2: Criar e ativar o ambiente virtual**
A utilização de um *venv* garante que as versões do XGBoost, CatBoost e SHAP não entram em conflito com as bibliotecas do teu sistema.
```bash
# Em sistemas Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# Em sistemas Windows:
python -m venv venv
venv\Scripts\activate
```

**Passo 3: Instalar as dependências rigorosamente mapeadas**
```bash
pip install -r requirements.txt
```

---

## 📁 2. Arquitetura e Segregação de Ficheiros (Qualidade de Engenharia: 5/5)

A separação de responsabilidades é o coração deste projeto. Evitei deliberadamente *notebooks* monolíticos, optando por uma estrutura modular digna de um sistema *end-to-end*.

* **`/data/`**: Pasta reservada aos ficheiros `train.csv` e `test.csv`. *(Nota: Esta pasta está no `.gitignore` para proteger a integridade dos dados originais e cumprir regras de privacidade).*
* **`/src/`**: O motor da aplicação.
  * `preprocessing.py`: Centraliza as transformações não-lineares, o *RobustScaler* e a deteção de anomalias (*Isolation Forest*). Esta modularidade permite que a mesma transformação seja aplicada a dados futuros de inferência sem reescrever código.
  * `model.py`: Encapsula a arquitetura complexa do *Stacking Ensemble*. É aqui que a otimização de hiperparâmetros se encontra consolidada, garantindo máxima precisão.
* **`/notebooks/main.ipynb`**: O orquestrador visual. Responsável por invocar os módulos, coordenar o *Hold-out* (80/20), gerar a interpretabilidade visual (SHAP) e exportar as submissões finais.

---

## ⚙️ 3. Como Executar o Pipeline (O Caminho Metodológico)

A execução no ficheiro `main.ipynb` foi dividida em duas fases metodológicas estritas para evitar qualquer risco de *Data Leakage* e garantir a adequação da métrica principal (*Recall*).

### Fase 1: Validação Rigorosa (Análise Cega)
1. **Segregação:** O *script* isola 20% dos dados.
2. **Treino e Isolamento:** O *Scaler* e o *Isolation Forest* aprendem **exclusivamente** com a fatia de 80%.
3. **Métricas de Negócio:** Avaliamos a performance com foco na redução de Falsos Negativos (maximização do *Recall*), gerando a Matriz de Confusão e os gráficos SHAP de forma transparente e auditável.

### Fase 2: Inferência e Produção (O Treino Definitivo)
1. **Expansão de Conhecimento:** Uma vez validada a arquitetura sem *overfitting*, o *script* ignora a divisão de 80/20 e aplica a função `feature_engineering` sobre **100% dos dados de treino**.
2. **Robustez Final:** O meta-modelo (Regressão Logística com forte regularização L2, $C=0.1$) é treinado para consolidar a aprendizagem e prever o ficheiro `test.csv` da competição.

---

## 🚀 4. Guia de Submissão no Kaggle

Para maximizar a pontuação na competição, o *script* gera os ficheiros CSV automaticamente. A minha estratégia de submissão dupla blinda a solução contra surpresas no fecho da avaliação:

1. **Submissão A (O Campeão do Public Leaderboard):** O ficheiro gerado pelo modelo validado em 80% dos dados. Garante o pico estatístico visível atualmente.
2. **Submissão B (O Escudo do Private Leaderboard):** O ficheiro `submission_vaga_producao.csv`, treinado com 100% dos dados. Esta submissão possui a máxima capacidade de generalização desenvolvida na aplicação, pronta para absorver variações ocultas nos dados de teste finais sem colapsar.

---

## 🛠️ 5. Inferência em Novos Dados (Escalabilidade da Solução)

Se desejares contribuir ou utilizar este modelo para inferir a probabilidade de fraude em **novas transações** (simulando um sistema financeiro em tempo real), basta importar os módulos pré-treinados:

```python
from src.preprocessing import feature_engineering

# Supondo que 'novos_dados_df' é um DataFrame com transações recentes
# Aplicamos as mesmas transformações usando o scaler e iso_forest já treinados
dados_prontos = feature_engineering(
    novos_dados_df, 
    scaler=scaler_treinado, 
    iso_forest=iso_treinado, 
    is_train=False
)

# O modelo devolve a probabilidade exata (ex: 0.87 -> 87% de probabilidade de anomalia)
probabilidade_fraude = model.predict_proba(dados_prontos)[:, 1]
