#!/usr/bin/env python3
"""
Script principal para análisis de patrones de interferencia del Interferómetro de Michelson
Determina la longitud de onda del láser mediante FFT y calcula la velocidad de la luz.

Autores: Santiago Silva Estacio, Gabriela Ruiz, Sean Paul Perdomo, Juan David Ruiz
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from src.image_processing import load_and_preprocess_image, extract_line_profile
from src.fft_analysis import analyze_fringe_pattern, calculate_wavelength, calculate_speed_of_light


def main():
    """Función principal para el análisis de patrones de interferencia"""

    # Configuración
    imgs_dir = Path("imgs")
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # Parámetros conocidos del experimento
    LASER_FREQUENCY = 4.74e14  # Hz (frecuencia del láser He-Ne)
    NOMINAL_WAVELENGTH = 632.8e-9  # m (longitud de onda nominal del láser)
    THEORETICAL_SPEED_OF_LIGHT = 3.0e8  # m/s

    # Buscar imágenes JPEG en el directorio
    image_files = sorted(imgs_dir.glob("*.jpeg"))

    if not image_files:
        print("❌ No se encontraron imágenes en el directorio 'imgs/'")
        return

    print(f"📊 Encontradas {len(image_files)} imágenes para analizar\n")
    print("="*70)

    results = []

    for idx, img_path in enumerate(image_files, 1):
        print(f"\n🔬 Analizando imagen {idx}/{len(image_files)}: {img_path.name}")
        print("-"*70)

        try:
            # 1. Cargar y preprocesar la imagen
            img_gray = load_and_preprocess_image(str(img_path))

            # 2. Extraer perfil de línea (promedio a lo largo de las franjas)
            line_profile = extract_line_profile(img_gray)

            # 3. Analizar patrón de franjas con FFT
            fringe_spacing_pixels, dominant_freq, power_spectrum = analyze_fringe_pattern(line_profile)

            if fringe_spacing_pixels is None:
                print(f"⚠️  No se pudo determinar el espaciado de franjas")
                continue

            print(f"   ✓ Espaciado de franjas: {fringe_spacing_pixels:.2f} píxeles")
            print(f"   ✓ Frecuencia dominante: {dominant_freq:.4f} ciclos/píxel")

            # 4. Calcular longitud de onda (requiere calibración física)
            # NOTA: Este es un valor de ejemplo. En un experimento real, necesitas
            # la distancia física real correspondiente a los píxeles
            pixel_to_meter = 1e-5  # 10 micrómetros por píxel (AJUSTAR SEGÚN CALIBRACIÓN)

            wavelength = calculate_wavelength(fringe_spacing_pixels, pixel_to_meter)
            print(f"   ✓ Longitud de onda calculada: {wavelength*1e9:.2f} nm")

            # 5. Calcular velocidad de la luz
            speed_of_light = calculate_speed_of_light(wavelength, LASER_FREQUENCY)
            error_percentage = abs(speed_of_light - THEORETICAL_SPEED_OF_LIGHT) / THEORETICAL_SPEED_OF_LIGHT * 100

            print(f"   ✓ Velocidad de la luz: {speed_of_light:.3e} m/s")
            print(f"   ✓ Error porcentual: {error_percentage:.2f}%")

            # Guardar resultados
            results.append({
                'image': img_path.name,
                'fringe_spacing_pixels': fringe_spacing_pixels,
                'wavelength_nm': wavelength * 1e9,
                'speed_of_light': speed_of_light,
                'error_percentage': error_percentage
            })

            # 6. Generar visualizaciones
            plot_analysis(img_gray, line_profile, power_spectrum, dominant_freq,
                         img_path.name, results_dir)

        except Exception as e:
            print(f"❌ Error procesando {img_path.name}: {str(e)}")
            continue

    # Resumen de resultados
    print("\n" + "="*70)
    print("📈 RESUMEN DE RESULTADOS")
    print("="*70)

    if results:
        wavelengths = [r['wavelength_nm'] for r in results]
        speeds = [r['speed_of_light'] for r in results]
        errors = [r['error_percentage'] for r in results]

        print(f"\n🔬 Longitud de onda:")
        print(f"   Promedio: {np.mean(wavelengths):.2f} ± {np.std(wavelengths):.2f} nm")
        print(f"   Valor nominal: {NOMINAL_WAVELENGTH*1e9:.2f} nm")

        print(f"\n⚡ Velocidad de la luz:")
        print(f"   Promedio: {np.mean(speeds):.3e} ± {np.std(speeds):.2e} m/s")
        print(f"   Valor teórico: {THEORETICAL_SPEED_OF_LIGHT:.3e} m/s")
        print(f"   Error promedio: {np.mean(errors):.2f}%")

        # Guardar resultados en archivo
        save_results_to_file(results, wavelengths, speeds, errors,
                            NOMINAL_WAVELENGTH, THEORETICAL_SPEED_OF_LIGHT, results_dir)
    else:
        print("\n⚠️  No se pudieron analizar imágenes")

    print(f"\n✅ Análisis completado. Resultados guardados en '{results_dir}/'")


def plot_analysis(img_gray, line_profile, power_spectrum, dominant_freq, filename, output_dir):
    """Genera visualizaciones del análisis"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Imagen original
    axes[0, 0].imshow(img_gray, cmap='gray')
    axes[0, 0].set_title('Patrón de Interferencia Original')
    axes[0, 0].axis('off')

    # 2. Perfil de intensidad
    axes[0, 1].plot(line_profile, 'r-', linewidth=1.5)
    axes[0, 1].set_title('Perfil de Intensidad')
    axes[0, 1].set_xlabel('Posición (píxeles)')
    axes[0, 1].set_ylabel('Intensidad')
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Espectro de potencia (FFT)
    # power_spectrum ya viene recortado a frecuencias positivas
    freqs = np.fft.fftfreq(len(line_profile))
    positive_freqs = freqs[:len(freqs)//2]
    axes[1, 0].plot(positive_freqs, power_spectrum, 'b-')
    axes[1, 0].axvline(dominant_freq, color='r', linestyle='--',
                       label=f'Freq. dominante: {dominant_freq:.4f}')
    axes[1, 0].set_title('Espectro de Potencia (FFT)')
    axes[1, 0].set_xlabel('Frecuencia espacial (ciclos/píxel)')
    axes[1, 0].set_ylabel('Potencia')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xlim(0, 0.5)

    # 4. FFT 2D de la imagen
    fft_2d = np.fft.fft2(img_gray)
    fft_2d_shifted = np.fft.fftshift(fft_2d)
    magnitude_spectrum = np.log(np.abs(fft_2d_shifted) + 1)

    axes[1, 1].imshow(magnitude_spectrum, cmap='hot')
    axes[1, 1].set_title('Espectro de Fourier 2D')
    axes[1, 1].axis('off')

    plt.tight_layout()
    output_path = output_dir / f"analysis_{Path(filename).stem}.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"   ✓ Visualización guardada: {output_path}")


def save_results_to_file(results, wavelengths, speeds, errors,
                         nominal_wavelength, theoretical_c, output_dir):
    """Guarda los resultados en un archivo de texto"""

    output_file = output_dir / "resultados_analisis.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("ANÁLISIS DE PATRONES DE INTERFERENCIA - INTERFERÓMETRO DE MICHELSON\n")
        f.write("="*70 + "\n\n")

        f.write("RESULTADOS INDIVIDUALES:\n")
        f.write("-"*70 + "\n")
        for r in results:
            f.write(f"\nImagen: {r['image']}\n")
            f.write(f"  - Espaciado de franjas: {r['fringe_spacing_pixels']:.2f} píxeles\n")
            f.write(f"  - Longitud de onda: {r['wavelength_nm']:.2f} nm\n")
            f.write(f"  - Velocidad de la luz: {r['speed_of_light']:.3e} m/s\n")
            f.write(f"  - Error porcentual: {r['error_percentage']:.2f}%\n")

        f.write("\n" + "="*70 + "\n")
        f.write("ESTADÍSTICAS FINALES:\n")
        f.write("="*70 + "\n\n")

        f.write(f"Longitud de onda:\n")
        f.write(f"  Promedio: {np.mean(wavelengths):.2f} ± {np.std(wavelengths):.2f} nm\n")
        f.write(f"  Valor nominal: {nominal_wavelength*1e9:.2f} nm\n")
        f.write(f"  Desviación: {abs(np.mean(wavelengths) - nominal_wavelength*1e9):.2f} nm\n\n")

        f.write(f"Velocidad de la luz:\n")
        f.write(f"  Promedio: {np.mean(speeds):.3e} ± {np.std(speeds):.2e} m/s\n")
        f.write(f"  Valor teórico: {theoretical_c:.3e} m/s\n")
        f.write(f"  Error promedio: {np.mean(errors):.2f}%\n\n")

        f.write("="*70 + "\n")
        f.write("NOTA: Los resultados dependen de la calibración física correcta\n")
        f.write("      del factor píxel-a-metro. Ajustar según el experimento.\n")
        f.write("="*70 + "\n")

    print(f"   ✓ Resultados guardados: {output_file}")


if __name__ == "__main__":
    main()
