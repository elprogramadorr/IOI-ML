import pandas as pd

# Suponiendo que ya tienes un DataFrame llamado df

# 1. Visualización de Datos

# Muestra las primeras 'n' filas del DataFrame (por defecto n=5)
df.head(10)  # Muestra las primeras 10 filas

# Muestra las últimas 'n' filas del DataFrame (por defecto n=5)
df.tail(10)  # Muestra las últimas 10 filas

# Resumen rápido de las columnas, el tipo de datos, y los valores no nulos
df.info()

# Estadísticas descriptivas básicas para cada columna numérica
df.describe()

# 2. Exploración de Datos

# Cuenta la cantidad de valores únicos en una columna
df['columna'].value_counts()

# Muestra los valores únicos de una columna
df['columna'].unique()

# Muestra la cantidad de valores nulos en cada columna
df.isnull().sum()

# 3. Filtrado de Datos

# Filtra filas en las que la columna 'columna' tiene un valor específico
df[df['columna'] == 'valor']

# Filtra filas con múltiples condiciones
df[(df['columna1'] > 5) & (df['columna2'] == 'valor')]

# 4. Limpieza de Datos

# Elimina columnas especificadas
df.drop(['columna1', 'columna2'], axis=1, inplace=True)

# Elimina filas con valores nulos
df.dropna(inplace=True)

# Rellena valores nulos en una columna con un valor específico
df['columna'].fillna(valor, inplace=True)

# 5. Operaciones en Columnas

# Renombra columnas
df.rename(columns={'columna_antigua': 'columna_nueva'}, inplace=True)

# Convierte una columna a otro tipo de dato
df['columna'] = df['columna'].astype(float)

# Crea una nueva columna basada en otras
df['nueva_columna'] = df['columna1'] + df['columna2']

# 6. Agrupación y Resumen

# Agrupa por una columna y calcula estadísticas
df.groupby('columna').mean()
df.groupby('columna')['otra_columna'].sum()

# 7. Ordenación de Datos

# Ordena los datos por una columna (ascendente o descendente)
df.sort_values(by='columna', ascending=False, inplace=True)

# 8. Guardado y Carga de Datos

# Guarda el DataFrame en un archivo CSV
df.to_csv('nombre_archivo.csv', index=False)

# Carga datos desde un archivo CSV
df = pd.read_csv('nombre_archivo.csv')
