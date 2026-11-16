import tkinter as tk
import random
import time

FILAS, COLS, MINAS = 12, 12, 20   # cambiá esto para ajustar la dificultad
TAM = 36
BG, CERRADA, ABIERTA = "#1e1e2e", "#3b3b55", "#2a2a3d"
COLORES = {1: "#4fc3f7", 2: "#81c784", 3: "#e57373", 4: "#9575cd",
           5: "#ffb74d", 6: "#4dd0e1", 7: "#f06292", 8: "#bdbdbd"}


class Buscaminas:
    def __init__(self, root):
        self.root = root
        root.title("Buscaminas")
        root.configure(bg=BG)
        root.resizable(False, False)

        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", padx=10, pady=8)
        fuente = ("Consolas", 18, "bold")
        self.lbl_minas = tk.Label(top, font=fuente, fg="#ff6b6b", bg=BG)
        self.lbl_minas.pack(side="left")
        self.btn = tk.Button(top, text="🙂", font=("Segoe UI Emoji", 16), bd=0,
                             bg=CERRADA, fg="white", activebackground=ABIERTA,
                             command=self.nuevo)
        self.btn.pack(side="left", expand=True)
        self.lbl_tiempo = tk.Label(top, font=fuente, fg="#ffd166", bg=BG)
        self.lbl_tiempo.pack(side="right")

        self.canvas = tk.Canvas(root, width=COLS * TAM, height=FILAS * TAM,
                                bg=BG, highlightthickness=0)
        self.canvas.pack(padx=10, pady=(0, 10))
        self.canvas.bind("<Button-1>", self.izquierdo)
        self.canvas.bind("<Button-3>", self.derecho)  # Windows / Linux
        self.canvas.bind("<Button-2>", self.derecho)  # Mac
        self.nuevo()

    def nuevo(self):
        self.minas, self.abiertas, self.banderas = set(), set(), set()
        self.primer_click, self.fin, self.explotada = True, False, None
        self.inicio = None
        self.btn.config(text="🙂")
        self.lbl_tiempo.config(text="⏱ 000")
        self.dibujar()
        self.tick()

    def tick(self):
        if self.inicio and not self.fin:
            self.lbl_tiempo.config(text=f"⏱ {min(int(time.time() - self.inicio), 999):03d}")
        if getattr(self, "_t", None):
            self.root.after_cancel(self._t)
        self._t = self.root.after(200, self.tick)

    def vecinos(self, f, c):
        for df in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nf, nc = f + df, c + dc
                if (df or dc) and 0 <= nf < FILAS and 0 <= nc < COLS:
                    yield nf, nc

    def numero(self, f, c):
        return sum((v in self.minas) for v in self.vecinos(f, c))

    def colocar_minas(self, f, c):
        prohibidas = {(f, c), *self.vecinos(f, c)}
        libres = [(i, j) for i in range(FILAS) for j in range(COLS) if (i, j) not in prohibidas]
        self.minas = set(random.sample(libres, MINAS))

    def abrir(self, f, c):
        pila = [(f, c)]
        while pila:
            celda = pila.pop()
            if celda in self.abiertas or celda in self.banderas:
                continue
            self.abiertas.add(celda)
            if self.numero(*celda) == 0:
                pila.extend(self.vecinos(*celda))

    def izquierdo(self, e):
        if self.fin:
            return
        c, f = e.x // TAM, e.y // TAM
        if not (0 <= f < FILAS and 0 <= c < COLS) or (f, c) in self.banderas:
            return
        if self.primer_click:
            self.colocar_minas(f, c)
            self.primer_click = False
            self.inicio = time.time()
        if (f, c) in self.minas:
            self.fin, self.explotada = True, (f, c)
            self.btn.config(text="😵")
        else:
            self.abrir(f, c)
            if len(self.abiertas) == FILAS * COLS - MINAS:
                self.fin = True
                self.banderas = set(self.minas)
                self.btn.config(text="😎")
        self.dibujar()

    def derecho(self, e):
        if self.fin or self.primer_click:
            return
        c, f = e.x // TAM, e.y // TAM
        celda = (f, c)
        if celda in self.abiertas:
            return
        self.banderas ^= {celda}
        self.dibujar()

    def dibujar(self):
        cv = self.canvas
        cv.delete("all")
        for f in range(FILAS):
            for c in range(COLS):
                celda, x, y = (f, c), c * TAM, f * TAM
                if celda in self.abiertas:
                    color = ABIERTA
                elif self.fin and celda in self.minas:
                    color = "#7a2e3a" if celda == self.explotada else ABIERTA
                else:
                    color = CERRADA
                cv.create_rectangle(x + 1, y + 1, x + TAM - 1, y + TAM - 1, fill=color, outline="")
                centro = (x + TAM // 2, y + TAM // 2)
                if celda in self.abiertas:
                    n = self.numero(f, c)
                    if n:
                        cv.create_text(*centro, text=n, fill=COLORES[n], font=("Consolas", 16, "bold"))
                elif self.fin and celda in self.minas and celda not in self.banderas:
                    cv.create_text(*centro, text="💣", font=("Segoe UI Emoji", 14))
                elif celda in self.banderas:
                    cv.create_text(*centro, text="🚩", font=("Segoe UI Emoji", 14))
        self.lbl_minas.config(text=f"💣 {MINAS - len(self.banderas):02d}")


if __name__ == "__main__":
    root = tk.Tk()
    Buscaminas(root)
    root.mainloop()