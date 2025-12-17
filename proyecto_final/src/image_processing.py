"""
Módulo de procesamiento de imágenes para análisis de patrones de interferencia.

Este módulo contiene funciones para cargar, preprocesar y extraer información
de las imágenes de patrones de interferencia del Interferómetro de Michelson.
"""

import numpy as np
from PIL import Image
import cv2


def load_and_preprocess_image(image_path):
    """
    Carga una imagen y la convierte a escala de grises para análisis.

    Parameters:
    -----------
    image_path : str
        Ruta al archivo de imagen

    Returns:
    --------
    img_gray : numpy.ndarray
        Imagen en escala de grises (valores entre 0-255)
    """
    # Cargar imagen
    img = Image.open(image_path)

    # Convertir a RGB si es necesario
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Convertir a numpy array
    img_array = np.array(img)

    # Convertir a escala de grises
    # Para láser rojo, podemos usar solo el canal rojo para mejor SNR
    if len(img_array.shape) == 3:
        # Usar el canal rojo (índice 0) ya que es láser He-Ne (rojo)
        img_gray = img_array[:, :, 0]
    else:
        img_gray = img_array

    return img_gray


def extract_line_profile(img_gray, method='horizontal'):
    """
    Extrae un perfil de línea de la imagen para análisis FFT.

    Parameters:
    -----------
    img_gray : numpy.ndarray
        Imagen en escala de grises
    method : str
        Método de extracción: 'horizontal', 'vertical', 'average'

    Returns:
    --------
    line_profile : numpy.ndarray
        Perfil de intensidad 1D
    """
    if method == 'horizontal':
        # Promediar a lo largo del eje vertical (promedio de todas las filas)
        line_profile = np.mean(img_gray, axis=0)

    elif method == 'vertical':
        # Promediar a lo largo del eje horizontal (promedio de todas las columnas)
        line_profile = np.mean(img_gray, axis=1)

    elif method == 'average':
        # Promediar ambas direcciones
        h_profile = np.mean(img_gray, axis=0)
        v_profile = np.mean(img_gray, axis=1)

        # Usar el perfil con mayor varianza (más información de franjas)
        if np.var(h_profile) > np.var(v_profile):
            line_profile = h_profile
        else:
            line_profile = v_profile

    else:
        # Por defecto, usar horizontal
        line_profile = np.mean(img_gray, axis=0)

    return line_profile


def apply_preprocessing_filters(img_gray, denoise=True, enhance_contrast=True):
    """
    Aplica filtros de preprocesamiento para mejorar la calidad del análisis.

    Parameters:
    -----------
    img_gray : numpy.ndarray
        Imagen en escala de grises
    denoise : bool
        Si True, aplica filtro de reducción de ruido
    enhance_contrast : bool
        Si True, mejora el contraste

    Returns:
    --------
    img_processed : numpy.ndarray
        Imagen procesada
    """
    img_processed = img_gray.copy()

    # Reducción de ruido
    if denoise:
        img_processed = cv2.fastNlMeansDenoising(img_processed, None, h=10, templateWindowSize=7, searchWindowSize=21)

    # Mejora de contraste
    if enhance_contrast:
        # Ecualización adaptativa de histograma (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_processed = clahe.apply(img_processed)

    return img_processed


def detect_fringe_orientation(img_gray):
    """
    Detecta la orientación dominante de las franjas de interferencia.

    Parameters:
    -----------
    img_gray : numpy.ndarray
        Imagen en escala de grises

    Returns:
    --------
    orientation : str
        'horizontal' o 'vertical' según la orientación dominante
    angle : float
        Ángulo de orientación en grados
    """
    # Calcular FFT 2D
    fft_2d = np.fft.fft2(img_gray)
    fft_2d_shifted = np.fft.fftshift(fft_2d)
    magnitude_spectrum = np.abs(fft_2d_shifted)

    # Encontrar el pico dominante (excluyendo el centro)
    center_y, center_x = np.array(magnitude_spectrum.shape) // 2
    mask = np.ones_like(magnitude_spectrum, dtype=bool)

    # Enmascarar región central
    mask_size = 20
    mask[center_y-mask_size:center_y+mask_size, center_x-mask_size:center_x+mask_size] = False

    masked_spectrum = magnitude_spectrum.copy()
    masked_spectrum[~mask] = 0

    # Encontrar coordenadas del máximo
    max_idx = np.unravel_index(np.argmax(masked_spectrum), masked_spectrum.shape)
    dy = max_idx[0] - center_y
    dx = max_idx[1] - center_x

    # Calcular ángulo
    angle = np.degrees(np.arctan2(dy, dx))

    # Determinar orientación
    if abs(angle) < 45 or abs(angle) > 135:
        orientation = 'horizontal'
    else:
        orientation = 'vertical'

    return orientation, angle


def extract_roi(img_gray, roi_percentage=0.8):
    """
    Extrae una región de interés (ROI) del centro de la imagen.

    Parameters:
    -----------
    img_gray : numpy.ndarray
        Imagen en escala de grises
    roi_percentage : float
        Porcentaje de la imagen a mantener (0-1)

    Returns:
    --------
    roi : numpy.ndarray
        Región de interés extraída
    """
    h, w = img_gray.shape
    roi_h = int(h * roi_percentage)
    roi_w = int(w * roi_percentage)

    start_y = (h - roi_h) // 2
    start_x = (w - roi_w) // 2

    roi = img_gray[start_y:start_y+roi_h, start_x:start_x+roi_w]

    return roi
