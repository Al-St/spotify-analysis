"""Аналитические таблицы: топы треков, статистики исполнителей, лидеры платформ."""

from __future__ import annotations

import pandas as pd

from spotify_analysis import config


def top_clean_tracks(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Топ-N треков без возрастного ограничения по совокупности метрик.

    Треки ранжируются по ``All Time Rank`` и по ``Track Score``. Ожидается,
    что оба топа совпадают (так в датасете 2024 года); в противном случае
    возбуждается ошибка, чтобы не публиковать неоднозначный результат.

    Возвращает таблицу с колонками Track / Album Name / Artist /
    Release Date / ISRC и индексом 1..n.
    """
    clean = df[df[config.EXPLICIT] == 0]
    by_rank = clean.sort_values(config.ALL_TIME_RANK).head(n)
    by_score = clean.sort_values(config.TRACK_SCORE, ascending=False).head(n)

    if set(by_rank[config.ISRC]) != set(by_score[config.ISRC]):
        raise ValueError(
            "Топы по 'All Time Rank' и 'Track Score' не совпадают; "
            "требуется уточнить правило выбора совокупного топа."
        )

    table = by_rank[config.ID_COLUMNS].copy()
    table.index = range(1, len(table) + 1)
    table.index.name = None
    return table


def artist_track_score_stats(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Описательные статистики Track Score для top-N исполнителей по числу треков.

    Возвращает таблицу, где строки — статистики (count, mean, std, min,
    median, max), а столбцы — исполнители в порядке убывания количества
    треков в датасете.
    """
    counts = df[config.ARTIST].value_counts().nlargest(top_n)
    stats = (
        df[df[config.ARTIST].isin(counts.index)]
        .groupby(config.ARTIST)[config.TRACK_SCORE]
        .agg(["count", "mean", "std", "min", "median", "max"])
        .T
    )
    return stats.round(2)[counts.index]


def platform_leaders(df: pd.DataFrame) -> pd.DataFrame:
    """Самый популярный трек по каждому показателю каждой платформы.

    Для метрик из ``EXCLUDE_EXPLICIT_METRICS`` (см. конфигурацию) лидер
    выбирается только среди треков без возрастного ограничения.
    """
    rows: list[pd.Series] = []
    for metric in config.METRIC_COLUMNS:
        subset = df[df[config.EXPLICIT] == 0] if metric in config.EXCLUDE_EXPLICIT_METRICS else df
        leader = subset.sort_values(metric, ascending=False).iloc[0][config.ID_COLUMNS]
        rows.append(leader.rename(metric))

    table = pd.DataFrame(rows)
    table.index.name = "Metric"

    for (metric, column), value in config.LEADER_OVERRIDES.items():
        table.loc[metric, column] = value

    return table


def tracks_by_release_year(df: pd.DataFrame) -> pd.Series:
    """Количество треков датасета по году релиза (индекс отсортирован)."""
    years = df[config.RELEASE_DATE].dt.year.value_counts().sort_index()
    years.index.name = "Release Year"
    years.name = "Tracks"
    return years


def top_artists_by_track_count(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Топ-N исполнителей по количеству треков в датасете."""
    counts = df[config.ARTIST].value_counts().nlargest(n)
    counts.index.name = "Artist"
    counts.name = "Tracks"
    return counts


def platform_totals_by_explicit(df: pd.DataFrame) -> pd.DataFrame:
    """Суммы показателей каждой платформы отдельно для треков с explicit-флагом 0 и 1.

    Возвращает таблицу с индексом по ``Explicit Track`` (0/1) и колонками
    — названиями платформ из ``PLATFORM_METRICS``.
    """
    metric_sums = df.groupby(config.EXPLICIT)[config.METRIC_COLUMNS].sum()
    totals = pd.DataFrame(
        {
            platform: metric_sums[columns].sum(axis=1)
            for platform, columns in config.PLATFORM_METRICS.items()
        }
    )
    totals.index.name = config.EXPLICIT
    return totals
