
import pathlib
import collections as cs

import yaml


def main():
    with open('config.yaml', encoding='utf-8') as fsock:
        config = yaml.safe_load(fsock)

    output_path = pathlib.Path(config.get('output_path')).absolute()
    if not output_path.is_dir():
        raise SystemExit('No output path')

# ---

    # Were there any errors?
    # If so, there will be content in the .err files.
    # Gather these files and store list of nonempty .err files.
    # These indicate what processes went wrong.

    error_files = []
    for stem in ('fitgeoid1', 'gbin', 'geoid'):
        error_files.extend(output_path.glob(f'**/{stem}.err'))

    nonempty = []
    for fname in error_files:
        with open(fname, encoding='utf-8') as f:
            if f.read():
                nonempty.append(fname)

    if len(nonempty) != 0:
        print('There are non-empty error files:')
        print('\n'.join(str(path) for path in nonempty))
        if (answer := input('Delete files?')) and answer.lower() == 'y':
            [path.unlink() for path in nonempty]
    else:
        print(f'No errors (stderr) have been reported in any error-output files.')

# ---

    # How many interpolated-point-data files are there
    # This number should be the same as the number of lines (points) in the original point-data file.

    fname_point = config.get('point_interpolated')
    point_files = sorted(output_path.glob(f'**/{fname_point}'))

    with open(config.get('gps_measurements')) as fsock:
        N_points = len(fsock.readlines())

    N_interp_files = len(point_files)
    print(f'Number of interpolated point-data files ({N_interp_files}) same as number of points ({N_points})? {N_interp_files == N_points}')

# ---

    # How many times does a given point (line) occur in all the working directories?
    # This number should be N - 1 for each line, where N = number of lines in the original data-file.

    fname = config.get('gps_measurements_subset')
    fnames = sorted(output_path.glob(f'**/{fname}'))
    lines = cs.Counter()
    # Each line should be counted the same amount of times, except any trailing empty line.
    for fname in fnames:
        with open(fname) as fsock:
            # Notice the use of splitlines, which removes all new line characters.
            lines.update(fsock.read().splitlines())

    count_set = set(count for (_, count) in lines.items())
    N_fnames = len(fnames)
    print(f'Line occurrences {count_set!r} are all the same? {len(count_set) == 1}')
    print(f'Number of occurrences is N - 1, where N = number of interpolated files {N_fnames} = number of points {N_points}? {list(count_set)[0] == N_fnames - 1 == N_points - 1}')


# ---


if __name__ == '__main__':
    main()
