# Actividad 1: Distribución de Poisson - Análisis de Radiación Natural

## Descripción

Este proyecto contiene el análisis completo de datos de radiación natural capturados con un contador Geiger remoto, como parte de la Actividad 1 del curso de Física Experimental III.

El objetivo es verificar si los eventos de detección de radiación natural siguen una **distribución de Poisson** y comparar datos experimentales con simulaciones y predicciones teóricas.

---

## Contenido del Directorio

```
distribuciones/
│
├── datosGeigerRadNatural_20251126.txt          # Datos crudos del contador Geiger
├── Actividad1_Poisson.ipynb                    # Notebook con análisis completo
├── Reporte_Actividad1_Poisson.tex              # Documento LaTeX del reporte
├── README_Actividad1.md                        # Este archivo
│
├── Archivos generados por el notebook:
├── datos_experimentales_limpios.txt            # Datos procesados (sin outliers)
├── datos_simulados_poisson.txt                 # Datos simulados con Poisson
├── resumen_resultados.csv                      # Tabla resumen en CSV
├── resumen_resultados.tex                      # Tabla resumen en LaTeX
│
└── Gráficos generados:
    ├── boxplot_outliers.png                    # Análisis de outliers
    ├── comparacion_series_temporales.png       # Series temporales
    ├── analisis_residuos.png                   # Residuos
    └── histogramas_poisson.png                 # Histogramas vs teórica
```

---

## Datos Experimentales

### Información de la Toma de Datos

- **Fuente**: Contador Geiger remoto en línea
- **URL**: https://luramire.github.io/GeigerCounter.io
- **Fecha**: 26 de noviembre de 2025
- **Duración**: 30 minutos
- **Intervalo de muestreo**: 10 segundos
- **Tipo de radiación**: Radiación natural (de fondo)

### Formato de Datos

El archivo `datosGeigerRadNatural_20251126.txt` contiene:
- **Cuentas acumuladas** de partículas detectadas
- Se calcula `Δn = n_{i+1} - n_i` para obtener cuentas por intervalo
- Incluye mensajes del sistema que deben ser filtrados

---

## Análisis Realizado

### 1. Detección de Outliers

**Método**: Criterio de cuartiles (IQR - Interquartile Range)

Un dato es considerado atípico si:
```
x < Q₁ - 1.5 × IQR   o   x > Q₃ + 1.5 × IQR
```

donde `IQR = Q₃ - Q₁`

### 2. Distribución de Poisson

La distribución de Poisson modela eventos discretos aleatorios:

```
P(k; λ) = (λᵏ × e⁻λ) / k!
```

**Características**:
- `λ` = número promedio de eventos por intervalo
- `E[X] = Var(X) = λ` (propiedad fundamental)
- Para verificar Poisson: razón `Varianza/Media ≈ 1`

### 3. Análisis Estadístico

El notebook incluye:

#### a) Estadísticas Descriptivas
- Media (λ) y desviación estándar
- Varianza y razón varianza/media
- Cuartiles y rango intercuartílico

#### b) Comparación Experimental vs Simulado
- Generación de datos sintéticos con `scipy.stats.poisson.rvs()`
- Gráficos de series temporales
- Análisis visual de similitudes y diferencias

#### c) Análisis de Residuos
- Cálculo: `residuo = x - media`
- Test de rachas (runs test) para aleatoriedad
- Distribución de residuos

#### d) Ajuste a Distribución Teórica
- Histogramas normalizados
- Superposición con PMF de Poisson teórica
- Test Chi-cuadrado de bondad de ajuste

#### e) Cálculo de Probabilidades
- `P(2 ≤ k ≤ 5)` en 10 segundos
- Eventos esperados en 3 minutos
- Tasa de detección (partículas/segundo)

---

## Requisitos

### Software

```bash
Python 3.8+
jupyter notebook
```

### Bibliotecas de Python

```bash
numpy
scipy
matplotlib
pandas
seaborn
```

### Instalación

```bash
pip install numpy scipy matplotlib pandas seaborn jupyter
```

### Para compilar el documento LaTeX

```bash
sudo apt-get install texlive-full
# o
brew install --cask mactex  # en macOS
```

---

## Uso

### 1. Ejecutar el Análisis

```bash
cd distribuciones
jupyter notebook Actividad1_Poisson.ipynb
```

Ejecutar todas las celdas en orden. El notebook generará automáticamente:
- Archivos de datos procesados (`.txt`)
- Tablas resumen (`.csv` y `.tex`)
- Gráficos (`.png`)

### 2. Compilar el Reporte LaTeX

```bash
pdflatex Reporte_Actividad1_Poisson.tex
pdflatex Reporte_Actividad1_Poisson.tex  # Segunda pasada para referencias
```

**Nota**: Antes de compilar, completar los campos marcados con `[COMPLETAR]` en el archivo `.tex` con los resultados del notebook.

---

## Estructura del Análisis

### Flujo de Trabajo

```
1. Cargar datos crudos
   ↓
2. Limpiar y filtrar (remover texto del sistema)
   ↓
3. Calcular diferencias (cuentas por intervalo)
   ↓
4. Detectar y remover outliers
   ↓
5. Calcular λ (media)
   ↓
6. Generar datos simulados (Poisson con λ)
   ↓
7. Análisis comparativo
   ↓
8. Cálculo de probabilidades
   ↓
9. Generación de gráficos y tablas
```

### Gráficos Generados

1. **boxplot_outliers.png**
   - Boxplot mostrando cuartiles
   - Histograma con outliers marcados
   - Límites IQR visualizados

