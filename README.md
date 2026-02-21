# 🛡️ Detecção de Fraudes em Cartões de Crédito: Uma Abordagem Robusta com Stacking Ensembles e XAI

**Autor:** Willian Rupert (Estudante de Ciência da Computação - CIn/UFPE)  
**Objetivo:** Desenvolvimento de um modelo de *Machine Learning* de alta precisão para o desafio de classificação de transações financeiras fraudulentas, priorizando o rigor metodológico, a reprodutibilidade e a explicabilidade voltada para o negócio.

---

## 🎯 1. O Problema e a Visão de Negócio (Adequação da Métrica)

Em sistemas de pagamentos reais, lidamos com um cenário de **extremo desbalanceamento de classes**, onde as fraudes representam uma fração minúscula das transações diárias. 

Ao analisar o histórico de avaliações de modelos preditivos em cenários críticos (como saúde e finanças), observei que muitos cientistas de dados cometem o erro de focar na métrica F1-Score ou na Acurácia. No entanto, a minha modelagem foi construída com os olhos estritamente voltados para o impacto de negócio: **a prioridade financeira é o Recall (Sensibilidade)**. 

Aprovar uma transação fraudulenta (Falso Negativo) tem um custo de estorno e perda de credibilidade devastador. Portanto, a arquitetura deste projeto foi desenhada para maximizar a captura de fraudes reais, ajustando os limiares de decisão (*thresholds*) para manter os Falsos Positivos (clientes legítimos bloqueados) em um volume operacionalmente aceitável para uma equipe de análise manual.

---

## 🧪 2. Rigor Metodológico e Prevenção de Data Leakage

Para garantir que os resultados obtidos não fossem fruto de *overfitting* ou memorização de dados, adotei uma política estrita de segregação:
* **Hold-out Validation (80/20):** Separei 20% dos dados como um conjunto cego. Todas as decisões de arquitetura, otimização e geração de métricas de validação foram feitas olhando **apenas** para o conjunto de treino de 80%.
* **Isolamento de Transformadores:** Algoritmos como o `RobustScaler` e o `IsolationForest` foram ajustados (`.fit()`) exclusivamente nos dados de treino. Seus parâmetros aprendidos foram então aplicados (`.transform()`) aos dados de validação e teste, eliminando qualquer possibilidade de vazamento de informações do futuro (*Data Leakage*).

---

## 🚀 3. A Evolução da Arquitetura (Minha Jornada de 7 Submissões)

O desenvolvimento deste modelo não foi uma tentativa de força bruta algorítmica, mas um processo científico e iterativo. Ao longo de 7 submissões na plataforma Kaggle, evoluí a solução desde a análise exploratória até um *ensemble* de estado da arte.

### Fase 1: Análise Exploratória e Feature Engineering (Sinal Supervisionado)
Antes de testar modelos complexos, foquei em extrair o sinal matemático oculto na base de dados. Através de correlações empíricas, percebi que algumas variáveis anonimizadas escondiam comportamentos geométricos valiosos:
1. **Interações Matemáticas Otimizadas:** A criação da diferença algébrica `V4 - V14` e da soma `V14 + V12` amplificou o sinal das fraudes de forma drástica, criando separadores de classe muito mais fortes do que as variáveis isoladas.
2. **Tratamento do Tempo e Valor:** A variável `Time` foi decomposta em componentes cíclicas (seno e cosseno) para capturar a sazonalidade diária das fraudes. A variável `Amount` sofreu uma transformação logarítmica para mitigar o peso de *outliers* extremos.

### Fase 2: Otimização de Hiperparâmetros e a Conquista do 0.99090
Para evitar a simplicidade e extrair o máximo de performance, utilizei otimização Bayesiana (**Optuna**) para encontrar a configuração ideal de um **Stacking Ensemble**:
* **Nível 0 (Diversidade de Aprendizado):** Integrei os três algoritmos de *Gradient Boosting* mais poderosos da literatura: **XGBoost, LightGBM e CatBoost**. Cada um foi configurado com uma baixa taxa de aprendizagem (`learning_rate=0.05`) para convergência suave e pesados rigorosamente para penalizar a classe majoritária (`scale_pos_weight=89.8`).
* **Nível 1 (O Juiz Conservador):** Para consolidar as previsões do Nível 0, utilizei uma Regressão Logística. O grande diferencial aqui foi a aplicação de uma **forte regularização L2 ($C=0.1$)**, que blindou o meta-modelo contra o vício nas árvores de decisão.
* **Resultado:** Validado estritamente no *Hold-out* de 20%, este modelo cravou **0.99090 de ROC-AUC** no *Public Leaderboard* do Kaggle.

