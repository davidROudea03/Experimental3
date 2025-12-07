# Documentación: Práctica_FisExpIII.ipynb

## Descripción General

Este notebook implementa análisis de **Óptica de Fourier** para estudiar patrones de difracción de Fraunhofer. El código procesa imágenes experimentales de patrones de difracción capturados en una pantalla y utiliza la **Transformada de Fourier Inversa** para reconstruir la apertura u objeto que generó el patrón.

El experimento analiza tres casos:
1. **Estrella**: Patrón de difracción de una apertura con forma de estrella
2. **Rejilla**: Patrón de difracción de una rejilla de difracción
3. **Rejilla + Estrella**: Combinación de ambos objetos

## Fundamento Teórico

### Difracción de Fraunhofer

En el régimen de Fraunhofer (campo lejano), el patrón de difracción observado en una pantalla es proporcional a la **transformada de Fourier del campo de amplitud en la apertura**:

```
U₂(x, y) ∝ FFT[U₁(ξ, η)]
```

Donde:
- `U₁(ξ, η)`: Campo de amplitud en el plano del objeto/apertura
- `U₂(x, y)`: Campo observado en el plano de la pantalla (patrón de difracción)

### Reconstrucción del Objeto

Si fotografiamos el patrón de difracción (U₂), podemos aplicar la **transformada inversa** para recuperar información sobre el objeto original:

```
U₁(ξ, η) ∝ IFFT[U₂(x, y)]
```

---

## Estructura del Código

### 1. Importación de Librerías

```python
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
from skimage import io
```

**Librerías utilizadas:**
- `numpy`: Cálculos numéricos y operaciones con arrays
- `matplotlib.pyplot`: Visualización de imágenes y datos
- `google.colab.files`: Carga de archivos en Google Colab
- `skimage.io`: Lectura y procesamiento de imágenes

**Nota**: Este código está diseñado para ejecutarse en **Google Colab**.

---

## PARTE 1: Análisis de la Estrella

### 2. Carga de la Imagen de Difracción

```python
#@title NO VOLVER A CORRER
estrella_uploaded = files.upload()
```

**Función:**
- `files.upload()`: Abre un diálogo para subir archivos desde el ordenador
- **Importante**: La celda tiene el marcador "NO VOLVER A CORRER" para evitar subir la imagen múltiples veces

### 3. Lectura y Extracción de la Imagen

```python
for i in estrella_uploaded.keys():
  filename = i
estrella = io.imread(filename)
sizeX = np.shape(estrella)[1]  # Número de columnas
sizeY = np.shape(estrella)[0]  # Número de filas
```

**Proceso:**
1. Extrae el nombre del archivo subido
2. `io.imread()`: Lee la imagen como un array NumPy
3. Obtiene las dimensiones: `shape[0]` = filas, `shape[1]` = columnas

### 4. Separación de Canales RGB

```python
imageR = np.zeros((sizeY, sizeX))
imageG = np.zeros((sizeY, sizeX))
imageB = np.zeros((sizeY, sizeX))
imagebw = np.zeros((sizeY, sizeX))

for i in range(sizeX):
  for j in range(sizeY):
    imageR[j][i] = estrella[j][i][0]  # Componente Roja (R)
    imageG[j][i] = estrella[j][i][1]  # Componente Verde (G)
    imageB[j][i] = estrella[j][i][2]  # Componente Azul (B)
```

**Explicación:**
- Las imágenes RGB tienen 3 componentes de color en cada píxel
- Se crean matrices separadas para cada canal (R, G, B)
- `estrella[j][i][0/1/2]`: Accede a cada componente de color individual
- Este proceso permite trabajar con un solo canal de color

### 5. Normalización de la Intensidad

```python
intensity = imageR/255
plt.imshow(intensity, cmap='gray')
plt.colorbar()
```

**Detalles:**
- `imageR/255`: Normaliza los valores de 0-255 a 0-1
- Se trabaja solo con el canal rojo (también se podría usar verde o azul)
- `cmap='gray'`: Muestra la imagen en escala de grises
- `plt.colorbar()`: Añade barra de color para referencia de intensidades

