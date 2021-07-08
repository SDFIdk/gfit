# Geoid Fit Cross Validation (GFIT)

by [Joachim Mortensen](https://github.com/xidus)

## Installation

Requirements:

*   A conda environment (miniconda) installed.
*   Git installed.
*   Necessary binary packages from GRAVSOFT: `fitgeoid1.exe`, `gbin.exe` and `geoid.exe`

Steps:

*   Open an Anaconda Prompt
*   Change directory to where you keep git-repositories.

    Example:
    
    ```
    > c:
    > cd /
    c:\>
    ```

*   Clone the repository:

    Example:
    
    ```
    c:\> git clone https://github.com/Kortforsyningen/gfit
    c:\> cd gfit
    ```

*   Install `gfit`:

    Example:
    
    ```
    c:\gfit> conda env create --file environment.yml
    # wait / agree to install
    c:\gfit> python -m pip install -r requirements.txt
    # Install in developer mode (makes possible to fetch minor updates without needing to re-install)
    c:\gfit> python -m pip install -e .
    ```

## Running

*   Activate the conda environment: `conda activate gfit`
*   Copy `example/config.yaml` to where you want to run the commands from. (Change directory to this location before executing the commands.)
*   Edit your own version of `config.yaml`, so that the paths to the data, the executables and the output_path are set to something useful.
*   Run the commands.

### Command: `gfit-cv`

This command is the work horse of the tool. for each point in the `.n` file wth GPS measurements, it creates a work directory containing input and output for fitgeoid1, gbin and geoid. In each work directory one point is excluded from the list of points used for the fit. This point's location is then used to get the interpolated value of the geoid (to be gathered later).

First time the program is run, you may see something like this.

```
gfit-cv
Completed 4 of 157 processes ( 3%) - /
```

After running each separate process (fitgeoid1, gbin or geoid) for any point, the program creates a `.done` file (empty dummy file) named after the process, e.g. `fitgeoid.done`.

This file is created to avoid starting over, if you need to run `gfit-cv` more than once due to an unforeseen error or other (more on this below).

Running the command, when some processes were unfinished:

```
gfit-cv
001 completed - skipping
Completed 1 of 2 processes ( 50%) - /
```

Running the command, when all processes are finished:

```
gfit-cv
001 completed - skipping
(...)
157 completed - skipping
Nothing to do. Exiting.
```

### Command: `gfit-check`

This is a command for checking the output quality. It checks assumptions about the input files (the point-lists in the .n files) and makes sure the correct amount of files were created.

Running the command, you, hopefully, see the following. Otherwise, you need to examine the input (or the code).

```
gfit-check
No errors (stderr) have been reported in any error-output files.
Number of interpolated point-data files (157) same as number of points (157)? True
Line occurrences {156} are all the same? True
Number of occurrences is N - 1, where N = number of interpolated files 157 = number of points 157? T
```

### Command: `gfit-gather`

This command gathers all the interpolated fit values at the location of the excluded points and assemples them in a separate column in a copy of the original point file.

```
gfit-gather
# no output
```

You will find the output file in the root of `output_path`.


### Command: `gfit-clean`

This command lets you, simply, delete all files with the pre-defined extensions.

```
gfit-clean.exe
Clean up files ending with '.in'? [y/N]
Clean up files ending with '.out'? [y/N]
Clean up files ending with '.err'? [y/N]
Clean up files ending with '.done'? [y/N]
```

So far it used to clean everything, but may be edited to do more.

Or you may create your own cleanup script based on how this module was written:)

---
