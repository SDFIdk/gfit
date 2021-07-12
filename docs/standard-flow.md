<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script> <script>mermaid.initialize({startOnLoad:true});</script>

## Overblik over de eksisterende programmer og deres anvendelse

Følgende er en grafisk illustration af, hvilke filer hvert program bruger og producerer.

<div class="mermaid">
    graph TD
    X(geoid_gravimetric.gri) --> A[fitgeoid1]
    Y(points_measured.n) -->A
    A -->|produces| X2(geoid_fitted.gri)
    A -->|produces| X2a("(other files)")
    X2 -->B[gbin]
    B -->|produces| X3(geoid_fitted.bin)
    X3 --> C[geoid]
    Z(point_position.dat) --> C
    C -->|produces| Z2(point_interpolated_geoid_data.dat)

    style A fill:#f0f1cc
    style B fill:#f0f1cc
    style C fill:#f0f1cc

    style X2a fill:#ddd,stroke:#ccc
</div>

*   `fitgeoid1` tilpasser en gravimetrisk geoide $N_{grav}$ til observerede geoidehøjder $N_{obs}$.
*   `gbin` oversætter geoide-data mellem klar tekst og binært format.
*   `geoid` tager geoide-data i binært format og interpolerer geoide-højden i et givet punkt.

Alle tre programmer kan køres enten interaktivt eller med forprogrammeret input (via `stdin`) efter følgende form:

```
[PROGRAM] < input > output
```

hvor `[PROGRAM]` $\in$ $\{$ `fitgeoid1`, `gbin`, `geoid` $\}$. `input` og `output` er arbitrære filnavne.

`input` sendes til programmet via `stdin` og indeholder parametre og filnavne på input data til det pågældende program i samme rækkefølge, det ville komme i under interaktivt input. `output` overskrives med programmets output til `stdout`.

Endvidere kan programmerne have sideeffekter, som producerede filer (se nedenfor).

### Program: `fitgeoid1`



