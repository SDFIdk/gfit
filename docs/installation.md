
## Krav og forudsætninger

*   [`conda`](https://docs.conda.io/en/latest/miniconda.html) | [repo](https://repo.anaconda.com/miniconda/)
*   [`git`](https://git-scm.com/)
*   Programmer fra GRAVSOFT-pakken: `fitgeoid1.exe`, `gbin.exe` and `geoid.exe`

## Skridt

*   Åbn en Anaconda Prompt
*   Gå til en mappe, hvor du vil have `gfit` liggende.

    Eksempel:
    
    ```
    > c:
    > cd /
    c:\>
    ```

*   Hent koden:

    Eksempel:
    
    ```
    c:\> git clone https://github.com/Kortforsyningen/gfit
    c:\> cd gfit
    ```

*   Installér `gfit`:

    Eksempel:
    
    ```
    c:\gfit> conda env create --file environment.yml
    # wait / agree to install
    c:\gfit> python -m pip install -r requirements.txt
    # Install in developer mode (makes possible to fetch minor updates without needing to re-install)
    c:\gfit> python -m pip install -e .
    ```

