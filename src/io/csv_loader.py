import pandas as pd
from pathlib import Path

REQUIRED_COLS = {"chart", "chart_date", "rank", "song_name", "artist", "weeks"}

def load_chart_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")
    # tipos básicos
    df["rank"] = df["rank"].astype(int)
    df["weeks"] = df["weeks"].astype(int)
    df["chart_date"] = df["chart_date"].astype(str)
    return df