### Fase 3: Detecção Não-Supervisionada e a Estratégia de Produção
Fraudes financeiras são mutáveis. Para proteger o modelo contra padrões de ataque inéditos (*Zero-Day Fraud*), implementei a terceira fase da arquitetura:
* **Isolation Forest:** Um modelo não-supervisionado treinado paralelamente para calcular um *Anomaly Score* baseado na densidade de isolamento estatístico das transações.
* **O Treino Definitivo (100% dos Dados):** Compreendendo que o *Public Leaderboard* avalia apenas $\approx 30\%$ dos dados de teste, tomei a decisão arquitetural de re-treinar a versão final do modelo com **100% dos dados de treino originais**. Esta estratégia abdica do *overfitting* nas métricas públicas em favor de uma generalização robusta e definitiva para a avaliação privada (*Private Leaderboard*).

---

## 🧠 4. Tradução de Resultados e Explicabilidade (XAI)

Na indústria de pagamentos, um modelo que atua como "caixa-preta" é inaceitável devido a exigências regulatórias. Para solucionar isso, integrei a Teoria dos Jogos através da biblioteca **SHAP (SHapley Additive exPlanations)**.

* **Visão Macro (Global):** Os gráficos *SHAP Summary* confirmaram a eficácia da Engenharia de Características. As interações matemáticas manuais (`V4_minus_V14` e `V14_V12_sum`) assumiram as posições de liderança no ranqueamento de importância, provando que o poder do modelo veio da manipulação inteligente dos dados, e não do acaso.

<div align="center">
  <img src="notebooks/shap_summary.png" alt="SHAP Summary - Importância Global das Features" width="700"/>
</div>

<br>

* **Visão Micro (Local):** Utilizei o *SHAP Waterfall* para destrinchar casos individuais de fraude. O sistema agora é capaz de emitir um relatório explicando exatamente quantos pontos percentuais cada variável contribuiu para o bloqueio de uma transação específica, entregando uma ferramenta pronta para as equipes de Prevenção a Fraude.

<div align="center">
  <img src="notebooks/shap_local_fraude.png" alt="SHAP Waterfall - Explicabilidade Local de uma Fraude" width="700"/>
</div>

<br>

* **Impacto Operacional (Matriz de Confusão):** Para coroar a tradução para o negócio, a matriz de confusão demonstra o excelente equilíbrio alcançado. O modelo restringe severamente os Falsos Positivos, permitindo que a operação de aprovação de cartões flua de forma saudável e sem fricções desnecessárias para os clientes legítimos, ao passo que garante a captura implacável das anomalias.

<div align="center">
  <img src="notebooks/matriz_confusao.png" alt="Matriz de Confusão - Equilíbrio de Falsos Positivos e Negativos" width="500"/>
</div>

---

## 🏗️ 5. Qualidade de Engenharia e Reprodutibilidade

O código foi construído seguindo rigorosos padrões de engenharia de software, garantindo modularidade e fácil implantação em sistemas legados:
* **`src/preprocessing.py`:** Isola toda a lógica de limpeza, transformação cíclica, normalização matemática e inferência do *Isolation Forest*.
* **`src/model.py`:** Encapsula a arquitetura complexa do *Stacking Ensemble*, facilitando testes unitários e a substituição de algoritmos base.
* **`notebooks/main.ipynb`:** O orquestrador limpo, responsável exclusivamente pelo fluxo de dados, visualização (Matriz de Confusão e SHAP) e geração do artefato final (`.csv`).

---

## 🏁 6. Conclusão

Este projeto prova que a resolução de problemas complexos de *Machine Learning* não depende apenas de importar bibliotecas pesadas, mas sim de uma profunda compreensão matemática dos dados aliada à visão de negócio. A solução apresentada vai muito além de uma simples submissão no Kaggle: ela entrega um *pipeline end-to-end* resiliente, otimizado metodologicamente, auditável por humanos (SHAP) e focado na redução real de perdas financeiras operacionais.
