"""
Módulo de análisis FFT para determinar la longitud de onda y velocidad de la luz.

Este módulo contiene funciones para analizar patrones de interferencia usando
la Transformada Rápida de Fourier (FFT) y calcular parámetros físicos del láser.
"""

import numpy as np
from scipy import signal
from scipy.signal import find_peaks


def analyze_fringe_pattern(line_profile, min_distance=5):
    """
    Analiza el patrón de franjas usando FFT para determinar el espaciado.

    Parameters:
    -----------
    line_profile : numpy.ndarray
        Perfil de intensidad 1D
    min_distance : int
        Distancia mínima entre picos en píxeles

    Returns:
    --------
    fringe_spacing : float
        Espaciado entre franjas en píxeles
    dominant_freq : float
        Frecuencia espacial dominante (ciclos/píxel)
    power_spectrum : numpy.ndarray
        Espectro de potencia del perfil
    """
    # Remover tendencia (componente DC)
    line_profile_detrended = signal.detrend(line_profile)

    # Aplicar ventana para reducir efectos de borde
    window = signal.windows.hann(len(line_profile_detrended))
    line_profile_windowed = line_profile_detrended * window

    # Calcular FFT
    fft_result = np.fft.fft(line_profile_windowed)
    power_spectrum = np.abs(fft_result) ** 2

    # Obtener frecuencias
    freqs = np.fft.fftfreq(len(line_profile_windowed))

    # Trabajar solo con frecuencias positivas
    positive_freqs = freqs[:len(freqs)//2]
    positive_power = power_spectrum[:len(power_spectrum)//2]

    # Encontrar el pico dominante (excluyendo DC - frecuencia 0)
    # Buscar en el rango de frecuencias razonables
    min_freq = 0.01  # Evitar frecuencias muy bajas
    max_freq = 0.5   # Nyquist

    freq_mask = (positive_freqs > min_freq) & (positive_freqs < max_freq)
    masked_power = positive_power.copy()
    masked_power[~freq_mask] = 0

    # Encontrar picos en el espectro de potencia
    peaks, properties = find_peaks(masked_power, height=np.max(masked_power)*0.1, distance=min_distance)

    if len(peaks) == 0:
        return None, None, positive_power

    # Tomar el pico más alto
    dominant_peak_idx = peaks[np.argmax(properties['peak_heights'])]
    dominant_freq = positive_freqs[dominant_peak_idx]

    # Calcular espaciado de franjas (inverso de la frecuencia)
    if dominant_freq > 0:
        fringe_spacing = 1.0 / dominant_freq
    else:
        fringe_spacing = None

    return fringe_spacing, dominant_freq, positive_power


def calculate_wavelength(fringe_spacing_pixels, pixel_to_meter, geometry_factor=2.0):
    """
    Calcula la longitud de onda del láser a partir del espaciado de franjas.

    Para un Interferómetro de Michelson con geometría estándar:
    λ = d * (pixel_to_meter) / geometry_factor

    Parameters:
    -----------
    fringe_spacing_pixels : float
        Espaciado entre franjas en píxeles
    pixel_to_meter : float
        Factor de conversión píxel a metros (calibración física)
    geometry_factor : float
        Factor geométrico del interferómetro (típicamente 2.0 para Michelson)

    Returns:
    --------
    wavelength : float
        Longitud de onda en metros
    """
    # Distancia física entre franjas
    fringe_spacing_meters = fringe_spacing_pixels * pixel_to_meter

    # Para interferencia de dos haces:
    # Cada franja corresponde a un cambio de λ/2 en la diferencia de camino óptico
    wavelength = fringe_spacing_meters / geometry_factor

    return wavelength


def calculate_speed_of_light(wavelength, frequency):
    """
    Calcula la velocidad de la luz usando la relación c = λf.

    Parameters:
    -----------
    wavelength : float
        Longitud de onda en metros
    frequency : float
        Frecuencia del láser en Hz

    Returns:
    --------
    speed_of_light : float
        Velocidad de la luz en m/s
    """
    return wavelength * frequency


def estimate_uncertainty(measurements):
    """
    Estima la incertidumbre estadística de las mediciones.

    Parameters:
    -----------
    measurements : list or numpy.ndarray
        Lista de valores medidos

    Returns:
    --------
    mean : float
        Valor promedio
    std : float
        Desviación estándar
    uncertainty : float
        Incertidumbre (desviación estándar de la media)
    """
    measurements = np.array(measurements)
    mean = np.mean(measurements)
    std = np.std(measurements, ddof=1)  # Desviación estándar de la muestra
    uncertainty = std / np.sqrt(len(measurements))  # Error estándar de la media

    return mean, std, uncertainty


def analyze_multiple_images(image_profiles):
    """
    Analiza múltiples imágenes y combina los resultados.

    Parameters:
    -----------
    image_profiles : list of numpy.ndarray
        Lista de perfiles de línea de diferentes imágenes

    Returns:
    --------
    results : dict
        Diccionario con estadísticas combinadas
    """
    fringe_spacings = []
    dominant_freqs = []

    for profile in image_profiles:
        spacing, freq, _ = analyze_fringe_pattern(profile)
        if spacing is not None:
            fringe_spacings.append(spacing)
            dominant_freqs.append(freq)

    if len(fringe_spacings) == 0:
        return None

    mean_spacing, std_spacing, unc_spacing = estimate_uncertainty(fringe_spacings)
    mean_freq, std_freq, unc_freq = estimate_uncertainty(dominant_freqs)

    results = {
        'mean_fringe_spacing': mean_spacing,
        'std_fringe_spacing': std_spacing,
        'uncertainty_fringe_spacing': unc_spacing,
        'mean_frequency': mean_freq,
        'std_frequency': std_freq,
        'uncertainty_frequency': unc_freq,
        'n_measurements': len(fringe_spacings)
    }

    return results


def apply_bandpass_filter(line_profile, lowcut, highcut, fs=1.0):
    """
    Aplica un filtro pasa-banda al perfil de línea para mejorar SNR.

    Parameters:
    -----------
    line_profile : numpy.ndarray
        Perfil de intensidad 1D
    lowcut : float
        Frecuencia de corte inferior (ciclos/píxel)
    highcut : float
        Frecuencia de corte superior (ciclos/píxel)
    fs : float
        Frecuencia de muestreo (píxeles^-1)

    Returns:
    --------
    filtered_profile : numpy.ndarray
        Perfil filtrado
    """
    nyquist = fs / 2.0
    low = lowcut / nyquist
    high = highcut / nyquist

    # Diseñar filtro Butterworth
    b, a = signal.butter(4, [low, high], btype='band')

    # Aplicar filtro
    filtered_profile = signal.filtfilt(b, a, line_profile)

    return filtered_profile


def calculate_fringe_visibility(line_profile):
    """
    Calcula la visibilidad (contraste) de las franjas de interferencia.

    V = (I_max - I_min) / (I_max + I_min)

    Parameters:
    -----------
    line_profile : numpy.ndarray
        Perfil de intensidad 1D

    Returns:
    --------
    visibility : float
        Visibilidad de las franjas (0-1)
    """
    I_max = np.max(line_profile)
    I_min = np.min(line_profile)

    if I_max + I_min == 0:
        return 0.0

    visibility = (I_max - I_min) / (I_max + I_min)

    return visibility


def autocorrelation_analysis(line_profile):
    """
    Analiza el patrón de franjas usando autocorrelación como método alternativo.

    Parameters:
    -----------
    line_profile : numpy.ndarray
        Perfil de intensidad 1D

    Returns:
    --------
    fringe_spacing : float
        Espaciado entre franjas en píxeles (método de autocorrelación)
    """
    # Normalizar perfil
    profile_normalized = (line_profile - np.mean(line_profile)) / np.std(line_profile)

    # Calcular autocorrelación
    autocorr = np.correlate(profile_normalized, profile_normalized, mode='full')
    autocorr = autocorr[len(autocorr)//2:]  # Solo parte positiva

    # Normalizar
    autocorr = autocorr / autocorr[0]

    # Encontrar primer pico (excluyendo el pico en cero)
    peaks, _ = find_peaks(autocorr[1:], height=0.3)

    if len(peaks) > 0:
        fringe_spacing = peaks[0] + 1  # +1 porque empezamos desde índice 1
        return fringe_spacing
    else:
        return None
