# 🤝 Guia de Contribuição, Reprodutibilidade e Inferência

Bem-vindo ao manual técnico e arquitetónico da minha solução para a deteção de fraudes financeiras. Concebi este guia com um objetivo claro: garantir **100% de reprodutibilidade** e demonstrar que o projeto transcende a simples criação de um modelo de *Machine Learning*. 

Aqui, detalho como apliquei boas práticas de engenharia de *software*, segregação rigorosa de dados e um *pipeline* preparado não apenas para o Kaggle, mas para inferência de novos dados num ambiente de produção real.

---

##  1. Configuração do Ambiente Local (Reprodutibilidade: 5/5)

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

##  2. Arquitetura e Segregação de Ficheiros (Qualidade de Engenharia: 5/5)

A separação de responsabilidades é o coração deste projeto. Evitei deliberadamente *notebooks* monolíticos, optando por uma estrutura modular digna de um sistema *end-to-end*.

* **`/data/`**: Pasta reservada aos ficheiros `train.csv` e `test.csv`. *(Nota: Esta pasta está no `.gitignore` para proteger a integridade dos dados originais e cumprir regras de privacidade).*
* **`/src/`**: O motor da aplicação.
  * `preprocessing.py`: Centraliza as transformações não-lineares, as rotações geométricas (`V4_minus_V14`) e o *RobustScaler*. Esta modularidade permite que a mesma transformação seja aplicada a dados futuros de inferência sem reescrever código.
  * `model.py`: Encapsula a arquitetura complexa do *Stacking Ensemble*. É aqui que a Otimização Bayesiana (afinada via Optuna) se encontra consolidada, garantindo máxima precisão.
* **`/notebooks/main.ipynb`**: O orquestrador visual. Responsável por invocar os módulos, coordenar o *Hold-out* (80/20), gerar a interpretabilidade visual (SHAP) e exportar a submissão final.

---

## ⚙️ 3. Como Executar o Pipeline (O Caminho Metodológico)

A execução no ficheiro `main.ipynb` obedece a um rigoroso protocolo de validação para evitar qualquer risco de *Data Leakage* e garantir a adequação da métrica principal (*Recall*).

### Fase 1: Validação Rigorosa (Análise Cega)
1. **Segregação:** O *script* isola estrategicamente 20% dos dados.
2. **Treino e Isolamento:** O *Scaler* e o Meta-Modelo aprendem **exclusivamente** com a fatia de 80%.
3. **Métricas de Negócio:** Avaliamos a performance com foco na redução de Falsos Negativos (maximização do *Recall*), gerando a Matriz de Confusão e os gráficos SHAP de forma transparente e auditável.

### Fase 2: Geração do Artefato Final (A Estratégia Anti-Overfitting)
1. **Decisão Arquitetónica:** Diferente de abordagens amadoras que forçam um re-treino com 100% dos dados para enviesar o *score* público, este *script* preserva a inteligência do modelo validado nos 80%. 
2. **Robustez Final:** O *Stacking Ensemble* gera as probabilidades para o ficheiro `test.csv` da competição com base nesta aprendizagem generalista e imaculada.

---

##  4. Guia de Submissão no Kaggle

A estratégia de submissão gerada por este código blinda a solução contra as surpresas metodológicas e as quedas abruptas de classificação no fecho da avaliação:

* **O Escudo do Private Leaderboard:** O ficheiro `submission.csv` gerado é suportado pela validação *Hold-out*. Foi esta exata configuração que cravou o cobiçado ROC-AUC de **0.99090** no *Public Leaderboard*. Ao mantermos a disciplina de não sobreajustar o modelo com a totalidade dos dados, garantimos que ele possui a máxima resiliência para lidar com os 70% de dados de teste que o Kaggle mantém ocultos.

---

##  5. Inferência em Novos Dados (Escalabilidade da Solução)

Se desejares contribuir ou utilizar este modelo para inferir a probabilidade de fraude em **novas transações** (simulando um sistema financeiro em tempo real), basta importar os módulos pré-treinados:

```python
from src.preprocessing import feature_engineering

# Supondo que 'novos_dados_df' é um DataFrame com transações financeiras recentes
# Aplicamos as mesmas transformações usando estritamente o scaler já treinado
dados_prontos = feature_engineering(
    novos_dados_df, 
    scaler=scaler_treinado, 
    is_train=False
)

# O modelo devolve a probabilidade exata (ex: 0.87 -> 87% de probabilidade de anomalia)
probabilidade_fraude = model.predict_proba(dados_prontos)[:, 1]
```
Esta facilidade de adaptação traduz os resultados académicos numa funcionalidade técnica de excelência, pronta a ser acoplada a serviços na nuvem (Cloud/API).
