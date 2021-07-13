
import pathlib

import yaml
import pandas as pd

from gfit.util import (
    parse_point_line,
    point_value_fields,
)


def main():
    # Read config file
    with open('config.yaml', encoding='utf-8') as fsock:
        config = yaml.safe_load(fsock)

    # Make sure path exists, before moving on
    output_path = pathlib.Path(config.get('output_path')).absolute()
    if not output_path.is_dir():
        raise SystemExit('No output path')

    # Extract the interpolated value of each excluded point
    fname = config.get('point_interpolated')
    fnames = sorted(output_path.glob(f'**/{fname}'))
    values_raw = []
    for ifname in fnames:
        with ifname.open() as fsock:
            values_raw.append(parse_point_line(fsock.readlines()[0]))

    # Use Pandas to merge the data

    # Interpolated data
    interp = pd.DataFrame(data=values_raw, columns=['id', 'value']).set_index('id')

    # Read original measurements
    rkw = dict(
        # How to use regex as separator/delimiter:
        # https://stackoverflow.com/questions/36790948/pandas-read-csv-indicating-space-delimited#36791314
        sep=r'\s{1,}',    # Read one or more whitespace characters
        engine='python',  # Suppresses 'ParserWarning' about using python engine due to the regex.
        # The rest of the arguments
        names=point_value_fields,
    )
    measured = pd.read_csv(config.get('gps_measurements'), **rkw).set_index('id')

    # We should have an interpolated value for each measurement.
    assert len(interp) == len(measured), f'Number of records must be the same. Got {len(interp)!r} and {len(measured)!r}'

    # Insert interpolated values new column
    measured.loc[interp.index, 'interp'] = interp.value
    # Add additional column with residual
    measured['residual'] = (measured.interp - measured.data1).map(lambda v: round(v, ndigits=6))

    # Make the index column a normal column again
    measured = measured.reset_index('id')
    # Save the gathered data as a file
    measured.to_csv(output_path / config.get('points_gathered'), index=False, sep=';')


if __name__ == '__main__':
    main()
