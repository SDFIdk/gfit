
from gfit.util import (
    make_point_line,
    make_subsets,
)

from run import (
    load_config,
    get_cwd_info
)


def main():

    config = load_config()

    with open(config.get('gps_measurements')) as fsock:
        lines = [
            stripped
            for line in fsock.readlines()
            if (stripped := line.strip())
        ]
    subsets = make_subsets(lines)

    for (line_index, subset) in subsets.items():
        info = get_cwd_info(line_index=line_index)
        
        # Store the subset of lines to fit to
        with open(info.cwd / config.get('gps_measurements_subset'), 'w+', encoding='ascii') as fsock:
            fsock.write('\n'.join(subset))

        # Store the relevant data from the excluded line
        with open(info.cwd / config.get('point_excluded'), 'w+') as fsock:
            fsock.write(make_point_line(lines[info.line_index]))


if __name__ == '__main__':
    main()

