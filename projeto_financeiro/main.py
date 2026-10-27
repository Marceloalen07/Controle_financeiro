
import tkinter as tk
from tkinter import messagebox

from interface import AplicativoFinanceiro


def main():
    janela = tk.Tk()

    try:
        AplicativoFinanceiro(janela)

    except (ValueError, OSError) as erro:
        messagebox.showerror(
            "Erro ao iniciar",
            f"Não foi possível carregar os dados:\n{erro}",
            parent=janela
        )
        janela.destroy()
        return

    janela.mainloop()


if __name__ == "__main__":
    main()
