# Calibración del Factor Píxel-a-Metro - PENDIENTE

## Estado Actual del Problema

El análisis FFT está detectando correctamente las franjas de interferencia, pero los valores calculados de longitud de onda y velocidad de la luz están **muy alejados de los valores reales** debido a un factor de calibración incorrecto.

### Valores Actuales (Incorrectos)

```
Factor actual: pixel_to_meter = 1e-5 m/píxel (10 μm/píxel)

Resultados obtenidos:
- Espaciado de franjas: ~85 píxeles
- Longitud de onda calculada: ~420,000 nm (420 μm)
- Velocidad de la luz: ~1.991×10¹¹ m/s
- Error: 66,260% ❌
```

### Valores Esperados (Correctos)

```
Longitud de onda nominal láser He-Ne: 632.8 nm
Velocidad de la luz teórica: 3.0×10⁸ m/s
Error aceptable: < 10%
```

## Opciones de Calibración Pendientes

### ✅ Opción 1: Calibración Inversa (Usando Conocimiento del Láser)

**Descripción**: Ya que conocemos la longitud de onda nominal del láser He-Ne (632.8 nm), podemos calcular retrospectivamente el factor de calibración correcto.

**Método**:

```python
# Fórmula: λ = (espaciado_píxeles × pixel_to_meter) / 2
# Despejando: pixel_to_meter = (2 × λ) / espaciado_píxeles

λ_nominal = 632.8e-9  # m
espaciado_promedio = 85  # píxeles (de los resultados)

pixel_to_meter = (2 × λ_nominal) / espaciado_promedio
pixel_to_meter ≈ 1.49×10⁻⁸ m/píxel  # ≈ 14.9 nm/píxel
```

**Ventajas**:
- ✅ Rápido y fácil de implementar
- ✅ No requiere equipo adicional
- ✅ Verifica que el código funciona correctamente
- ✅ Útil para análisis preliminar

**Desventajas**:
- ❌ Asume que conocemos λ de antemano (circular)
- ❌ No es un método experimental riguroso
- ❌ No sirve para "medir" la velocidad de la luz (ya usamos λ conocida)

**Cuándo usar**: Para validar el código y el método FFT antes del experimento real.

**Implementación**:
- Archivo: `analyze_interference.py`, línea ~45
- Modificar: `pixel_to_meter = 1.49e-8`

---

### ✅ Opción 2: Calibración Física Real (Método Experimental Riguroso)

**Descripción**: Determinar el factor de calibración mediante medición directa con un objeto de dimensiones conocidas en el mismo plano que el patrón de interferencia.

**Materiales Necesarios**:
- Regla milimetrada o papel milimetrado
- Calibre Vernier (ya listado en materiales del proyecto)
- Cámara en la misma configuración que para capturar las franjas

**Procedimiento**:

1. **Captura de imagen de calibración**:
   - Sin desmontar el experimento, colocar una regla o papel milimetrado en el plano donde se forma el patrón de interferencia
   - Capturar imagen con la misma cámara y configuración
   - Asegurar que la regla esté perpendicular al eje óptico

2. **Medición en la imagen**:
   ```python
   # Ejemplo: Si 100 píxeles = 5 mm
   distancia_real = 5e-3  # m (5 mm)
   distancia_pixeles = 100  # píxeles
   pixel_to_meter = distancia_real / distancia_pixeles
   pixel_to_meter = 5e-5 m/píxel  # 50 μm/píxel
   ```

3. **Verificación**:
   - Medir varias distancias en la imagen
   - Calcular promedio y desviación estándar
   - Verificar que el factor sea consistente

**Ventajas**:
- ✅ Método experimental riguroso
- ✅ Independiente del conocimiento previo de λ
- ✅ Permite verdadera medición de la velocidad de la luz
- ✅ Cumple con estándares de física experimental

**Desventajas**:
- ⏱️ Requiere tiempo adicional de experimentación
- 🔧 Necesita acceso al montaje experimental
- 📸 Requiere captura de imagen adicional

**Cuándo usar**: Para el experimento final y el informe oficial.

**Notas importantes**:
- La regla debe estar en el **mismo plano** que el patrón de interferencia
- Considerar distorsión de la cámara (usar varias mediciones)
- Documentar la configuración de la cámara (zoom, distancia focal)

