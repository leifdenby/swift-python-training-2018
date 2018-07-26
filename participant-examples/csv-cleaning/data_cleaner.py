
# coding: utf-8

import re
import pandas as pd

RE_PATTERN = '\d+-\d+-\d+'

def find_date_position(s):
    matches = list(re.finditer(RE_PATTERN, s))
    return matches[0].start()

def cleanup_line(line):
    date_posn = find_date_position(line)
    date, rain_amount, lat, lon = line[date_posn:].split(',')

    comma_posn = line.index(',')

    station_name = line[:comma_posn]
    location = line[comma_posn+1:date_posn-1]

    return (station_name, location, date, rain_amount, lat, lon)

def main(filename_in):
    filename_out = filename_in.replace(".csv", ".cleaned.csv")
    text = open(filename_in).read()

    lines = text.split('\n')

    header = lines[0]

    header_items = header.split(',')

    for (n, line) in enumerate(lines):
        num_parts = len(line.split(','))

    cleaned_lines = []

    for line in lines[1:]:
        cleaned_lines.append(cleanup_line(line))

    df = pd.DataFrame(data=cleaned_lines, columns=header_items)
    df.to_csv(filename_out)

    print("Wrote output to {}".format(filename_out))

if __name__ == '__main__':
    import argparse

    argparser = argparse.ArgumentParser("For cleaning obs data")
    argparser.add_argument('filename_in', type=str)

    args = argparser.parse_args()

    main(args.filename_in)
