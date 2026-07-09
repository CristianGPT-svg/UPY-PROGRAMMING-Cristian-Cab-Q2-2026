# INPUT
# ==========================================
pronombres = ['yo', 'tu', 'el', 'nosotros', 'vosotros', 'ellos']

terminaciones = {
    'ar': ['o', 'as', 'a', 'amos', 'ais', 'an'],
    'er': ['o', 'es', 'e', 'emos', 'eis', 'en'],
    'ir': ['o', 'es', 'e', 'imos', 'is', 'en']
}

try:
    verbo = input("Ingrese un verbo regular en infinitivo: ").strip().lower()
    
    if not verbo:
        raise ValueError("La entrada no puede estar vacía.")
        
    if not verbo.isalpha():
        raise ValueError("El verbo debe contener únicamente letras (sin números ni caracteres especiales).")

    if len(verbo) < 3:
        raise ValueError("El verbo ingresado es demasiado corto para ser un infinitivo válido.")

    stem = verbo[:-2]
    ending = verbo[-2:]

    if ending not in terminaciones:
        raise KeyError(f"La terminación '-{ending}' no es válida. El verbo debe terminar en -ar, -er o -ir.")

except (ValueError, KeyError) as e:
    print(f"Error de Validación: {e}")
    exit()

# ==========================================
# PROCESS & OUTPUT
# ==========================================
lista_sufijos = terminaciones[ending]

print(f"\nConjugación en presente para el verbo '{verbo}':")
for i in range(len(pronombres)):
    pronoun = pronombres[i]
    sufijo = lista_sufijos[i]
    print(f"{pronoun.capitalize()} {stem}{sufijo}")