!!! example "Eksempler"

    === "`input`-eksempel"

        ```
        geoid_gravimetric.gri
        geoid_obs_gps+lev.n
        geoid_fitted.gri
        20 1 1 t
        60.0 0.004
        54 58 7 17 .01 .0166
        ```

    === "`input`-forklaring"

        |           Fil           |                                                 Beskrivelse                                                 |
        |-------------------------|-------------------------------------------------------------------------------------------------------------|
        | `geoid_gravimetric.gri` | Inputfil - geoiden som skal fittes                                                                          |
        | `geoid_obs_gps+lev.n`   | Datafil som geoiden skal fittes til                                                                         |
        | `geoid_fitted.gri`      | Output geoide efter fit                                                                                     |
        | `20 1 1 t`              | Fit parametre: nqmax, itrend, ipred, lsigma Itrend 0=ingen fit, 1= kun bias, 2=plan                         |
        | `60.0 0.004`            | ½-correlation-length    sigma/noise på N(obs) is the smallest std. dev. used when data is given with sigmas |
        | `54 58 7 17 .01 .0166`  | Grid specs lat1 lat2 lon1 lon2 spacing-lat spacing-lon                                                      |

    === "`output`-eksempel"

        ```
        *********************************************************
        *    FITGEOID - GRAVSOFT geoid fitter - vers. OCT11     *
        *********************************************************
        Internal Lambert map projection center:    55.750   12.000

        === Subtraction: Ngps minus geoid grid: ===
        number of prediction points:     156
        within area    54.4949   57.7404    8.1231   15.0013

        grid file information:
        gridlab:    53.5000  58.0000   7.0000  17.0000   0.0100   0.0167  451 601
        selected subgrid:   54.4900  57.7500   8.1167  15.0167
        points: 327 x 415 =  135705, zero values:       0, unknown (9999):       0
        min  max  mean  std.dev.:     31.23     40.69     36.92      2.24

        points predicted:    156,  skipped points:      0
        minimum distance to grid edges for predictions:   28.9 km
        statistics:                     mean   std.dev.   min      max    unknown
        original data             :   38.737    1.430   34.523   40.906       0
        grid interpolation results:   38.419    1.452   34.070   40.625       0
        predicted values output   :    0.318    0.029    0.275    0.479       0

        === Gridding of GPS corrections ===
        minimal and maximal standard deviations of data:      0.00     0.00
        detrending done on data, itrend = 1
        no of trend parameters estimated:  1
        solution:   0.3181E+00
        detrended data (min,max,mean,stddev):    -0.043    0.161    0.000    0.029

        collocation prediction - sqrc0,xhalf(km),rmsn =    0.03  60.00   0.00
        selection: 20 closest points per quadrant

        data organization limits in lambert proj: -139278.  222067. -239869.  191036.
        subrectangles (n,e,total):     7    8   56
        size (km):     51.62    53.86, average pts per rect (rdat):    2.786
        max points in subrects:   14, percentage with no points:  42.9

        predicted:  271051 points
        prediction pts mean std.dev. min max:      0.33     0.03     0.28     0.47
        prediction error values min max:                             0.00     0.03

        === Addition of gridded corrections to geoid file ===
        number of prediction points:  271051
        within area    53.5000   58.0000    7.0000   17.0000

        grid file information:
        gridlab:    53.5000  58.0000   7.0000  17.0000   0.0100   0.0167  451 601
        selected subgrid:   53.5000  58.0000   7.0000  17.0000
        points: 451 x 601 =  271051, zero values:       0, unknown (9999):       0
        min  max  mean  std.dev.:     26.68     40.99     36.30      3.22

        points predicted: 271051,  skipped points:      0
        minimum distance to grid edges for predictions:    0.0 km
        statistics:                     mean   std.dev.   min      max    unknown
        original data             :    0.328    0.028    0.276    0.475       0
        grid interpolation results:   36.300    3.223   26.681   40.990       0
        predicted values output   :   36.628    3.210   26.999   41.309       0

        === Fit of GPS levelling data to fitted geoid ===
        Name of fitted geoid: fg7p_4.gri                                                              
        number of prediction points:     156
        within area    54.4949   57.7404    8.1231   15.0013

        grid file information:
        gridlab:    53.5000  58.0000   7.0000  17.0000   0.0100   0.0167  451 601
        selected subgrid:   54.4900  57.7500   8.1167  15.0167
        points: 327 x 415 =  135705, zero values:       0, unknown (9999):       0
        min  max  mean  std.dev.:     31.55     40.99     37.25      2.22

        points predicted:    156,  skipped points:      0
        minimum distance to grid edges for predictions:   28.9 km
        statistics:                     mean   std.dev.   min      max    unknown
        original data             :   38.737    1.430   34.523   40.906       0
        grid interpolation results:   38.737    1.430   34.524   40.906       0
        predicted values output   :    0.000    0.004   -0.019    0.013       0
        ```

    === "Sideeffekter: Producerede data-filer"

        !!! warning "Bemærk"
        
            Alle filer overskrives ved en ny kørsel af programmet, hvis ikke de ændres/flyttes!
        
        |        Fil        |                                Beskrivelse                                 |
        |-------------------|----------------------------------------------------------------------------|
        | geoid_fitted.gri  | Den nye fitted geoide                                                      |
        | fitgeoid_dif.dat  | Forskel ml. grav geoiden og inputdata $N_{obs}$                            |
        | fitgeoid_dif2.dat | Forskel mellem ny fitted geoide og input data $N_{obs}$                    |
        | fitgeoid_dif.gri  | Forskel ml grav geoiden og den nye fittede geoide                          |
        | fitgeoid_dif.err  | Estimatet på fejlen ved **???** geoidefittet eller prediktering af grid... |

### Program: `gbin`

