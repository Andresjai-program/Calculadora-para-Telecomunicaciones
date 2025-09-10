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
<<<<<<< HEAD
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
=======
    """Devuelve resultado con valor completo, prefijo SI y notación científica"""
    if value == 0:
        return f"0 {unit} | 0 {unit} | 0 {unit}"

    # Valor completo normal
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

    # Notación científica
    mantissa, exp = f"{value:.6e}".split("e")
    sci = f"{float(mantissa):.6f} × 10^{int(exp)} {unit}"

    return f"{normal}   |   {prefix_text}   |   {sci}"

# ---------- Cálculos ----------
def calc_bandwidth(vals): return vals["Fmax"] - vals["Fmin"], "Hz"
def calc_shannon(vals): return vals["B"] * math.log2(1 + (vals["S"] / vals["N"])), "bits/s"
def calc_noise_power(vals): return K * vals["T"] * vals["B"], "W"
def calc_noise_voltage(vals): return math.sqrt(4 * K * vals["R"] * vals["T"] * vals["B"]), "V"
def calc_noise_factor(vals): return (vals["S_in"] / vals["N_in"]) / (vals["S_out"] / vals["N_out"]), "adim"
def calc_noise_figure(vals): return 10 * math.log10(vals["F"]), "dB"
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)

# ---------- Especificación de fórmulas ----------
FORMULAS = {
    "1. Ancho de banda": {
        "desc": "B = Fmax − Fmin",
<<<<<<< HEAD
        "explain": "Calcula el rango de frecuencias ocupadas por una señal. Un mayor ancho de banda permite transmitir más información.",
=======
        "explain": "Calcula el rango de frecuencias ocupadas por una señal.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("Fmax", "Frecuencia máxima", "Hz"),
                   ("Fmin", "Frecuencia mínima", "Hz")],
        "fn": calc_bandwidth,
        "graph": "bandwidth",
    },
    "2. Límite de Shannon": {
        "desc": "I = B · log₂(1 + S/N)",
<<<<<<< HEAD
        "explain": "Determina la capacidad máxima teórica de un canal (bits/s) según el ancho de banda y la relación señal/ruido. Explica el límite de transmisión sin errores.",
=======
        "explain": "Capacidad máxima teórica de un canal en bits/s.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("B", "Ancho de banda", "Hz"),
                   ("S", "Potencia de señal (S)", "W"),
                   ("N", "Potencia de ruido (N)", "W")],
        "fn": calc_shannon,
        "graph": "shannon",
    },
    "3. Potencia de ruido térmico": {
        "desc": "N = K · T · B",
<<<<<<< HEAD
        "explain": "Calcula la potencia de ruido generada por el movimiento térmico de electrones. Depende de la temperatura (K) y el ancho de banda (Hz).",
=======
        "explain": "Potencia de ruido generada por agitación térmica.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("T", "Temperatura", "K"),
                   ("B", "Ancho de banda", "Hz")],
        "fn": calc_noise_power,
        "graph": "noise_power",
    },
    "4. Voltaje de ruido térmico": {
        "desc": "Vn = √(4 · K · R · T · B)",
<<<<<<< HEAD
        "explain": "Determina el voltaje equivalente del ruido térmico en una resistencia. Es útil para analizar la sensibilidad de receptores y circuitos.",
=======
        "explain": "Voltaje equivalente del ruido térmico en una resistencia.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("R", "Resistencia", "Ω"),
                   ("T", "Temperatura", "K"),
                   ("B", "Ancho de banda", "Hz")],
        "fn": calc_noise_voltage,
        "graph": "noise_voltage",
    },
    "5. Factor de ruido": {
        "desc": "F = (S/N)in / (S/N)out",
<<<<<<< HEAD
        "explain": "Indica cuánto se degrada la relación señal/ruido al pasar por un dispositivo. F=1 sería ideal; valores mayores significan más ruido añadido.",
=======
        "explain": "Degradación de la relación señal/ruido al pasar por un dispositivo.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("S_in", "Señal de entrada (S_in)", "W"),
                   ("N_in", "Ruido de entrada (N_in)", "W"),
                   ("S_out", "Señal de salida (S_out)", "W"),
                   ("N_out", "Ruido de salida (N_out)", "W")],
        "fn": calc_noise_factor,
        "graph": "noise_factor",
    },
    "6. Índice de ruido": {
        "desc": "NF(dB) = 10 · log₁₀(F)",
<<<<<<< HEAD
        "explain": "Convierte el factor de ruido a decibelios (dB). Es la forma estándar de comparar dispositivos: mientras menor sea NF, mejor desempeño.",
=======
        "explain": "Factor de ruido convertido a decibelios.",
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        "fields": [("F", "Factor de ruido (F)", "adim")],
        "fn": calc_noise_figure,
        "graph": "noise_figure",
    },
}

