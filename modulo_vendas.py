"""Funções de leitura, limpeza, transformação e análise de vendas.
Projeto: SalesInsight PY
Utiliza apenas bibliotecas da biblioteca padrão do Python.
"""
import csv
import json
import os
import random
from datetime import date


CAMPOS_OBRIGATORIOS = [
    "id_venda", "data_venda", "cliente", "produto",
    "categoria", "regiao", "quantidade", "preco_unitario"
]


def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=150, seed=42):
    """Cria uma base reproduzível com algumas inconsistências para testar a limpeza."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {
        "Notebook": "Eletrônicos", "Smartphone": "Celulares",
        "Tablet": "Celulares", "Monitor": "Eletrônicos",
        "Teclado": "Acessórios", "Mouse": "Acessórios"
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(CAMPOS_OBRIGATORIOS)
        for i in range(1, n_registros + 1):
            produto = random.choice(produtos)
            quantidade = str(random.randint(1, 8)) if random.random() > 0.05 else ""
            preco = f"{random.uniform(100, 3500):.2f}" if random.random() > 0.05 else ""
            nome_produto = f"  {produto} " if random.random() < 0.10 else produto
            escritor.writerow([
                i,
                f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                f"Cliente_{random.randint(1, 30):03d}",
                nome_produto,
                categorias[produto],
                random.choice(regioes),
                quantidade,
                preco
            ])
    print(f"[OK] Dataset sintético criado: {caminho_arquivo}")


def carregar_csv(caminho_arquivo):
    """Lê o CSV usando csv.DictReader e retorna uma lista de dicionários."""
    with open(caminho_arquivo, "r", newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)
        if not leitor.fieldnames:
            raise ValueError("O CSV está vazio ou não possui cabeçalho.")
        ausentes = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in leitor.fieldnames]
        if ausentes:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(ausentes)}")
        return list(leitor)


def inspecionar_dados(dados):
    """Mostra quantidade de linhas e contabiliza campos vazios por coluna."""
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if not dados:
        print("A base não contém registros.")
        return
    print(f"Campos disponíveis: {list(dados[0].keys())}")
    vazios_por_campo = {}
    linhas_incompletas = 0
    for linha in dados:
        linha_tem_vazio = False
        for campo, valor in linha.items():
            if valor is None or not str(valor).strip():
                vazios_por_campo[campo] = vazios_por_campo.get(campo, 0) + 1
                linha_tem_vazio = True
        if linha_tem_vazio:
            linhas_incompletas += 1
    print(f"Linhas com pelo menos um campo vazio: {linhas_incompletas}")
    print(f"Campos vazios por coluna: {vazios_por_campo or 'Nenhum'}")
    print(f"Exemplo de registro: {dados[0]}")


def limpar_dados(dados_brutos):
    """Remove campos textuais vazios, valores numéricos inválidos e datas inválidas."""
    dados_limpos = []
    removidos = 0

    for linha in dados_brutos:
        try:
            registro = {chave: str(valor or "").strip() for chave, valor in linha.items()}
            if any(not registro.get(campo) for campo in CAMPOS_OBRIGATORIOS):
                removidos += 1
                continue

            quantidade = int(registro["quantidade"])
            preco = float(registro["preco_unitario"].replace(",", "."))
            if quantidade <= 0 or preco < 0:
                removidos += 1
                continue

            data_venda = date.fromisoformat(registro["data_venda"])
            id_venda = int(registro["id_venda"])
            if not registro["cliente"] or not registro["produto"] or not registro["categoria"] or not registro["regiao"]:
                removidos += 1
                continue

            dados_limpos.append({
                "id_venda": id_venda,
                "data_venda": data_venda.isoformat(),
                "cliente": registro["cliente"],
                "produto": registro["produto"],
                "categoria": registro["categoria"],
                "regiao": registro["regiao"],
                "quantidade": quantidade,
                "preco_unitario": round(preco, 2)
            })
        except (ValueError, TypeError):
            removidos += 1

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros válidos: {len(dados_limpos)} | Registros removidos: {removidos}")
    return dados_limpos


def criar_campos_derivados(dados):
    """Acrescenta receita_total e faixa_preco a cada venda."""
    for item in dados:
        receita = round(item["quantidade"] * item["preco_unitario"], 2)
        item["receita_total"] = receita
        # A faixa é determinada pelo valor da receita do item, conforme o enunciado.
        if receita < 500:
            item["faixa_preco"] = "Baixo"
        elif receita <= 2000:
            item["faixa_preco"] = "Médio"
        else:
            item["faixa_preco"] = "Alto"
    return dados


def processar_transformacao(dados, funcao):
    """Aplica uma função recebida como argumento a cada registro (exemplo com lambda)."""
    return [funcao(item) for item in dados]


def calcular_metricas(dados):
    """Calcula receita total por categoria, região e no conjunto completo."""
    receita_categoria = {}
    receita_regiao = {}
    total_geral = 0.0

    for item in dados:
        categoria = item["categoria"]
        regiao = item["regiao"]
        receita = item["receita_total"]
        receita_categoria[categoria] = receita_categoria.get(categoria, 0.0) + receita
        receita_regiao[regiao] = receita_regiao.get(regiao, 0.0) + receita
        total_geral += receita

    return {
        "total_geral": round(total_geral, 2),
        "por_categoria": {k: round(v, 2) for k, v in sorted(receita_categoria.items())},
        "por_regiao": {k: round(v, 2) for k, v in sorted(receita_regiao.items())}
    }


def segmentar_clientes(dados):
    """Soma as compras por cliente e classifica em Bronze, Prata ou Ouro."""
    gastos_cliente = {}
    for item in dados:
        cliente = item["cliente"]
        gastos_cliente[cliente] = gastos_cliente.get(cliente, 0.0) + item["receita_total"]

    segmentos = {}
    for cliente, total in sorted(gastos_cliente.items()):
        if total > 8000:
            segmento = "Ouro"
        elif total >= 3000:
            segmento = "Prata"
        else:
            segmento = "Bronze"
        segmentos[cliente] = {
            "total_gasto": round(total, 2),
            "segmento": segmento
        }
    return segmentos


def obter_top_clientes(segmentos, top_n=5):
    """Retorna os clientes com maior gasto acumulado."""
    return sorted(
        segmentos.items(),
        key=lambda par: par[1]["total_gasto"],
        reverse=True
    )[:top_n]


def exportar_resultados(metricas, clientes, pasta_saida="outputs"):
    """Exporta métricas e segmentos em JSON e resumo de categorias em CSV."""
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_json = os.path.join(pasta_saida, "estatisticas.json")
    with open(caminho_json, "w", encoding="utf-8") as arquivo:
        json.dump(
            {"metricas_gerais": metricas, "clientes": clientes},
            arquivo, indent=4, ensure_ascii=False
        )

    caminho_csv = os.path.join(pasta_saida, "metricas_resumo.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Categoria", "Receita Total"])
        for categoria, receita in metricas["por_categoria"].items():
            escritor.writerow([categoria, f"{receita:.2f}"])

    print(f"[OK] JSON exportado: {caminho_json}")
    print(f"[OK] CSV exportado: {caminho_csv}")
