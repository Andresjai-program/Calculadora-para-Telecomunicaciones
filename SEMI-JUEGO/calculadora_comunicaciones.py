import customtkinter as ctk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
import numpy as np

# Constante de Boltzmann
K = 1.38e-23  

# Prefijos SI con valor y notación
PREFIXES = {
    "": (1, " (10^0)"),        
    "Y": (1e24, " (10^24)"),   
    "Z": (1e21, " (10^21)"),   
    "E": (1e18, " (10^18)"),   
    "P": (1e15, " (10^15)"),   
    "T": (1e12, " (10^12)"),   
    "G": (1e9,  " (10^9)"),    
    "M": (1e6,  " (10^6)"),    
    "k": (1e3,  " (10^3)"),    
    "h": (1e2,  " (10^2)"),    
    "da": (1e1, " (10^1)"),    
    "d": (1e-1, " (10^-1)"),   
    "c": (1e-2, " (10^-2)"),   
    "m": (1e-3, " (10^-3)"),   
    "µ": (1e-6, " (10^-6)"),   
    "n": (1e-9, " (10^-9)"),   
    "p": (1e-12," (10^-12)"),  
    "f": (1e-15," (10^-15)"),  
    "a": (1e-18," (10^-18)"),  
    "z": (1e-21," (10^-21)"),  
    "y": (1e-24," (10^-24)"),  
}

# ---------- Función para formatear resultados ----------
def format_result(value, unit):
    """Devuelve resultado con prefijo SI y notación científica (×10^n)"""
    if value == 0:
        return f"0 {unit}"

    # buscar prefijo adecuado
    for symbol, (factor, _) in sorted(PREFIXES.items(), key=lambda x: -x[1][0]):
        if factor != 1 and abs(value) >= factor:
            scaled = value / factor
            mantissa, exp = f"{value:.3e}".split("e")
            exp = int(exp)
            sci = f"{float(mantissa):.3f} × 10^{exp}"
            return f"{scaled:.3f} {symbol}{unit}   |   {sci} {unit}"

    mantissa, exp = f"{value:.3e}".split("e")
    exp = int(exp)
    sci = f"{float(mantissa):.3f} × 10^{exp}"
    return f"{value:.6f} {unit}   |   {sci} {unit}"

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
        "desc": "B = Fmax − Fmin",
        "explain": "Calcula el rango de frecuencias ocupadas por una señal. Un mayor ancho de banda permite transmitir más información.",
        "fields": [("Fmax", "Frecuencia máxima", "Hz"),
                   ("Fmin", "Frecuencia mínima", "Hz")],
        "fn": calc_bandwidth,
        "graph": "bandwidth",
    },
    "2. Límite de Shannon": {
        "desc": "I = B · log₂(1 + S/N)",
        "explain": "Determina la capacidad máxima teórica de un canal (bits/s) según el ancho de banda y la relación señal/ruido. Explica el límite de transmisión sin errores.",
        "fields": [("B", "Ancho de banda", "Hz"),
                   ("S", "Potencia de señal (S)", "W"),
                   ("N", "Potencia de ruido (N)", "W")],
        "fn": calc_shannon,
        "graph": "shannon",
    },
    "3. Potencia de ruido térmico": {
        "desc": "N = K · T · B",
        "explain": "Calcula la potencia de ruido generada por el movimiento térmico de electrones. Depende de la temperatura (K) y el ancho de banda (Hz).",
        "fields": [("T", "Temperatura", "K"),
                   ("B", "Ancho de banda", "Hz")],
        "fn": calc_noise_power,
        "graph": "noise_power",
    },
    "4. Voltaje de ruido térmico": {
        "desc": "Vn = √(4 · K · R · T · B)",
        "explain": "Determina el voltaje equivalente del ruido térmico en una resistencia. Es útil para analizar la sensibilidad de receptores y circuitos.",
        "fields": [("R", "Resistencia", "Ω"),
                   ("T", "Temperatura", "K"),
                   ("B", "Ancho de banda", "Hz")],
        "fn": calc_noise_voltage,
        "graph": "noise_voltage",
    },
    "5. Factor de ruido": {
        "desc": "F = (S/N)in / (S/N)out",
        "explain": "Indica cuánto se degrada la relación señal/ruido al pasar por un dispositivo. F=1 sería ideal; valores mayores significan más ruido añadido.",
        "fields": [("S_in", "Señal de entrada (S_in)", "W"),
                   ("N_in", "Ruido de entrada (N_in)", "W"),
                   ("S_out", "Señal de salida (S_out)", "W"),
                   ("N_out", "Ruido de salida (N_out)", "W")],
        "fn": calc_noise_factor,
        "graph": "noise_factor",
    },
    "6. Índice de ruido": {
        "desc": "NF(dB) = 10 · log₁₀(F)",
        "explain": "Convierte el factor de ruido a decibelios (dB). Es la forma estándar de comparar dispositivos: mientras menor sea NF, mejor desempeño.",
        "fields": [("F", "Factor de ruido (F)", "adim")],
        "fn": calc_noise_figure,
        "graph": "noise_figure",
    },
}

