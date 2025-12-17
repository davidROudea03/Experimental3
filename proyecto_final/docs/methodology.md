# Metodología Detallada del Análisis FFT

## Introducción

Este documento describe detalladamente la metodología matemática y computacional utilizada para analizar los patrones de interferencia del Interferómetro de Michelson mediante la Transformada Rápida de Fourier (FFT).

## 1. Fundamento Matemático

### 1.1 Patrón de Interferencia

La intensidad del patrón de interferencia en un punto se describe por:

```
I(x) = I₀[1 + V·cos(2πx/d + φ)]
```

Donde:
- `I(x)` = intensidad en la posición x
- `I₀` = intensidad promedio
- `V` = visibilidad (contraste) de las franjas
- `d` = espaciado entre franjas
- `φ` = fase inicial

### 1.2 Transformada de Fourier

La Transformada de Fourier Discreta (DFT) de un perfil de intensidad es:

```
F[k] = Σ(n=0 to N-1) I[n] · exp(-2πikn/N)
```

El espectro de potencia se calcula como:

```
P[k] = |F[k]|²
```

La FFT es un algoritmo eficiente para calcular la DFT, reduciendo la complejidad de O(N²) a O(N·log N).

### 1.3 Frecuencia Espacial

La frecuencia espacial dominante `f` está relacionada con el espaciado de franjas:

```
f = 1/d
```

En términos de píxeles, si el pico máximo en el espectro de potencia ocurre en el índice `k_max`:

```
f_max = k_max / N
d_píxeles = 1 / f_max = N / k_max
```

## 2. Pipeline de Procesamiento

### 2.1 Preprocesamiento

#### a) Conversión a Escala de Grises

Para un láser He-Ne (rojo, 632.8 nm), extraemos solo el canal rojo de la imagen RGB:

```python
img_gray = img_rgb[:, :, 0]  # Canal rojo
```

**Justificación**: El canal rojo contiene la mayor relación señal-ruido (SNR) para luz roja.

#### b) Extracción del Perfil de Línea

Promediamos perpendicular a las franjas para obtener un perfil 1D:

```python
line_profile = np.mean(img_gray, axis=0)  # Promedio vertical
```

**Ventajas**:
- Reduce ruido aleatorio (promediado estadístico)
- Simplifica el análisis a 1D
- Preserva la información de frecuencia espacial

#### c) Remoción de Tendencia

Eliminamos la componente DC (offset) del perfil:

```python
line_profile_detrended = signal.detrend(line_profile)
```

**Efecto**: Centra el perfil en cero, mejorando la detección de frecuencias periódicas.

#### d) Ventana de Hann

Aplicamos una ventana para reducir efectos de borde (leakage espectral):

```python
window = signal.windows.hann(N)
line_profile_windowed = line_profile_detrended * window
```

**Propiedades de Hann**:
- Suprime discontinuidades en los bordes
- Ancho de lóbulo principal: 8π/N
- Atenuación de lóbulos laterales: -31.5 dB

### 2.2 Análisis FFT

#### a) Cálculo de FFT

```python
fft_result = np.fft.fft(line_profile_windowed)
power_spectrum = np.abs(fft_result)**2
freqs = np.fft.fftfreq(N)
```

#### b) Selección de Frecuencias Positivas

Por simetría hermítica, solo necesitamos la mitad positiva:

```python
positive_freqs = freqs[:N//2]
positive_power = power_spectrum[:N//2]
```

#### c) Filtrado de Frecuencias

Aplicamos límites físicamente razonables:

```python
min_freq = 0.01  # Evitar DC y frecuencias muy bajas
max_freq = 0.5   # Frecuencia de Nyquist
```

**Razones**:
- `min_freq > 0`: Excluye DC y variaciones lentas no relacionadas con franjas
- `max_freq ≤ 0.5`: Límite de Nyquist (teorema de muestreo)

#### d) Detección de Picos

Usamos `scipy.signal.find_peaks` con criterios:

```python
peaks, properties = find_peaks(
    masked_power,
    height=max_power * 0.1,  # Altura mínima: 10% del máximo
    distance=min_distance     # Separación mínima entre picos
)
```

Seleccionamos el pico de mayor altura:

```python
dominant_peak_idx = peaks[np.argmax(properties['peak_heights'])]
dominant_freq = positive_freqs[dominant_peak_idx]
```

### 2.3 Cálculo de Longitud de Onda

#### a) Espaciado de Franjas

```python
fringe_spacing_pixels = 1.0 / dominant_freq
```

#### b) Conversión a Distancia Física

```python
fringe_spacing_meters = fringe_spacing_pixels * pixel_to_meter
```

**CALIBRACIÓN CRÍTICA**: `pixel_to_meter` debe determinarse experimentalmente.

#### c) Relación Geométrica

Para el Interferómetro de Michelson, cada franja corresponde a un cambio de λ/2 en la diferencia de camino óptico:

```
Δ(OPD) = λ/2
d_franja = λ/2
λ = 2 * d_franja
```

Implementación:

```python
wavelength = fringe_spacing_meters / geometry_factor
# geometry_factor = 2.0 para Michelson estándar
```

### 2.4 Cálculo de Velocidad de la Luz

Usando la relación fundamental de ondas electromagnéticas:

```python
c = wavelength * frequency
```

Donde `frequency` es la frecuencia del láser He-Ne (~4.74 × 10¹⁴ Hz).

