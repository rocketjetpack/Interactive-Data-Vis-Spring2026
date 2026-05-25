"""
This script adds an is_night flag to every tornado record using sun elevation
at time of touchdown and location. It also reduces the column count.
"""

import pandas as pd
from datetime import datetime, timezone, timedelta
from astral import Observer
from astral.sun import elevation

INPUT_CSV = "../data/tornadoes/1950-2025_actual_tornadoes.csv"
OUTPUT_CSV = "../data/tornadoes/tornadoes_with_night_flag.csv"
NIGHT_THRESHOLD_DEG = -6 # Astronomical twilight
CST = timezone(timedelta(hours=-6))

def cst_to_utc(date_str: str, time_str: str) -> datetime:
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    return naive.replace(tzinfo=CST).astimezone(timezone.utc)

def is_night(lat: float, lon: float, when_utc: datetime, threshold_deg: float = NIGHT_THRESHOLD_DEG) -> bool:
    observer = Observer(latitude=lat, longitude=lon)
    sun_elev = elevation(observer, when_utc)
    return sun_elev < threshold_deg

def load_and_filter(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    n0 = len(df)
    df = df[df.tz == 3] # Only consider tornadoes with known timezone (CST)
    n1 = len(df)
    df = df[df["slat"].notna() & df["slon"].notna() & df["date"].notna() & df["time"].notna()]
    n2 = len(df)
    df = df[(df.slat > 23) & (df.slat < 50) & (df.slon > -125) & (df.slon < -65)] # Only consider tornadoes in continental US
    n3 = len(df)
    print(f"loaded {n0:,}  →  tz=3: {n1:,}  →  has coords: {n2:,}  →  CONUS: {n3:,}")
    return df

def classify(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["datetime_utc"] = [cst_to_utc(d,t) for d, t in zip(df["date"], df["time"])]
    df["is_night"] = [
        is_night(lat, lon, when) for lat,lon,when in zip(df["slat"], df["slon"], df["datetime_utc"])
    ]
    return df

if __name__ == "__main__":
    df = load_and_filter(INPUT_CSV)
    df = classify(df)
    print(df[["yr", "date", "time", "slat", "slon", "is_night"]].head())
    print(f"Night tornadoes: {df['is_night'].sum()} / {len(df)}")

    out = df[["yr", "date", "time", "stf", "f1", "slat", "slon", "is_night", "mag", "inj", "fat", "st"]].sort_values(["date", "time"])
    out["is_night"] = out["is_night"].astype(int)
    out.to_csv(OUTPUT_CSV, index=False)
    print(f"wrote {len(out):,} rows to {OUTPUT_CSV}")