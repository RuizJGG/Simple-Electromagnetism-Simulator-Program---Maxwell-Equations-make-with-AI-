import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class MaxwellSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Simulador Mágico das Equações de Maxwell ✨")
        self.root.geometry("1100x700")
        self.root.configure(bg="#ffe6f0")  # Fundo rosa clarinho

        # Estilo
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5, background="#ffccd5", foreground="#ff6699")
        style.configure("TLabel", font=("Arial", 12), background="#ffe6f0")

        # Título com Easter Egg
        self.title_label = tk.Label(root, text="🌸 Simulador Dinâmico das Equações de Maxwell 🌸", 
                                    font=("Arial", 18, "bold"), bg="#ffe6f0", fg="#ff6699")
        self.title_label.pack(pady=10)
        self.title_label.bind("<Button-1>", self.show_easter_egg)  # Clique no título ativa o Easter Egg

        # Frame principal
        main_frame = ttk.Frame(root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Painel de controle à esquerda
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side="left", padx=10, fill="y")

        ttk.Label(control_frame, text="✨ Escolha uma Equação! ✨", font=("Arial", 16, "italic"), 
                  background="#ffe6f0", foreground="#ff99cc").pack(pady=5)
        self.buttons = [
            ("1. Lei de Gauss (Elétrica) 💫", self.simular_gauss_eletrica),
            ("2. Lei de Gauss (Magnética) 🌟", self.simular_gauss_magnetica),
            ("3. Lei de Faraday ⚡️", self.simular_faraday),
            ("4. Lei de Ampère-Maxwell 🌈", self.simular_ampere_maxwell)
        ]
        for text, command in self.buttons:
            ttk.Button(control_frame, text=text, command=command).pack(fill="x", pady=5)

        # Área de texto explicativo
        self.info_text = tk.Text(control_frame, height=15, width=35, font=("Arial", 12), 
                                 bg="#ffccd5", fg="#ed0e0e", wrap="word")
        self.info_text.pack(pady=10)
        self.info_text.insert("end", "💖 Selecione uma equação para simular em tempo real.\n\n"
                                     "✨ Ajuste os sliders para ver mudanças instantâneas! ✨")
        self.info_text.config(state="disabled")

        # Área de controles adicionais
        self.control_panel = ttk.Frame(control_frame)
        self.control_panel.pack(pady=10)

        # Área de gráficos à direita
        self.graph_frame = ttk.Frame(main_frame)
        self.graph_frame.pack(side="right", fill="both", expand=True)

        # Variáveis globais para animação
        self.ani = None

    def show_easter_egg(self, event):
        messagebox.showinfo("Easter Egg", "Feito para a Gatinha 😻!")

    def limpar_grafico(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        for widget in self.control_panel.winfo_children():
            widget.destroy()

    def atualizar_texto(self, texto):
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("end", texto)
        self.info_text.config(state="disabled")

    def simular_gauss_eletrica(self):
        self.limpar_grafico()
        texto = ("∇·E = ρ/ε₀\n\n"
                 "A Lei de Gauss para eletricidade relaciona o campo elétrico (E) à densidade de carga (ρ). "
                 "O fluxo de E é proporcional à carga. "
                 "Simulação: Campo radial de uma carga. Ajuste a carga (q) em tempo real.")
        self.atualizar_texto(texto)

        # Sliders
        self.carga_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_panel, text="💖 Carga (q): -5 a 5").pack()
        ttk.Scale(self.control_panel, from_=-5, to=5, variable=self.carga_var, orient="horizontal").pack(fill="x")

        self.plot_gauss_eletrica()

    def plot_gauss_eletrica(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        x, y = np.meshgrid(np.linspace(-5, 5, 20), np.linspace(-5, 5, 20))
        r = np.sqrt(x**2 + y**2)
        r[r == 0] = 0.1

        quiver = ax.quiver(x, y, x, y, color="blue")  # Placeholder inicial
        ax.set_title("Campo Elétrico Dinâmico 💫", fontsize=14)
        ax.set_xlabel("x (m)", fontsize=12)
        ax.set_ylabel("y (m)", fontsize=12)
        ax.grid(True)

        def update(frame):
            q = self.carga_var.get()
            Ex = q * x / r**3
            Ey = q * y / r**3
            quiver.set_UVC(Ex, Ey)
            ax.set_title(f"Campo Elétrico (q = {q:.1f} C) 💫", fontsize=14)
            return quiver,

        self.ani = FuncAnimation(fig, update, frames=range(100), interval=100, blit=True)
        canvas.draw()

    def simular_gauss_magnetica(self):
        self.limpar_grafico()
        texto = ("∇·B = 0\n\n"
                 "A Lei de Gauss para magnetismo diz que o campo magnético (B) não tem fontes ou sumidouros. "
                 "Mostra a natureza dipolar do magnetismo. "
                 "Simulação: Campo de um dipolo. Ajuste o momento magnético (m).")
        self.atualizar_texto(texto)

        # Sliders
        self.momento_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_panel, text="🌟 Momento Magnético (m): 0 a 5").pack()
        ttk.Scale(self.control_panel, from_=0, to=5, variable=self.momento_var, orient="horizontal").pack(fill="x")

        self.plot_gauss_magnetica()

    def plot_gauss_magnetica(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        x, y = np.meshgrid(np.linspace(-5, 5, 20), np.linspace(-5, 5, 20))
        r = np.sqrt(x**2 + y**2)
        r[r == 0] = 0.1

        quiver = ax.quiver(x, y, x, y, color="green")  # Placeholder inicial
        ax.set_title("Campo Magnético Dinâmico 🌟", fontsize=14)
        ax.set_xlabel("x (m)", fontsize=12)
        ax.set_ylabel("y (m)", fontsize=12)
        ax.grid(True)

        def update(frame):
            m = self.momento_var.get()
            Bx = m * (-y / r**3)
            By = m * (x / r**3)
            quiver.set_UVC(Bx, By)
            ax.set_title(f"Campo Magnético (m = {m:.1f}) 🌟", fontsize=14)
            return quiver,

        self.ani = FuncAnimation(fig, update, frames=range(100), interval=100, blit=True)
        canvas.draw()

    def simular_faraday(self):
        self.limpar_grafico()
        texto = ("∇×E = -∂B/∂t\n\n"
                 "A Lei de Faraday mostra que um campo magnético variável induz um campo elétrico. "
                 "É a base da geração de eletricidade. "
                 "Simulação: E induzido por B oscilante. Ajuste frequência e amplitude.")
        self.atualizar_texto(texto)

        # Sliders
        self.freq_faraday_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_panel, text="⚡️ Frequência (Hz): 0 a 5").pack()
        ttk.Scale(self.control_panel, from_=0, to=5, variable=self.freq_faraday_var, orient="horizontal").pack(fill="x")

        self.amp_b_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_panel, text="⚡️ Amplitude de B: 0 a 2").pack()
        ttk.Scale(self.control_panel, from_=0, to=2, variable=self.amp_b_var, orient="horizontal").pack(fill="x")

        self.plot_faraday()

    def plot_faraday(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        x = np.linspace(0, 10, 100)
        line_b, = ax.plot(x, np.sin(x), label="B (Magnético)", color="green")
        line_e, = ax.plot(x, -np.cos(x), label="E (Induzido)", color="red")
        ax.set_ylim(-3, 3)
        ax.set_title("Indução de Faraday Dinâmica ⚡️", fontsize=14)
        ax.set_xlabel("Posição (m)", fontsize=12)
        ax.set_ylabel("Amplitude", fontsize=12)
        ax.legend()
        ax.grid(True)

        def update(frame):
            freq = self.freq_faraday_var.get()
            amp_b = self.amp_b_var.get()
            line_b.set_ydata(amp_b * np.sin(freq * (x + frame / 20)))
            line_e.set_ydata(-amp_b * np.cos(freq * (x + frame / 20)))
            return line_b, line_e

        self.ani = FuncAnimation(fig, update, frames=range(200), interval=50, blit=True)
        canvas.draw()

    def simular_ampere_maxwell(self):
        self.limpar_grafico()
        texto = ("∇×B = μ₀J + μ₀ε₀∂E/∂t\n\n"
                 "A Lei de Ampère-Maxwell relaciona o campo magnético a correntes e à variação de E. "
                 "Explica a propagação de ondas EM. "
                 "Simulação: Onda EM. Ajuste frequência e densidade de corrente.")
        self.atualizar_texto(texto)

        # Sliders
        self.freq_ampere_var = tk.DoubleVar(value=1.0)
        ttk.Label(self.control_panel, text="🌈 Frequência (Hz): 0 a 5").pack()
        ttk.Scale(self.control_panel, from_=0, to=5, variable=self.freq_ampere_var, orient="horizontal").pack(fill="x")

        self.j_var = tk.DoubleVar(value=0.5)
        ttk.Label(self.control_panel, text="🌈 Densidade de Corrente (J): 0 a 2").pack()
        ttk.Scale(self.control_panel, from_=0, to=2, variable=self.j_var, orient="horizontal").pack(fill="x")

        self.plot_ampere_maxwell()

    def plot_ampere_maxwell(self):
        fig, ax = plt.subplots(figsize=(6, 5))
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)

        x = np.linspace(0, 10, 100)
        line_e, = ax.plot(x, np.sin(x), label="E (Elétrico)", color="red")
        line_b, = ax.plot(x, np.cos(x), label="B (Magnético)", color="green")
        ax.set_ylim(-3, 3)
        ax.set_title("Onda Eletromagnética Dinâmica 🌈", fontsize=14)
        ax.set_xlabel("Distância (m)", fontsize=12)
        ax.set_ylabel("Amplitude", fontsize=12)
        ax.legend()
        ax.grid(True)

        def update(frame):
            freq = self.freq_ampere_var.get()
            j = self.j_var.get()
            line_e.set_ydata(np.sin(freq * (x + frame / 20)))
            line_b.set_ydata(j + np.cos(freq * (x + frame / 20)))
            return line_e, line_b

        self.ani = FuncAnimation(fig, update, frames=range(200), interval=50, blit=True)
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MaxwellSimulator(root)
    root.mainloop()