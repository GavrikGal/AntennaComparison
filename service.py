import numpy as np
import pandas as pd
import scipy.stats as st


def read_data(path: str, col_n: int) -> pd.DataFrame:
    df = pd.read_csv(path, sep=',', encoding='utf-8', usecols=range(col_n+1), skiprows=45,
                     names=['F, MHz'] + [f'E{i}, dBuV/m' for i in range(1, col_n+1)],
                     index_col=0)
    df.index /= 1000000
    df.name = 'До поверки'
    return df


def read_comsol_data(path: str, col_n: int, calibrate: int) -> pd.DataFrame:
    df = pd.read_csv(path, sep='         ', encoding='utf-8', usecols=range(col_n+1), skiprows=5,
                     names=['F, MHz'] + [f'E{i}, dBuV/m' for i in range(1, col_n+1)],
                     index_col=0)
    df.index *= 1000
    df = df + calibrate
    df.name = 'Расчетные данные'
    return df


def stats(df: pd.DataFrame) -> pd.DataFrame:
    df_out = pd.DataFrame()
    df_out['mean'] = df.mean(axis=1)
    df_out['min'] = df.min(axis=1)
    df_out['max'] = df.max(axis=1)
    df_out['sem'] = df.sem(axis=1)
    df_out['interval-'], df_out['interval+'] = st.t.interval(confidence=0.95, df=len(df.columns) - 1,
                                                             loc=df_out['mean'], scale=df_out['sem'])
    return df_out


def plot_stats(ax, df_stats: pd.DataFrame, color=None) -> None:
    ax.plot(df_stats['mean'], linewidth=1.0, label='Среднее после поверки')
    ax.fill_between(df_stats.index.values, df_stats['interval-'], df_stats['interval+'], color=color,
                    alpha=0.4, linewidth=0.4, label='Доверительный интервал')


def plot_min_max(ax, df_stats: pd.DataFrame, color=None) -> None:
    ax.fill_between(df_stats.index.values, df_stats['min'], df_stats['max'], color=color, alpha=0.15,
                    linewidth=0.5, label='Мин-Макс значения')


def plot_line(ax, df: pd.DataFrame, color=None, linestyle=None) -> None:
    label = 'До поверки' if not df.name else df.name
    ax.plot(df, linewidth=1.2, color=color, label=label, linestyle=linestyle)


def setup_grid(ax, f_min, f_max, f_tick, fm_tick, y_min, y_max, y_tick, ym_tick):
    ax.set(ylim=(y_min, y_max))

    major_xticks = np.arange(f_min, f_max, f_tick)
    minor_xticks = np.arange(f_min, f_max, fm_tick)
    major_yticks = np.arange(y_min, y_max, y_tick)
    minor_yticks = np.arange(y_min, y_max, ym_tick)

    ax.set_xticks(major_xticks)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_yticks(major_yticks)
    ax.set_yticks(minor_yticks, minor=True)

    ax.grid(visible=True, alpha=0.3)
    ax.grid(visible=True, which='minor', alpha=0.05)


def mean_p_value(df1, df2, df2_stats):
    df3 = pd.merge(df2, df1, right_index=True, left_index=True)
    t_value, p_value = st.ttest_1samp(df3.iloc[:, :-1], df3.iloc[:, -1:], axis=1)
    # df2_stats['t-value'] = t_value
    # df2_stats['p-value'] = p_value
    # mean_p_value = df2_stats['p-value'].mean()
    return p_value.mean()
