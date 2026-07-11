# ==========================================
# INPUT
# ==========================================
pronombres = ['yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos']
terminaciones = {
    'ar': ['o', 'as', 'a', 'amos', 'ais', 'an'],
    'er': ['o', 'es', 'e', 'emos', 'eis', 'en'],
    'ir': ['o', 'es', 'e', 'imos', 'is', 'en']
}

try:
    verbo = input("Ingrese un verbo regular en infinitivo: ")

    if verbo != verbo.strip():
        raise ValueError("El verbo no debe tener espacios extra")

    if verbo != verbo.lower():
        raise ValueError("El verbo debe escribirse en minúsculas")

    stem = verbo[:-2]
    ending = verbo[-2:]
    lista_sufijos = terminaciones[ending]

except ValueError as e:
    print(f"Error de Validación: {e}")
    exit()
except KeyError:
    print("Error de Validación: El verbo debe terminar en ar, er o ir")
    exit()

# ==========================================
# PROCESS & OUTPUT
# ==========================================
print(f"\nConjugación en presente para el verbo '{verbo}':")
for i in range(len(pronombres)):
    pronoun = pronombres[i]
    sufijo = lista_sufijos[i]
    print(f"{pronoun.capitalize()} {stem}{sufijo}")
