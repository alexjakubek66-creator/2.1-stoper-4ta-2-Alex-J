"""
Stoper - Aplikacja desktopowa do mierzenia czasu.
Autor: Automatycznie wygenerowana
"""

import tkinter as tk
from tkinter import font as tkfont
import time


class StoperApp:
    """Główna klasa aplikacji Stoper."""

    # --- Kolory i stałe stylu ---
    BG_COLOR = "#1a1a2e"           # ciemne tło
    PANEL_COLOR = "#16213e"        # panel wyświetlacza
    ACCENT_COLOR = "#0f3460"       # akcent
    START_COLOR = "#00b894"        # zielony – START
    START_HOVER = "#00a381"
    STOP_COLOR = "#e17055"         # czerwony – STOP
    STOP_HOVER = "#d35400"
    RESET_COLOR = "#636e72"        # szary – RESET
    RESET_HOVER = "#535c60"
    TEXT_COLOR = "#ffffff"
    TIME_COLOR = "#00cec9"         # kolor cyfrowego zegara
    LABEL_COLOR = "#a0a0b0"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._configure_window()

        # Stan stopera
        self._running = False
        self._start_time = 0.0
        self._elapsed = 0.0

        # Budowa interfejsu
        self._build_ui()

        # Rozpocznij pętlę aktualizacji
        self._update_display()

    # ------------------------------------------------------------------ #
    #  Konfiguracja okna                                                  #
    # ------------------------------------------------------------------ #
    def _configure_window(self) -> None:
        self.root.title("⏱ Stoper")
        self.root.geometry("560x700")
        self.root.minsize(480, 600)
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(True, True)

        # Wycentruj okno na ekranie
        self.root.update_idletasks()
        w = 560
        h = 700
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ------------------------------------------------------------------ #
    #  Budowa interfejsu                                                  #
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        # Nagłówek
        header = tk.Frame(self.root, bg=self.BG_COLOR, pady=20)
        header.pack(fill=tk.X)

        title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        tk.Label(
            header,
            text="⏱  STOPER",
            font=title_font,
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
        ).pack()

        # Panel z wyświetlaczem czasu
        display_frame = tk.Frame(
            self.root, bg=self.PANEL_COLOR, bd=0, highlightthickness=2,
            highlightbackground=self.ACCENT_COLOR, pady=30, padx=20,
        )
        display_frame.pack(fill=tk.X, padx=40, pady=(10, 5))

        time_font = tkfont.Font(family="Consolas", size=64, weight="bold")
        self.time_label = tk.Label(
            display_frame,
            text="00:00:00",
            font=time_font,
            fg=self.TIME_COLOR,
            bg=self.PANEL_COLOR,
        )
        self.time_label.pack()

        # Milisekundy
        ms_font = tkfont.Font(family="Consolas", size=28)
        self.ms_label = tk.Label(
            display_frame,
            text=".000",
            font=ms_font,
            fg="#778ca3",
            bg=self.PANEL_COLOR,
        )
        self.ms_label.pack()

        # Etykieta statusu
        status_font = tkfont.Font(family="Segoe UI", size=12)
        self.status_label = tk.Label(
            self.root,
            text="Gotowy",
            font=status_font,
            fg=self.LABEL_COLOR,
            bg=self.BG_COLOR,
            pady=10,
        )
        self.status_label.pack()

        # Ramka na przyciski
        btn_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=20)
        btn_frame.pack(fill=tk.X, padx=40)

        btn_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")

        # Przycisk START
        self.start_btn = tk.Button(
            btn_frame,
            text="▶  START",
            font=btn_font,
            fg=self.TEXT_COLOR,
            bg=self.START_COLOR,
            activebackground=self.START_HOVER,
            activeforeground=self.TEXT_COLOR,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=18,
            command=self._start,
        )
        self.start_btn.pack(fill=tk.X, pady=(0, 12))

        # Przycisk STOP
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹  STOP",
            font=btn_font,
            fg=self.TEXT_COLOR,
            bg=self.STOP_COLOR,
            activebackground=self.STOP_HOVER,
            activeforeground=self.TEXT_COLOR,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=18,
            state=tk.DISABLED,
            command=self._stop,
        )
        self.stop_btn.pack(fill=tk.X, pady=(0, 12))

        # Przycisk RESET
        self.reset_btn = tk.Button(
            btn_frame,
            text="↺  RESET",
            font=btn_font,
            fg=self.TEXT_COLOR,
            bg=self.RESET_COLOR,
            activebackground=self.RESET_HOVER,
            activeforeground=self.TEXT_COLOR,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            padx=30,
            pady=18,
            state=tk.DISABLED,
            command=self._reset,
        )
        self.reset_btn.pack(fill=tk.X)

        # Hover na przyciskach
        self._bind_hover(self.start_btn, self.START_COLOR, self.START_HOVER)
        self._bind_hover(self.stop_btn, self.STOP_COLOR, self.STOP_HOVER)
        self._bind_hover(self.reset_btn, self.RESET_COLOR, self.RESET_HOVER)

        # Stopka
        footer_font = tkfont.Font(family="Segoe UI", size=9)
        tk.Label(
            self.root,
            text="Stoper v1.0  •  Aplikacja desktopowa",
            font=footer_font,
            fg="#555566",
            bg=self.BG_COLOR,
        ).pack(side=tk.BOTTOM, pady=10)

    # ------------------------------------------------------------------ #
    #  Efekty hover                                                       #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _bind_hover(button: tk.Button, normal: str, hover: str) -> None:
        def on_enter(_event: tk.Event) -> None:
            if button["state"] != "disabled":
                button.configure(bg=hover)

        def on_leave(_event: tk.Event) -> None:
            if button["state"] != "disabled":
                button.configure(bg=normal)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # ------------------------------------------------------------------ #
    #  Logika stopera                                                     #
    # ------------------------------------------------------------------ #
    def _start(self) -> None:
        """Uruchom stoper."""
        if not self._running:
            self._running = True
            self._start_time = time.perf_counter() - self._elapsed
            self.start_btn.configure(state=tk.DISABLED, bg="#2d6a4f")
            self.stop_btn.configure(state=tk.NORMAL, bg=self.STOP_COLOR)
            self.reset_btn.configure(state=tk.DISABLED, bg="#4a4e50")
            self.status_label.configure(text="▶  Pomiar w toku…", fg="#00b894")

    def _stop(self) -> None:
        """Zatrzymaj stoper."""
        if self._running:
            self._running = False
            self._elapsed = time.perf_counter() - self._start_time
            self.start_btn.configure(state=tk.NORMAL, bg=self.START_COLOR)
            self.stop_btn.configure(state=tk.DISABLED, bg="#8B4513")
            self.reset_btn.configure(state=tk.NORMAL, bg=self.RESET_COLOR)
            self.status_label.configure(text="⏸  Zatrzymany", fg="#e17055")

    def _reset(self) -> None:
        """Resetuj stoper do zera."""
        self._running = False
        self._elapsed = 0.0
        self.time_label.configure(text="00:00:00")
        self.ms_label.configure(text=".000")
        self.start_btn.configure(state=tk.NORMAL, bg=self.START_COLOR)
        self.stop_btn.configure(state=tk.DISABLED, bg="#8B4513")
        self.reset_btn.configure(state=tk.DISABLED, bg="#4a4e50")
        self.status_label.configure(text="Gotowy", fg=self.LABEL_COLOR)

    # ------------------------------------------------------------------ #
    #  Aktualizacja wyświetlacza                                          #
    # ------------------------------------------------------------------ #
    def _update_display(self) -> None:
        """Aktualizuje wyświetlacz co ~10 ms."""
        if self._running:
            self._elapsed = time.perf_counter() - self._start_time

        total_seconds = int(self._elapsed)
        millis = int((self._elapsed - total_seconds) * 1000)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        self.time_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.ms_label.configure(text=f".{millis:03d}")

        self.root.after(10, self._update_display)


def main() -> None:
    """Punkt wejścia aplikacji."""
    root = tk.Tk()
    StoperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
