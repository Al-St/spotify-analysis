"""Центральная конфигурация проекта: пути, константы датасета и группы колонок.

Все обращения к колонкам датасета в коде идут через имена, объявленные здесь.
Это защищает анализ от тихих поломок при изменении порядка колонок в CSV.
"""

from __future__ import annotations

from pathlib import Path

# --- Пути -----------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "spotify_most_streamed_2024.csv"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"

# --- Чтение данных ---------------------------------------------------------

# Файл с Kaggle — не валидный UTF-8: часть символов уже безвозвратно заменена
# на U+FFFD, часть осталась «сырыми» байтами. latin-1 читает файл без ошибок
# и сохраняет байты как есть; правка кодировки на стороне датасета невозможна.
RAW_CSV_ENCODING = "latin-1"

# --- Колонки датасета ------------------------------------------------------

TRACK = "Track"
ALBUM = "Album Name"
ARTIST = "Artist"
RELEASE_DATE = "Release Date"
ISRC = "ISRC"
ALL_TIME_RANK = "All Time Rank"
TRACK_SCORE = "Track Score"
EXPLICIT = "Explicit Track"

# Колонка пуста во всём датасете (4600 из 4600 значений отсутствуют).
EMPTY_COLUMN = "TIDAL Popularity"

# Идентификационные (неизмерительные) колонки таблицы лидеров.
ID_COLUMNS = [TRACK, ALBUM, ARTIST, RELEASE_DATE, ISRC]

# Текстовые колонки, приводимые к типу string при очистке.
TEXT_COLUMNS = [TRACK, ALBUM, ARTIST, ISRC]

# Показатели, сгруппированные по платформам. Порядок словаря определяет
# порядок платформ в таблице лидеров и на диаграммах.
PLATFORM_METRICS: dict[str, list[str]] = {
    "Spotify": [
        "Spotify Streams",
        "Spotify Playlist Count",
        "Spotify Playlist Reach",
        "Spotify Popularity",
    ],
    "YouTube": [
        "YouTube Views",
        "YouTube Likes",
        "YouTube Playlist Reach",
    ],
    "TikTok": [
        "TikTok Posts",
        "TikTok Likes",
        "TikTok Views",
    ],
    "Pandora": [
        "Pandora Streams",
        "Pandora Track Stations",
    ],
    "Deezer": [
        "Deezer Playlist Count",
        "Deezer Playlist Reach",
    ],
    "AirPlay": ["AirPlay Spins"],
    "Apple Music": ["Apple Music Playlist Count"],
    "SiriusXM": ["SiriusXM Spins"],
    "Amazon": ["Amazon Playlist Count"],
    "Soundcloud": ["Soundcloud Streams"],
    "Shazam": ["Shazam Counts"],
}

# Плоский список всех измерительных колонок (порядок = порядок платформ).
METRIC_COLUMNS: list[str] = [column for columns in PLATFORM_METRICS.values() for column in columns]

# --- Бизнес-правила ---------------------------------------------------------

# Заказчику нужны треки без возрастного ограничения, поэтому в таблице лидеров
# по Soundcloud (платформа, где доминируют explicit-треки) лидер выбирается
# только среди «чистых» треков.
EXCLUDE_EXPLICIT_METRICS = {"Soundcloud Streams"}

# Ручные исправления таблицы лидеров: (метрика, колонка) -> значение.
# В опубликованном Kaggle-файле у самого часто постящегося в TikTok звука
# (Laxed (Siren Beat), Jawsh 685) имя трека повреждено кодировкой
# («Laxed ï¿½ï¿½ï¿½ Sire»), хотя ISRC и альбом корректны; у лидера YouTube
# «Baby Shark» имя альбома также повреждено. ISRC остаётся источником истины.
LEADER_OVERRIDES: dict[tuple[str, str], str] = {
    ("TikTok Posts", TRACK): "Laxed (Siren Beat)",
    ("YouTube Views", ALBUM): "-",
}
