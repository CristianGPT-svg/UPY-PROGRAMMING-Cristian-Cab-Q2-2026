# ==========================================
# INPUT
# ==========================================
try:
    entrada = input("Introduce el rol con dígito verificador (ej. 123456789-2): ").strip()

    partes = [p.strip() for p in entrada.split("-")]

    if len(partes) != 2 or partes[0] == "" or partes[1] == "":
        raise ValueError("Rol inválido: No tiene el formato XXXXXXXXX-X")

    rol, dv_ingresado = partes

    if not rol.isdigit():
        raise ValueError("Los digitos del rol deben ser numéricos")

    if not (dv_ingresado.isdigit() or dv_ingresado.upper() == "K"):
        raise ValueError("El digito verificador debe ser numérico")

except ValueError as e:
    print(e)
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
    multiplicador = secuencia[i % 6]
    suma_total += rol_invertido[i] * multiplicador

modulo = suma_total % 11
resta = 11 - modulo

if resta == 11:
    dv_esperado = "0"
elif resta == 10:
    dv_esperado = "K"
else:
    dv_esperado = str(resta)

# ==========================================
# OUTPUT
# ==========================================
if dv_ingresado.upper() != dv_esperado:
    print(f"Error: El dígito verificador no conicide, se esperaba {dv_esperado}")
    exit()

print(f"{rol}-{dv_esperado}")