### 6. Calibración Espacial - Imagen en Centímetros

```python
cm = 4.3 / 1350

N = len(intensity[0,:])
plt.imshow(intensity, cmap='gray', extent=[-N*cm/2, N*cm/2-cm, -N*cm/2, N*cm/2-cm])
plt.ylabel('x (cm)')
plt.xlabel('y (cm)')
plt.colorbar()
```

**Calibración:**
- `cm = 4.3 / 1350`: Factor de conversión píxel → centímetros
  - 1350 píxeles corresponden a 4.3 cm en la imagen real
  - Por tanto: 1 píxel = 4.3/1350 cm
- `N`: Número total de píxeles (columnas)
- `extent`: Define los límites de los ejes en centímetros centrados en el origen

### 7. Conversión a Campo de Amplitud

```python
u2 = intensity**0.5
plt.imshow(u2, cmap='gray', extent=[-N*cm/2, N*cm/2-cm, -N*cm/2, N*cm/2-cm])
plt.ylabel('x (cm)')
plt.xlabel('y (cm)')
plt.colorbar()
```

**Relación Física:**
- `intensity ∝ |U₂|²` (la intensidad es propproporcional al módulo al cuadrado del campo)
- `u2 = intensity**0.5` → `u2 ∝ |U₂|` (campo de amplitud)
- **Motivo**: La transformada de Fourier opera sobre campos de amplitud, no sobre intensidades

### 8. Conversión al Espacio de Frecuencias

```python
dx = cm*1E-2  # Conversión a metros
lam = 632.8E-9  # Longitud de onda en metros (láser HeNe rojo)
theta = np.arcsin(lam/5e-2)
z = 5e-2 / np.tan(theta)  # Distancia a la pantalla en metros
df = dx/(lam*z)

plt.imshow(np.abs(u2), cmap='gray', extent=[-N*df/2, N*df/2-df, -N*df/2, N*df/2-df])
plt.ylabel('$1/f_\\xi$ (1/m)')
plt.xlabel('$1/f_\\eta$ (1/m)')
plt.colorbar()
```

**Parámetros Físicos:**
- `dx`: Tamaño de píxel en metros
- `lam = 632.8 nm`: Longitud de onda del láser HeNe (rojo)
- `theta`: Ángulo de difracción calculado con `sin(θ) = λ/d` donde `d = 5 cm`
- `z`: Distancia de propagación (distancia objeto-pantalla)

**Fórmula de Frecuencia Espacial:**
```
df = dx / (λ × z)
```
- `df`: Resolución en frecuencias espaciales (1/m)
- Convierte coordenadas espaciales en la pantalla a frecuencias espaciales

### 9. Función de Propagación de Fraunhofer

```python
def propFF(u2, L2, lam, z):
  # propagation - FRAUNHOFER PATTERN
  # u2 - observation plane field (campo en el plano de observación)
  # L2 - observation plane side length (tamaño del plano de observación)
  # lam - wavelength (longitud de onda)
  # z - propagation distance (distancia de propagación)
  #
  # Retorna:
  # u1 - source plane field (campo en el plano de la fuente)
  # L1 - source plane side length (tamaño del plano de la fuente)

  Ny, Nx = u2.shape

  # Paso espacial en el plano de observación
  dx2 = L2 / Nx
  dy2 = L2 / Ny

  # Coordenadas del plano de observación
  x2_coords = np.linspace(-L2/2, L2/2 - dx2, Nx)
  y2_coords = np.linspace(-L2/2, L2/2 - dy2, Ny)
  X2, Y2 = np.meshgrid(x2_coords, y2_coords)

  k = 2*np.pi/lam  # Número de onda

  # Factor de fase cuadrático (aproximación de Fraunhofer)
  c = 1/(1j*lam*z) * np.exp(1j*k/(2*z)*(X2**2 + Y2**2))

  # Parámetros del plano de la fuente
  L1 = lam*z/dx2
  dx1 = lam*z/L2

  # Transformada inversa para obtener el campo en el plano de la fuente
  u1 = np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(u2/(c*dx1**2))))

  return u1, L1
```

**Componentes Clave:**

