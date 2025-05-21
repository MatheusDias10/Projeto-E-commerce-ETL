# Importando a biblioteca necessária
import pandas as pd

# Lendo o DataFrame
df = pd.read_csv("vendas_ecommerce_inconsistent.csv")

# LIMPEZA E TRANSFORMAÇÃO DOS DADOS

# Removendo linhas com valores nulos nas colunas específicas
df.dropna(subset=["data", "produto", "endereco_envio"], inplace=True)

# Preenchendo valores ausentes na coluna 'cliente'
df["cliente"] = df["cliente"].fillna("Cliente Desconhecido")

# Corrigindo valores incorretos na coluna 'quantidade'
media_quantidade = df["quantidade"].mean()
df["quantidade"] = df["quantidade"].replace(-3, media_quantidade)

# Preenchendo valores nulos na coluna 'avaliacao' com a média da coluna
media_avaliacao = df["avaliacao"].mean()
df["avaliacao"] = df["avaliacao"].fillna(media_avaliacao)

# TRANSFORMAÇÃO E ANÁLISE DE DADOS

# 1. Criando uma nova coluna 'preco_total' a partir da quantidade e preço unitário
df["preco_total"] = df["quantidade"] * df["preco_unitario"]

# 2. Agrupando por 'produto' e 'estado' para calcular o total de vendas por produto em cada estado
df_agrupado = df.groupby(['produto', 'estado'])['preco_total'].sum().reset_index()
print("\nTotal de vendas por produto e estado:")
print(df_agrupado)

# 3. Filtrando produtos com avaliação menor ou igual a 3
df_filtrado = df[df["avaliacao"] <= 3]
print("\nProdutos com avaliação abaixo ou igual a 3:")
print(df_filtrado)

# 4. Listando os 3 produtos mais vendidos
df_quantidade_vendida = df.groupby('produto')['quantidade'].sum().reset_index()
df_quantidade_vendida = df_quantidade_vendida.sort_values(by='quantidade', ascending=False)
top_3_produtos = df_quantidade_vendida.head(3)
print("\nTop 3 produtos mais vendidos:")
print(top_3_produtos)

# 5. Calculando a média de avaliação para cada produto
media_avaliacao_produto = df.groupby("produto")["avaliacao"].mean().round(2).reset_index()
print("\nMédia de avaliação de cada produto:")
print(media_avaliacao_produto)

# 6. Contagem de produtos por estado
contagem_estado = df.groupby(['produto', 'estado']).size().reset_index(name='quantidade_por_estado')
print("\nContagem de produtos por estado:")
print(contagem_estado)
