rol = input("Ingrese el rol sin guión ni dígito verificador: ")

rol_invertido = rol[::-1]

secuencia = [2, 3, 4, 5, 6, 7]
suma = 0
for i, digito in enumerate(rol_invertido):
    factor = secuencia[i % len(secuencia)]
    suma += int(digito) * factor

modulo = suma % 11
digito_verificador = 11 - modulo

print(f"Suma: {suma}")
print(f"Módulo 11: {modulo}")
print(f"Dígito verificador: {digito_verificador}")
print(f"Rol completo: {rol}-{digito_verificador}")
