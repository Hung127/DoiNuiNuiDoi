import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

# Ensure we can import from repo root when running from ui/
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from hill_cipher import HillCipher, get_inverse_mod
from model.matrix import Matrix
from transformation.determinant import determinant

PASTEL = {
    "bg": "#f7f8fb",
    "card": "#ffffff",
    "card2": "#f2f5ff",
    "text": "#253047",
    "muted": "#6b7280",
    "accent": "#8aa6ff",
    "accent2": "#a7f3d0",
    "border": "#e5e9f2",
    "danger": "#ff8ba7",
    "success": "#7dd3fc",
}


class HillCipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hill Cipher — Pastel UI")
        self.geometry("1050x720")
        self.minsize(960, 640)

        self.theme = PASTEL
        self.configure(bg=self.theme["bg"])

        self.block_size = 3
        self.cipher = None

        self._build_style()
        self._build_ui()
        self._init_cipher()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Card.TFrame", background=self.theme["card"])
        style.configure("Title.TLabel", background=self.theme["bg"], foreground=self.theme["text"], font=("Inter", 20, "bold"))
        style.configure("Muted.TLabel", background=self.theme["card"], foreground=self.theme["muted"], font=("Inter", 10))
        style.configure("Text.TLabel", background=self.theme["card"], foreground=self.theme["text"], font=("Inter", 11))
        style.configure("Accent.TButton", background=self.theme["accent"], foreground="white", font=("Inter", 10, "bold"))
        style.map("Accent.TButton", background=[("active", self.theme["accent"])])

        style.configure("TButton", font=("Inter", 10), background=self.theme["card2"], foreground=self.theme["text"])
        style.map("TButton", background=[("active", self.theme["card2"])])

        style.configure("TEntry", fieldbackground=self.theme["card2"], foreground=self.theme["text"])
        style.configure("TCombobox", fieldbackground=self.theme["card2"], foreground=self.theme["text"])

    def _build_ui(self):
        top = tk.Frame(self, bg=self.theme["bg"])
        top.pack(fill="x", padx=20, pady=16)

        title = tk.Label(top, text="Hill Cipher", bg=self.theme["bg"], fg=self.theme["text"], font=("Inter", 24, "bold"))
        title.pack(side="left")

        subtitle = tk.Label(top, text="Modern pastel UI · Encrypt / Decrypt with matrix key", bg=self.theme["bg"], fg=self.theme["muted"], font=("Inter", 10))
        subtitle.pack(side="left", padx=14)

        main = tk.Frame(self, bg=self.theme["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=10)

        left = tk.Frame(main, bg=self.theme["bg"])
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(main, bg=self.theme["bg"])
        right.pack(side="right", fill="both", expand=True)

        # LEFT CARD
        self.card_left = ttk.Frame(left, style="Card.TFrame")
        self.card_left.pack(fill="both", expand=True)

        tk.Label(self.card_left, text="Key & Matrix", bg=self.theme["card"], fg=self.theme["text"], font=("Inter", 14, "bold")).pack(anchor="w", padx=16, pady=(14, 6))

        bs_frame = tk.Frame(self.card_left, bg=self.theme["card"])
        bs_frame.pack(fill="x", padx=16, pady=6)

        tk.Label(bs_frame, text="Block size", bg=self.theme["card"], fg=self.theme["muted"]).pack(side="left")

        self.bs_buttons = {}
        for size in [2, 3, 4, 5]:
            btn = ttk.Button(bs_frame, text=f"{size}×{size}", command=lambda s=size: self.set_block_size(s))
            btn.pack(side="left", padx=4)
            self.bs_buttons[size] = btn

        ttk.Button(bs_frame, text="↺ New Key", style="Accent.TButton", command=self._init_cipher).pack(side="right")

        # Key import/export
        key_frame = tk.Frame(self.card_left, bg=self.theme["card"])
        key_frame.pack(fill="x", padx=16, pady=8)

        tk.Label(key_frame, text="Key matrix (CSV, rows separated by ';')", bg=self.theme["card"], fg=self.theme["muted"]).pack(anchor="w")
        self.key_entry = ttk.Entry(key_frame)
        self.key_entry.pack(fill="x", pady=4)

        btn_row = tk.Frame(key_frame, bg=self.theme["card"])
        btn_row.pack(fill="x")
        ttk.Button(btn_row, text="Import Key", command=self.import_key).pack(side="left")
        ttk.Button(btn_row, text="Export Key", command=self.export_key).pack(side="left", padx=6)

        self.det_label = tk.Label(self.card_left, text="", bg=self.theme["card"], fg=self.theme["muted"], font=("Inter", 10))
        self.det_label.pack(anchor="w", padx=16, pady=(6, 0))

        self.kmat_frame = tk.Frame(self.card_left, bg=self.theme["card"])
        self.kmat_frame.pack(fill="x", padx=16, pady=8)

        self.imat_frame = tk.Frame(self.card_left, bg=self.theme["card"])
        self.imat_frame.pack(fill="x", padx=16, pady=8)

        # RIGHT CARD
        self.card_right = ttk.Frame(right, style="Card.TFrame")
        self.card_right.pack(fill="both", expand=True)

        tk.Label(self.card_right, text="Encrypt / Decrypt", bg=self.theme["card"], fg=self.theme["text"], font=("Inter", 14, "bold")).pack(anchor="w", padx=16, pady=(14, 6))

        tk.Label(self.card_right, text="Input", bg=self.theme["card"], fg=self.theme["muted"]).pack(anchor="w", padx=16)
        self.input_text = tk.Text(self.card_right, height=6, bg=self.theme["card2"], fg=self.theme["text"], insertbackground=self.theme["text"], relief="flat")
        self.input_text.pack(fill="x", padx=16, pady=6)

        action_row = tk.Frame(self.card_right, bg=self.theme["card"])
        action_row.pack(fill="x", padx=16, pady=4)
        ttk.Button(action_row, text="Encrypt →", style="Accent.TButton", command=lambda: self.run("enc")).pack(side="left", padx=4)
        ttk.Button(action_row, text="← Decrypt", command=lambda: self.run("dec")).pack(side="left", padx=4)
        ttk.Button(action_row, text="Use output as input", command=self.swap_output).pack(side="left", padx=4)

        tk.Label(self.card_right, text="Output", bg=self.theme["card"], fg=self.theme["muted"]).pack(anchor="w", padx=16, pady=(12, 0))
        self.output_text = tk.Text(self.card_right, height=6, bg=self.theme["card2"], fg=self.theme["text"], insertbackground=self.theme["text"], relief="flat")
        self.output_text.pack(fill="x", padx=16, pady=6)

        stats_row = tk.Frame(self.card_right, bg=self.theme["card"])
        stats_row.pack(fill="x", padx=16, pady=4)
        self.stats_label = tk.Label(stats_row, text="", bg=self.theme["card"], fg=self.theme["muted"], font=("Inter", 10))
        self.stats_label.pack(side="left")

        ttk.Button(stats_row, text="Copy Output", command=self.copy_output).pack(side="right")

    def _init_cipher(self):
        self.cipher = HillCipher(self.block_size)
        self._refresh_matrix()
        self._highlight_bs()

    def _highlight_bs(self):
        for size, btn in self.bs_buttons.items():
            btn.state(["!pressed"])
            if size == self.block_size:
                btn.state(["pressed"])

    def set_block_size(self, size):
        self.block_size = size
        self._init_cipher()

    def _refresh_matrix(self):
        for w in self.kmat_frame.winfo_children():
            w.destroy()
        for w in self.imat_frame.winfo_children():
            w.destroy()

        tk.Label(self.kmat_frame, text="Key matrix K", bg=self.theme["card"], fg=self.theme["text"]).pack(anchor="w")
        mat = self.cipher.key_matrix.get_matrix_part()
        self._render_matrix(self.kmat_frame, mat)

        tk.Label(self.imat_frame, text="Inverse K⁻¹ (mod 26)", bg=self.theme["card"], fg=self.theme["text"]).pack(anchor="w", pady=(8, 0))
        inv = self.cipher.inversed_key.get_matrix_part()
        self._render_matrix(self.imat_frame, inv)

        det = round(determinant(self.cipher.key_matrix))
        self.det_label.config(text=f"det(K) = {det} · gcd(det, 26)=1 ✓")

    def _render_matrix(self, parent, mat):
        table = tk.Frame(parent, bg=self.theme["card"])
        table.pack(anchor="w", pady=4)
        for i, row in enumerate(mat):
            for j, val in enumerate(row):
                cell = tk.Label(
                    table,
                    text=int(val),
                    bg=self.theme["card2"],
                    fg=self.theme["text"],
                    width=4,
                    padx=4,
                    pady=2
                )
                cell.grid(row=i, column=j, padx=3, pady=3)

    def import_key(self):
        try:
            raw = self.key_entry.get().strip()
            rows = [r.strip() for r in raw.split(";") if r.strip()]
            matrix = [list(map(int, r.split(","))) for r in rows]
            if not matrix or any(len(r) != len(matrix) for r in matrix):
                raise ValueError("Key matrix không hợp lệ (phải vuông)")
            m = Matrix(matrix)
            self.cipher.key_matrix = m
            self.cipher.inversed_key = get_inverse_mod(m, 26)
            self.block_size = len(matrix)
            self._refresh_matrix()
            messagebox.showinfo("OK", "Import key thành công!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_key(self):
        mat = self.cipher.key_matrix.get_matrix_part()
        csv = ";".join([",".join(str(int(x)) for x in row) for row in mat])
        self.clipboard_clear()
        self.clipboard_append(csv)
        messagebox.showinfo("Copied", "Key đã copy vào clipboard!")

    def run(self, mode):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            return
        try:
            if mode == "enc":
                out = self.cipher.encrypt(text)
            else:
                out = self.cipher.decrypt(text)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", out)

            alpha = sum(c.isalpha() for c in text)
            blocks = (alpha + self.block_size - 1) // self.block_size
            self.stats_label.config(text=f"length: {len(out)} | alpha: {alpha} | blocks: {blocks}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_output(self):
        out = self.output_text.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(out)
        messagebox.showinfo("Copied", "Output đã copy!")

    def swap_output(self):
        out = self.output_text.get("1.0", "end").strip()
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", out)


if __name__ == "__main__":
    app = HillCipherApp()
    app.mainloop()
