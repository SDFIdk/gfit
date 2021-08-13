import itertools as it
import pathlib
import subprocess
import sys
import time
from dataclasses import dataclass

import yaml

from gfit.util import (
    input_fitgeoid1,
    input_gbin,
    input_geoid,
    make_point_line,
    make_subsets,
)


infile_content = dict(
    fitgeoid1=input_fitgeoid1,
    gbin=input_gbin,
    geoid=input_geoid,
)



root = pathlib.Path(__file__).absolute().parent
output_path = root / '__testing__'
output_path.mkdir(exist_ok=True)


def load_config():
    config_path = root / 'config.yaml'
    assert config_path.is_file(), f'Config file path {config_path!r} does not exist.'
    with open(config_path) as fsock:
        return yaml.safe_load(fsock)


def get_cwd_info(*, line_number: int = None, line_index: int = None) -> 'CWDInfo':
    if line_number is not None:
        assert line_number > 0, f'Line numbers can not be zero or negative. Got {line_number!r}'
        line_index = line_number - 1
    else:
        assert line_index >= 0, f'Line index can not be negative. Got {line_index!r}'
        line_number = line_index + 1

    line_name = f'{line_number:03d}'
    cwd = output_path / line_name
    cwd.mkdir(exist_ok=True)
    return type('CWDInfo', (), dict(
            line_index=line_index,
            line_number=line_number,
            line_name=line_name,
            cwd=cwd,
        )
    )


def main():

    try:
        line_number, *programs = sys.argv[1:]
        line_number = int(line_number)
    except Exception as e:
        raise SystemExit(e)

    animation = it.cycle('|/-\\')
    info = get_cwd_info(line_number=line_number)
    config = load_config()

    print(f'Running programs {programs!r} for line {info.line_number!r}')

    for program in programs:
        assert program in infile_content, f'{program!r} not in {set(infile_content.keys())!r}.'

        fname_infile = info.cwd / f'{program}.in'
        fname_outfile = info.cwd / f'{program}.out'
        fname_errfile = info.cwd / f'{program}.err'

        with open(fname_infile, 'w+') as infile:
            infile.write(infile_content.get(program)(**config))

        # process
        with open(fname_infile) as infile, open(fname_outfile, 'w+') as outfile, open(fname_errfile, 'w+') as errfile:
            p = subprocess.Popen(
                config.get(program),
                stdin=infile,
                stdout=outfile,
                stderr=errfile,
                cwd=info.cwd,
            )

            while p.poll() is None:
                print(f'\r{program} working on line {info.line_number} {next(animation)}', end=' ', flush=True)
                time.sleep(.25)
        print(f'\n{program} [DONE]')


if __name__ == '__main__':
    main()
