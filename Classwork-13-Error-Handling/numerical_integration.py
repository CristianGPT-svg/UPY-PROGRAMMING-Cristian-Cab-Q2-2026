import math
# INPUT
pi = math.pi

try:
    a_input = input("Write the left endpoint of the interval (a): ").strip()
    b_input = input("Write the right endpoint of the interval (b): ").strip()
    f_x = input("Write the function to integrate (use 'math.cos(x)', 'x**2', etc.): ").strip()
    method = input("Write the integration method (LRM/RRM/MRM/TRAP): ").strip().upper()

    # Validación y evaluación segura de los límites
    try:
        a = float(eval(a_input))
        b = float(eval(b_input))
    except (ValueError, SyntaxError, NameError, TypeError):
        raise ValueError("The endpoints 'a' and 'b' must be valid numerical constants or expressions (e.g., '2*math.pi').")

    if a >= b:
        raise ValueError("The left endpoint (a) must be strictly less than the right endpoint (b).")

    valid_methods = ["LRM", "RRM", "MRM", "TRAP"]
    if method not in valid_methods:
        raise ValueError(f"Unknown integration method '{method}'. Valid options are: {', '.join(valid_methods)}")

    if not f_x:
        raise ValueError("The mathematical function field cannot be empty.")

except ValueError as e:
    print(f"Input Validation Error: {e}")
    exit()

# Parameters
n = 1000
h = (b - a) / n
area = 0.0
shift = 0
constant = 0
variable = 0

# ==========================================
# PROCESS
# ==========================================
try:
    if method == "TRAP":
        variable = 1
        
        # Evaluar de forma segura f(a)
        f_0 = f_x.replace("x", f"({a})")
        area += (h / 2) * float(eval(f_0))
        
        # Evaluar términos intermedios
        for i in range(variable, n):
            xi = a + (i * h)
            f_xi = f_x.replace("x", f"({xi})")
            area += (h / 2) * 2 * float(eval(f_xi))
            
        # Evaluar f(b)
        f_xn = f_x.replace("x", f"({b})")
        area += (h / 2) * float(eval(f_xn)) 

    else:
        if method == "RRM":
            shift = 1
        if method == "MRM":
            constant = h / 2

        for i in range(shift, n + shift):
            if method == "MRM":
                xi = a + (i * h) + constant
            else:
                xi = a + (i * h)
                
            height_expr = f_x.replace("x", f"({xi})")
            area += h * float(eval(height_expr))

except ZeroDivisionError:
    print("Mathematical Error: Division by zero encountered during function evaluation in the interval.")
    exit()
except (SyntaxError, NameError, TypeError) as e:
    print(f"Function Evaluation Error: The expression '{f_x}' contains invalid syntax or unknown functions. ({e})")
    exit()
except Exception as e:
    print(f"Unexpected Runtime Error: {e}")
    exit()

# ==========================================
# OUTPUT
# ==========================================
print(f"The approximate integration of f(x) = {f_x} is: {area:.6f}")
