
import pathlib
import collections as cs
import re

TAB = re.compile(r'\s+')


def make_subsets(lines):
    """
    Create subset for each point in which that point is left out.

    """
    subsets = dict()
    for ix in range(len(lines)):
        if ix == 0:
            subsets[ix] = lines[1:]
            continue
        if ix == len(lines) - 1:
            subsets[ix] = lines[:-1]
            continue
        subsets[ix] = lines[:ix] + lines[ix + 1:]

    # Check assumptions about the state so far
    N_lines = len(lines)
    N_lines_subsets = set(len(subset) for subset in subsets.values())
    assert len(subsets) == N_lines
    assert len(N_lines_subsets) == 1
    assert N_lines_subsets == {N_lines - 1}

    return subsets


def add_infix(fname, infix):
    fname = pathlib.Path(fname)
    return f'{fname.stem}_{infix}{fname.suffix}'


def input_fitgeoid1(geoid_gravimetric, gps_measurements_subset, geoid_fitted, **kwargs):
    return f"""\
{geoid_gravimetric}
{gps_measurements_subset}
{geoid_fitted}
20 1 1 t
60.0 0.004
53.50 58.00 7.00 17.000020  0.010 0.0166667
"""

def input_gbin(geoid_fitted, geoid_fitted_bin, **kwargs):
    return f"""\
{geoid_fitted}
{geoid_fitted_bin}
1
"""


def input_geoid(geoid_fitted_bin, point_excluded, point_interpolated, **kwargs):
    return f"""\
1
{geoid_fitted_bin}
y
{point_excluded}
{point_interpolated}
1
"""

point_value_fields = ['id', 'lat', 'lon', 'h', 'data1', 'data2']
PointValues = cs.namedtuple('PointValues', point_value_fields)
"Point data format, GRAVSOFT manual, §6.2"


def make_point_line(line):
    replaced = TAB.sub(' ', line).split(' ')
    values = PointValues(*replaced)
    return f'{values.id}\t{values.lat}\t{values.lon}\n'


def parse_point_line(line):
    values = [stripped for raw in line.strip().split(' ') if (stripped := raw.strip()) != '']
    return int(values[0]), float(values[-1])
