# SalesInsight PY — Pipeline de Análise de Dados de Vendas

## 1. Objetivo
Projeto acadêmico de análise de vendas com Python, usando somente a biblioteca padrão. O programa carrega um CSV, inspeciona e limpa os dados, cria campos derivados, calcula métricas, segmenta clientes e exporta relatórios em CSV e JSON.

## 2. Requisitos
- Python 3 instalado.
- Git instalado para realizar o versionamento exigido.
- Não são necessárias bibliotecas externas.

## 3. Estrutura
- `main.py`: ponto de entrada e coordenação do pipeline.
- `modulo_vendas.py`: funções de leitura, inspeção, limpeza, transformação, agregação, segmentação e exportação.
- `vendas.csv`: dataset de entrada. Se não existir, será gerado um dataset sintético com 150 registros.
- `outputs/metricas_resumo.csv`: receita total por categoria.
- `outputs/estatisticas.json`: métricas gerais, receita por categoria/região e gastos/segmentos por cliente.

## 4. Como executar
Abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

No Windows, também pode funcionar:

```bash
py main.py
```

Na primeira execução, se `vendas.csv` não existir, o programa cria a base sintética. As linhas com valores obrigatórios vazios, datas inválidas ou números inválidos são descartadas e contabilizadas.

## 5. Regras de negócio
### Receita por venda
`receita_total = quantidade * preco_unitario`

### Faixa de preço
- Baixo: receita do item abaixo de R$ 500.
- Médio: receita do item de R$ 500 até R$ 2.000, inclusive.
- Alto: receita do item acima de R$ 2.000.

### Segmentação de clientes
- Bronze: gasto acumulado abaixo de R$ 3.000.
- Prata: gasto acumulado de R$ 3.000 até R$ 8.000, inclusive.
- Ouro: gasto acumulado acima de R$ 8.000.

## 6. Versionamento Git
Execute os comandos abaixo dentro da pasta do projeto. Para atender ao critério de branches e commits, os comandos de exemplo criam uma branch por etapa; faça os commits após adicionar os arquivos correspondentes.

```bash
git init
git branch -M main
git add README.md
git commit -m "docs: documenta objetivo e estrutura inicial"

git checkout -b feat/dataset-csv
git add modulo_vendas.py
git commit -m "feat: implementa geração e leitura do dataset"

git checkout -b feat/limpeza-transformacao
git add modulo_vendas.py
git commit -m "feat: implementa inspeção limpeza e campos derivados"

git checkout -b feat/metricas-clientes
git add modulo_vendas.py main.py
git commit -m "feat: calcula métricas e segmenta clientes"

git checkout -b feat/exportacao-relatorios
git add main.py
git commit -m "feat: executa pipeline e exporta relatórios"

git checkout main
git merge feat/dataset-csv
git merge feat/limpeza-transformacao
git merge feat/metricas-clientes
git merge feat/exportacao-relatorios
git log --oneline --all
```

**Importante:** os comandos acima são um roteiro ilustrativo. Se os mesmos arquivos forem adicionados e alterados em etapas diferentes, faça cada commit na etapa correspondente. O Git não permite criar commits reais antes de as alterações existirem. Se preferir um fluxo simples e linear, crie pelo menos cinco commits reais, com mensagens descritivas, e mostre `git log` no vídeo. Não apresente histórico fictício.

## 7. Roteiro para vídeo de até 5 minutos
1. (0:00–0:40) Apresente o objetivo e mostre a estrutura de arquivos.
2. (0:40–1:20) Abra `modulo_vendas.py` e explique leitura e inspeção.
3. (1:20–2:10) Explique limpeza, conversão de tipos e campos derivados.
4. (2:10–3:10) Mostre métricas por categoria/região e segmentação de clientes.
5. (3:10–4:10) Execute `python main.py` no terminal.
6. (4:10–4:40) Abra os arquivos gerados em `outputs/`.
7. (4:40–5:00) Mostre `git log --oneline --all`.

## 8. Checklist de entrega
- [ ] `main.py` e `modulo_vendas.py` presentes.
- [ ] `vendas.csv` com pelo menos 100 registros.
- [ ] Execução sem erros.
- [ ] `outputs/metricas_resumo.csv` e `outputs/estatisticas.json` gerados.
- [ ] README revisado.
- [ ] Pelo menos cinco commits reais no Git.
- [ ] Vídeo de até cinco minutos gravado.
- [ ] Links enviados no AVA conforme orientação da disciplina.
