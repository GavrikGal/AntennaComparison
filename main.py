import pandas as pd
import matplotlib.pyplot as plt

from service import read_data, plot_line, plot_stats, plot_min_max, mean_p_value, setup_grid, stats


first_file = r'data\П6-23М\Перед поверкой\750-2000 МГц [tr1-ГП, tr2-ВП].csv'
# sec_file = r'z:\0. Данные\SA\data\traces\2023\Антенны\П6-23М\После поверки\750-2000 МГц ГП_3_центр.csv'
files = [
    r'data\П6-23М\После поверки\750-2000 МГц ГП_3_лево.csv',
    r'data\П6-23М\После поверки\750-2000 МГц ГП_3_право.csv',
    r'data\П6-23М\После поверки\750-2000 МГц ГП_3_центр.csv',
]

df1 = read_data(first_file, 1)
# df2 = read_data(sec_file, 6)

df2 = pd.DataFrame()
for file in files:
    df2 = pd.concat([df2, read_data(file, 6)], axis=1)
df2_stats = stats(df2)

fig, ax = plt.subplots(figsize=(12, 8))
setup_grid(ax, f_min=600, f_max=2100, f_tick=200, fm_tick=25,
           y_min=40, y_max=95, y_tick=10, ym_tick=1)

plot_stats(ax, df2_stats, color='tab:blue')
plot_min_max(ax, df2_stats, color='tab:blue')
plot_line(ax, df1, color='tab:red')

df2_stats.to_csv(r'data\П6-23М\results.csv')

mean_p_value = mean_p_value(df1, df2, df2_stats)
plt.title(f'Средняя вероятность, принадлежности первой выборки ко второй: {mean_p_value*100:.2f}%')
plt.legend()
plt.show()
