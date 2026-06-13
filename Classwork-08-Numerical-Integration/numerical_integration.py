import math

# =========================================================
# Numerical Integration Tool
# Methods: LRM (Left), RRM (Right), MRM (Midpoint), TRAP (Trapezoid)
# =========================================================

# INPUT
a = input("Write the left endpoint of the interval: ")
b = input("Write the right endpoint of the interval: ")
f_x = input("Write the function to integrate (use 'X' as the variable, e.g. math.sin(X)): ")
method = input("Write the integration method (LRM/RRM/MRM/TRAP): ")
mode = input("Choose mode - Default/Custom/Auto (D/C/A): ")
exact = float(input("Write the exact value of the integral (for error comparison): "))

if mode == "C":
    n = int(input("Write the number of subintervals (n): "))

if mode == "A":
    threshold = float(input("Write the target relative error (%): "))


# PROCESS

# --- Convert interval endpoints (allow 'pi' in the expression) ---
if "pi" in a:
    a = eval(a.replace("pi", str(math.pi)))
else:
    a = float(a)

if "pi" in b:
    b = eval(b.replace("pi", str(math.pi)))
else:
    b = float(b)


# --- Function that computes the integral for a given n ---
def integrate(a, b, f_x, method, n):
    h = (b - a) / n
    area = 0.0
    constant = 0
    shift = 0

    if method == "RRM":
        shift = 1

    if method == "MRM":
        constant = h / 2

    if method == "TRAP":
        f_0 = f_x.replace("X", str(a))
        area += (h / 2) * eval(f_0)

        for i in range(1, n):
            xi = a + i * h
            f_xi = f_x.replace("X", str(xi))
            area += (h / 2) * 2 * eval(f_xi)

        f_xn = f_x.replace("X", str(b))
        area += (h / 2) * eval(f_xn)

    else:
        for i in range(shift, n + shift):
            xi = a + i * h
            height = f_x.replace("X", str(xi + constant))
            area += h * eval(height)

    return area


# --- Mode selection ---
if mode == "D":
    # Default mode: fixed n = 100
    n = 100
    area = integrate(a, b, f_x, method, n)

elif mode == "C":
    # Custom mode: n was already provided in the INPUT section
    area = integrate(a, b, f_x, method, n)

else:
    # Auto-adjust mode: increase n until the relative error meets the threshold
    n = 10
    area = integrate(a, b, f_x, method, n)
    rel_error = abs(exact - area) / abs(exact) * 100

    while rel_error > threshold:
        n = n * 2
        area = integrate(a, b, f_x, method, n)
        rel_error = abs(exact - area) / abs(exact) * 100


# --- Error calculation ---
abs_error = abs(exact - area)
rel_error = abs(exact - area) / abs(exact) * 100


# OUTPUT
print(f"\nThe integral of {f_x} from {a} to {b} using {method} with n = {n} is: {area}")
print(f"Exact value: {exact}")
print(f"Absolute error: {abs_error}")
print(f"Relative error: {rel_error} %")
