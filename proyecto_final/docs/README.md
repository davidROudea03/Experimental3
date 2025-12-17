# Análisis de Patrones de Interferencia - Interferómetro de Michelson

## Descripción

Este proyecto implementa un sistema de análisis automatizado para determinar la longitud de onda de un láser He-Ne y calcular la velocidad de la luz mediante el análisis de patrones de interferencia obtenidos con un Interferómetro de Michelson, utilizando la Transformada Rápida de Fourier (FFT).

## Autores

- Santiago Silva Estacio
- Gabriela Ruiz
- Sean Paul Perdomo
- Juan David Ruiz

## Objetivo General

Determinar experimentalmente la velocidad de la luz mediante el análisis del patrón de interferencia en un interferómetro de Michelson, utilizando transformada de Fourier para el procesamiento de datos.

## Fundamento Teórico

### Interferómetro de Michelson

El Interferómetro de Michelson divide un haz de luz en dos rayos perpendiculares mediante un divisor de haz (beam splitter). Cada rayo se refleja en un espejo y regresa al divisor, donde se recombina produciendo un patrón de interferencia.

### Relación entre Franjas y Longitud de Onda

Para un interferómetro de Michelson ideal, la diferencia de camino óptico entre los dos brazos determina el patrón de interferencia:

```
Δx = 2 * d
```

Donde `d` es el desplazamiento del espejo móvil. Cada franja brillante corresponde a un cambio de longitud de onda:

```
λ = 2 * Δd
```

### Velocidad de la Luz

La velocidad de la luz se calcula usando la relación fundamental:

```
c = λ * f
```

Donde:
- `c` = velocidad de la luz (m/s)
- `λ` = longitud de onda (m)
- `f` = frecuencia del láser (Hz)

Para el láser He-Ne:
- Longitud de onda nominal: 632.8 nm
- Frecuencia: ~4.74 × 10¹⁴ Hz

## Metodología

### 1. Adquisición de Imágenes

Las imágenes de los patrones de interferencia se capturan usando:
- Láser He-Ne (632.8 nm)
- Cámara o fotodetector
- Interferómetro de Michelson calibrado

### 2. Procesamiento de Imágenes

El código realiza las siguientes operaciones:

1. **Carga de imagen**: Lee archivos JPEG de patrones de interferencia
2. **Conversión a escala de grises**: Extrae el canal rojo (óptimo para láser He-Ne)
3. **Extracción de perfil de línea**: Promedia la imagen a lo largo de las franjas
4. **Preprocesamiento**: Remoción de tendencias y aplicación de ventana

### 3. Análisis FFT

La Transformada Rápida de Fourier convierte el perfil espacial al dominio de frecuencias:

```python
FFT[I(x)] → P(f)
```

Donde:
- `I(x)` = intensidad en función de la posición
- `P(f)` = espectro de potencia en función de la frecuencia espacial

El pico dominante en el espectro de potencia corresponde a la frecuencia espacial de las franjas:

```
f_franjas = 1 / d_franjas
```

### 4. Cálculo de Longitud de Onda

La longitud de onda se calcula a partir del espaciado de franjas:

```python
λ = (d_franjas [píxeles] * factor_conversión [m/píxel]) / 2
```

**IMPORTANTE**: El factor de conversión `píxel → metro` debe determinarse mediante calibración física con un objeto de dimensiones conocidas.

### 5. Cálculo de Velocidad de la Luz

Con la longitud de onda determinada y la frecuencia conocida del láser:

```python
c = λ * f
```

## Estructura del Proyecto

```
proyecto_final/
├── analyze_interference.py    # Script principal
├── src/
│   ├── __init__.py
│   ├── image_processing.py    # Módulo de procesamiento de imágenes
│   └── fft_analysis.py        # Módulo de análisis FFT
├── imgs/                      # Imágenes de patrones de interferencia
├── docs/
│   ├── README.md             # Esta documentación
│   ├── anteproy.md          # Documento del anteproyecto
│   └── methodology.md       # Metodología detallada
├── results/                  # Resultados del análisis (generado)
├── requirements.txt         # Dependencias Python
└── .gitignore              # Archivos a ignorar en git
```

## Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

O instalación manual:

```bash
pip install numpy scipy matplotlib pillow opencv-python
```

## Uso

### Análisis Básico

1. Coloca las imágenes de patrones de interferencia en el directorio `imgs/`
2. Ejecuta el script principal:

```bash
python analyze_interference.py
```

