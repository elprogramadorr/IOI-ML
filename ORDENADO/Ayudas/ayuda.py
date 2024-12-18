import pandas as pd

# Cargar los archivos CSV
df1 = pd.read_csv('data.csv')
df2 = pd.read_csv('dataset_con_problem.csv')

# Verificar si ambos DataFrames tienen el mismo número de filas
if len(df1) == len(df2):
    # Añadir la columna 'Highest Rated Problem' de df2 a df1
    df1['Highest Rated Problem'] = df2['Highest Rated Problem']

    # Guardar el DataFrame combinado en un nuevo archivo CSV
    df1.to_csv('archivo_combinado.csv', index=False)

    print("Archivo CSV combinado guardado como 'archivo_combinado.csv'")
else:
    print("Los DataFrames tienen diferente número de filas. Asegúrate de que sean iguales.")
