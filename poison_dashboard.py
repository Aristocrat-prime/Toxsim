"""
poison_dashboard.py — Poison Mixing Dashboard
Run: python poison_dashboard.py
"""

import os
import re
import hashlib
import threading

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import requests
from PIL import Image, ImageTk

try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import AllChem, Draw, rdMolDescriptors
    from rdkit.Chem.Draw import rdMolDraw2D
    RDLogger.DisableLog("rdApp.*")
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False

from poison_database import (
    POISONS, list_poisons, get_poison, get_interaction,
    search_pubchem, _default_organs, register_compound,
    repair_smiles_for,
)
from poison_pk_engine import PoisonPK, PoisonSimulator, create_poison_pk

STRUCTURE_CACHE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "structures"
)

SOUNDS = {
    "boot":     [(440, 60), (660, 60), (880, 90)],
    "click":    [(1000, 25)],
    "add":      [(880, 50), (1100, 60)],
    "purge":    [(700, 40), (500, 60)],
    "purge_all":[(900, 40), (700, 40), (500, 70)],
    "run":      [(400, 70), (600, 70), (800, 100)],
    "complete": [(660, 60), (880, 60), (1320, 120)],
    "error":    [(300, 150), (200, 200)],
    "browse":   [(1200, 40)],
    "save":     [(800, 50), (1000, 50), (1200, 70)],
    "load":     [(1200, 50), (1000, 50), (800, 70)],
}


class PoisonDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("TOXICOLOGY INTERFACE")

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        w = min(1450, int(sw * 0.94))
        h = min(950, int(sh * 0.92))
        x = (sw - w) // 2
        y = max(0, (sh - h) // 2 - 20)
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(1050, 650)
        self.root.configure(bg="#0a0f0a")

        self.selected_poisons = {}
        self.simulator = PoisonSimulator(body_weight_kg=70.0)
        self.results = None
        self._current_structure_photo = None
        self._mixture_photos = []

        self.bg_color = "#0a0f0a"
        self.panel_bg = "#0f1a0f"
        self.right_bg = "#12200f"
        self.right_sub_bg = "#0f1c0f"
        self.fg_color = "#33ff33"
        self.accent_color = "#00ff66"
        self.dim_color = "#1b4d1b"

        self.plot_fig_bg = "#101e10"
        self.plot_ax_bg = "#0a140a"
        self.grid_color = "#2a6d2a"

        self.sound_enabled = tk.BooleanVar(value=True)

        os.makedirs(STRUCTURE_CACHE_DIR, exist_ok=True)

        self._configure_pipboy_styles()
        self._build_ui()
        self._sfx("boot")

    def _sfx(self, name: str):
        if not WINSOUND_AVAILABLE or not self.sound_enabled.get():
            return
        seq = SOUNDS.get(name)
        if not seq:
            return

        def worker():
            for freq, ms in seq:
                try:
                    winsound.Beep(freq, ms)
                except Exception:
                    pass

        threading.Thread(target=worker, daemon=True).start()

    def _configure_pipboy_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabelframe", background=self.bg_color, bordercolor=self.fg_color, relief="solid")
        style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.accent_color, font=("Consolas", 10, "bold"))
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Consolas", 10))

        style.configure("TButton",
                        background=self.dim_color,
                        foreground=self.fg_color,
                        bordercolor=self.fg_color,
                        font=("Consolas", 10, "bold"),
                        relief="raised")
        style.map("TButton",
                  background=[("active", self.fg_color)],
                  foreground=[("active", self.bg_color)])

        style.configure("Accent.TButton",
                        background=self.fg_color,
                        foreground=self.bg_color,
                        font=("Consolas", 11, "bold"))
        style.map("Accent.TButton",
                  background=[("active", self.accent_color)],
                  foreground=[("active", self.bg_color)])

        style.configure("TNotebook",
                        background=self.right_bg,
                        bordercolor=self.fg_color,
                        tabmargins=[2, 5, 2, 0])
        style.configure("TNotebook.Tab",
                        background=self.dim_color,
                        foreground=self.fg_color,
                        padding=[10, 4],
                        font=("Consolas", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", self.right_bg), ("active", self.fg_color)],
                  foreground=[("selected", self.accent_color), ("active", self.bg_color)])

        style.configure("TCheckbutton",
                        background=self.bg_color,
                        foreground=self.fg_color,
                        font=("Consolas", 9))
        style.map("TCheckbutton",
                  background=[("active", self.bg_color)],
                  foreground=[("active", self.accent_color)])

        style.configure("Vertical.TScrollbar",
                        background=self.dim_color,
                        troughcolor=self.bg_color,
                        bordercolor=self.fg_color,
                        arrowcolor=self.fg_color,
                        width=10)

    def _build_ui(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # === LEFT PANEL: scrollable ===
        left_outer = ttk.Frame(paned)
        paned.add(left_outer, weight=0)

        left_canvas = tk.Canvas(left_outer, bg=self.bg_color,
                                highlightthickness=0, width=400)
        left_scroll = ttk.Scrollbar(left_outer, orient=tk.VERTICAL,
                                    command=left_canvas.yview,
                                    style="Vertical.TScrollbar")
        left_canvas.configure(yscrollcommand=left_scroll.set)

        left_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(left_canvas)
        left_canvas.create_window((0, 0), window=left_frame, anchor="nw",
                                  width=390)

        def _sync_left_scroll(_event=None):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))

        left_frame.bind("<Configure>", _sync_left_scroll)

        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_wheel(_event):
            left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_wheel(_event):
            left_canvas.unbind_all("<MouseWheel>")

        left_canvas.bind("<Enter>", _bind_wheel)
        left_canvas.bind("<Leave>", _unbind_wheel)

        right_frame = tk.Frame(paned, bg=self.right_bg)
        paned.add(right_frame, weight=1)

        # === LEFT CONTENT ===
        db_frame = ttk.LabelFrame(left_frame, text=" [ DATABASE // SPECIMEN INSPECT ] ")
        db_frame.pack(fill=tk.X, padx=3, pady=3)

        search_box_frame = ttk.Frame(db_frame)
        search_box_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(search_box_frame, text="FILTER:").pack(side=tk.LEFT, padx=(0, 4))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_box_frame, textvariable=self.search_var,
                                font=("Consolas", 10), bg="#0f1a0f", fg="#33ff33",
                                insertbackground="#33ff33", relief="solid", bd=1)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        search_entry.bind("<Return>", lambda e: self._trigger_live_search())
        self.search_var.trace_add("write", self._filter_list)

        ttk.Button(search_box_frame, text="BROWSE",
                   command=self._trigger_live_search).pack(side=tk.LEFT)

        sound_row = ttk.Frame(db_frame)
        sound_row.pack(fill=tk.X, padx=4, pady=(0, 4))
        ttk.Checkbutton(sound_row, text="SOUND FX",
                        variable=self.sound_enabled,
                        command=lambda: self._sfx("click")).pack(side=tk.LEFT)
        self.sound_status = tk.StringVar(
            value="" if WINSOUND_AVAILABLE else "(unavailable)"
        )
        tk.Label(sound_row, textvariable=self.sound_status,
                 bg=self.bg_color, fg="#1b4d1b",
                 font=("Consolas", 8)).pack(side=tk.LEFT, padx=(6, 0))

        self.poison_listbox = tk.Listbox(db_frame, font=("Consolas", 10), height=8,
                                         bg="#050a05", fg="#33ff33",
                                         selectbackground="#1b4d1b", selectforeground="#ffffff",
                                         highlightthickness=0, borderwidth=1, relief="solid")
        self.poison_listbox.pack(fill=tk.X, padx=4, pady=(0, 4))
        self._populate_list()
        self.poison_listbox.bind("<<ListboxSelect>>", self._on_select)

        self.details_text = tk.Text(db_frame, font=("Consolas", 9),
                                    bg="#050a05", fg="#00ff66", wrap=tk.WORD, height=9,
                                    highlightthickness=0, borderwidth=1, relief="solid")
        self.details_text.pack(fill=tk.X, padx=4, pady=(0, 4))
        self.details_text.insert("1.0", "> SELECT SPECIMEN FOR BIO-DATA...")
        self.details_text.config(state=tk.DISABLED)

        mix_frame = ttk.LabelFrame(left_frame, text=" [ MIXTURE FORMULATION & EXECUTION ] ")
        mix_frame.pack(fill=tk.X, padx=3, pady=3)

        add_ctrl_frame = ttk.Frame(mix_frame)
        add_ctrl_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Label(add_ctrl_frame, text="DOSE (mg/kg):").pack(side=tk.LEFT, padx=(0, 4))
        self.dose_var = tk.StringVar(value="0.1")
        dose_entry = tk.Entry(add_ctrl_frame, textvariable=self.dose_var, width=8,
                              font=("Consolas", 10), bg="#0f1a0f", fg="#33ff33",
                              insertbackground="#33ff33", relief="solid", bd=1)
        dose_entry.pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(add_ctrl_frame, text="LOAD INTO MIX",
                   command=self._add_to_mixture).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.mixture_listbox = tk.Listbox(mix_frame, height=4, font=("Consolas", 9),
                                          bg="#050a05", fg="#ff5555",
                                          selectbackground="#4d1b1b", selectforeground="#ffffff",
                                          highlightthickness=0, borderwidth=1, relief="solid")
        self.mixture_listbox.pack(fill=tk.X, padx=4, pady=(0, 4))

        mix_btn_frame = ttk.Frame(mix_frame)
        mix_btn_frame.pack(fill=tk.X, padx=4, pady=(0, 4))
        ttk.Button(mix_btn_frame, text="PURGE SELECTED", command=self._remove_from_mixture).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(mix_btn_frame, text="PURGE ALL", command=self._clear_mixture).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        io_btn_frame = ttk.Frame(mix_frame)
        io_btn_frame.pack(fill=tk.X, padx=4, pady=(0, 4))
        ttk.Button(io_btn_frame, text="SAVE", command=self._save_mixture).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(io_btn_frame, text="LOAD", command=self._load_mixture).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        run_frame = ttk.Frame(mix_frame)
        run_frame.pack(fill=tk.X, padx=4, pady=(4, 6))
        ttk.Button(run_frame, text="▶ INITIATE SIMULATION PROTOCOL",
                   command=self._run_simulation,
                   style="Accent.TButton").pack(fill=tk.X, ipady=6)

        # === RIGHT PANEL ===
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # --- STRUCTURE TAB ---
        self.tab_structure = tk.Frame(self.notebook, bg=self.right_bg)
        self.notebook.add(self.tab_structure, text=" [ STRUCTURE ] ")

        struct_canvas = tk.Canvas(self.tab_structure, bg=self.right_bg,
                                  highlightthickness=0)
        struct_scrollbar = ttk.Scrollbar(self.tab_structure, orient=tk.VERTICAL,
                                         command=struct_canvas.yview,
                                         style="Vertical.TScrollbar")
        struct_canvas.configure(yscrollcommand=struct_scrollbar.set)

        struct_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        struct_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.struct_inner = tk.Frame(struct_canvas, bg=self.right_bg)
        struct_canvas.create_window((0, 0), window=self.struct_inner, anchor="nw")

        def _on_struct_config(event):
            struct_canvas.configure(scrollregion=struct_canvas.bbox("all"))
        self.struct_inner.bind("<Configure>", _on_struct_config)

        def _on_canvas_config(event):
            struct_canvas.itemconfig(
                struct_canvas.find_all()[0], width=event.width
            )
        struct_canvas.bind("<Configure>", _on_canvas_config)

        def _struct_wheel(event):
            struct_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_struct_wheel(_event):
            struct_canvas.bind_all("<MouseWheel>", _struct_wheel)

        def _unbind_struct_wheel(_event):
            struct_canvas.unbind_all("<MouseWheel>")

        struct_canvas.bind("<Enter>", _bind_struct_wheel)
        struct_canvas.bind("<Leave>", _unbind_struct_wheel)

        self.structure_mixture_header = tk.Label(
            self.struct_inner,
            bg=self.right_bg, fg="#ffd966",
            font=("Consolas", 12, "bold"),
            anchor="w", justify="left",
            text=""
        )
        self.structure_mixture_header.pack(fill=tk.X, padx=15, pady=(15, 5))

        self.structure_mixture_formula_var = tk.StringVar(value="")
        tk.Label(self.struct_inner, textvariable=self.structure_mixture_formula_var,
                 bg=self.right_bg, fg="#66ff99",
                 font=("Consolas", 11, "bold"),
                 anchor="w", justify="left", wraplength=1000
                 ).pack(fill=tk.X, padx=15, pady=(0, 5))

        self.structure_mixture_smiles_var = tk.StringVar(value="")
        tk.Label(self.struct_inner, textvariable=self.structure_mixture_smiles_var,
                 bg=self.right_bg, fg="#4d9e4d",
                 font=("Consolas", 8),
                 anchor="w", justify="left", wraplength=1000
                 ).pack(fill=tk.X, padx=15, pady=(0, 5))

        self.mixture_image_label = tk.Label(
            self.struct_inner,
            bg=self.right_sub_bg, fg="#2a6d2a",
            font=("Consolas", 10),
            text="[ load 2+ compounds to render combined structure ]",
            bd=1, relief="solid"
        )
        self.mixture_image_label.pack(pady=10, padx=20)

        self.mixture_component_frame = tk.Frame(self.struct_inner, bg=self.right_bg)
        self.mixture_component_frame.pack(fill=tk.X, padx=15, pady=(5, 15))

        self.single_header = tk.Label(
            self.struct_inner,
            bg=self.right_bg, fg="#66ff99",
            font=("Consolas", 11, "bold"),
            anchor="w", justify="left",
            text="> SELECTED SPECIMEN"
        )
        self.single_header.pack(fill=tk.X, padx=15, pady=(15, 3))

        self.structure_title_var = tk.StringVar(value="> NO SPECIMEN SELECTED")
        tk.Label(self.struct_inner, textvariable=self.structure_title_var,
                 bg=self.right_bg, fg="#66ff99",
                 font=("Consolas", 14, "bold"),
                 anchor="w").pack(fill=tk.X, padx=15)

        self.structure_formula_var = tk.StringVar(value="")
        self.structure_formula_label = tk.Label(
            self.struct_inner, textvariable=self.structure_formula_var,
            bg=self.right_bg, fg="#66ff99",
            font=("Consolas", 11, "bold"),
            anchor="w", justify="left", wraplength=1000
        )
        self.structure_formula_label.pack(fill=tk.X, padx=15, pady=(6, 0))

        self.structure_source_var = tk.StringVar(value="")
        self.structure_source_label = tk.Label(
            self.struct_inner, textvariable=self.structure_source_var,
            bg=self.right_bg, fg="#4d9e4d",
            font=("Consolas", 9),
            anchor="w", justify="left", wraplength=1000
        )
        self.structure_source_label.pack(fill=tk.X, padx=15, pady=(2, 0))

        self.structure_image_label = tk.Label(
            self.struct_inner,
            bg=self.right_sub_bg, fg="#2a6d2a",
            font=("Consolas", 10),
            text="[ select a specimen to render ]",
            bd=1, relief="solid"
        )
        self.structure_image_label.pack(pady=20, padx=20)

        self.structure_smiles_var = tk.StringVar(value="")
        tk.Label(self.struct_inner, textvariable=self.structure_smiles_var,
                 bg=self.right_bg, fg="#4d9e4d",
                 font=("Consolas", 8),
                 anchor="w", justify="left", wraplength=1000
                 ).pack(fill=tk.X, padx=15, pady=(0, 15))

        # --- PK CURVES ---
        self.tab_pk = tk.Frame(self.notebook, bg=self.right_bg)
        self.notebook.add(self.tab_pk, text=" [ PK CURVES ] ")

        self.fig_pk = Figure(figsize=(6, 4.5), dpi=100, facecolor=self.plot_fig_bg)
        self.ax_pk = self.fig_pk.add_subplot(111)
        self.ax_pk.set_facecolor(self.plot_ax_bg)
        self.canvas_pk = FigureCanvasTkAgg(self.fig_pk, self.tab_pk)
        self.canvas_pk.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- ORGAN DAMAGE ---
        self.tab_organs = tk.Frame(self.notebook, bg=self.right_bg)
        self.notebook.add(self.tab_organs, text=" [ ORGAN DEGRADATION ] ")

        self.fig_organs = Figure(figsize=(6, 4.5), dpi=100, facecolor=self.plot_fig_bg)
        self.ax_organs = self.fig_organs.add_subplot(111)
        self.ax_organs.set_facecolor(self.plot_ax_bg)
        self.canvas_organs = FigureCanvasTkAgg(self.fig_organs, self.tab_organs)
        self.canvas_organs.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- SYNERGY MATRIX ---
        self.tab_interaction = tk.Frame(self.notebook, bg=self.right_bg)
        self.notebook.add(self.tab_interaction, text=" [ SYNERGY ] ")

        self.interaction_text = tk.Text(self.tab_interaction, font=("Consolas", 10),
                                        bg=self.plot_ax_bg, fg="#66ff99", wrap=tk.WORD,
                                        highlightthickness=0, borderwidth=1, relief="solid",
                                        insertbackground="#66ff99")
        int_scroll = ttk.Scrollbar(self.tab_interaction, orient=tk.VERTICAL,
                                   command=self.interaction_text.yview,
                                   style="Vertical.TScrollbar")
        self.interaction_text.configure(yscrollcommand=int_scroll.set)
        self.interaction_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        int_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.interaction_text.insert("1.0", "> AWAITING MIXTURE INPUT AND SIMULATION RUN...")

        # --- STATUS REPORT ---
        self.tab_summary = tk.Frame(self.notebook, bg=self.right_bg)
        self.notebook.add(self.tab_summary, text=" [ REPORT ] ")

        self.summary_text = tk.Text(self.tab_summary, font=("Consolas", 10),
                                    bg=self.plot_ax_bg, fg="#66ff99", wrap=tk.WORD,
                                    highlightthickness=0, borderwidth=1, relief="solid",
                                    insertbackground="#66ff99")
        sum_scroll = ttk.Scrollbar(self.tab_summary, orient=tk.VERTICAL,
                                   command=self.summary_text.yview,
                                   style="Vertical.TScrollbar")
        self.summary_text.configure(yscrollcommand=sum_scroll.set)
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        sum_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.summary_text.insert("1.0", "> NO ACTIVE SIMULATION LOGS FOUND.")

        self.notebook.select(0)

        self.status_var = tk.StringVar(
            value=f"TOXIOCOLOGY TERMINAL READY . RDKit: {'available' if RDKIT_AVAILABLE else 'MISSING'} | Sound: {'on' if WINSOUND_AVAILABLE else 'off'}"
        )
        status = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, font=("Consolas", 9))
        status.pack(side=tk.BOTTOM, fill=tk.X)

    def _populate_list(self, filter_text=""):
        self.poison_listbox.delete(0, tk.END)
        for name in list_poisons():
            if filter_text.lower() in name.lower():
                self.poison_listbox.insert(tk.END, name)

    def _filter_list(self, *args):
        self._populate_list(self.search_var.get())

    def _rdkit_formula(self, smiles: str) -> str:
        if not RDKIT_AVAILABLE or not smiles:
            return ""
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return ""
            return rdMolDescriptors.CalcMolFormula(mol)
        except Exception:
            return ""

    def _rdkit_render(self, smiles: str, out_path: str, size=(500, 500)) -> bool:
        if not RDKIT_AVAILABLE or not smiles:
            return False
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return False
            AllChem.Compute2DCoords(mol)

            drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
            opts = drawer.drawOptions()
            opts.clearBackground = False
            opts.bondLineWidth = 3
            opts.padding = 0.05
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()

            with open(out_path, "wb") as f:
                f.write(drawer.GetDrawingText())
            return True
        except Exception as e:
            print(f"[rdkit] render failed: {e}")
            return False

    def _build_mixture_smiles(self) -> str:
        parts = []
        for name in self.selected_poisons:
            p = get_poison(name)
            if p:
                s = p.get("structure", "")
                if s and s not in ("Unknown", "N/A", ""):
                    parts.append(s)
        return ".".join(parts) if parts else ""

    def _build_mixture_formula(self) -> str:
        mixture_smiles = self._build_mixture_smiles()
        if not mixture_smiles:
            formulas = []
            for name in self.selected_poisons:
                p = get_poison(name)
                if p:
                    f = p.get("formula", "")
                    if f and f not in ("Unknown", "N/A"):
                        formulas.append(f)
            return self._combine_formulas(formulas)
        if RDKIT_AVAILABLE:
            f = self._rdkit_formula(mixture_smiles)
            if f:
                return f
        return ""

    def _combine_formulas(self, formulas):
        atom_counts = {}
        for f in formulas:
            if not f or f in ("Unknown", "N/A"):
                continue
            for element, count in re.findall(r"([A-Z][a-z]?)(\d*)", f):
                if not element:
                    continue
                n = int(count) if count else 1
                atom_counts[element] = atom_counts.get(element, 0) + n

        if not atom_counts:
            return ""

        order = []
        if "C" in atom_counts:
            order.append("C")
        if "H" in atom_counts:
            order.append("H")
        for el in sorted(atom_counts):
            if el not in order:
                order.append(el)

        parts = []
        for el in order:
            n = atom_counts[el]
            parts.append(f"{el}{n}" if n > 1 else el)
        return "".join(parts)

    def _render_mixture_structure(self):
        if not self.selected_poisons or len(self.selected_poisons) < 2:
            self.structure_mixture_header.configure(text="")
            self.structure_mixture_formula_var.set("")
            self.structure_mixture_smiles_var.set("")
            self.mixture_image_label.configure(
                image="", text="[ load 2+ compounds to render combined structure ]"
            )
            self._clear_component_grid()
            return

        mixture_smiles = self._build_mixture_smiles()
        combined_formula = self._build_mixture_formula()

        self.structure_mixture_header.configure(text="> MIXTURE STRUCTURE")
        self.structure_mixture_formula_var.set(
            f"COMBINED FORMULA: {combined_formula or 'unavailable'}"
        )
        self.structure_mixture_smiles_var.set(
            f"COMBINED SMILES: {mixture_smiles or 'unavailable'}"
        )

        if mixture_smiles and RDKIT_AVAILABLE:
            key = hashlib.md5(mixture_smiles.encode()).hexdigest()[:16]
            out_path = os.path.join(STRUCTURE_CACHE_DIR, f"mix_{key}.png")

            if not os.path.exists(out_path):
                self._rdkit_render(mixture_smiles, out_path, size=(900, 500))

            if os.path.exists(out_path):
                try:
                    img = Image.open(out_path)
                    img.thumbnail((900, 500), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.mixture_image_label.configure(image=photo, text="")
                    self.mixture_image_label.image = photo
                    self._current_structure_photo = photo
                except Exception as e:
                    self.mixture_image_label.configure(
                        image="", text=f"[mixture render error: {e}]"
                    )
            else:
                self.mixture_image_label.configure(
                    image="", text="[ mixture render unavailable ]"
                )
        else:
            self.mixture_image_label.configure(
                image="", text="[ install rdkit to render combined structure ]"
            )

        self._build_component_grid()

    def _clear_component_grid(self):
        for child in self.mixture_component_frame.winfo_children():
            child.destroy()
        self._mixture_photos = []

    def _build_component_grid(self):
        self._clear_component_grid()

        names = list(self.selected_poisons.keys())
        if len(names) < 2:
            return

        tk.Label(
            self.mixture_component_frame,
            text="COMPONENT STRUCTURES",
            bg=self.right_bg, fg="#66ff99",
            font=("Consolas", 10, "bold"), anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))

        grid = tk.Frame(self.mixture_component_frame, bg=self.right_bg)
        grid.pack(fill=tk.X)

        for i, name in enumerate(names):
            p = get_poison(name)
            if not p:
                continue

            card = tk.Frame(grid, bg=self.right_sub_bg, bd=1, relief="solid")
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")

            tk.Label(
                card, text=name, bg=self.right_sub_bg, fg="#66ff99",
                font=("Consolas", 9, "bold"), wraplength=200, justify="left"
            ).pack(padx=6, pady=(6, 2), anchor="w")

            tk.Label(
                card, text=p.get("formula", "N/A"),
                bg=self.right_sub_bg, fg="#33ff33",
                font=("Consolas", 9)
            ).pack(padx=6, pady=(0, 4), anchor="w")

            img_path, _ = self._fetch_structure_image(name, p)
            if img_path:
                try:
                    img = Image.open(img_path)
                    img.thumbnail((180, 180), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    lbl = tk.Label(card, image=photo, bg=self.plot_ax_bg)
                    lbl.image = photo
                    lbl.pack(padx=6, pady=6)
                    self._mixture_photos.append(photo)
                except Exception:
                    tk.Label(card, text="[img error]", bg=self.right_sub_bg,
                             fg="#ff5555", font=("Consolas", 8)).pack(padx=6, pady=6)
            else:
                tk.Label(card, text="[no image]", bg=self.right_sub_bg,
                         fg="#2a6d2a", font=("Consolas", 8)).pack(padx=6, pady=6)

    def _pubchem_image(self, poison, out_path) -> bool:
        cid = poison.get("cid")
        smiles = poison.get("structure")
        try:
            if cid:
                url = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                       f"cid/{cid}/PNG?image_size=500x500")
            elif smiles:
                url = (f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
                       f"smiles/{smiles}/PNG?image_size=500x500")
            else:
                return False

            r = requests.get(url, timeout=20)
            if r.status_code == 200 and r.content:
                with open(out_path, "wb") as f:
                    f.write(r.content)
                return True
        except Exception as e:
            print(f"[pubchem-image] failed: {e}")
        return False

    def _fetch_structure_image(self, name, poison):
        smiles = poison.get("structure") or ""
        cid = poison.get("cid")

        if smiles and smiles not in ("Unknown", "N/A", ""):
            key = hashlib.md5(smiles.encode()).hexdigest()[:16]
            rdkit_path = os.path.join(STRUCTURE_CACHE_DIR, f"rdkit_{key}.png")
            pubchem_path = os.path.join(STRUCTURE_CACHE_DIR, f"pubchem_smi_{key}.png")
        elif cid:
            rdkit_path = None
            pubchem_path = os.path.join(STRUCTURE_CACHE_DIR, f"pubchem_cid_{cid}.png")
        else:
            return None, None

        if RDKIT_AVAILABLE and smiles and rdkit_path:
            if os.path.exists(rdkit_path):
                return rdkit_path, "rendered locally by RDKit"
            if self._rdkit_render(smiles, rdkit_path):
                return rdkit_path, "rendered locally by RDKit"

        if pubchem_path and os.path.exists(pubchem_path):
            return pubchem_path, "fetched from PubChem"
        if pubchem_path and self._pubchem_image(poison, pubchem_path):
            return pubchem_path, "fetched from PubChem"

        return None, None

    def _update_structure_view(self, name, poison):
        # auto-repair a bad SMILES before rendering
        repaired = repair_smiles_for(name)
        if repaired:
            poison = get_poison(name) or poison

        data_formula = poison.get("formula", "N/A")
        rdkit_formula = self._rdkit_formula(poison.get("structure", ""))

        self.structure_formula_label.configure(fg="#66ff99")
        self.structure_source_label.configure(fg="#4d9e4d")

        if rdkit_formula and rdkit_formula != data_formula:
            formula_line = (
                f"FORMULA: {data_formula}   (RDKit: {rdkit_formula})"
                f"   MISMATCH — SMILES in DB does not match formula"
            )
            self.structure_formula_label.configure(fg="#ffcc00")
            self.structure_source_var.set(
                "WARNING: compound data mismatch — could not auto-repair"
            )
            self.structure_source_label.configure(fg="#ff8800")
        else:
            formula_line = f"FORMULA: {data_formula}"

        self.structure_title_var.set(f"> {name.upper()}")
        self.structure_formula_var.set(formula_line)
        self.structure_smiles_var.set(f"SMILES: {poison.get('structure', 'N/A')}")

        img_path, source = self._fetch_structure_image(name, poison)
        if not self.structure_source_var.get().startswith("WARNING"):
            self.structure_source_var.set(f"IMAGE SOURCE: {source or 'unavailable'}")

        if img_path:
            try:
                img = Image.open(img_path)
                img.thumbnail((500, 500), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.structure_image_label.configure(image=photo, text="")
                self.structure_image_label.image = photo
                self._current_structure_photo = photo
            except Exception as e:
                self.structure_image_label.configure(image="", text=f"[image error: {e}]")
                self._current_structure_photo = None
        else:
            self.structure_image_label.configure(
                image="", text="[ no structure image available ]"
            )
            self._current_structure_photo = None

    def _trigger_live_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("WARNING", "Enter a chemical name in the FILTER field.")
            self._sfx("error")
            return

        self._sfx("browse")
        self.status_var.set(f"SEARCHING PubChem for '{query}'...")
        self.root.update()

        results = search_pubchem(query)
        added = 0
        for r in results:
            name = r["name"]
            data = {
                "cas": r.get("cas", "PubChem-Fetched"),
                "formula": r["formula"],
                "mw": r["mw"],
                "type": r.get("type", "PubChem Compound"),
                "structure": r["smiles"] or "",
                "mechanism": r.get("mechanism") or f"PubChem CID {r['cid']}. IUPAC: {r['iupac'] or 'N/A'}",
                "targets": r.get("targets") or ["See PubChem record"],
                "organs": _default_organs(),
                "half_life_hr": 4.0,
                "vd_l_kg": 1.0,
                "clearance_ml_min": 50.0,
                "bioavailability": 0.8,
                "ld50_mg_kg": 50.0,
                "tox_threshold_mg_L": 10.0,
                "cyp_substrate": ["CYP3A4"],
                "cyp_inhibitor": [],
                "cid": r["cid"],
                "source": "PubChem",
            }
            if register_compound(name, data):
                added += 1

        self._populate_list(query)
        self.status_var.set(f"PubChem: {len(results)} found, {added} added to catalog.")

        if self.poison_listbox.size() > 0:
            self.poison_listbox.selection_clear(0, tk.END)
            self.poison_listbox.selection_set(0)
            self.poison_listbox.see(0)
            self._on_select(None)

    def _on_select(self, event):
        selection = self.poison_listbox.curselection()
        if not selection:
            return
        name = self.poison_listbox.get(selection[0])
        poison = get_poison(name)
        if not poison:
            return

        details = f"""SPECIMEN: {name.upper()}
CAS: {poison.get('cas', 'N/A')}
FORMULA: {poison.get('formula', 'N/A')}
MW: {poison.get('mw', 0)} g/mol
TYPE: {poison.get('type', 'N/A')}

MECHANISM:
{poison.get('mechanism', 'N/A')}

TARGETS: {', '.join(poison.get('targets', []))}
ORGANS: {', '.join(poison.get('organs', {}).keys())}

PHARMACOKINETICS:
  Half-life: {poison.get('half_life_hr', 4.0)} hr
  Vd: {poison.get('vd_l_kg', 1.0)} L/kg
  Clearance: {poison.get('clearance_ml_min', 10.0)} mL/min
  LD50: {poison.get('ld50_mg_kg', 100.0)} mg/kg
  Tox Threshold: {poison.get('tox_threshold_mg_L', 1.0)} mg/L

CYP450: sub={poison.get('cyp_substrate', [])}, inh={poison.get('cyp_inhibitor', [])}
"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", details)
        self.details_text.config(state=tk.DISABLED)

        self._update_structure_view(name, poison)

    def _add_to_mixture(self):
        selection = self.poison_listbox.curselection()
        if not selection:
            messagebox.showwarning("WARNING", "Select a specimen from database first.")
            self._sfx("error")
            return

        name = self.poison_listbox.get(selection[0])
        try:
            dose = float(self.dose_var.get())
            if dose <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("ERROR", "Invalid dose format specified.")
            self._sfx("error")
            return

        self.selected_poisons[name] = dose
        self._update_mixture_display()
        self.status_var.set(f"LOADED: {name} @ {dose} mg/kg")
        self._sfx("add")

    def _remove_from_mixture(self):
        selection = self.mixture_listbox.curselection()
        if not selection:
            return
        item_text = self.mixture_listbox.get(selection[0])
        name = item_text.split(" @")[0]
        if name in self.selected_poisons:
            del self.selected_poisons[name]
            self._update_mixture_display()
            self.status_var.set(f"PURGED: {name}")
            self._sfx("purge")

    def _clear_mixture(self):
        self.selected_poisons.clear()
        self._update_mixture_display()
        self.status_var.set("MIXTURE PURGED CLEAN.")
        self._sfx("purge_all")

    def _update_mixture_display(self):
        self.mixture_listbox.delete(0, tk.END)
        for name, dose in self.selected_poisons.items():
            self.mixture_listbox.insert(tk.END, f"{name} @ {dose} mg/kg")
        self._render_mixture_structure()

    def _run_simulation(self):
        if not self.selected_poisons:
            messagebox.showwarning("WARNING", "Mixture is empty. Load specimens first.")
            self._sfx("error")
            return

        self._sfx("run")
        self.status_var.set("RUNNING SIMULATION MATRIX...")
        self.root.update()

        try:
            poisons = []
            for name in self.selected_poisons:
                data = get_poison(name)
                if data:
                    poisons.append(create_poison_pk(data, name))

            self.results = self.simulator.simulate_mixture(
                poisons=poisons,
                doses_mg_kg=self.selected_poisons,
                time_end=24.0,
            )

            self._plot_results()
            self._update_interaction_display()
            self._update_summary()
            self.status_var.set(f"SIMULATION COMPLETE — LETHALITY: {self.results['lethality_score']:.2f} | CRITICAL: {self.results['critical_organ'].upper()}")
            self._sfx("complete")

        except Exception as e:
            messagebox.showerror("CRITICAL ERROR", str(e))
            self.status_var.set("SIMULATION FAILED.")
            self._sfx("error")

    def _plot_results(self):
        self.ax_pk.clear()
        self.ax_pk.set_facecolor(self.plot_ax_bg)

        colors = ["#33ff33", "#00ffcc", "#ffbb00", "#ff6666", "#cc66ff"]
        for i, (name, conc) in enumerate(self.results["concentrations"].items()):
            color = colors[i % len(colors)]
            self.ax_pk.plot(self.results["time"], conc, label=name, color=color, linewidth=2.4)
            poison = get_poison(name)
            if poison:
                self.ax_pk.axhline(y=poison.get("tox_threshold_mg_L", 1.0),
                                   color=color, linestyle=":", alpha=0.8)

        self.ax_pk.set_xlabel("TIME (hr)", color="#66ff99")
        self.ax_pk.set_ylabel("CONCENTRATION (mg/L)", color="#66ff99")
        self.ax_pk.set_title("PLASMA CONCENTRATION CURVES", color="#66ff99", fontweight="bold")
        self.ax_pk.legend(facecolor="#0f1c0f", labelcolor="#66ff99", edgecolor="#2a6d2a")
        self.ax_pk.tick_params(colors="#66ff99")
        self.ax_pk.grid(True, color=self.grid_color, alpha=0.7)
        self.canvas_pk.draw()

        self.ax_organs.clear()
        self.ax_organs.set_facecolor(self.plot_ax_bg)

        organ_names = list(self.results["organ_damage"].keys())
        final_damage = [self.results["organ_damage"][o][-1] for o in organ_names]

        self.ax_organs.barh(organ_names, final_damage, color="#33ff33", edgecolor="#66ff99")
        self.ax_organs.set_xlabel("DAMAGE INDEX (0-10)", color="#66ff99")
        self.ax_organs.set_title("ORGAN DEGRADATION (T+24H)", color="#66ff99", fontweight="bold")
        self.ax_organs.tick_params(colors="#66ff99")
        self.ax_organs.set_xlim(0, 10)
        self.ax_organs.grid(True, color=self.grid_color, alpha=0.7)
        self.canvas_organs.draw()

    def _update_interaction_display(self):
        self.interaction_text.delete("1.0", tk.END)

        names = list(self.selected_poisons.keys())
        if len(names) < 2:
            self.interaction_text.insert("1.0", "> ADD 2+ SPECIMENS FOR INTERACTION MATRIX ANALYSIS.")
            return

        lines = ["=" * 65, "VAULT-TEC SYNERGY & ANTAGONISM MATRIX", "=" * 65, ""]

        for i, n1 in enumerate(names):
            for j, n2 in enumerate(names):
                if i < j:
                    inter = get_interaction(n1, n2)
                    lines.append(f"[{n1}] + [{n2}]")
                    lines.append(f"  TYPE: {inter['type'].upper()}")
                    lines.append(f"  MULTIPLIER: {inter['multiplier']:.2f}x")
                    lines.append(f"  MECHANISM: {inter['mechanism']}")
                    lines.append("")

        lines.append("=" * 65)
        lines.append("CYP450 METABOLIC ENZYME ACTIVITY STATUS")
        lines.append("=" * 65)
        for cyp, activity in self.results["cyp_activity"].items():
            status = "NOMINAL" if activity > 0.9 else "INHIBITED" if activity < 0.5 else "SUPPRESSED"
            lines.append(f"  {cyp}: {activity:.2f} [{status}]")

        self.interaction_text.insert("1.0", "\n".join(lines))

    def _update_summary(self):
        self.summary_text.delete("1.0", tk.END)

        lines = ["=" * 65, "CLINICAL SIMULATION STATUS REPORT", "=" * 65, ""]

        lines.append(f"Subject Body Weight: {self.simulator.bw} kg")
        lines.append(f"Active Compound Count: {len(self.selected_poisons)}")
        lines.append("")

        lines.append("DOSAGE LOAD:")
        for name, dose in self.selected_poisons.items():
            poison = get_poison(name)
            ld50_frac = (dose / poison["ld50_mg_kg"]) * 100 if poison else 0
            lines.append(f"  {name}: {dose} mg/kg ({ld50_frac:.1f}% of LD50)")
        lines.append("")

        combined = self._build_mixture_formula()
        lines.append("MIXTURE FORMULA:")
        for name in self.selected_poisons:
            p = get_poison(name)
            if p:
                lines.append(f"  {name}: {p.get('formula', 'N/A')}")
        lines.append(f"  => combined: {combined or 'unavailable'}")
        lines.append("")

        lines.append("EVALUATION OUTCOMES:")
        lines.append(f"  Overall Lethality Index: {self.results['lethality_score']:.2f} / 10.0")
        lines.append(f"  Primary Target Failure: {self.results['critical_organ'].upper()}")
        lines.append("")

        lines.append("TIME TO TOXIC THRESHOLD:")
        for name, t in self.results["time_to_toxicity"].items():
            if t:
                lines.append(f"  {name}: breached at {t:.2f} hrs")
            else:
                lines.append(f"  {name}: threshold unreached")
        lines.append("")

        lines.append("ORGAN STATUS (24 HOUR FINAL):")
        for organ, damage in self.results["organ_damage"].items():
            final = damage[-1]
            status = "CRITICAL" if final > 7 else "SEVERE" if final > 4 else "MODERATE" if final > 2 else "MILD" if final > 0.5 else "STABLE"
            lines.append(f"  {organ.capitalize()}: {final:.2f}/10 [{status}]")

        self.summary_text.insert("1.0", "\n".join(lines))

    def _save_mixture(self):
        if not self.selected_poisons:
            messagebox.showwarning("WARNING", "Mixture is empty.")
            self._sfx("error")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile="vault_mixture.json"
        )
        if filepath:
            poison_data = {}
            for name in self.selected_poisons:
                data = get_poison(name)
                if data:
                    poison_data[name] = data

            payload = {
                "body_weight_kg": self.simulator.bw,
                "poisons": self.selected_poisons,
                "poison_data": poison_data,
            }
            with open(filepath, "w") as f:
                json.dump(payload, f, indent=2)
            self.status_var.set(f"MIXTURE SAVED TO {filepath}")
            self._sfx("save")

    def _load_mixture(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")]
        )
        if filepath:
            with open(filepath, "r") as f:
                data = json.load(f)

            self.selected_poisons = data.get("poisons", {})
            self.simulator.bw = data.get("body_weight_kg", 70.0)

            poison_data = data.get("poison_data", {})
            restored = 0
            for name, pdata in poison_data.items():
                if name not in POISONS:
                    POISONS[name] = pdata
                    restored += 1

            self._update_mixture_display()
            self._populate_list(self.search_var.get())
            self.status_var.set(
                f"MIXTURE LOADED FROM {filepath} ({restored} compounds restored)"
            )
            self._sfx("load")


if __name__ == "__main__":
    root = tk.Tk()
    app = PoisonDashboard(root)
    root.mainloop()