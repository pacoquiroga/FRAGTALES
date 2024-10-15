import pygame
import numpy as np

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fractales en Pygame')

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)
shadow_color = (0, 0, 0, 128)  # Color negro con transparencia

# Fuentes
font = pygame.font.SysFont(None, 40)

# Cargar imagen de fondo
background_image = pygame.image.load('fondo.jpg')  # Asegúrate de tener esta imagen en el directorio de tu proyecto
background_image = pygame.transform.scale(background_image, (width, height))  # Escalar la imagen si es necesario

shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
shadow_surface.fill(shadow_color)

# Parámetros iniciales del fractal
x_min, x_max, y_min, y_max = -2.5, 1.5, -2.0, 2.0
max_iter = 100
zoom_factor = 0.5
pan_factor = 0.1 

# Crear un botón
def draw_button(screen, text, rect, color):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Generar fractal de Mandelbrot
def mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter):
    x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    img = np.zeros(C.shape, dtype=int)

    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        img[mask] += 1

    return img

# Generar fractal de Julia
def julia(c, x_min, x_max, y_min, y_max, width, height, max_iter):
    x, y = np.linspace(x_min, x_max, width), np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    img = np.zeros(Z.shape, dtype=int)

    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask] * Z[mask] + c
        img[mask] += 1

    return img

# Bucle principal
running = True
fractal = None
fractal_selected = None

while running:
    screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo
    screen.blit(shadow_surface, (0, 0)) 

    if fractal_selected is None:
        # Pantalla de selección de fractales
        title_surface = font.render("Fractales en Pygame", True, white)
        screen.blit(title_surface, (width // 2 - title_surface.get_width() // 2, 250))
        mandelbrot_button = pygame.Rect(50, 300, 300, 50)
        julia_button = pygame.Rect(450, 300, 300, 50)
        draw_button(screen, "Mandelbrot", mandelbrot_button, gray)
        draw_button(screen, "Julia", julia_button, gray)
    else:
        # Visualización del fractal seleccionado
        if fractal_selected == "Mandelbrot":
            fractal = mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter)
        elif fractal_selected == "Julia":
            fractal = julia(-0.7 + 0.27015j, x_min, x_max, y_min, y_max, width, height, max_iter)

        fractal_color = np.uint8(255 * fractal / np.max(fractal))
        fractal_color = np.stack([fractal_color]*3, axis=-1)
        pygame.surfarray.blit_array(screen, fractal_color)

        # Botón de regresar al menú
        back_button = pygame.Rect(50, 700, 150, 50)
        draw_button(screen, "Volver", back_button, red)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if fractal_selected is None:
                # Selección de fractal
                if mandelbrot_button.collidepoint(event.pos):
                    fractal_selected = "Mandelbrot"
                elif julia_button.collidepoint(event.pos):
                    fractal_selected = "Julia"
            else:
                if back_button.collidepoint(event.pos):
                    # Regresar al menú principal
                    fractal_selected = None
                    x_min, x_max, y_min, y_max = -2.5, 1.5, -2.0, 2.0
                    max_iter = 100
        elif event.type == pygame.KEYDOWN:
            if fractal_selected is not None:
                if event.key == pygame.K_j:  # Zoom in
                    x_range = (x_max - x_min) * (1 - zoom_factor)
                    y_range = (y_max - y_min) * (1 - zoom_factor)

                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2

                    x_min = x_center - x_range / 2
                    x_max = x_center + x_range / 2
                    y_min = y_center - y_range / 2
                    y_max = y_center + y_range / 2

                    max_iter += 50  # Aumentar iteraciones para mayor detalle

                elif event.key == pygame.K_k:  # Zoom out
                    x_range = (x_max - x_min) * (1 + zoom_factor)
                    y_range = (y_max - y_min) * (1 + zoom_factor)

                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2

                    x_min = x_center - x_range / 2
                    x_max = x_center + x_range / 2
                    y_min = y_center - y_range / 2
                    y_max = y_center + y_range / 2

                    max_iter = max(100, max_iter - 50)  # Reducir iteraciones si es necesario para zoom out
                    
                elif event.key == pygame.K_LEFT:  # Desplazarse a la izquierda
                    pan_amount = (y_max - y_min) * pan_factor
                    y_min -= pan_amount
                    y_max -= pan_amount

                elif event.key == pygame.K_RIGHT:  # Desplazarse a la derecha
                    pan_amount = (y_max - y_min) * pan_factor
                    y_min += pan_amount
                    y_max += pan_amount

                elif event.key == pygame.K_UP:  # Desplazarse hacia arriba
                    pan_amount = (x_max - x_min) * pan_factor
                    x_min -= pan_amount
                    x_max -= pan_amount

                elif event.key == pygame.K_DOWN:  # Desplazarse hacia abajo
                    pan_amount = (x_max - x_min) * pan_factor
                    x_min += pan_amount
                    x_max += pan_amount

pygame.quit()
