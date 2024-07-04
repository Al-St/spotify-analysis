"""Тесты аналитических таблиц."""

from __future__ import annotations

import pandas as pd
import pytest

from spotify_analysis import analysis, config
from spotify_analysis.data import clean_data
from tests.helpers import make_raw_df


@pytest.fixture()
def df() -> pd.DataFrame:
    return clean_data(make_raw_df())


def test_top_clean_tracks_excludes_explicit(df):
    top = analysis.top_clean_tracks(df, n=1)
    assert top[config.TRACK].tolist() == ["Track A"]


def test_top_clean_tracks_has_ordinal_index_and_id_columns(df):
    top = analysis.top_clean_tracks(df, n=2)
    assert list(top.index) == [1, 2]
    assert list(top.columns) == config.ID_COLUMNS


def test_top_clean_tracks_raises_when_rankings_diverge(df):
    diverged = df.copy()
    # Track Score у Track C делаем выше, чем у Track A, — топы перестанут совпадать.
    diverged.loc[diverged[config.TRACK] == "Track C", config.TRACK_SCORE] = 999.0
    with pytest.raises(ValueError, match="не совпадают"):
        analysis.top_clean_tracks(diverged, n=1)


def test_artist_track_score_stats_order_and_shape(df):
    stats = analysis.artist_track_score_stats(df)
    # Artist X встречается дважды, Artist Y — один раз.
    assert list(stats.columns) == ["Artist X", "Artist Y"]
    assert stats.loc["count", "Artist X"] == 2
    assert stats.loc["count", "Artist Y"] == 1
    assert set(stats.index) == {"count", "mean", "std", "min", "median", "max"}


def test_platform_leaders_one_row_per_metric(df):
    leaders = analysis.platform_leaders(df)
    assert len(leaders) == len(config.METRIC_COLUMNS)
    assert list(leaders.columns) == config.ID_COLUMNS
    # По Spotify Streams лидирует самый прослушиваемый трек.
    assert leaders.loc["Spotify Streams", config.TRACK] == "Track A"


def test_platform_leaders_soundcloud_ignores_explicit(df):
    leaders = analysis.platform_leaders(df)
    # Explicit-трек Track B обходит всех по Soundcloud,
    # но для этой метрики лидер ищется только среди «чистых» треков.
    assert leaders.loc["Soundcloud Streams", config.TRACK] == "Track A"


def test_platform_leaders_applies_manual_overrides(df):
    leaders = analysis.platform_leaders(df)
    for (metric, column), value in config.LEADER_OVERRIDES.items():
        assert leaders.loc[metric, column] == value


def test_tracks_by_release_year(df):
    yearly = analysis.tracks_by_release_year(df)
    assert yearly.tolist() == [1, 1, 1]
    assert list(yearly.index) == [2020, 2023, 2024]


def test_top_artists_by_track_count(df):
    assert analysis.top_artists_by_track_count(df, n=1).index[0] == "Artist X"


def test_platform_totals_by_explicit(df):
    totals = analysis.platform_totals_by_explicit(df)
    assert list(totals.index) == [0, 1]
    assert totals.loc[0, "Spotify"] == (1000 + 10 + 100 + 90) + (500 + 5 + 50 + 50)
    assert totals.loc[1, "Spotify"] == 900 + 9 + 90 + 80
    assert list(totals.columns) == list(config.PLATFORM_METRICS)
