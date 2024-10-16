# Fractales en Pygame

Este proyecto implementa visualizaciones interactivas de dos fractales famosos: el fractal de Mandelbrot y el fractal de Julia, utilizando la librería **Pygame** para la visualización y **NumPy** para los cálculos matemáticos.

## Características

- **Selección de fractal**: Puedes elegir entre generar un fractal de Mandelbrot o uno de Julia desde el menú principal.
- **Zoom y desplazamiento**: Navega a través de los fractales con las teclas:
  - `J` para hacer zoom in.
  - `K` para hacer zoom out.
  - Flechas (`←`, `→`, `↑`, `↓`) para desplazarte en cualquier dirección.
- **Interfaz visual**: La interfaz incluye botones interactivos para seleccionar el tipo de fractal y volver al menú.

## Requisitos

- Python 3.x
- Pygame
- NumPy

## Instalación

1. Clona este repositorio:

    ```bash
    https://github.com/pacoquiroga/FRAGTALES.git
    ```

2. Instala las dependencias:

    ```bash
    pip install pygame numpy
    ```

3. Asegúrate de tener la imagen de fondo `fondo.jpg` en el directorio raíz del proyecto.

## Uso

Ejecuta el siguiente comando para iniciar el programa:

```bash
python fractales.py