1. **Factor de Fase `c`:**
   ```
   c = (1/iλz) × exp[ik(x² + y²)/(2z)]
   ```
   - Representa la fase cuadrática de la propagación de Fraunhofer

2. **Relaciones Espaciales:**
   ```
   L1 = λz/dx2  (tamaño del objeto)
   dx1 = λz/L2  (resolución en el objeto)
   ```

3. **Secuencia de Transformada Inversa:**
   - `fftshift`: Centra el espectro de frecuencias
   - `ifft2`: Transformada de Fourier inversa 2D
   - `ifftshift`: Reordena el resultado

**Aplicación:**
```python
mod_u1_1 = abs(propFF(u2, cm, lam, z)[0]) / np.max(abs(propFF(u2, cm, lam, z)[0]))
```
- Calcula el módulo del campo reconstruido
- Normaliza dividiendo por el valor máximo

### 10. Visualización del Objeto Reconstruido

```python
dx_o = 1/(N*df)
plt.imshow(mod_u1_1, cmap='gray', extent=[-N*dx_o/2, N*dx_o/2-dx_o, -N*dx_o/2, N*dx_o/2-dx_o])
plt.title('Imagen del objeto')
plt.ylabel('y (m)')
plt.xlabel('x (m)')
plt.colorbar()
```

**Calibración del Objeto:**
- `dx_o = 1/(N*df)`: Resolución espacial en el plano del objeto
- `extent`: Define los ejes en metros para el objeto reconstruido

### 11. Visualización con Zoom

```python
plt.imshow(mod_u1_1, cmap='gray', extent=[-N*dx_o/2, N*dx_o/2-dx_o, -N*dx_o/2, N*dx_o/2-dx_o],
           vmin=0.015, vmax=0.05)
plt.title('Imagen del objeto')
plt.ylabel('y (m)')
plt.xlabel('x (m)')

zoom = 0.01
plt.xlim(-zoom*N*dx_o/2, zoom*N*dx_o/2-dx_o)
plt.ylim(-zoom*N*dx_o/2, zoom*N*dx_o/2-dx_o)
plt.colorbar()
```

**Ajustes de Visualización:**
- `vmin`, `vmax`: Ajustan el rango de intensidades mostrado (contraste)
- `zoom = 0.01`: Factor de acercamiento (1% del tamaño total)
- `xlim`, `ylim`: Limitan el área visible para hacer zoom

**Nota**: Si la imagen no es cuadrada, `dx` y `dy` deben ajustarse por separado.

---

## PARTE 2: Análisis de la Rejilla

### 12-19. Procesamiento de la Rejilla

El proceso es **idéntico** al de la estrella, con los siguientes cambios en los parámetros:

```python
cm = 5 / 185  # Nueva calibración para la rejilla
```

**Diferencias:**
- Factor de calibración diferente: `5 cm / 185 píxeles`
- Parámetros de visualización ajustados (`vmin=0.00095`, `vmax=0.01`)
- `zoom = 0.03` (zoom del 3%)

**Resultado Esperado:**
- Reconstrucción de la estructura periódica de la rejilla de difracción

---

## PARTE 3: Análisis de Rejilla + Estrella

### 20-28. Procesamiento de la Combinación

Proceso idéntico aplicado a la imagen combinada:

```python
cm = 4.3 / 410  # Calibración para la imagen combinada
```

**Parámetros específicos:**
- `vmax = 0.01` para contraste
- `zoom = 0.06` (6% del tamaño)

**Objetivo:**
- Observar cómo la difracción de dos objetos simultáneos produce un patrón que contiene información de ambos
- La transformada inversa permite recuperar la forma de ambos objetos

---

## Conceptos Físicos Clave

### 1. Difracción de Fraunhofer (Campo Lejano)

Condición: `z >> a²/λ` donde `a` es el tamaño de la apertura

En este régimen:
- El patrón de difracción es la transformada de Fourier de la apertura
- La relación es lineal e instantánea (no hay efectos de propagación cercana)

### 2. Teorema de la Transformada de Fourier en Óptica

```
Campo en pantalla ∝ FFT[Campo en apertura]
```

