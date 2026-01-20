import pandas as pd
import networkx as nx

filename = 'tt_fixed.csv'

df = pd.read_csv(filename, sep=';', encoding='utf-8', skipinitialspace=True, dtype=str)
df.columns = ['номер маршрута', 'тип', 'название', 'id', 'порядок', 'ширина', 'долгота']

df = df.dropna(subset=['номер маршрута', 'название', 'порядок'])
df['порядок'] = pd.to_numeric(df['порядок'], errors='coerce')
df['название'] = df['название'].str.strip()

G = nx.Graph()
route_ids = df['номер маршрута'].unique()

for r_id in route_ids:
    route_stops = df[df['номер маршрута'] == r_id].sort_values('порядок')
    stop_names = route_stops['название'].tolist()
    if len(stop_names) > 1:
        for i in range(len(stop_names) - 1):
            u = stop_names[i]
            v = stop_names[i+1]
            if u != v:
                G.add_edge(u, v)

components = list(nx.connected_components(G))
components.sort(key=len, reverse=True)

print(f"Найдено компонент: {len(components)}")

isolated_groups = components[1:]

if not isolated_groups:
    print("Изолированных групп нет, все связано!")
else:
    print(f"Найдено {len(isolated_groups)} изолированных групп(ы):")
    for i, comp in enumerate(isolated_groups):
        print(f"\n--- Группа №{i+1} (Размер: {len(comp)} остановок) ---")
        print(f"Остановки: {', '.join(comp)}")
        routes_in_group = df[df['название'].isin(comp)]['номер маршрута'].unique()
        print(f"МАРШРУТЫ в этой группе: {list(routes_in_group)}")
        print("-" * 50)