2. **comparacion_series_temporales.png**
   - Serie temporal experimental
   - Serie temporal simulada
   - Comparación directa

3. **analisis_residuos.png**
   - Residuos vs tiempo (experimental y simulado)
   - Histogramas de distribución de residuos

4. **histogramas_poisson.png**
   - Experimental vs Poisson teórica
   - Simulado vs Poisson teórica
   - Comparación completa

---

## Resultados Esperados

### Verificación de Poisson

Si los datos siguen Poisson:
- ✅ `Varianza/Media ≈ 1`
- ✅ Histograma se ajusta a la PMF teórica
- ✅ Test Chi-cuadrado: `p-valor > 0.05`
- ✅ Residuos distribuidos aleatoriamente

### Comparación Experimental vs Simulado

Los datos simulados deben:
- Tener estadísticas similares (media, varianza)
- Mostrar el mismo comportamiento aleatorio
- Seguir la misma distribución de probabilidades

---

## Interpretación Física

### ¿Por qué Poisson?

La **desintegración radiactiva** es un proceso estocástico donde:
1. Los eventos son **independientes**
2. Ocurren a una **tasa promedio constante** (λ)
3. La probabilidad de múltiples eventos simultáneos es **despreciable**

Estas son exactamente las condiciones para una distribución de Poisson.

### Parámetro λ

`λ` representa:
- **Físicamente**: Actividad de la fuente radiactiva × eficiencia del detector
- **Estadísticamente**: Valor esperado de cuentas por intervalo
- **Unidades**: cuentas/10s (en este experimento)

### Tasa de Detección

La tasa calculada refleja:
- Nivel de **radiación de fondo** natural
- Incluye: rayos cósmicos, radón ambiental, materiales radiactivos naturales
- Varía según ubicación geográfica, altitud, y condiciones locales

---

## Preguntas de Análisis

Al completar el reporte, considerar:

### 1. Ajuste a Poisson
- ¿Los datos experimentales se ajustan bien a Poisson?
- ¿Qué indica la razón varianza/media?
- ¿El test Chi-cuadrado confirma el ajuste?

### 2. Outliers
- ¿Cuántos outliers se detectaron?
- ¿Qué podrían representar físicamente? (¿fluctuaciones extremas? ¿errores de medición?)

### 3. Aleatoriedad
- ¿Los residuos muestran patrones sistemáticos?
- ¿Hay evidencia de tendencias temporales?
- ¿Los datos son verdaderamente aleatorios?

### 4. Probabilidades
- ¿La probabilidad teórica coincide con la experimental?
- ¿Cuántas partículas se esperan detectar en diferentes intervalos de tiempo?

---

## Conceptos Clave

### Distribución de Poisson
- Modelo para eventos discretos raros
- Un solo parámetro: λ
- Media = Varianza = λ

### Test Chi-cuadrado
- Mide bondad de ajuste a una distribución
- `p-valor > 0.05`: No se rechaza H₀ (datos siguen la distribución)
- `p-valor < 0.05`: Evidencia contra H₀

### Análisis de Residuos
- Detecta patrones no aleatorios
- Residuos deben estar centrados en cero
- ~68% dentro de ±1σ, ~95% dentro de ±2σ

### Test de Rachas (Runs Test)
- Cuenta cambios de signo en residuos
- Muchas rachas → alta aleatoriedad
- Pocas rachas → posible patrón sistemático

---

## Referencias

### Artículos y Libros

1. **Bevington & Robinson** (2003). *Data reduction and error analysis for the physical sciences*
2. **Taylor** (1997). *An introduction to error analysis*
3. **Ross** (2014). *Introduction to probability and statistics for engineers and scientists*
4. **Springer**: https://link.springer.com/book/10.1007/978-3-030-65140-4

### Documentación de Software

- **NumPy**: https://numpy.org/doc/stable/
- **SciPy Stats**: https://docs.scipy.org/doc/scipy/reference/stats.html
- **Matplotlib**: https://matplotlib.org/stable/contents.html
- **Pandas**: https://pandas.pydata.org/docs/

### Recursos del Curso

- Diapositivas sobre distribuciones (archivo adjunto en Teams)
- Artículo: "Contando Carros" - aplicación de Poisson

---

## Solución de Problemas

### Error: "No module named 'scipy'"
```bash
pip install scipy
```

### Error al cargar el archivo de datos
Verificar que el archivo `datosGeigerRadNatural_20251126.txt` esté en el mismo directorio que el notebook.

### LaTeX no compila
1. Verificar que todos los paquetes estén instalados: `texlive-full`
2. Completar los campos `[COMPLETAR]` con datos reales
3. Verificar que los archivos de imágenes `.png` existan

### Gráficos no se guardan
Ejecutar la celda con:
```python
plt.savefig('nombre_archivo.png', dpi=300, bbox_inches='tight')
```

---

## Notas Adicionales

### Reproducibilidad

El notebook usa `np.random.seed(42)` para garantizar que los datos simulados sean reproducibles entre ejecuciones.

### Personalización

Para usar con otros datos de contador Geiger:
1. Actualizar el nombre del archivo en `load_geiger_data()`
2. Ajustar la fecha y franja horaria en el notebook
3. Verificar el formato de datos (puede variar según el sistema)

### Extensiones Posibles

- Analizar variación de λ a diferentes horas del día
- Comparar con modelos de radiación de fondo teóricos
- Estudiar correlaciones con actividad solar
- Implementar filtros más sofisticados para outliers

---

## Autor

[Nombre del Estudiante]
[Código]
Física Experimental III
Universidad de Antioquia
2025

---

## Licencia

Este material es de uso académico para el curso de Física Experimental III.
