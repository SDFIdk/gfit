<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script> <script>mermaid.initialize({startOnLoad:true});</script>

# Automatiserings-opsætningen

Følgende er en illustration af, hvad `gfit-cv` og `gfit-gather` hver især gør for at producere det endelige resultat af krydsvalideringen.

<div class="mermaid">
    flowchart TD
        subgraph CV [Leave one point out at the time for NNN points]
            direction TB
            I(points_measured.n) --> Q[gfit-cv]
            Q -->|Remove line NNN| Y_(points_measured_excluding_line_NNN.n)
            Q -->|Use position from line NNN| Z_(point_position_from_line_NNN.dat)
        end
        X_(geoid_gravimetric.gri) -->|unchanged| X
        Y_ --> Y
        Z_ --> Z
        subgraph STANDARD [Work directory for point NNN]
            direction TB
            X(geoid_gravimetric.gri) --> A[fitgeoid1]
            Y(points_measured.n) --> A
            A -->|produces| X2(geoid_fitted.gri)
            A -->|produces| X2a("(other files)")
            X2 -->B[gbin]
            B -->|produces| X3(geoid_fitted.bin)
            X3 --> C[geoid]
            Z(point_position.dat) --> C
            C -->|produces| Z2(point_interpolated_geoid_data.dat)
        end
        subgraph GATHER [Combine interpolated point values with corresponding measurements]
            direction TB
            Z2 --> Z2_NNN(NNN)
            Z2_negN(...) --> W[gfit-gather]
            Z2_neg2(NNN - 2) --> W
            Z2_neg1(NNN - 1) --> W
            Z2_NNN(NNN) --> W
            Z2_pos1(NNN + 1) --> W
            Z2_pos2(NNN + 2) --> W
            Z2_posN(...) --> W
            W --> Z2_(points_measured_gathered.csv)
        end

    style A fill:#f0f1cc,stroke:#ccc
    style B fill:#f0f1cc,stroke:#ccc
    style C fill:#f0f1cc,stroke:#ccc

    style Q fill:#f0f1cc,stroke:#ccc
    style W fill:#f0f1cc,stroke:#ccc

    style CV fill:#fcfcfc,stroke:#ddd
    style GATHER fill:#fcfcfc,stroke:#ddd
    style STANDARD fill:#fcfcfc,stroke:#ddd
</div>

*   `gfit-cv`