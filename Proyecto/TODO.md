# TODO del proyecto TEL252

Firmas basadas en hash frente a ECDSA. La presentación es el **lun 30-nov o el mié 2-dic**; el día lo asigna la profesora. Mientras tanto, preparamos para el lunes.

| Rol | Persona | Qué le toca |
|---|---|---|
| P1 | Bastián Reyes | Código base: Lamport, WOTS, ataque y demo |
| P2 | Josué Leiva | Merkle, mediciones y gráficos |
| P3 | Sebastián Moya | Marco teórico y diapositivas |
| P4 | Cristian Pizarro | Informe y coordinación |

Actualizado: 26-nov.

## Ya hecho
- [x] Repartir roles
- [x] Inscribir el equipo y el proyecto, y responder la encuesta
- [x] Crear el repo (`Proyecto/` reúne todo: código, informe y presentación)
- [x] Merkle h=4 con rechazo de índice usado (`codigo/merkle_wots.py`) (P2)
- [x] ECDSA P-256 de referencia (P2)
- [x] Benchmark con N = 10 000 repeticiones (no 100), tablas y 2 gráficos (`codigo/bench.ipynb`, `codigo/resultados.json`) (P2)
- [x] Resultados del informe: Tablas 1 y 2 y Figura 1 (P2)
- [x] Análisis: contraste con la hipótesis (las 4 partes se cumplen), predicción frente a medición y variabilidad (P2)
- [x] PoC de Merkle: 16 firmas, mensaje alterado, firma de otro árbol y firma #17 rechazada (P2)
- [x] Borrador de la presentación Beamer (`presentacion/main.tex`, 13 láminas)

## Pendiente

### P1: Bastián
- [ ] Lamport con sus 3 pruebas (firma válida, mensaje alterado, otra clave)
- [ ] WOTS w = 4, 16 y 256 con sus 3 pruebas. Ya existe en `codigo/merkle_wots.py`: reutilizarlo o validarlo, no duplicarlo
- [ ] Ataque a Lamport con k = 6 firmas: bits fijos e intentos observados frente a los esperados (≈ 2^8)
- [ ] `demo.py` para el video
- [ ] Informe: párrafo "Prueba de concepto" (Lamport, WOTS y ataque) y la "Firma medida" de Lamport en la Tabla 1
- [ ] Código nuevo en `codigo/`, importando `H` de `merkle_wots.py` (sirve como `common.py`)

### P3: Seba
- [ ] Revisar y recortar el marco teórico
- [ ] Confirmar en FIPS 205 los tamaños de firma del nivel de 128 bits (marca en rojo en el informe)
- [ ] Revisar y ajustar el borrador de las diapositivas (`presentacion/main.tex`)

### P4: Cristian
- [ ] Dudas para Berioska: si la portada, las referencias y el anexo cuentan en las 7 páginas (hoy el PDF tiene 9 con portada e índices); si vale usar una librería para ECDSA; dónde publicar el video
- [ ] Conseguir un grupo para la retroalimentación cruzada, y el anexo con la retroalimentación dada y recibida
- [ ] Revisar la introducción y la metodología
- [ ] Nombre del equipo y Roles USM de Seba, Cristian y Bastián (portada del informe)
- [ ] Revisión final y PDF de entrega (`\borradorfalse`)

### P2 y P4
- [ ] Análisis: "Limitaciones y contexto" (migración del NIST, tamaño frente a SLH-DSA)
- [ ] Conclusión de 3 a 5 frases (falta el resultado del ataque a Lamport)

### Video y presentación
- [ ] Grabar el video de 5 min (P1 o P2)
- [ ] Publicar el video y poner el link en `\urlvideo` (informe) y en la lámina del video (P4)
- [ ] Poner en la lámina del video una miniatura clickeable que apunte a YouTube o al archivo local (P2, cuando exista el video)
- [ ] Ensayo de 15 min: intro de 3 a 5 min, video de 5 min, y conclusiones con preguntas en máximo 7 min (todos)

## Compilar

Todo se compila con `latexmk` (pdflatex más biber). En code-server, LaTeX Workshop lo hace al guardar.

```bash
cd Proyecto/informe-tel252 && latexmk -pdf main.tex
cd Proyecto/presentacion   && latexmk -pdf main.tex
```

- **Modo borrador:** el informe y la presentación tienen `\borradortrue`. Con eso, cada `\pend{...}` se ve en **rojo** y marca lo que falta. Para entregar, cambien a `\borradorfalse` en los dos `main.tex` (informe, línea ~20; presentación, en el preámbulo). Antes de entregar, busquen que no quede ningún `\pend{` con contenido real.
- **Figuras:** las genera `codigo/bench.ipynb` directo en `informe-tel252/figuras/`, y la presentación las toma de ahí.
- **Archivos generados:** los auxiliares y los `main.pdf` están en `.gitignore`. No los suban.
- **Git:** antes de editar, hagan `git pull`. Hagan commits chicos para no pisarse.
