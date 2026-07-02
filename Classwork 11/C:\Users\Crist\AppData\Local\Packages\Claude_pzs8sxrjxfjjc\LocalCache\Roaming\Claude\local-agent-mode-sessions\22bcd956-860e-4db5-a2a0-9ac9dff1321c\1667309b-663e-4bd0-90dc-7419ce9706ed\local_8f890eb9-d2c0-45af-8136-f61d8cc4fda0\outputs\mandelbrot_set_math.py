# ============================================================
# Classwork #11 - The Mandelbrot Set
# ============================================================

# ============================================================
# MODE SELECTION
# Three modes select different viewing regions of the set.
# Each mode writes its own config.txt before running.
# ============================================================

print("=" * 50)
print("       Mandelbrot Set Generator")
print("=" * 50)
print("  Mode 1 - Full View (default Mandelbrot window)")
print("  Mode 2 - Zoomed View (detail of main cardioid)")
print("  Mode 3 - Mini Brot  (small copy near real axis)")
print("=" * 50)

# INPUT - Repeat until user picks a valid mode
while True:
    modo_input = input("Select mode (1, 2 or 3): ").strip()
    if modo_input in ('1', '2', '3'):
        modo = int(modo_input)
        break
    print("  Invalid. Enter 1, 2, or 3.")

# ============================================================
# STEP 1 — Write config.txt for the chosen mode, then read it
# ============================================================

# PROCESS - Write config.txt based on selected mode
if modo == 1:
    # Full Mandelbrot view
    cfg_content = (
        "ancho=200\n"
        "alto=200\n"
        "real_min=-2.0\n"
        "real_max=1.0\n"
        "imag_min=-1.5\n"
        "imag_max=1.5\n"
        "max_iter=100\n"
    )
elif modo == 2:
    # Zoomed into the main cardioid / bulb boundary
    cfg_content = (
        "ancho=200\n"
        "alto=200\n"
        "real_min=-0.8\n"
        "real_max=-0.6\n"
        "imag_min=0.0\n"
        "imag_max=0.2\n"
        "max_iter=200\n"
    )
else:
    # Mini Mandelbrot copy near real axis
    cfg_content = (
        "ancho=200\n"
        "alto=200\n"
        "real_min=-1.8\n"
        "real_max=-1.6\n"
        "imag_min=-0.1\n"
        "imag_max=0.1\n"
        "max_iter=300\n"
    )

# OUTPUT - Save selected config to file
cfg_file = open('config.txt', 'w')
cfg_file.write(cfg_content)
cfg_file.close()

print("\nMode " + str(modo) + " config written to config.txt")

# ============================================================
# STEP 1 — Read the Config File
# ============================================================

# INPUT - Open config.txt and load all key=value pairs
config = {}
archivo = open('config.txt', 'r')
for linea in archivo:
    clave, valor = linea.strip().split('=')
    config[clave] = float(valor)
archivo.close()

print("Config loaded: " + str(config))

# ============================================================
# STEP 2 — Map Pixels to Complex Numbers
# STEP 3 — Iterate and Count
# STEP 4 — Write to CSV
# ============================================================

# PROCESS - Extract grid dimensions and iteration limit
ancho    = int(config['ancho'])
alto     = int(config['alto'])
max_iter = int(config['max_iter'])

# OUTPUT - Open CSV output file and write header
salida = open('mandelbrot.csv', 'w')
salida.write('fila,columna,iteraciones\n')

print("Computing " + str(alto) + "x" + str(ancho) + " grid (" + str(alto * ancho) + " points)...")

# PROCESS - Iterate over every pixel in the grid
for fila in range(alto):
    for columna in range(ancho):

        # PROCESS - Map (fila, columna) to a point c on the complex plane
        #   columna → real axis
        #   fila    → imaginary axis
        real = config['real_min'] + (columna / ancho) * (config['real_max'] - config['real_min'])
        imag = config['imag_min'] + (fila    / alto)  * (config['imag_max'] - config['imag_min'])
        c    = complex(real, imag)

        # PROCESS - Mandelbrot iteration: z_{n+1} = z_n^2 + c, starting at z = 0
        z           = 0 + 0j
        iteraciones = 0

        while abs(z) <= 2 and iteraciones < max_iter:
            z           = z * z + c
            iteraciones += 1

        # OUTPUT - Write pixel row to CSV
        salida.write(f'{fila},{columna},{iteraciones}\n')

# PROCESS - Close output file
salida.close()

# OUTPUT - Done message
print("Done. " + str(alto * ancho) + " points written to mandelbrot.csv")