<<<<<<< HEAD
# ---------- Interfaz con CustomTkinter ----------
=======
# ---------- Interfaz ----------
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Comunicaciones")
        self.geometry("750x750")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

<<<<<<< HEAD
        # Título
        ctk.CTkLabel(self, text="📡 Calculadora de Fórmulas", font=("Segoe UI", 22, "bold")).pack(pady=(16, 6))
        ctk.CTkLabel(self, text="Selecciona la operación y completa los campos necesarios.",
                     font=("Segoe UI", 14)).pack(pady=(0, 12))

        # Selector de fórmula
=======
        ctk.CTkLabel(self, text="📡 Calculadora de Fórmulas", font=("Segoe UI", 22, "bold")).pack(pady=(16, 6))
        ctk.CTkLabel(self, text="Selecciona la operación y completa los campos necesarios.", font=("Segoe UI", 14)).pack(pady=(0, 12))

>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        self.combo = ctk.CTkComboBox(self, values=list(FORMULAS.keys()), command=self.on_formula_change, width=420)
        self.combo.set("Elige una fórmula…")
        self.combo.pack(pady=10)

<<<<<<< HEAD
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
=======
        self.desc = ctk.CTkLabel(self, text="", font=("Segoe UI", 14), text_color="#60A5FA")
        self.desc.pack(pady=(5,2))

        self.explain_lbl = ctk.CTkLabel(self, text="", font=("Segoe UI", 12), text_color="#9CA3AF", wraplength=680, justify="left")
        self.explain_lbl.pack(pady=(0,10))

        self.fields_frame = ctk.CTkFrame(self)
        self.fields_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.result_var = ctk.StringVar(value="Resultado: —")
        ctk.CTkLabel(self, textvariable=self.result_var, font=("Segoe UI", 16, "bold")).pack(pady=10)

>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(pady=10)
        ctk.CTkButton(btns, text="Calcular", command=self.calcular).grid(row=0, column=0, padx=8)
        ctk.CTkButton(btns, text="Mostrar gráfica", command=self.mostrar_grafica).grid(row=0, column=1, padx=8)
        ctk.CTkButton(btns, text="Limpiar", command=self.limpiar).grid(row=0, column=2, padx=8)

        self.current_fields = {}

    def on_formula_change(self, _event=None):
<<<<<<< HEAD
        for w in self.fields_frame.winfo_children():
            w.destroy()
=======
        for w in self.fields_frame.winfo_children(): w.destroy()
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
        self.current_fields.clear()
        self.result_var.set("Resultado: —")

        key = self.combo.get()
        spec = FORMULAS[key]
        self.desc.configure(text=spec["desc"])
        self.explain_lbl.configure(text=spec["explain"])

        for (name, label, unit) in spec["fields"]:
<<<<<<< HEAD
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

=======
            row = ctk.CTkFrame(self.fields_frame); row.pack(fill="x", padx=10, pady=6)
            ctk.CTkLabel(row, text=label, width=180, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, placeholder_text=f"{label}..."); entry.pack(side="left", padx=5)
            options = [f"{sym}{info[1]}" for sym, info in PREFIXES.items()]
            prefix_box = ctk.CTkComboBox(row, values=options, width=100)
            prefix_box.set(" (10^0)")
            prefix_box.pack(side="left", padx=5)
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
            ctk.CTkLabel(row, text=unit).pack(side="left")
            self.current_fields[name] = (entry, prefix_box)

    def leer_valores(self):
        vals = {}
        for name, (entry, prefix_box) in self.current_fields.items():
            raw = entry.get().strip()
