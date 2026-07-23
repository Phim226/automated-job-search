from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = ROOT_DIR/"src"/"automated_job_search"
JOB_DATA_DIR = ROOT_DIR/"job_data"

type Disqualifiers = dict[str, list[str] | float]
type Scores = dict[str, dict[str, int]]