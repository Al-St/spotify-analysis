"""Загрузка и очистка датасета Most Streamed Spotify Songs 2024."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from spotify_analysis import config


def load_raw_data(path: Path | None = None) -> pd.DataFrame:
    """Загрузить сырой CSV из выгрузки Kaggle.

    Файл содержит повреждённые многобайтовые символы, поэтому читается
    в latin-1 — см. комментарий в :mod:`spotify_analysis.config`.
    """
    return pd.read_csv(path or config.RAW_DATA_PATH, encoding=config.RAW_CSV_ENCODING)


def _to_int(series: pd.Series) -> pd.Series:
    """Привести показатель к int64: убрать разделители тысяч и заполнить пропуски.

    Пропуск трактуется как 0 (отсутствие трека на платформе), что корректно
    для всех метрик датасета: статистики по пропускам отдельно не считаются.
    """
    if series.dtype == object or pd.api.types.is_string_dtype(series):
        series = series.str.replace(",", "", regex=False)
    return pd.to_numeric(series).fillna(0).astype("int64")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Привести сырой датасет к аналитическому виду. Возвращает копию.

    Шаги:
    1. удалить колонку ``TIDAL Popularity`` — она пуста целиком;
    2. привести ``Release Date`` к datetime;
    3. привести текстовые колонки к pandas-типу ``string``;
    4. привести все измерительные колонки к int64 (числа в CSV хранятся
       строками с разделителями тысяч);
    5. заполнить пропуски в измерительных колонках нулями.
    """
    df = df.copy()

    df = df.drop(columns=config.EMPTY_COLUMN)

    df[config.RELEASE_DATE] = pd.to_datetime(df[config.RELEASE_DATE])

    for column in config.TEXT_COLUMNS:
        df[column] = df[column].astype("string")

    numeric_columns = [
        config.ALL_TIME_RANK,
        config.TRACK_SCORE,
        config.EXPLICIT,
        *config.METRIC_COLUMNS,
    ]
    for column in numeric_columns:
        if column == config.TRACK_SCORE:
            # Track Score — единственный дробный показатель (например, 725.4).
            if df[column].dtype == object or pd.api.types.is_string_dtype(df[column]):
                df[column] = df[column].str.replace(",", "", regex=False)
            df[column] = pd.to_numeric(df[column]).fillna(0).astype("float64")
        else:
            df[column] = _to_int(df[column])

    return df


def load_clean_data(path: Path | None = None) -> pd.DataFrame:
    """Загрузить и очистить датасет одной операцией."""
    return clean_data(load_raw_data(path))
