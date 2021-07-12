
Data kommer fra to kilder:

|         Fil         |                               Beskrivelse                               | Kilde |
|---------------------|-------------------------------------------------------------------------|-------|
| `gravgeoid2021.gri` | Gravimetrisk geoide i GRAVSOFT-format (ASCII)                           | **?** |
| `gpslev_*.n`        | Forskellige versioner af SDFEs GNSS/NIV-højder ($N_{obs}$) med $\sigma$ | SDFE  |


De observerede geoidehøjder $N_{obs}$ er baseret på nivellement (i DVR90) $H_{niv}$ og GNSS observationer $N_{ellip}$ af ellipsoidehøjden:

$$
\begin{equation}
\displaylines{N_{obs} = h_{ellip} – H_{niv} \\ e = N_{obs} – N_{grav} \\ e = e_{trend} + e'}
\end{equation}
$$

<!--
$$
\begin{align}
N_{obs} = h_{ellip} – H_{niv} \\
e = N_{obs} – N_{grav} \\
e = e_{trend} + e'
\end{align}
$$
-->

Bias er ca. $0.317$ m

$e'$ fittes med collocation (kriging) vha. programmet `geogrid`.
