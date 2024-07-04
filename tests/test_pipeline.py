"""Интеграционный тест пайплайна на реальном датасете (если он на месте)."""

from __future__ import annotations

from pathlib import Path

import pytest

from spotify_analysis import config
from spotify_analysis.pipeline import run_analysis


@pytest.mark.skipif(not config.RAW_DATA_PATH.exists(), reason="сырой CSV отсутствует в data/raw")
def test_run_analysis_produces_reports(tmp_path: Path):
    tables = run_analysis(reports_dir=tmp_path, save_reports=True)

    assert len(tables["top_clean_tracks"]) == 10
    assert len(tables["artist_stats"].columns) == 10
    assert len(tables["platform_leaders"]) == len(config.METRIC_COLUMNS)

    for filename in (
        "top_10_clean_tracks.xlsx",
        "artist_track_score_stats.xlsx",
        "platform_leaders.xlsx",
    ):
        assert (tmp_path / "tables" / filename).exists()

    for filename in (
        "tracks_by_release_year.png",
        "top_artists_by_track_count.png",
        "platform_totals_by_explicit.png",
    ):
        assert (tmp_path / "figures" / filename).exists()