# ---------- Interfaz con CustomTkinter ----------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Comunicaciones")
        self.geometry("750x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Título
        ctk.CTkLabel(self, text="📡 Calculadora de Fórmulas", font=("Segoe UI", 22, "bold")).pack(pady=(16, 6))
        ctk.CTkLabel(self, text="Selecciona la operación y completa los campos necesarios.",
                     font=("Segoe UI", 14)).pack(pady=(0, 12))

        # Selector de fórmula
        self.combo = ctk.CTkComboBox(self, values=list(FORMULAS.keys()), command=self.on_formula_change, width=420)
        self.combo.set("Elige una fórmula…")
        self.combo.pack(pady=10)

        # Descripción (ecuación)
        self.desc = ctk.CTkLabel(self, text="", font=("Segoe UI", 14), text_color="#60A5FA")
        self.desc.pack(pady=(5,2))

        # Explicación (texto adicional)
        self.explain_lbl = ctk.CTkLabel(self, text="", font=("Segoe UI", 12), text_color="#9CA3AF", wraplength=680, justify="left")
        self.explain_lbl.pack(pady=(0,10))

        # Frame para campos
        self.fields_frame = ctk.CTkFrame(self)
        self.fields_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Resultado
        self.result_var = ctk.StringVar(value="Resultado: —")
        self.result_lbl = ctk.CTkLabel(self, textvariable=self.result_var, font=("Segoe UI", 16, "bold"))
        self.result_lbl.pack(pady=10)

        # Botones
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Calcular", command=self.calcular).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btns, text="Mostrar gráfica", command=self.mostrar_grafica).grid(row=0, column=1, padx=8)
        ctk.CTkButton(btns, text="Limpiar", command=self.limpiar).grid(row=0, column=2, padx=8)

        self.current_fields = {}

    def on_formula_change(self, _event=None):
        for w in self.fields_frame.winfo_children():
            w.destroy()
        self.current_fields.clear()
        self.result_var.set("Resultado: —")

        key = self.combo.get()
        spec = FORMULAS[key]
        self.desc.configure(text=spec["desc"])
        self.explain_lbl.configure(text=spec["explain"])

        for (name, label, unit) in spec["fields"]:
            row = ctk.CTkFrame(self.fields_frame)
            row.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(row, text=label, width=180, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, placeholder_text=f"{label}...")
            entry.pack(side="left", padx=5)

            # Prefijos mostrados con símbolo y notación
            options = [f"{sym}{info[1]}" for sym, info in PREFIXES.items()]
            prefix_box = ctk.CTkComboBox(row, values=options, width=100)
            prefix_box.set(" (10^0)")  
            prefix_box.pack(side="left", padx=5)

            ctk.CTkLabel(row, text=unit).pack(side="left")
            self.current_fields[name] = (entry, prefix_box)

    def leer_valores(self):
        vals = {}
        for name, (entry, prefix_box) in self.current_fields.items():
            raw = entry.get().strip()
            if raw == "":
                raise ValueError(f"Falta el valor de '{name}'.")
            selected = prefix_box.get().split()[0]
            factor = PREFIXES[selected][0]
            vals[name] = float(raw) * factor
        return vals

    def calcular(self):
        try:
            key = self.combo.get()
            if key not in FORMULAS:
                messagebox.showwarning("Atención", "Selecciona una fórmula.")
                return
            vals = self.leer_valores()
            result, unit = FORMULAS[key]["fn"](vals)
            txt = format_result(result, unit)
            self.result_var.set(f"Resultado: {txt}")
        except ValueError as ve:
            messagebox.showerror("Datos incompletos", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def mostrar_grafica(self):
        key = self.combo.get()
        if key not in FORMULAS:
            messagebox.showwarning("Atención", "Selecciona una fórmula.")
            return
        try:
            vals = self.leer_valores()
        except Exception as e:
            messagebox.showerror("Datos faltantes", str(e))
            return

        if FORMULAS[key]["graph"] == "shannon":
            B = vals["B"]
            snr_db = np.linspace(-20, 30, 200) 
            snr_lin = 10 ** (snr_db / 10)
            C = B * np.log2(1 + snr_lin)
            plt.figure()
            plt.plot(snr_db, C)
            plt.xlabel("SNR (dB)")
            plt.ylabel("Capacidad (bits/s)")
            plt.title("Capacidad de Shannon vs SNR (B fijo)")
            plt.grid(True)
            plt.show()

        elif FORMULAS[key]["graph"] == "noise_power":
            T = vals["T"]
            B = np.linspace(max(1.0, 0.1 * vals["B"]), 2 * vals["B"], 200)
            N = K * T * B
            plt.figure()
            plt.plot(B, N)
            plt.xlabel("B (Hz)")
            plt.ylabel("N (W)")
            plt.title("Potencia de ruido térmico vs Ancho de banda (T fijo)")
            plt.grid(True)
            plt.show()

        elif FORMULAS[key]["graph"] == "noise_voltage":
            R = vals["R"]; B = vals["B"]
            T = np.linspace(max(1.0, 0.5 * vals["T"]), 1.5 * vals["T"], 200)
            Vn = np.sqrt(4 * K * R * T * B)
            plt.figure()
            plt.plot(T, Vn)
            plt.xlabel("Temperatura (K)")
            plt.ylabel("Vn (V)")
            plt.title("Voltaje de ruido térmico vs Temperatura (R y B fijos)")
            plt.grid(True)
            plt.show()

        elif FORMULAS[key]["graph"] == "noise_factor":
            Sin, Nin, Sout, Nout = vals["S_in"], vals["N_in"], vals["S_out"], vals["N_out"]
            F0 = (Sin / Nin) / (Sout / Nout)
            F = np.linspace(max(1.01, 0.5 * F0), 2.0 * F0, 200)
            NF = 10 * np.log10(F)
            plt.figure()
            plt.plot(F, NF)
            plt.axvline(F0, color="red", linestyle="--")
            plt.axhline(10 * math.log10(F0), color="red", linestyle="--")
            plt.xlabel("F (adimensional)")
            plt.ylabel("NF (dB)")
            plt.title("Índice de ruido vs Factor de ruido")
            plt.grid(True)
            plt.show()

        elif FORMULAS[key]["graph"] == "noise_figure":
            F = np.linspace(1.0, max(1.2, 2.5 * vals["F"]), 200)
            NF = 10 * np.log10(F)
            plt.figure()
            plt.plot(F, NF)
            plt.axvline(vals["F"], color="red", linestyle="--")
            plt.axhline(10 * math.log10(vals["F"]), color="red", linestyle="--")
            plt.xlabel("F (adimensional)")
            plt.ylabel("NF (dB)")
            plt.title("Índice de ruido vs Factor de ruido")
            plt.grid(True)
            plt.show()

        else:
            messagebox.showinfo("Sin gráfica", "Esta fórmula no tiene gráfica asociada.")

    def limpiar(self):
        for e in self.current_fields.values():
            e.delete(0, "end")
        self.result_var.set("Resultado: —")

if __name__ == "__main__":
    app = App()
    app.mainloop()
