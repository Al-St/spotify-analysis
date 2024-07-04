"""Фабрика небольшого синтетического датасета в формате сырого CSV.

Значения задаются поимённо, чтобы тесты не зависели от порядка метрик.
Сюжет синтетики:
  * Track A — «чистый» трек, лидер по большинству метрик;
  * Track B — explicit-трек, обходит всех только по Soundcloud;
  * Track C — «чистый» трек-аутсайдер с пропуском в Apple Music Playlist Count.
"""

from __future__ import annotations

import pandas as pd

from spotify_analysis import config

RAW_COLUMNS = [
    config.TRACK,
    config.ALBUM,
    config.ARTIST,
    config.RELEASE_DATE,
    config.ISRC,
    config.ALL_TIME_RANK,
    config.TRACK_SCORE,
    *config.METRIC_COLUMNS,
    config.EMPTY_COLUMN,
    config.EXPLICIT,
]

_TRACK_A = {
    "Spotify Streams": "1,000",
    "Spotify Playlist Count": "10",
    "Spotify Playlist Reach": "100",
    "Spotify Popularity": "90",
    "YouTube Views": "2,000",
    "YouTube Likes": "200",
    "YouTube Playlist Reach": "30",
    "TikTok Posts": "300",
    "TikTok Likes": "3,000",
    "TikTok Views": "150",
    "Pandora Streams": "50",
    "Pandora Track Stations": "5",
    "Deezer Playlist Count": "1",
    "Deezer Playlist Reach": "7",
    "AirPlay Spins": "70",
    "Apple Music Playlist Count": "500",
    "SiriusXM Spins": "1",
    "Amazon Playlist Count": "700",
    "Soundcloud Streams": "800",
    "Shazam Counts": "9",
}

_TRACK_B = {
    "Spotify Streams": "900",
    "Spotify Playlist Count": "9",
    "Spotify Playlist Reach": "90",
    "Spotify Popularity": "80",
    "YouTube Views": "1,500",
    "YouTube Likes": "150",
    "YouTube Playlist Reach": "20",
    "TikTok Posts": "200",
    "TikTok Likes": "2,000",
    "TikTok Views": "120",
    "Pandora Streams": "40",
    "Pandora Track Stations": "4",
    "Deezer Playlist Count": "2",
    "Deezer Playlist Reach": "6",
    "AirPlay Spins": "40",
    "Apple Music Playlist Count": "400",
    "SiriusXM Spins": "2",
    "Amazon Playlist Count": "600",
    "Soundcloud Streams": "900",
    "Shazam Counts": "8",
}

_TRACK_C = {
    "Spotify Streams": "500",
    "Spotify Playlist Count": "5",
    "Spotify Playlist Reach": "50",
    "Spotify Popularity": "50",
    "YouTube Views": "800",
    "YouTube Likes": "80",
    "YouTube Playlist Reach": "10",
    "TikTok Posts": "100",
    "TikTok Likes": "1,000",
    "TikTok Views": "80",
    "Pandora Streams": "30",
    "Pandora Track Stations": "3",
    "Deezer Playlist Count": "3",
    "Deezer Playlist Reach": "5",
    "AirPlay Spins": "20",
    "Apple Music Playlist Count": None,
    "SiriusXM Spins": "3",
    "Amazon Playlist Count": "500",
    "Soundcloud Streams": "700",
    "Shazam Counts": "7",
}


def make_raw_df() -> pd.DataFrame:
    """Синтетический «сырой» датасет: строки с разделителями тысяч, пропуски,
    пустая колонка TIDAL Popularity — как в настоящем файле с Kaggle."""
    tracks = [
        (
            {
                "Track": "Track A",
                "Album Name": "Album A",
                "Artist": "Artist X",
                "Release Date": "1/5/2024",
                "ISRC": "AAA1",
                "All Time Rank": "1",
                "Track Score": "700.5",
                "Explicit Track": 0,
            },
            _TRACK_A,
        ),
        (
            {
                "Track": "Track B",
                "Album Name": "Album B",
                "Artist": "Artist Y",
                "Release Date": "2/10/2023",
                "ISRC": "BBB2",
                "All Time Rank": "2",
                "Track Score": "600.0",
                "Explicit Track": 1,
            },
            _TRACK_B,
        ),
        (
            {
                "Track": "Track C",
                "Album Name": "Album C",
                "Artist": "Artist X",
                "Release Date": "3/15/2020",
                "ISRC": "CCC3",
                "All Time Rank": "3",
                "Track Score": "500.5",
                "Explicit Track": 0,
            },
            _TRACK_C,
        ),
    ]
    rows = [{**ids, **metrics, config.EMPTY_COLUMN: None} for ids, metrics in tracks]
    return pd.DataFrame(rows, columns=RAW_COLUMNS)
