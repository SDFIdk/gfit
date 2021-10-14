from setuptools import (
    setup,
    find_packages,
)


setup(
    name="gfit",
    version="0.2.0",
    description="Geoid Fit Cross Validation (GFIT)",
    url="https://github.com/Kortforsyningen/diveg",
    author="Joachim Mortensen (SDFE, GRF) <joamo@sdfe.dk>",
    author_email="grf@sdfe.dk",
    license="BSD",

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'gfit-cv = gfit.cv:main',
            'gfit-check = gfit.check_output:main',
            'gfit-gather = gfit.gather_output:main',
            'gfit-clean = gfit.clean:main',
        ],
    },
)
