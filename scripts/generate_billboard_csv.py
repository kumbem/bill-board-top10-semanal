import argparse
from datetime import datetime
import pandas as pd
import billboard

from src.config import RAW_DIR, DEFAULT_CSV_PATH
from src.utils.dates import iter_week_dates


def fetch_week(chart_name: str, date_str: str, top_n: int) -> list[dict]:
    chart = billboard.ChartData(chart_name, date=date_str)
    rows = []
    for song in chart[:top_n]:
        rows.append({
            "chart": chart_name,
            "chart_date": date_str,
            "rank": int(song.rank),
            "song_name": song.title,
            "artist": song.artist,
            "weeks": int(song.weeks),
            "last_pos": int(song.lastPos) if song.lastPos not in ("", None) else None,
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", default="hot-100", choices=["hot-100", "billboard-200"])
    parser.add_argument("--start", default="2012-01-07")  # semana inicial segura
    parser.add_argument("--end", default=datetime.today().strftime("%Y-%m-%d"))
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--out", default=str(DEFAULT_CSV_PATH))
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    start_dt = datetime.strptime(args.start, "%Y-%m-%d")
    end_dt = datetime.strptime(args.end, "%Y-%m-%d")

    all_rows = []
    for dt in iter_week_dates(start_dt, end_dt):
        date_str = dt.strftime("%Y-%m-%d")
        print(f"Fetching {args.chart} @ {date_str}...")
        try:
            all_rows.extend(fetch_week(args.chart, date_str, args.top))
        except Exception as e:
            # Em projetos reais: log + retry/backoff; aqui só registra e segue
            print(f"  WARN: failed at {date_str}: {e}")

    df = pd.DataFrame(all_rows)
    df.to_csv(args.out, index=False, encoding="utf-8")
    print(f"Saved CSV -> {args.out} ({len(df)} rows)")


if __name__ == "__main__":
    main()
