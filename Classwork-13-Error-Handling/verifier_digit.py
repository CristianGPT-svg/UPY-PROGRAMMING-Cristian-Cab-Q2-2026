# INPUT
# ==========================================
try:
    rol_input = input("Introduce el rol (ej. 201012341): ").strip()
    
    if not rol_input:
        raise ValueError("El campo de entrada no puede estar vacío.")
        
    if not rol_input.isdigit():
        raise ValueError("El rol debe contener únicamente caracteres numéricos (0-9).")

    rol = rol_input

except ValueError as e:
    print(f"Error de Validación de Entrada: {e}")
    exit()

# ==========================================
# PROCESS
# ==========================================
rol_invertido = []
for digito in rol[::-1]:
    rol_invertido.append(int(digito))

secuencia = [2, 3, 4, 5, 6, 7]
suma_total = 0

for i in range(len(rol_invertido)):
    multiplicador = sequence = secuencia[i % 6]
    suma_total += rol_invertido[i] * multiplicador

modulo = suma_total % 11
resta = 11 - modulo

if resta == 11:
    dv = "0"
elif resta == 10:
    dv = "K"
else:
    dv = str(resta)

# ==========================================
# OUTPUT
# ==========================================
print(f"Resultado: {rol}-{dv}")
