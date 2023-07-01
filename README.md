# Health Insurance Cross-Sell

# 1.0 Problema de negócio

## 1.1 Contexto

Uma seguradora possui uma base de clientes que utiliza um determinado serviço de seguro de saúde anual. Agora, a empresa quer oferecer um novo serviço para novos clientes: um seguro de automóveis. Para isso, a seguradora tem o contato de 127 mil possíveis novos clientes. Entretanto, há um certo limite operacional, sendo possível realizar contato com apenas 2.000 pessoas. Então, é necessário prever quais são as 2 mil pessoas mais propensas desta lista a realizar a compra do novo serviço de seguro.

## 1.2 Como funciona o modelo de negócio de uma seguradora?

Exemplo prático: o usuário contrata um serviço de seguro de saúde no valor anual de R$5.000,00 e o serviço de seguro assegura R$200.000,00 a este usuário em caso de despesas médicas que estejam inclusas no contrato. Então, a seguradora calcula a probabilidade das pessoas ficarem doentes durante o ano. Por este motivo que os valores do seguro variam de acordo com as características de cada cliente (idade, habitos alimentares, estilo de vida...).

## 1.3 O que é um Cross-Sell?

Técnica baseada em oferecer serviços ou produtos complementares ou relacionados com base nos interesses do cliente ao adquirir um produto. No projeto em questão, os clientes já possuem um serviço de seguro adquirido e o estudo que será feito tem a motivação de captar a propensão de compra de serviços ou produtos complementares.

## 1.4 Como é calculado o lucro de uma seguradora?

O lucro (L) é dado pela multiplicação entre o preço médio anual do seguro (P) e a quantidade de clientes adquiridos (Q) subtraindo os custos (C):

$$ L = P\cdot Q - C $$

# 2.0 Planejamento da solução

Fonte dos dados: https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction

Definição do problema: classificação do tipo Learn to Rank (ranqueamento).

Ferramentas utilizadas: Python 3.9.16 e bibliotecas (contidas no arquivo do projeto 'requirements.txt').

Formato da entrega:
- Arquivo 'predictions.csv' contendo as propensões de compra dos 2.000 melhores clientes da base de teste.
- Planilha no Google Sheets 'pa004_googlesheets.gs', onde o usuário do time de negócio pode customizar as features existentes e realizar as predições individualmente.

Passos para a solução do problema:
1. Coleta e descrição dos dados;
2. Criação das hipóteses de negócio e análise exploratória dos dados;
3. Preparação dos dados e seleção dos atributos;
4. Modelagem de Machine Learning e avaliação da performance dos modelos;
5. Resultados de negócio;
6. Modelo em produção;
7. Integração do modelo com o Google Sheets.

# 3.0 Descrição dos dados

Descrição dos atributos:
- id: identificador único do cliente.
- Gender: gênero do cliente.
- Age: idade do cliente.
- Driving_License: 0 quando o cliente não tem licença para dirigir, 1 quando o cliente tem licença para dirigir.
- Region_Code: código único de localização do cliente.
- Previously_Insured: 0 quando o cliente não tem seguro de veículo, 1 quando o cliente já tem um seguro de veículo.
- Vehicle_Age: ano do veículo.
- Vehicle_Damage: 0 quando o cliente não teve seu carro danificado, 1 quando o cliente já teve seu carro danificado.
- Annual_Premium: o montante que o cliente precisa pagar como premium num ano.
- Policy_Sales_Channel: código anônimo para o canal de divulgação para o cliente, ou seja, agentes diferentes, por correio, por telefone, pessoalmente, etc.
- Vintage: período, em dias, desde que o cliente possui contrato com a empresa.
- Response: variável resposta, sendo 0 caso o cliente não tenha interesse na contratação e 1 caso tenha interesse.

Principais conclusões da análise estatística descritiva:
- Não há NAs e nem outliers aparentes.
- 12% dos clientes possuem interesse em um serviço de seguro de carros.

# 4.0 Criação e validação das hipóteses de negócio

Lista de hipóteses:
1. gender: mulheres possuem mais interesse em adquirir o seguro do que os homens, em proporção. **Falsa**.
2. driving_license: clientes com licença possuem mais interesse em adquirir o seguro do que clientes sem licença, em proporção. **Verdadeira**.
3. previously_insured: clientes que já possuem outro contrato de seguro com a empresa possuem mais interesse em adquirir o seguro do que clientes que não possuem outro contrato de seguro com a empresa, em proporção. **Verdadeira**.
4. vehicle_age: clientes com carros mais novos possuem mais interesse em adquirir o seguro do que clientes com carros mais novos, em proporção. **Falsa**.
5. vehicle_damage: clientes que já tiveram o carro danificado possuem mais interesse em adquirir o seguro do que clientes que nunca tiveram o carro danificado, em proporção. **Verdadeira**.

Principais conclusões da análise exploratória dos dados (EDA):
1. id: não possui nenhuma relação explícita com a variável resposta.
2. age: a maior quantidade de clientes da base possui menos de 30 anos (entre 21 e 25 anos). Porém, a maior parte dos interessados, em proporção (valores acima de 20%), está entre os 33 e 48 anos.
3. region_code: possui pouca relação explícita com a variável resposta. Destacam-se as regiões 5, 19, 28 e 38 com mais de 15% de proporção de interesse.
4. annual_premium: possui pouca relação explícita com a variável resposta. Seguros entre $200.000,00 e $300.000,00 possuem um percentual de interesse um pouco maior, mas a amostragem é muito pequena. Cerca de 17% dos clientes teriam um seguro anual no valor de $2.630,00 (valor mais baixo).
5. policy_sales_channel: o canal com maior contagem de clientes é o canal com menor proporção de interesse (canal 152). O canal 156 possui uma amostra relevante de clientes (mais de 10 mil) e um percentual de interesse maior que 20%.
6. vintage: possui pouca relação explícita com a variável resposta.

## 5.0 Modelagem de Machine Learning e performance dos modelos



