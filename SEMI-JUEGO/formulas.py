import math

# Constante de Boltzmann
K = 1.38e-23

# Prefijos SI con valor y notación (para referencia del frontend)
PREFIXES = {
    "": (1, " (10^0)"),
    "Y": (1e24, " (10^24)"),
    "Z": (1e21, " (10^21)"),
    "E": (1e18, " (10^18)"),
    "P": (1e15, " (10^15)"),
    "T": (1e12, " (10^12)"),
    "G": (1e9, " (10^9)"),
    "M": (1e6, " (10^6)"),
    "k": (1e3, " (10^3)"),
    "h": (1e2, " (10^2)"),
    "da": (1e1, " (10^1)"),
    "d": (1e-1, " (10^-1)"),
    "c": (1e-2, " (10^-2)"),
    "m": (1e-3, " (10^-3)"),
    "µ": (1e-6, " (10^-6)"),
    "n": (1e-9, " (10^-9)"),
    "p": (1e-12, " (10^-12)"),
    "f": (1e-15, " (10^-15)"),
    "a": (1e-18, " (10^-18)"),
    "z": (1e-21, " (10^-21)"),
    "y": (1e-24, " (10^-24)"),
}


def format_result(value: float, unit: str) -> str:
    """Devuelve resultado con valor completo, prefijo SI y notación científica."""
    if value == 0:
        return f"0 {unit}   |   0 {unit}   |   0 {unit}"

    normal = f"{value:.6f} {unit}"

    # Prefijo SI adecuado
    prefix_text = ""
    for symbol, (factor, _) in sorted(PREFIXES.items(), key=lambda x: -x[1][0]):
        if factor != 1 and abs(value) >= factor:
            scaled = value / factor
            prefix_text = f"{scaled:.3f} {symbol}{unit}"
            break
    if prefix_text == "":
        prefix_text = f"{value:.6f} {unit}"

    mantissa, exp = f"{value:.6e}".split("e")
    sci = f"{float(mantissa):.6f} × 10^{int(exp)} {unit}"

    return f"{normal}   |   {prefix_text}   |   {sci}"


# ---------- Cálculos ----------
def calc_bandwidth(vals):
    return vals["Fmax"] - vals["Fmin"], "Hz"


def calc_shannon(vals):
    return vals["B"] * math.log2(1 + (vals["S"] / vals["N"])), "bits/s"


def calc_noise_power(vals):
    return K * vals["T"] * vals["B"], "W"


def calc_noise_voltage(vals):
    return math.sqrt(4 * K * vals["R"] * vals["T"] * vals["B"]), "V"


def calc_noise_factor(vals):
    return (vals["S_in"] / vals["N_in"]) / (vals["S_out"] / vals["N_out"]), "adim"


def calc_noise_figure(vals):
    return 10 * math.log10(vals["F"]), "dB"


# ---------- Especificación de fórmulas ----------
FORMULAS = {
    "1. Ancho de banda": {
        "key": "bandwidth",
        "desc": "B = Fmax − Fmin",
        "explain": "Calcula el rango de frecuencias ocupadas por una señal.",
        "fields": [
            ("Fmax", "Frecuencia máxima", "Hz"),
            ("Fmin", "Frecuencia mínima", "Hz"),
        ],
        "fn": calc_bandwidth,
    },
    "2. Límite de Shannon": {
        "key": "shannon",
        "desc": "I = B · log₂(1 + S/N)",
        "explain": "Capacidad máxima teórica de un canal en bits/s.",
        "fields": [
            ("B", "Ancho de banda", "Hz"),
            ("S", "Potencia de señal (S)", "W"),
            ("N", "Potencia de ruido (N)", "W"),
        ],
        "fn": calc_shannon,
    },
    "3. Potencia de ruido térmico": {
        "key": "noise_power",
        "desc": "N = K · T · B",
        "explain": "Potencia de ruido generada por agitación térmica.",
        "fields": [
            ("T", "Temperatura", "K"),
            ("B", "Ancho de banda", "Hz"),
        ],
        "fn": calc_noise_power,
    },
    "4. Voltaje de ruido térmico": {
        "key": "noise_voltage",
        "desc": "Vn = √(4 · K · R · T · B)",
        "explain": "Voltaje equivalente del ruido térmico en una resistencia.",
        "fields": [
            ("R", "Resistencia", "Ω"),
            ("T", "Temperatura", "K"),
            ("B", "Ancho de banda", "Hz"),
        ],
        "fn": calc_noise_voltage,
    },
    "5. Factor de ruido": {
        "key": "noise_factor",
        "desc": "F = (S/N)in / (S/N)out",
        "explain": "Degradación de la relación señal/ruido al pasar por un dispositivo.",
        "fields": [
            ("S_in", "Señal de entrada (S_in)", "W"),
            ("N_in", "Ruido de entrada (N_in)", "W"),
            ("S_out", "Señal de salida (S_out)", "W"),
            ("N_out", "Ruido de salida (N_out)", "W"),
        ],
        "fn": calc_noise_factor,
    },
    "6. Índice de ruido": {
        "key": "noise_figure",
        "desc": "NF(dB) = 10 · log₁₀(F)",
        "explain": "Factor de ruido convertido a decibelios.",
        "fields": [
            ("F", "Factor de ruido (F)", "adim"),
        ],
        "fn": calc_noise_figure,
    },
}


def list_formulas_for_api():
    """Devuelve metadatos de fórmulas sin funciones, serializables a JSON."""
    items = []
    for title, spec in FORMULAS.items():
        items.append(
            {
                "title": title,
                "id": spec["key"],
                "desc": spec["desc"],
                "explain": spec["explain"],
                "fields": [
                    {"name": n, "label": l, "unit": u} for (n, l, u) in spec["fields"]
                ],
            }
        )
    return items


def calculate_by_id(formula_id: str, values: dict):
    """Calcula por identificador estable y devuelve dict con resultado y unidad."""
    for _title, spec in FORMULAS.items():
        if spec["key"] == formula_id:
            result, unit = spec["fn"](values)
            return {
                "value": result,
                "unit": unit,
                "display": format_result(result, unit),
            }
    raise ValueError("Fórmula no encontrada")