---

### ✅ Opción 3: Script de Calibración Automática

**Descripción**: Crear un script Python que calcule automáticamente el factor de calibración a partir de:
- Los patrones de interferencia capturados
- El conocimiento de la longitud de onda nominal del láser

**Funcionalidad**:

```python
# Pseudocódigo
def auto_calibrate(images, nominal_wavelength):
    """
    Calcula automáticamente pixel_to_meter

    Parameters:
    - images: Lista de patrones de interferencia
    - nominal_wavelength: λ conocida del láser (632.8 nm)

    Returns:
    - pixel_to_meter: Factor de calibración
    - uncertainty: Incertidumbre estadística
    """

    # 1. Analizar todas las imágenes
    spacings = []
    for img in images:
        spacing = detect_fringe_spacing(img)
        spacings.append(spacing)

    # 2. Promediar espaciados
    mean_spacing = np.mean(spacings)
    std_spacing = np.std(spacings)

    # 3. Calcular factor
    pixel_to_meter = (2 × nominal_wavelength) / mean_spacing

    # 4. Calcular incertidumbre
    uncertainty = pixel_to_meter × (std_spacing / mean_spacing)

    return pixel_to_meter, uncertainty
```

**Ventajas**:
- ✅ Automatización del proceso
- ✅ Análisis estadístico de múltiples imágenes
- ✅ Cálculo de incertidumbre automático
- ✅ Facilita análisis de diferentes conjuntos de datos

**Desventajas**:
- ❌ Sigue siendo calibración inversa (Opción 1)
- ❌ No es experimentalmente independiente

**Cuándo usar**: Como herramienta complementaria para análisis rápido de múltiples datasets.

**Archivos a crear**:
- `calibrate.py`: Script de calibración automática
- `analyze_with_autocal.py`: Versión del análisis que usa calibración automática

---

## Recomendaciones por Etapa del Proyecto

### 📅 Semana 4: Procesamiento Inicial de Datos
**Usar**: Opción 1 (Calibración Inversa)
- Verificar que el código FFT funciona correctamente
- Validar la metodología
- Generar gráficos preliminares

### 📅 Semana 5: Análisis Final y Validación
**Usar**: Opción 2 (Calibración Física Real)
- Realizar calibración experimental rigurosa
- Obtener mediciones independientes
- Calcular incertidumbres reales

### 📅 Extra: Automatización
**Usar**: Opción 3 (Script Automático)
- Facilitar análisis de múltiples datasets
- Comparar resultados de diferentes días
- Análisis de estabilidad temporal

---

## Acción Inmediata Requerida

Para continuar con el análisis, **debes elegir una opción**:

### Para Validación Rápida (hoy)
```bash
# Editar analyze_interference.py línea ~45
pixel_to_meter = 1.49e-8  # Calculado con Opción 1
```

### Para Experimento Riguroso (próxima sesión de laboratorio)
1. Capturar imagen de calibración con regla
2. Medir distancias píxel en la imagen
3. Calcular pixel_to_meter experimental
4. Actualizar el código

### Para Automatización (opcional)
- Solicitar creación del script `calibrate.py`

---

## Impacto en los Resultados

### Con Calibración Correcta (Opción 2)

Esperamos obtener:

```
Longitud de onda: 625-640 nm (±5-15 nm)
Velocidad de la luz: (2.85-3.15)×10⁸ m/s
Error: < 10% ✅
```

### Con Calibración Inversa (Opción 1)

Obtendremos:

```
Longitud de onda: ≈ 632.8 nm (por diseño)
Velocidad de la luz: ≈ 3.0×10⁸ m/s (por diseño)
Error: ≈ 0%
```

⚠️ **Nota**: La Opción 1 no constituye una medición real, sino una validación del método.

---

## Próximos Pasos

- [ ] Decidir qué opción usar para el análisis actual
- [ ] Implementar la calibración elegida
- [ ] Re-ejecutar `analyze_interference.py`
- [ ] Verificar que los resultados sean razonables
- [ ] Documentar el método de calibración usado
- [ ] (Opcional) Crear script de calibración automática
- [ ] Incluir análisis de calibración en el informe final

---

**Última actualización**: 2025-12-17
**Estado**: ⚠️ PENDIENTE - Calibración requerida antes de análisis final
