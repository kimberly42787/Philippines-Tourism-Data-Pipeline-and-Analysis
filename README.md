# Philippines-Tourism-Data-Pipeline-and-Analysis


flowchart LR
    A[Tourism Reports<br/>(PDFs 2015–2025)] --> B[Python PDF Extraction]
    B --> C[Data Cleaning & Standardization]
    C --> D[Relational Database]
    D --> E[Analytical Metrics]
    E --> F[Visualization & Dashboard]

    C --> C1[Country name normalization]
    C --> C2[Missing value handling]
    C --> C3[Data validation]

    E --> E1[Recovery Index]
    E --> E2[YoY Growth]
    E --> E3[Country Rankings]

    F --> F1[Python EDA]
    F --> F2[Tableau Dashboard]
