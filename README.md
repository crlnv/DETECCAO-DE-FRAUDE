# PREDICAO DE FRAUDE

Olá! vai aí um script em **python** para predição de fraude usando características temporais (hora, dia da semana, mês), particularmente importantes porque padrões fraudulentos frequentemente seguem padrões temporais específicos (um brinde à matéria **Reconhecimento de Padrões Estatísticos**). Por exemplo, certas fraudes podem ser mais comuns em determinados horários do dia ou dias da semana. Estas informações granulares permitem que o modelo identifique padrões temporais sutis que podem indicar atividade suspeita. O cálculo da distância entre o local da transação e o estabelecimento comercial é uma característica crucial. Transações fraudulentas frequentemente ocorrem em locais geograficamente distantes do estabelecimento comercial ou do local usual de compras do cliente. A utilização da fórmula de geodésica (através da biblioteca **geopy**) fornece a distância precisa considerando a curvatura da Terra. 

A criação de variáveis agregadas como 'daily_transaction_count' e 'merchant_consistency' busca capturar padrões comportamentais. O número de transações diárias pode identificar surtos incomuns de atividade, enquanto a consistência do comerciante analisa a frequência com que diferentes profissões interagem com determinados estabelecimentos. Anomalias nesses padrões podem ser indicadores fortes de atividade fraudulenta.

Na análise exploratória univariada, os histogramas foram escolhidos para visualizar a distribuição das variáveis contínuas (valores de transação, idade e população). Esta visualização permite identificar outliers, assimetrias e padrões de distribuição que podem ser relevantes para a detecção de fraudes. A inclusão de KDE (Kernel Density Estimation) nos histogramas ajuda a suavizar a visualização e identificar melhor a forma da distribuição. A análise bivariada utilizando boxplots é particularmente eficaz para comparar a distribuição das variáveis numéricas entre transações fraudulentas e legítimas. Os boxplots mostram claramente não apenas as diferenças nas medianas, mas também na dispersão e na presença de outliers entre os dois grupos. Esta visualização pode revelar características distintivas das transações fraudulentas que não seriam aparentes em uma análise univariada.

Considerações sobre os resultados:

- Os resultados do modelo de classificação para detecção de fraudes demonstram uma performance excepcional, com precisão quase perfeita. O modelo atingiu 100% de acurácia para transações não fraudulentas (3.769 casos) e 99% para transações fraudulentas (565 casos), indicando uma capacidade notável de discriminação entre as classes.

- A matriz de confusão revela apenas 5 erros em um total de 4.334 previsões: 1 falso positivo (transação normal classificada como fraude) e 4 falsos negativos (fraudes não detectadas). Embora estes números sejam impressionantes, é importante notar que em contextos reais de fraude, cada falso negativo pode representar um risco financeiro significativo.

- É importante manter uma perspectiva crítica diante desses resultados. Uma performance quase perfeita como pode sinalizar possíveis questões como overfitting.

