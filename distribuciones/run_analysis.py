#!/usr/bin/env python3
"""
Script auxiliar para ejecutar el análisis de la Actividad 1
Distribución de Poisson - Radiación Natural

Este script ejecuta el notebook automáticamente y genera todos los archivos.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    required_packages = ['numpy', 'scipy', 'matplotlib', 'pandas', 'seaborn', 'jupyter']
    missing = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Faltan los siguientes paquetes:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstalar con: pip install " + " ".join(missing))
        return False

    print("✅ Todas las dependencias están instaladas")
    return True

def check_data_file():
    """Verifica que el archivo de datos exista"""
    data_file = 'datosGeigerRadNatural_20251126.txt'

    if not os.path.exists(data_file):
        print(f"❌ No se encuentra el archivo de datos: {data_file}")
        return False

    print(f"✅ Archivo de datos encontrado: {data_file}")
    return True

def run_notebook():
    """Ejecuta el notebook Jupyter"""
    notebook = 'Actividad1_Poisson.ipynb'

    if not os.path.exists(notebook):
        print(f"❌ No se encuentra el notebook: {notebook}")
        return False

    print(f"\n📓 Ejecutando notebook: {notebook}")
    print("   (Esto puede tomar algunos minutos...)\n")

    try:
        # Ejecutar el notebook sin abrir el navegador
        result = subprocess.run([
            'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--inplace',
            notebook
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Notebook ejecutado exitosamente")
            return True
        else:
            print("❌ Error al ejecutar el notebook:")
            print(result.stderr)
            return False

    except FileNotFoundError:
        print("❌ No se encuentra jupyter. Instalarlo con: pip install jupyter")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def check_output_files():
    """Verifica que se hayan generado los archivos de salida"""
    expected_files = [
        'datos_experimentales_limpios.txt',
        'datos_simulados_poisson.txt',
        'resumen_resultados.csv',
        'resumen_resultados.tex',
        'boxplot_outliers.png',
        'comparacion_series_temporales.png',
        'analisis_residuos.png',
        'histogramas_poisson.png'
    ]

    print("\n📁 Verificando archivos generados:")
    all_exist = True

    for file in expected_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (no generado)")
            all_exist = False

    return all_exist

def compile_latex():
    """Intenta compilar el documento LaTeX"""
    tex_file = 'Reporte_Actividad1_Poisson.tex'

    if not os.path.exists(tex_file):
        print(f"\n⚠️  No se encuentra el archivo LaTeX: {tex_file}")
        return False

    print(f"\n📄 Intentando compilar LaTeX: {tex_file}")

    try:
        # Primera pasada
        result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file],
                                 capture_output=True, text=True)

        if result1.returncode == 0:
            # Segunda pasada para referencias
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file],
                          capture_output=True, text=True)
            print("✅ PDF generado exitosamente")

            # Limpiar archivos auxiliares
            for ext in ['.aux', '.log', '.out']:
                aux_file = tex_file.replace('.tex', ext)
                if os.path.exists(aux_file):
                    os.remove(aux_file)

            return True
        else:
            print("⚠️  Error al compilar LaTeX (revisar campos [COMPLETAR])")
            return False

    except FileNotFoundError:
        print("⚠️  pdflatex no está instalado. Instalar con:")
        print("     Ubuntu/Debian: sudo apt-get install texlive-full")
        print("     macOS: brew install --cask mactex")
        return False
    except Exception as e:
        print(f"⚠️  Error al compilar: {e}")
        return False

def main():
    """Función principal"""
    print("="*60)
    print("  Actividad 1: Distribución de Poisson")
    print("  Análisis de Radiación Natural con Contador Geiger")
    print("="*60)
    print()

    # 1. Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    print()

    # 2. Verificar archivo de datos
    if not check_data_file():
        sys.exit(1)

    print()

    # 3. Ejecutar notebook
    if not run_notebook():
        print("\n⚠️  El notebook no se ejecutó correctamente.")
        print("    Puedes ejecutarlo manualmente con: jupyter notebook")
        sys.exit(1)

    # 4. Verificar archivos de salida
    check_output_files()

    # 5. Intentar compilar LaTeX
    compile_latex()

    print("\n" + "="*60)
    print("✅ Análisis completado")
    print("="*60)
    print("\nArchivos generados:")
    print("  - Datos procesados: *.txt")
    print("  - Tablas: *.csv, *.tex")
    print("  - Gráficos: *.png")
    print("  - PDF (si LaTeX funcionó): Reporte_Actividad1_Poisson.pdf")
    print("\nPróximos pasos:")
    print("  1. Revisar los gráficos generados")
    print("  2. Completar campos [COMPLETAR] en el archivo .tex")
    print("  3. Compilar PDF final: pdflatex Reporte_Actividad1_Poisson.tex")
    print()

if __name__ == '__main__':
    main()