3. Los resultados se guardarán en el directorio `results/`:
   - `analysis_*.png`: Visualizaciones del análisis para cada imagen
   - `resultados_analisis.txt`: Resumen estadístico de los resultados

### Calibración del Factor Píxel-a-Metro

**CRÍTICO**: El código incluye un factor de conversión por defecto (`pixel_to_meter = 1e-5`), pero este debe ajustarse según tu configuración experimental.

Para calibrar:

1. Captura una imagen con un objeto de dimensiones conocidas (regla, papel milimetrado)
2. Mide cuántos píxeles corresponden a una distancia conocida
3. Calcula: `pixel_to_meter = distancia_real [m] / distancia_píxeles`
4. Actualiza el valor en `analyze_interference.py` (línea ~45)

Ejemplo:
```python
# Si 100 píxeles = 1 mm = 0.001 m
pixel_to_meter = 0.001 / 100  # = 1e-5 m/píxel
```

## Módulos

### `src/image_processing.py`

Funciones para procesamiento de imágenes:

- `load_and_preprocess_image(image_path)`: Carga y convierte imagen a escala de grises
- `extract_line_profile(img_gray, method)`: Extrae perfil 1D de intensidad
- `detect_fringe_orientation(img_gray)`: Detecta orientación de franjas
- `apply_preprocessing_filters(img_gray)`: Aplica filtros de mejora
- `extract_roi(img_gray)`: Extrae región de interés

### `src/fft_analysis.py`

Funciones para análisis FFT:

- `analyze_fringe_pattern(line_profile)`: Análisis FFT del patrón
- `calculate_wavelength(fringe_spacing, pixel_to_meter)`: Calcula λ
- `calculate_speed_of_light(wavelength, frequency)`: Calcula c
- `estimate_uncertainty(measurements)`: Análisis estadístico
- `calculate_fringe_visibility(line_profile)`: Calcula contraste
- `autocorrelation_analysis(line_profile)`: Método alternativo

## Interpretación de Resultados

### Visualizaciones

Cada análisis genera 4 gráficas:

1. **Patrón de Interferencia Original**: Imagen del patrón capturado
2. **Perfil de Intensidad**: Variación de intensidad a lo largo de las franjas
3. **Espectro de Potencia (FFT)**: Muestra las frecuencias espaciales presentes
4. **Espectro de Fourier 2D**: Representación 2D de las frecuencias espaciales

### Métricas

- **Espaciado de franjas**: Distancia entre franjas consecutivas (píxeles)
- **Frecuencia dominante**: Frecuencia espacial principal (ciclos/píxel)
- **Longitud de onda calculada**: λ calculada a partir del patrón (nm)
- **Velocidad de la luz**: c calculada usando c = λf (m/s)
- **Error porcentual**: Desviación respecto al valor teórico (3.0 × 10⁸ m/s)

### Valores Esperados

Según el anteproyecto:

- **Longitud de onda**: 625-640 nm (±5-15 nm)
- **Velocidad de la luz**: (2.85-3.15) × 10⁸ m/s
- **Error esperado**: 0-5% (exitoso si < 10%)

## Fuentes de Error

1. **Vibraciones mecánicas** (~40%): Aislamiento del montaje
2. **Deriva térmica** (~25%): Control de temperatura ambiente
3. **Precisión angular** (~20%): Calibración de espejos
4. **Incertidumbre del láser** (~10%): Estabilidad de frecuencia
5. **Efectos de difracción** (~5%): Alineación óptica

## Mejoras Posibles

- Implementar promediado temporal de múltiples capturas
- Aplicar filtros adaptativos según SNR de la imagen
- Usar métodos de ajuste de fase para mayor precisión
- Implementar corrección automática de inclinación de franjas
- Análisis de estabilidad temporal del patrón

## Referencias

1. Michelson, A. A. (1881). "The Relative Motion of the Earth and the Luminiferous Ether"
2. Hecht, E. (2017). "Optics" (5th Edition), Pearson
3. [Speed of Light Experiment by Michelson](https://www.youtube.com/watch?v=B_T_Xi_bd1c)
4. [Harvard Natural Sciences - Michelson Interferometer](https://sciencedemonstrations.fas.harvard.edu/presentations/michelson-interferometer)

## Licencia

Este proyecto es desarrollado con fines educativos para el curso de Física Experimental III, Universidad de Antioquia.

## Contacto

Para preguntas o sugerencias sobre el código, contacta a los autores del proyecto.

---

**Última actualización**: Diciembre 2025
