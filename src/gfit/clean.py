
"""
Clean generated files from the output path.

"""

import pathlib

import yaml


def answered_yes(question):
    return input(f'{question} [y/N]').lower() == 'y'


def main():
    with open('config.yaml', encoding='utf-8') as fsock:
        config = yaml.safe_load(fsock)

    output_path = pathlib.Path(config.get('output_path')).absolute()
    if not output_path.is_dir():
        raise SystemExit('No output path')

    extensions = ('.in', '.out', '.err', '.done')
    fnames = []
    for ext in extensions:
        if answered_yes(f'Clean up files ending with {ext!r}?'):
            fnames.extend(output_path.glob(f'**/*{ext}'))

    for fname in fnames:
        print(f'Deleting {fname=}')
        fname.unlink()


if __name__ == '__main__':
    main()