## 3. Análisis de Incertidumbre

### 3.1 Fuentes de Incertidumbre

1. **Resolución espectral**: Δf = 1/N
2. **Error de calibración**: σ(pixel_to_meter)
3. **Variabilidad entre imágenes**: σ(λ_medidas)
4. **Incertidumbre en frecuencia del láser**: σ(f)

### 3.2 Propagación de Errores

Para λ = d / 2:

```
σ(λ) = λ · √[(σ(d)/d)²]
```

Para c = λ · f:

```
σ(c) = c · √[(σ(λ)/λ)² + (σ(f)/f)²]
```

### 3.3 Estadística de Múltiples Mediciones

Desviación estándar de la media:

```python
uncertainty = np.std(measurements, ddof=1) / np.sqrt(n)
```

## 4. Validación del Método

### 4.1 Criterios de Calidad

- **Visibilidad de franjas**: V > 0.5 (contraste adecuado)
- **SNR en espectro**: Pico dominante > 10× nivel de ruido
- **Resolución suficiente**: d_franjas > 5 píxeles

### 4.2 Verificaciones Automáticas

El código implementa:

```python
if fringe_spacing_pixels < 3:
    # Advertencia: resolución insuficiente
if visibility < 0.3:
    # Advertencia: bajo contraste
```

## 5. Métodos Alternativos

### 5.1 Autocorrelación

Como complemento a FFT, se puede usar autocorrelación:

```python
autocorr = np.correlate(profile, profile, mode='full')
```

El primer pico (después del origen) indica el espaciado de franjas.

**Ventajas**:
- Robusto a ruido
- No requiere ventanas

**Desventajas**:
- Menos sensible a frecuencias débiles
- Mayor costo computacional para señales largas

### 5.2 Ajuste de Función Coseno

Ajuste directo al modelo:

```python
I(x) = A + B·cos(2πx/d + φ)
```

Usando `scipy.optimize.curve_fit`.

**Ventajas**:
- Extrae parámetros físicos directamente
- Proporciona incertidumbres del ajuste

**Desventajas**:
- Requiere buena estimación inicial
- Sensible a ruido

## 6. Optimizaciones Implementadas

### 6.1 Computacionales

- Uso de FFT en lugar de DFT: O(N log N) vs O(N²)
- Vectorización con NumPy (evita loops en Python)
- Procesamiento solo de frecuencias positivas

### 6.2 Calidad de Resultados

- Ventana de Hann para reducir leakage
- Remoción de tendencia para mejorar detección
- Filtrado de frecuencias no físicas
- Promediado de múltiples imágenes

## 7. Casos Especiales

### 7.1 Franjas Inclinadas

Si las franjas no son perfectamente horizontales/verticales:

```python
orientation, angle = detect_fringe_orientation(img_gray)
```

Solución: Rotar imagen o proyectar en dirección correcta.

### 7.2 Múltiples Frecuencias

Si aparecen múltiples picos en el espectro:
- Verificar alineación del interferómetro
- Puede indicar reflexiones parásitas
- Analizar cada frecuencia por separado

### 7.3 Bajo Contraste

Si V < 0.3:
- Verificar alineación de espejos
- Ajustar intensidad del láser
- Aplicar filtros de mejora de contraste (CLAHE)

## 8. Ejemplo Numérico

### Datos de Entrada

- Imagen: 640 × 480 píxeles
- Espaciado observado: 40 píxeles/franja
- Calibración: 10 μm/píxel
- Frecuencia láser: 4.74 × 10¹⁴ Hz

### Cálculo

```
1. Frecuencia espacial:
   f = 1/40 = 0.025 ciclos/píxel

2. Distancia física:
   d = 40 píxeles × 10 μm/píxel = 400 μm

3. Longitud de onda:
   λ = d/2 = 400 μm / 2 = 200 μm... ❌ INCORRECTO

   CORRECCIÓN: Calibración incorrecta
   Usando pixel_to_meter = 1.58 × 10⁻⁶ m/píxel:
   d = 40 × 1.58 × 10⁻⁶ = 6.32 × 10⁻⁵ m
   λ = 6.32 × 10⁻⁵ / 2 = 3.16 × 10⁻⁵ m... ❌ AÚN INCORRECTO

   La calibración debe dar:
   λ ≈ 632.8 nm = 6.328 × 10⁻⁷ m
   d = 2λ = 1.266 × 10⁻⁶ m
   pixel_to_meter = 1.266 × 10⁻⁶ / 40 = 3.16 × 10⁻⁸ m/píxel

4. Velocidad de la luz:
   c = λ × f
   c = 6.328 × 10⁻⁷ m × 4.74 × 10¹⁴ Hz
   c = 3.00 × 10⁸ m/s ✓
```

**Conclusión**: La calibración precisa del factor píxel-a-metro es fundamental.

## 9. Referencias Técnicas

1. Cooley, J. W., & Tukey, J. W. (1965). "An algorithm for the machine calculation of complex Fourier series"
2. Harris, F. J. (1978). "On the use of windows for harmonic analysis with the discrete Fourier transform"
3. Press, W. H., et al. (2007). "Numerical Recipes" (3rd Edition)
4. Born, M., & Wolf, E. (1999). "Principles of Optics" (7th Edition)

---

**Documento técnico preparado para el proyecto de Física Experimental III**
