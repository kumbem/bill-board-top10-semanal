from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SAMPLES_DIR = DATA_DIR / "samples"

DEFAULT_CSV_PATH = RAW_DIR / "billboard_hot100_2012_present.csv"
