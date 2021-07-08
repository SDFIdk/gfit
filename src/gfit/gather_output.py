
import pathlib

import yaml
import pandas as pd

from gfit.util import (
    parse_point_line,
    point_value_fields,
)


def main():
    with open('config.yaml', encoding='utf-8') as fsock:
        config = yaml.safe_load(fsock)

    output_path = pathlib.Path(config.get('output_path')).absolute()
    if not output_path.is_dir():
        raise SystemExit('No output path')

    fname = config.get('point_interpolated')
    fnames = sorted(output_path.glob(f'**/{fname}'))
    values_raw = []
    for ifname in fnames:
        with ifname.open() as fsock:
            values_raw.append(parse_point_line(fsock.readlines()[0]))

    interp = pd.DataFrame(data=values_raw, columns=['id', 'value']).set_index('id')
    df = pd.read_csv(config.get('gps_measurements'), sep='\t', names=point_value_fields).set_index('id')

    assert len(interp) == len(df)

    df.loc[interp.index, 'interp'] = interp.value
    df['residual'] = (df.interp - df.data1).map(lambda v: round(v, ndigits=6))
    df = df.reset_index('id')

    df.to_csv(output_path / config.get('points_gathered'), index=False, sep=';')


if __name__ == '__main__':
    main()
