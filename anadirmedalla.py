import pandas as pd

data = pd.read_csv('ioi_codeforces_completed.csv')

def assign_medal(row):
    rank_percentage = row['Ranking IOI 2024']  # Asumimos que la columna es 'Ranking IOI 2024'
    
    if rank_percentage >= 91.7:
        return 'Gold'  # Oro 🥇
    elif rank_percentage > 75:
        return 'Silver'  # Plata 🥈
    elif rank_percentage > 50:
        return 'Bronze'  # Bronce 🥉
    else:
        return 'None'  # Sin medalla ❌

data['Medal'] = data.apply(assign_medal, axis=1)

# 5. Guardar el nuevo archivo CSV con la columna 'Medal' añadida
data.to_csv('ioi_codeforces_with_medal.csv', index=False)

# Mostrar el dataframe con la nueva columna
print("¡Archivo guardado con la columna de medalla añadida! 🎉")
