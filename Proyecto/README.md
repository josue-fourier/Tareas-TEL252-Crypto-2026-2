# Proyecto TEL252: firmas digitales basadas en hash

```
Proyecto/
├── informe-tel252/      Informe LaTeX (main.tex, referencias.bib)
├── presentacion/        Beamer de la presentación (usa las figuras del informe)
│   └── figuras/         PDF de las figuras (los genera codigo/bench.ipynb)
└── codigo/
    ├── merkle_wots.py   H (SHA-256), chain, WOTS y MerkleTree: importar desde aquí, no copiar
    ├── bench.ipynb      Benchmark vs ECDSA P-256, PoC de Merkle y gráficos
    └── resultados.json  Medias y desviaciones de la última corrida (N=10000)
```

- Compilar el informe: `latexmk -pdf main.tex` dentro de `informe-tel252/`.
- Código nuevo (Lamport, ataque, etc.): agregar módulos en `codigo/` y reutilizar `H` de `merkle_wots.py`.
- `bench.ipynb` se ejecuta desde `codigo/` (ahí encuentra `merkle_wots.py`); con N=10000 tarda ~8 min.
