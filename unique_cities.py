import argparse
import pandas as pd
from typing import Optional


def find_ship_to_city_column(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if c.strip().lower() == 'ship to city':
            return c
    for c in df.columns:
        low = c.lower()
        if 'ship to' in low and 'city' in low:
            return c
    for c in df.columns:
        low = c.lower()
        if 'ship' in low and 'city' in low:
            return c
    return None


def main():
    parser = argparse.ArgumentParser(description='Print unique values from the "Ship To City" column in Test.csv')
    parser.add_argument('--input', '-i', default='Test.csv', help='CSV input file')
    parser.add_argument('--output', '-o', help='Optional output file to save unique values')
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    col = find_ship_to_city_column(df)
    if col is None:
        print('No "Ship To City" column found. Available columns:')
        for c in df.columns:
            print('-', c)
        return

    uniques = sorted(pd.Series(df[col].dropna().unique()).tolist())
    for v in uniques:
        print(v)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            for v in uniques:
                f.write(f"{v}\n")


if __name__ == '__main__':
    main()