!!! example "Eksempler"

    === "`input`-eksempel"

        ```
        geoid_fitted.gri
        geoid_fitted.bin
        1
        ```

    === "`input`-forklaring"

        |        Fil         |                              Beskrivelse                               |
        |--------------------|------------------------------------------------------------------------|
        | `geoid_fitted.gri` | Inputfil - geoiden som skal fittes                                     |
        | `geoid_fitted.bin` | Outputfil - Samme data, bare i binørt format, der kan læses af `geoid` |
        | `1`                | Ønsket format - `1` => binært format.                                  |

    === "`output`-eksempel"

        ```
        input: inputfile
               outputfile
               outputformat (1: bin, 2: txt, 3: txt int)
        ---  G B I N  ---
        conversion from text format
        grid label:
           53.500000   58.000000    7.000000   17.000020   0.0100000   0.0166667
        number of points in grid:     451    601   271051
             mean   std.dev.   min     max   unknown/9999
            36.63     3.21    27.00    41.31        0

        ```

    === "Sideeffekter: Producerede data-filer"
        
        |       Fil        |        Beskrivelse        |
        |------------------|---------------------------|
        | geoid_fitted.bin | Binær fil med geoide-data |

### Program: `geoid`

Programmet evaluerer et givet punkt (lokation) ud fra en grid-fil med geoide-højder.

!!! example "Eksempler"

    === "`input`-eksempel"

        ```
        1
        geoid_fitted.bin
        y
        point_excluded.dat
        point_interpolated.dat
        1
        ```

    === "`input`-forklaring"

        |           Fil            |                           Beskrivelse                            |
        |--------------------------|------------------------------------------------------------------|
        | `1`                      | Valgt opgave, programmet skal udføre                             |
        | `geoid_fitted.bin`       | Inputfil - geoiden som skal interpoleres                         |
        | `y`                      | Yes til at anvende punkt-input fra en fil                        |
        | `point_excluded.dat`     | Inputfil - Fil med punkt, der skal interpoleres en værdi for     |
        | `point_interpolated.dat` | Outputfil - Fil med det ønskede punkts interpolerede værdi       |
        | `1`                      | Ønsket format til output-koordinater - `1` => lat, lon (degrees) |

    === "`output`-eksempel"

        ```
           ***************************************************************
           *                                                             *
           *   GEOID - GRAVSOFT geoid interpolation and transformation   *
           *                                                             *
           *   vers. MAR92 (c) RF, Kort- og Matrikelstyrelsen, Denmark   *
           ***************************************************************
         
         Enter task: 1 = interpolate geoid heights
                     2 = ellipsoidal to orthometric heights using geoid
                     3 = orthometric heights to ellipsoidal   -     -
                     4 = geoid heights in different datum ...
         Enter binary geoid file name: CR=/usr3/geo/proj/DATA/nkg89geoid       
         Geoid grid limits and spacing in degrees:
            53.50000    58.00000   7.00000    17.00002     0.01000   0.01667
         Do you wish to input data points from a file? (Y/N or CR=N)
         Enter file name: (CR=geoid.pts) 
         Enter file name for output: (CR=geoid.out) 
         Type of input: 1 = statno, lat, lon (degrees)
                        2 = statno, lat, lon (deg,min,sec)
                        3 = statno, X, Y, Z (meter)
                        4 = statno, N, E (UTM, meter)
         - output coordinates are geographic degrees -
           794721   55.06709414   9.40396933    40.573
         --- number of points interpolated:   1, rejected:   0
         --- outputfile: point_interpolated.dat                                      
        ```

    === "Sideeffekter: Producerede data-filer"
        
        |           Fil            |                        Beskrivelse                         |
        |--------------------------|------------------------------------------------------------|
        | `point_interpolated.dat` | Outputfil - Fil med det ønskede punkts interpolerede værdi |


## Kilder

*   [GRAVSOFT manual](https://ftp.space.dtu.dk/pub/RF/gravsoft_manual2014.pdf)
