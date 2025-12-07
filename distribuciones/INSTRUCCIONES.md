# Instrucciones Rápidas - Actividad 1

## 🚀 Inicio Rápido

### Opción 1: Ejecutar automáticamente

```bash
cd distribuciones
python3 run_analysis.py
```

Este script:
- ✅ Verifica dependencias
- ✅ Ejecuta el notebook completo
- ✅ Genera todos los gráficos y tablas
- ✅ Intenta compilar el PDF

### Opción 2: Ejecutar manualmente

```bash
cd distribuciones
jupyter notebook Actividad1_Poisson.ipynb
```

Luego ejecutar todas las celdas: `Cell > Run All`

---

## 📋 Checklist de Entrega

### Antes de entregar:

- [ ] Ejecutar el notebook completo (sin errores)
- [ ] Verificar que se generaron todos los gráficos (4 archivos .png)
- [ ] Revisar las estadísticas en el notebook
- [ ] Completar campos `[COMPLETAR]` en el archivo LaTeX
- [ ] Agregar franja horaria de toma de datos
- [ ] Compilar PDF: `pdflatex Reporte_Actividad1_Poisson.tex`
- [ ] Registrar resultados en la bitácora del laboratorio

### Archivos a entregar:

1. **Notebook ejecutado**: `Actividad1_Poisson.ipynb`
2. **Reporte PDF**: `Reporte_Actividad1_Poisson.pdf`
3. **Registro en bitácora** (físico o digital según indicaciones)

---

## 📊 Análisis Incluido

El notebook realiza automáticamente:

1. ✅ Carga y limpieza de datos
2. ✅ Detección de outliers (método IQR)
3. ✅ Cálculo de λ (parámetro de Poisson)
4. ✅ Generación de datos simulados
5. ✅ Comparación experimental vs simulado
6. ✅ Análisis de residuos
7. ✅ Histogramas con distribución teórica
8. ✅ Test Chi-cuadrado
9. ✅ Cálculo de probabilidades P(2≤k≤5)
10. ✅ Eventos esperados en 3 minutos

---

## 🔧 Solución de Problemas

### "ModuleNotFoundError: No module named 'X'"

```bash
pip install numpy scipy matplotlib pandas seaborn jupyter
```

### El notebook no se ejecuta

1. Verificar que el archivo de datos esté en la misma carpeta
2. Abrir con: `jupyter notebook Actividad1_Poisson.ipynb`
3. Ejecutar celda por celda (Shift+Enter)

### LaTeX no compila

**En Ubuntu/Debian:**
```bash
sudo apt-get install texlive-full
```

**En macOS:**
```bash
brew install --cask mactex
```

**Alternativa**: Usar Overleaf (online)
1. Subir el archivo `.tex` a Overleaf
2. Subir los gráficos `.png`
3. Completar campos `[COMPLETAR]`
4. Compilar online

---

## 📈 Resultados Esperados

### Parámetro λ

El valor típico de λ para radiación de fondo natural suele estar entre:
- **2-8 cuentas/10s** (depende del detector y ubicación)

### Razón Varianza/Media

Para una distribución de Poisson perfecta:
- **Varianza/Media = 1.0**

En datos experimentales reales:
- **0.8 - 1.2** es aceptable (pequeñas desviaciones son normales)

### Test Chi-cuadrado

- **p-valor > 0.05**: Los datos siguen Poisson ✅
- **p-valor < 0.05**: Hay desviaciones significativas ⚠️

### Probabilidad P(2≤k≤5)

Depende de λ, pero típicamente:
- Si λ ≈ 5: P(2≤k≤5) ≈ 0.4-0.6 (40-60%)

---

## 📝 Campos a Completar en LaTeX

Buscar en `Reporte_Actividad1_Poisson.tex` los marcadores `[COMPLETAR]` y rellenar con:

1. **Información personal**:
   - Nombre del estudiante
   - Código
   - Fecha

2. **Franja horaria**: Hora de inicio y fin de la toma de datos

3. **Resultados numéricos** (copiar del notebook):
   - Total de datos
   - Outliers removidos
   - Valores de λ, desviación estándar, varianza
   - Resultados del test Chi-cuadrado
   - Probabilidades calculadas

4. **Análisis y conclusiones** (secciones específicas marcadas)

---

## 💡 Tips para el Análisis

### Interpretación de Resultados

1. **Outliers**: Pocos outliers (< 5%) es normal. Muchos pueden indicar problemas.

2. **Residuos**: Deben fluctuar aleatoriamente sin patrones. Si hay tendencias, investigar.

3. **Histogramas**: Deben seguir la forma de campana asimétrica de Poisson.

4. **Chi-cuadrado**: No te preocupes si p-valor es ~0.03-0.10. Datos reales no son perfectos.

### Respuestas en la Discusión

Considerar:
- ¿Por qué la radiación natural sigue Poisson?
- ¿Qué fuentes contribuyen a la radiación de fondo?
- ¿Cómo afectan las condiciones ambientales?
- ¿Qué limitaciones tiene el experimento?

---

## 📚 Referencias Útiles

### Distribución de Poisson

- **Condiciones**: Eventos independientes, tasa constante, no simultáneos
- **Parámetro**: λ = media = varianza
- **Aplicaciones**: Radiactividad, llamadas telefónicas, tráfico vehicular

### Test Estadísticos

- **Chi-cuadrado**: Mide bondad de ajuste
- **Test de rachas**: Verifica aleatoriedad
- **IQR**: Método robusto para outliers

### Python/Jupyter

- Ejecutar celda: `Shift + Enter`
- Autocompletar: `Tab`
- Ayuda de función: `?nombre_funcion`
- Ver variables: `%whos`

---

## ✉️ Contacto

Para dudas sobre el análisis:
- Revisar el README detallado: `README_Actividad1.md`
- Consultar documentación en los comentarios del notebook
- Preguntar en clase o foros del curso

---

## 📅 Fechas Importantes

- **Toma de datos**: Durante horario de clase
- **Entrega**: Según calendario del curso
- **Formato**: Registro en bitácora + notebook/PDF

---

**Última actualización**: Diciembre 2025
