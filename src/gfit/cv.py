
"""
Leave-one-out geoid fit

Caution:
    With 157 points tested as input, this program starts
    157 parallel processes of the program fitgeoid1.exe
    producing an output of size more than 1.22 GB.

"""

"""
TODO:
    Switch to JSON-format for configuration, if it is easier to use builtin Python functionality.
    Make this a package that can be installed and used in any prompt where its venv is activated.
    Configuration search:
        Use configuration file given at the command line.
        If not present, search for config file in user's home directory.
    Add output directories to configuration file?
    Let everything be set from the command line?

"""

import pathlib
import time
import itertools as it
import multiprocessing as mp

import yaml
from proman import ProcessHandler

from gfit.util import (
    make_subsets,
    input_fitgeoid1,
    input_gbin,
    input_geoid,
    make_point_line,
)


def main():
    with open('config.yaml', encoding='utf-8') as fsock:
        config = yaml.safe_load(fsock)

    # Path for input and output
    output_path = pathlib.Path(config.get('output_path'))
    output_path.mkdir(exist_ok=True)

    # Load all points
    with open(config.get('gps_measurements')) as fsock:
        lines = [
            stripped
            for line in fsock.readlines()
            if (stripped := line.strip())
        ]

    # Make subsets
    subsets = make_subsets(lines)

    input_helper = dict(
        fitgeoid1=input_fitgeoid1(**config),
        gbin=input_gbin(**config),
        geoid=input_geoid(**config),
    )

    # Run the fit program for each subset of points
    handlers = []
    for ix, subset in subsets.items():
        # Run each sub process in a directory (current working
        # directory, CWD) named after the line-number removed.
        line_number = f'{ix + 1:0>3d}'
        cwd = output_path / line_number
        cwd.mkdir(exist_ok=True)

        if all([
            (cwd / name).with_suffix('.done').is_file()
            for name in input_helper
        ]):
            print(f'{line_number} completed - skipping')
            continue

        # Create input for the executable's IO

        # Store the subset of lines to fit to
        with open(cwd / config.get('gps_measurements_subset'), 'w+', encoding='ascii') as fsock:
            fsock.write('\n'.join(subset))

        # Store the relevant data from the excluded line
        with open(cwd / config.get('point_excluded'), 'w+') as fsock:
            fsock.write(make_point_line(lines[ix]))

        # Add handler
        handler = ProcessHandler(cwd.absolute())
        for (input_name, input_content) in input_helper.items():

            if (cwd / input_name).with_suffix('.done').is_file():
                print(f'{line_number} - {input_name} completed - skipping')
                continue

            with open(cwd / f'{input_name}.in', 'w+', encoding='ascii') as fsock:
                fsock.write(input_content)
            handler.add_process(config.get(input_name))

        handlers.append(handler)

    if not handlers:
        raise SystemExit('Nothing to do. Exiting.')

    # Handle execution
    N_handlers = len(handlers)
    # Rather arbitrary, since I am not sure if this works (I am not controlling the processes).
    # But it does limit the maximum number of processes, running at the same time,
    # so it does keep some capacity available for other things.
    N_max = mp.cpu_count()

    # symbols = '_123_'
    # symbols = '_.=¨_'
    # frames = ['⢿', '⣻', '⣽', '⣾', '⣷', '⣯', '⣟', '⡿']
    frames = ['|', '/', '-', '\\']

    for frame in it.cycle(frames):
        for handler in handlers:
            handler.cleanup()

        # output = ''.join(symbols[handler.index] for handler in handlers)
        # print(f'\r{output}', end='', flush=True)
        N_completed = sum(handler.completed for handler in handlers)
        print(f'\rCompleted {N_completed: >3d} scenarios out of {N_handlers: >3d} ({N_completed / N_handlers: >4.0%}) {frame}', end='', flush=True)
        if N_completed == N_handlers:
            break

        N_running = sum(handler.active for handler in handlers)
        if N_running >= N_max:
            continue

        available = [handler for handler in handlers if handler.ready]
        if available:
            available[0].run_next()

        time.sleep(.25)

    # Final cleanup
    for handler in handlers:
        handler.cleanup()


    print('\n[DONE]')


if __name__ == '__main__':
    main()

