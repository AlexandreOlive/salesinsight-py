### Esse arquivo e o principal do nosso projeto ###
"""Ponto de entrada do projeto SalesInsight PY."""
import os
import modulo_vendas as mv


def main():
    print("=" * 62)
    print(" SALESINSIGHT PY - ANÁLISE DE DADOS DE VENDAS")
    print("=" * 62)

    arquivo_dados = "vendas.csv"

    # RF01: cria dados de demonstração se o arquivo ainda não existir.
    if not os.path.exists(arquivo_dados):
        mv.gerar_dataset_sintetico(arquivo_dados, n_registros=150, seed=42)

    # RF02 e RF03: leitura, inspeção e limpeza.
    dados_brutos = mv.carregar_csv(arquivo_dados)
    mv.inspecionar_dados(dados_brutos)
    dados_limpos = mv.limpar_dados(dados_brutos)

    if not dados_limpos:
        raise ValueError("Nenhum registro válido após a limpeza. Verifique vendas.csv.")

    # RF04: cria receita_total e faixa_preco.
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # Demonstra função de ordem superior e lambda.
    dados_processados = mv.processar_transformacao(
        dados_transformados,
        lambda item: {**item, "processado": True}
    )

    # RF05 e RF06: métricas agregadas e segmentação.
    metricas = mv.calcular_metricas(dados_processados)
    segmentos = mv.segmentar_clientes(dados_processados)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Registros válidos analisados: {len(dados_processados)}")
    print(f"Receita total da empresa: R$ {metricas['total_geral']:,.2f}")
    print("\nReceita por categoria:")
    for categoria, receita in metricas["por_categoria"].items():
        print(f"  - {categoria}: R$ {receita:,.2f}")
    print("\nReceita por região:")
    for regiao, receita in metricas["por_regiao"].items():
        print(f"  - {regiao}: R$ {receita:,.2f}")
    print("\nTop 5 clientes por gasto:")
    for cliente, info in top_clientes:
        print(f"  - {cliente}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # RF07: grava os dois relatórios exigidos.
    mv.exportar_resultados(metricas, segmentos, pasta_saida="outputs")
    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()
