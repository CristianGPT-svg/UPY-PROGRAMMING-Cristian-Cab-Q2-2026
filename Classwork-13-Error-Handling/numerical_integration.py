import math

pi = math.pi

# ==========================================
# INPUT
# ==========================================
try:
    a_input = input("Write the left endpoint of the interval (a): ").strip()
    b_input = input("Write the right endpoint of the interval (b): ").strip()
    f_x = input("Write the function to integrate (use 'math.cos(x)', 'x**2', etc.): ").strip()
    method = input("Write the integration method (LRM/RRM/MPM/TM): ").strip().upper()

    try:
        a = float(eval(a_input))
    except Exception:
        raise ValueError("El límite inferior debe ser numérico")

    try:
        b = float(eval(b_input))
    except Exception:
        raise ValueError("El límite superior debe ser numérico")

    if not f_x:
        raise ValueError("La función ingresada no es válida")

    if a >= b:
        raise ValueError("El límite inferior debe ser menor que el límite superior")

    valid_methods = ["LRM", "RRM", "MPM", "TM"]
    if method not in valid_methods:
        raise ValueError("El método de integración no es válido. Usa LRM, RRM, MPM o TM")

except ValueError as e:
    print(f"Input Validation Error: {e}")
    exit()

# Chequeo rápido de la función (sintaxis / variable) antes del cálculo completo
try:
    test_expr = f_x.replace("x", f"({a})")
    float(eval(test_expr))
except ZeroDivisionError:
    pass  # la división entre cero puede ocurrir en otro punto del intervalo; se revisa en el proceso
except NameError:
    print("Input Validation Error: La función debe estar escrita en términos de x")
    exit()
except (SyntaxError, TypeError, AttributeError):
    print("Input Validation Error: La función ingresada no es válida")
    exit()
except Exception:
    print("Input Validation Error: La función ingresada no es válida")
    exit()

# Parameters
n = 1000
h = (b - a) / n
area = 0.0
shift = 0
constant = 0

# ==========================================
# PROCESS
# ==========================================
try:
    if method == "TM":
        f_0 = f_x.replace("x", f"({a})")
        area += (h / 2) * float(eval(f_0))

        for i in range(1, n):
            xi = a + (i * h)
            f_xi = f_x.replace("x", f"({xi})")
            area += (h / 2) * 2 * float(eval(f_xi))

        f_xn = f_x.replace("x", f"({b})")
        area += (h / 2) * float(eval(f_xn))
    else:
        if method == "RRM":
            shift = 1
        if method == "MPM":
            constant = h / 2
        for i in range(shift, n + shift):
            if method == "MPM":
                xi = a + (i * h) + constant
            else:
                xi = a + (i * h)

            height_expr = f_x.replace("x", f"({xi})")
            area += h * float(eval(height_expr))
except ZeroDivisionError:
    print("Mathematical Error: La función no está definida en algún punto del intervalo")
    exit()
except (SyntaxError, NameError, TypeError, AttributeError) as e:
    print(f"Function Evaluation Error: La función ingresada no es válida ({e})")
    exit()
except Exception as e:
    print(f"Unexpected Runtime Error: {e}")
    exit()

# ==========================================
# OUTPUT
# ==========================================
print(f"The integration of {f_x} is {area:.3f}")
