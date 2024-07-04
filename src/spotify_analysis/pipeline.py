"""Сквозной пайплайн: данные -> аналитические таблицы -> отчёты.

Запуск из корня репозитория::

    spotify-analysis                 # или: python -m spotify_analysis
    spotify-analysis --input data/raw/custom.csv --reports-dir reports
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from spotify_analysis import analysis, config, data, plots

logger = logging.getLogger(__name__)

# Небольшие платформы выносим на отдельные диаграммы, иначе их столбцы
# не видны на фоне Spotify и YouTube.
SMALL_PLATFORMS = ["Deezer", "AirPlay", "Soundcloud", "Shazam"]
RADIO_PLATFORMS = ["Apple Music", "SiriusXM", "Amazon"]

TABLE_FILES = {
    "top_clean_tracks": "top_10_clean_tracks.xlsx",
    "artist_stats": "artist_track_score_stats.xlsx",
    "platform_leaders": "platform_leaders.xlsx",
}

FIGURE_FILES = {
    "release_year": "tracks_by_release_year.png",
    "top_artists": "top_artists_by_track_count.png",
    "platform_totals": "platform_totals_by_explicit.png",
    "platform_totals_small": "platform_totals_small_platforms.png",
    "platform_totals_radio": "platform_totals_radio_platforms.png",
}


def run_analysis(
    input_path: Path | None = None,
    reports_dir: Path | None = None,
    save_reports: bool = True,
) -> dict[str, pd.DataFrame]:
    """Выполнить анализ и вернуть все построенные таблицы.

    Args:
        input_path: путь к сыровому CSV (по умолчанию — из конфигурации).
        reports_dir: каталог для отчётов (по умолчанию — из конфигурации).
        save_reports: сохранять ли xlsx-таблицы и png-диаграммы.

    Returns:
        Словарь с таблицами: ``top_clean_tracks``, ``artist_stats``,
        ``platform_leaders``, а также рядами для диаграмм.
    """
    figures_dir = (reports_dir or config.REPORTS_DIR) / "figures"
    tables_dir = (reports_dir or config.REPORTS_DIR) / "tables"
    if save_reports:
        figures_dir.mkdir(parents=True, exist_ok=True)
        tables_dir.mkdir(parents=True, exist_ok=True)

    raw = data.load_raw_data(input_path)
    logger.info("Датасет загружен: %d строк, %d колонок", *raw.shape)

    df = data.clean_data(raw)
    logger.info(
        "Данные очищены: пропуски в измерительных колонках заполнены нулями, "
        "типы приведены (даты -> datetime, метрики -> int64)"
    )

    plots.set_plot_style()

    tables: dict[str, pd.DataFrame] = {}
    tables["top_clean_tracks"] = analysis.top_clean_tracks(df)
    tables["artist_stats"] = analysis.artist_track_score_stats(df)
    tables["platform_leaders"] = analysis.platform_leaders(df)
    tables["release_year"] = analysis.tracks_by_release_year(df).to_frame()
    tables["top_artists"] = analysis.top_artists_by_track_count(df).to_frame()
    tables["platform_totals"] = analysis.platform_totals_by_explicit(df)

    figures: dict[str, tuple] = {
        "release_year": plots.plot_tracks_by_release_year(analysis.tracks_by_release_year(df)),
        "top_artists": plots.plot_top_artists(analysis.top_artists_by_track_count(df)),
        "platform_totals": plots.plot_platform_totals_by_explicit(
            tables["platform_totals"], title_suffix="(все платформы)"
        ),
        "platform_totals_small": plots.plot_platform_totals_by_explicit(
            tables["platform_totals"],
            platforms=SMALL_PLATFORMS,
            title_suffix=f"({', '.join(SMALL_PLATFORMS)})",
        ),
        "platform_totals_radio": plots.plot_platform_totals_by_explicit(
            tables["platform_totals"],
            platforms=RADIO_PLATFORMS,
            title_suffix=f"({', '.join(RADIO_PLATFORMS)})",
        ),
    }

    if save_reports:
        for name, filename in TABLE_FILES.items():
            tables[name].to_excel(tables_dir / filename)
            logger.info("Таблица сохранена: %s", tables_dir / filename)
        for name, (fig, _) in figures.items():
            fig.savefig(figures_dir / FIGURE_FILES[name], dpi=300, bbox_inches="tight")
            plt.close(fig)
            logger.info("Диаграмма сохранена: %s", figures_dir / FIGURE_FILES[name])

    return tables


def main(argv: list[str] | None = None) -> None:
    """CLI-точка входа пайплайна."""
    parser = argparse.ArgumentParser(description="Анализ датасета Most Streamed Spotify Songs 2024")
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="путь к сыровому CSV (по умолчанию: data/raw/spotify_most_streamed_2024.csv)",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=None,
        help="каталог для отчётов (по умолчанию: reports/)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
    run_analysis(input_path=args.input, reports_dir=args.reports_dir)
    logger.info("Готово: отчёты в %s", (args.reports_dir or config.REPORTS_DIR))


if __name__ == "__main__":
    main()