Por tanto:
```
Campo en apertura ∝ IFFT[Campo en pantalla]
```

### 3. Relación entre Espacios

- **Plano de la apertura**: Coordenadas espaciales (ξ, η) en metros
- **Plano de la pantalla**: Coordenadas espaciales (x, y) en metros
- **Dominio de frecuencias**: (fξ, fη) en 1/metro

### 4. Conversión Intensidad ↔ Amplitud

- **Intensidad medida**: `I ∝ |U|²`
- **Amplitud para procesamiento**: `U ∝ √I`

### 5. Parámetros del Experimento

- **Láser HeNe**: λ = 632.8 nm (rojo)
- **Distancia típica**: ~5 cm (calculada según geometría)
- **Calibración**: Relación píxeles/cm medida experimentalmente

---

## Flujo de Trabajo

```
1. Fotografía del patrón de difracción → Imagen digital

2. Procesamiento de imagen:
   - Extracción del canal rojo
   - Normalización (0-1)
   - Calibración espacial (píxeles → cm)

3. Conversión a amplitud:
   - I → √I = |U₂|

4. Calibración física:
   - Conversión a frecuencias espaciales
   - Cálculo de parámetros de propagación

5. Transformada inversa:
   - Aplicación de propFF()
   - Obtención de |U₁| (campo en el objeto)

6. Visualización:
   - Normalización
   - Ajuste de contraste
   - Zoom para análisis detallado
```

---

## Resultados Esperados

### Estrella
- Patrón de difracción: Figura compleja con simetría relacionada con la forma de la estrella
- Objeto reconstruido: Forma de estrella reconocible

### Rejilla
- Patrón de difracción: Serie de máximos y mínimos regulares (órdenes de difracción)
- Objeto reconstruido: Estructura periódica de líneas

### Rejilla + Estrella
- Patrón de difracción: Superposición de ambos patrones
- Objeto reconstruido: Ambos objetos visibles simultáneamente

---

## Notas Importantes

### Para Imágenes No Cuadradas
Si `Nx ≠ Ny`, es necesario ajustar:
- `dx` y `dy` por separado
- `df_ξ` y `df_η` independientemente
- `dx_o` y `dy_o` con sus respectivos valores

### Precauciones
- **NO volver a ejecutar** las celdas de carga de archivos una vez subidas las imágenes
- Los factores de calibración (`cm`) son específicos de cada imagen y deben medirse experimentalmente
- Los parámetros `vmin`, `vmax` y `zoom` pueden necesitar ajuste según la imagen

### Limitaciones
- La reconstrucción asume difracción de Fraunhofer pura
- Se trabaja solo con el módulo del campo (se pierde información de fase en la fotografía)
- La resolución está limitada por el tamaño de la imagen capturada

---

## Aplicaciones

Este tipo de análisis tiene aplicaciones en:
- **Caracterización de objetos**: Determinar forma y tamaño de aperturas
- **Metrología óptica**: Medición de estructuras microscópicas
- **Procesamiento de señales**: Filtrado espacial de frecuencias
- **Holografía**: Reconstrucción de frentes de onda

---

## Referencias

- Goodman, J.W., "Introduction to Fourier Optics" (2005)
- Born & Wolf, "Principles of Optics" (1999)
- [NumPy FFT Documentation](https://numpy.org/doc/stable/reference/routines.fft.html)
- [scikit-image Documentation](https://scikit-image.org/)

---

## Ejercicios Sugeridos

1. **Análisis de resolución**: ¿Cómo afecta el tamaño de la imagen capturada a la resolución del objeto reconstruido?

2. **Efecto de la distancia**: ¿Qué sucede si se cambia el valor de `z`? ¿Cómo afecta a la reconstrucción?

3. **Comparación de canales**: Probar con los canales verde y azul en lugar del rojo. ¿Hay diferencias?

4. **Filtrado**: Modificar `u2` eliminando ciertas frecuencias espaciales antes de la transformada inversa. ¿Cómo afecta al objeto reconstruido?

5. **Objetos adicionales**: Aplicar el método a otros objetos (círculo, cuadrado, rendija simple) y comparar patrones.