<<<<<<< HEAD
            if raw == "":
                raise ValueError(f"Falta el valor de '{name}'.")
            selected = prefix_box.get().split()[0]
=======
            if raw == "": raise ValueError(f"Falta el valor de '{name}'.")
            selected = prefix_box.get().split()[0]
            if selected.startswith("("): selected = ""  # caso (10^0)
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
            factor = PREFIXES[selected][0]
            vals[name] = float(raw) * factor
        return vals

    def calcular(self):
        try:
            key = self.combo.get()
<<<<<<< HEAD
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
=======
            if key not in FORMULAS: return
            vals = self.leer_valores()
            result, unit = FORMULAS[key]["fn"](vals)
            self.result_var.set(f"Resultado: {format_result(result, unit)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_grafica(self):
        key = self.combo.get()
        if key not in FORMULAS: return
        vals = self.leer_valores()

        if key == "2. Límite de Shannon":
            B, S, N = vals["B"], vals["S"], vals["N"]
            snr_db = np.linspace(-5, 30, 200)
            snr_lin = 10**(snr_db/10)
            C = B * np.log2(1 + snr_lin)
            plt.figure(); plt.plot(snr_db, C)
            snr_calc_db = 10*math.log10(S/N)
            C_calc = B*math.log2(1+S/N)
            plt.scatter(snr_calc_db, C_calc, color="red", zorder=5)
            plt.xlabel("SNR (dB)"); plt.ylabel("Capacidad (bits/s)")
            plt.title("Capacidad de Shannon vs SNR (B fijo)")
            plt.grid(True); plt.show()

        elif key == "3. Potencia de ruido térmico":
            T, B = vals["T"], vals["B"]
            B_range = np.linspace(max(1.0,0.1*B), 2*B,200)
            N = K*T*B_range
            plt.figure(); plt.plot(B_range,N)
            plt.scatter(B, K*T*B, color="red", zorder=5)
            plt.xlabel("B (Hz)"); plt.ylabel("N (W)")
            plt.title("Potencia de ruido térmico vs Ancho de banda")
            plt.grid(True); plt.show()

        elif key == "4. Voltaje de ruido térmico":
            R,B,T = vals["R"], vals["B"], vals["T"]
            T_range = np.linspace(max(1.0,0.5*T),1.5*T,200)
            Vn = np.sqrt(4*K*R*T_range*B)
            plt.figure(); plt.plot(T_range,Vn)
            plt.scatter(T, math.sqrt(4*K*R*T*B), color="red", zorder=5)
            plt.xlabel("T (K)"); plt.ylabel("Vn (V)")
            plt.title("Voltaje de ruido térmico vs Temperatura")
            plt.grid(True); plt.show()

        elif key == "5. Factor de ruido":
            Sin,Nin,Sout,Nout=vals["S_in"],vals["N_in"],vals["S_out"],vals["N_out"]
            F0=(Sin/Nin)/(Sout/Nout)
            F=np.linspace(max(1.01,0.5*F0),2.0*F0,200)
            NF=10*np.log10(F)
            plt.figure(); plt.plot(F,NF)
            plt.scatter(F0,10*math.log10(F0),color="red",zorder=5)
            plt.xlabel("F (adim)"); plt.ylabel("NF (dB)")
            plt.title("Índice de ruido vs Factor de ruido")
            plt.grid(True); plt.show()

        elif key == "6. Índice de ruido":
            F=vals["F"]; F_range=np.linspace(1.0,max(1.2,2.5*F),200)
            NF=10*np.log10(F_range)
            plt.figure(); plt.plot(F_range,NF)
            plt.scatter(F,10*math.log10(F),color="red",zorder=5)
            plt.xlabel("F (adim)"); plt.ylabel("NF (dB)")
            plt.title("Índice de ruido vs Factor de ruido")
            plt.grid(True); plt.show()

    def limpiar(self):
        for e in self.current_fields.values(): e.delete(0,"end")
        self.result_var.set("Resultado: —")

if __name__=="__main__":
    app=App(); app.mainloop()
>>>>>>> 1c08af4 (Backend calculadora comunicaciones 2.0)
