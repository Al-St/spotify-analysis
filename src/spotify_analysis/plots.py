"""Диаграммы анализа. Все функции возвращают (fig, ax) и ничего не сохраняют —
запись в файлы выполняет вызывающий код (пайплайн или ноутбук)."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd

BAR_COLOR = "#4C72B0"
CLEAN_TRACK_COLOR = "#55A868"
EXPLICIT_TRACK_COLOR = "#C44E52"
EXPLICIT_LABELS = {0: "без ограничения (0)", 1: "с ограничением (1)"}


def set_plot_style() -> None:
    """Единый стиль для всех диаграмм проекта."""
    plt.rcParams.update(
        {
            "figure.autolayout": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 13,
            "axes.titlepad": 12,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.alpha": 0.3,
        }
    )


def plot_tracks_by_release_year(yearly_counts: pd.Series) -> tuple[plt.Figure, plt.Axes]:
    """Количество популярных в 2024 году треков по году выпуска."""
    fig, ax = plt.subplots(figsize=(12, 5))
    yearly_counts.plot.bar(ax=ax, color=BAR_COLOR, rot=45)
    ax.set_title("Количество популярных в 2024 году треков по году выпуска")
    ax.set_xlabel("Год выпуска")
    ax.set_ylabel("Число треков")
    return fig, ax


def plot_top_artists(artist_counts: pd.Series) -> tuple[plt.Figure, plt.Axes]:
    """Топ исполнителей по количеству треков в рейтингах 2024 года."""
    fig, ax = plt.subplots(figsize=(10, 5))
    artist_counts.plot.bar(ax=ax, color=BAR_COLOR, rot=30)
    ax.set_title("Топ-10 исполнителей по количеству популярных в 2024 году треков")
    ax.set_xlabel("")
    ax.set_ylabel("Число треков")
    return fig, ax


def plot_platform_totals_by_explicit(
    totals: pd.DataFrame,
    platforms: Sequence[str] | None = None,
    title_suffix: str = "",
) -> tuple[plt.Figure, plt.Axes]:
    """Суммарные показатели платформ раздельно для треков с explicit-флагом 0 и 1.

    ``platforms`` ограничивает набор платформ (например, чтобы мелкие платформы
    не терялись на фоне Spotify), ``title_suffix`` уточняет заголовок.
    """
    data = totals if platforms is None else totals[list(platforms)]

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = pd.Series(0, index=data.index, dtype=float)
    x = [EXPLICIT_LABELS[i] for i in data.index]
    for platform in data.columns:
        values = data[platform].astype(float)
        ax.bar(x, values, bottom=bottom, label=platform)
        bottom = bottom + values

    ax.set_title(
        "Сумма показателей платформ для треков "
        f"без возрастного ограничения и с ним {title_suffix}".strip()
    )
    ax.set_xlabel("Возрастное ограничение")
    ax.set_ylabel("Сумма показателей")
    ax.legend(prop={"size": 8})
    return fig, ax
