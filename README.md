# Fronteira de Markowitz
<p>Desenvolvimento de um portifólio que escolhe ações e as combina de modo a encontrar a os melhores pontos na fronteira eficiente de Markowitz.</p>

## Instalação das dependências

<code>sudo apt install python3</code>

<code>pip install yfinance --upgrade --no-cache-dir</code>

## Introdução

<p>A Fronteira Eficiente, uma ideia proposta por Harry Markowitz, sugere que o risco associado a um portfólio de investimentos não é meramente a média dos riscos dos ativos individuais, mas sim uma função da diversificação do portfólio como um todo. Em termos gerais, o risco de um portfólio é a possibilidade de ganhos ou perdas em um conjunto de ativos. Existem várias métricas para medir esse risco, sendo o desvio padrão a mais comum. No entanto, o desvio padrão de um portfólio não pode ser calculado simplesmente somando as médias dos desvios dos ativos individualmente. Isso ocorre porque existe uma correlação entre as movimentações de diferentes ativos financeiros. Foi precisamente para encontrar uma forma de medir o risco de um portfólio que o modelo de Markowitz, também conhecido como modelo de portfólio, foi desenvolvido.</p>

<h1>Metodologia</h1>

<h2>1. Definição do Problema e Objetivo</h2>
<p>O objetivo deste estudo é analisar o desempenho de diferentes ações brasileiras e construir portfólios eficientes com base na teoria da Fronteira Eficiente de Markowitz. A análise abrange um período de 4 anos (2020-2024) e inclui ações de seis empresas: ITUB4.SA, BBDC4.SA, DIRR3.SA, PETR4.SA, VALE3.SA e ABEV3.SA.</p>

<h2>2. Coleta e Pré-processamento de Dados</h2>
<ol>
    <li><strong>Coleta de Dados:</strong>
        <p>Utilizou-se a biblioteca <code>yfinance</code> para baixar os dados históricos de fechamento ajustado das ações selecionadas. Os dados foram coletados para o período de 1º de janeiro de 2020 a 30 de junho de 2024, com frequência diária.</p>
    </li>
    <li><strong>Normalização dos Dados:</strong>
        <p>Os dados de fechamento ajustado foram normalizados para começar com valor 100 no início do período, permitindo uma comparação uniforme entre as ações.</p>
    </li>
</ol>

<h2>3. Análise Exploratória dos Dados</h2>
<ol>
    <li><strong>Visualização Inicial:</strong>
        <p>Plotaram-se os dados normalizados para visualizar o comportamento histórico das ações.</p>
    </li>
    <li><strong>Cálculo de Retornos e Volatilidade:</strong>
        <ul>
            <li><strong>Retorno Acumulado:</strong> Calculado como a variação percentual entre o valor final e inicial das ações.</li>
            <li><strong>Retorno Anualizado:</strong> Calculado com base no retorno acumulado ajustado para uma base anual.</li>
            <li><strong>Volatilidade Anualizada:</strong> Calculada a partir da volatilidade diária, ajustada para uma base anual.</li>
        </ul>
    </li>
    <li><strong>Matriz de Correlação:</strong>
        <p>Calculada a partir dos retornos diários das ações para entender as correlações entre os ativos.</p>
    </li>
    <li><strong>Visualização de Portfólio:</strong>
        <p>Criou-se um portfólio hipotético com 50% em PETR4.SA e 50% em VALE3.SA, e analisou-se o desempenho deste portfólio comparado com as ações individuais.</p>
    </li>
</ol>

<h2>4. Análise da Fronteira Eficiente de Markowitz</h2>
<ol>
    <li><strong>Cálculo da Fronteira Eficiente:</strong>
        <p>Inicialmente, calculou-se a fronteira eficiente considerando dois ativos: PETR4.SA e VALE3.SA. Foram testadas alocações variando de 0% a 100% em incrementos de 5%.</p>
        <p>A função <code>calc_ret_vol</code> foi utilizada para calcular o retorno e a volatilidade anualizados para cada combinação de pesos.</p>
    </li>
    <li><strong>Visualização da Fronteira Eficiente:</strong>
        <p>Plotaram-se os pontos da fronteira eficiente em um gráfico, incluindo os pontos de retorno e volatilidade das ações individuais e do portfólio com menor volatilidade.</p>
    </li>
    <li><strong>Expansão da Análise:</strong>
        <p>A análise foi expandida para incluir um terceiro ativo, ABEV3.SA, e repetiu-se o cálculo da fronteira eficiente, considerando todas as combinações possíveis de pesos entre PETR4.SA, VALE3.SA e ABEV3.SA.</p>
    </li>
    <li><strong>Visualização da Fronteira Eficiente com Três Ativos:</strong>
        <p>Repetiu-se o processo de visualização com três ativos, destacando o portfólio de mínima volatilidade e as ações individuais no gráfico.</p>
    </li>
</ol>

<h2>5. Cálculo e Visualização de Drawdown</h2>
<ol>
    <li><strong>Cálculo de Drawdown:</strong>
        <p>A função <code>calculate_drawdown</code> foi utilizada para calcular o drawdown percentual para cada ativo e portfólio, representando a queda em relação ao pico anterior.</p>
    </li>
    <li><strong>Visualização do Drawdown:</strong>
        <p>Plotou-se o drawdown dos portfólios e ações selecionadas para analisar o risco de perda ao longo do período estudado.</p>
    </li>
</ol>
