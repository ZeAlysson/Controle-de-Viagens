import os
import sys
import django
import pandas as pd

# Configuração do Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema.settings")
django.setup()

from controle.models import Setor

# Caminho para o CSV
csv_path = "/home/itallo/projetos/ControleDeVeiculo/banco configs/SETORESESIGLAS.csv"

# Leitura do CSV com o delimitador correto
df = pd.read_csv(
    csv_path,
    encoding="latin1",
    delimiter=';',  # Especifica que o delimitador é ponto-e-vírgula
    skipinitialspace=True  # Remove espaços extras após o delimitador
)

# Verifique os dados lidos
print("Primeiras linhas do arquivo:")
print(df.head())
print("\nColunas encontradas:", df.columns.tolist())

# Inserção dos setores
for _, row in df.iterrows():
    # Verifique se há valores NaN (caso alguma linha esteja incompleta)
    if pd.isna(row['SETOR']) or pd.isna(row['SIGLA']) or pd.isna(row['CIDADE']):
        print(f"Aviso: Linha com valores faltando - {row}")
        continue
    
    Setor.objects.get_or_create(
        setor=row['SETOR'].strip(),
        sigla=row['SIGLA'].strip(),
        cidade=row['CIDADE'].strip()
    )

print("Importação finalizada com sucesso!")
