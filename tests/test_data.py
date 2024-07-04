"""Тесты загрузки и очистки данных."""

from __future__ import annotations

from spotify_analysis import config
from spotify_analysis.data import clean_data
from tests.helpers import make_raw_df


def test_clean_data_drops_empty_column():
    df = clean_data(make_raw_df())
    assert config.EMPTY_COLUMN not in df.columns


def test_clean_data_parses_release_date():
    df = clean_data(make_raw_df())
    assert str(df[config.RELEASE_DATE].dtype).startswith("datetime64")
    assert df[config.RELEASE_DATE].iloc[0].year == 2024


def test_clean_data_numeric_metrics_stripped_of_thousands_separators():
    df = clean_data(make_raw_df())
    assert df["Spotify Streams"].tolist() == [1000, 900, 500]
    assert df["Spotify Streams"].dtype == "int64"
    assert df[config.ALL_TIME_RANK].tolist() == [1, 2, 3]


def test_clean_data_keeps_track_score_as_float():
    df = clean_data(make_raw_df())
    assert df[config.TRACK_SCORE].tolist()[0] == 700.5
    assert df[config.TRACK_SCORE].dtype == "float64"


def test_clean_data_fills_missing_metric_with_zero():
    df = clean_data(make_raw_df())
    # У третьего трека не заполнен Apple Music Playlist Count.
    assert df["Apple Music Playlist Count"].tolist() == [500, 400, 0]


def test_clean_data_text_columns_are_string_dtype():
    df = clean_data(make_raw_df())
    for column in config.TEXT_COLUMNS:
        assert df[column].dtype == "string"


def test_clean_data_does_not_mutate_input():
    raw = make_raw_df()
    clean_data(raw)
    assert config.EMPTY_COLUMN in raw.columns
    assert raw["Spotify Streams"].iloc[0] == "1,000"
