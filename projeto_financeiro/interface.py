
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import financeiro


def formatar_dinheiro(centavos):
    """Converte centavos para o formato monetário brasileiro."""
    valor = centavos / 100
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class AplicativoFinanceiro:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Controle Financeiro Pessoal")
        self.janela.geometry("1000x650")
        self.janela.minsize(800, 550)

        self.criar_interface()
        self.atualizar_tela()

    def criar_interface(self):
        principal = ttk.Frame(self.janela, padding=20)
        principal.pack(fill="both", expand=True)

        # Título
        ttk.Label(
            principal,
            text="Controle Financeiro Pessoal",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        # Indicadores financeiros
        indicadores = ttk.Frame(principal)
        indicadores.pack(fill="x", pady=(0, 20))

        self.label_receitas = ttk.Label(
            indicadores,
            text="Receitas: R$ 0,00"
        )
        self.label_despesas = ttk.Label(
            indicadores,
            text="Despesas: R$ 0,00"
        )
        self.label_saldo = ttk.Label(
            indicadores,
            text="Saldo: R$ 0,00"
        )

        for coluna, label in enumerate([
            self.label_receitas,
            self.label_despesas,
            self.label_saldo
        ]):
            label.grid(
                row=0,
                column=coluna,
                padx=10,
                sticky="w"
            )
            label.configure(font=("Arial", 12, "bold"))

        for coluna in range(3):
            indicadores.columnconfigure(coluna, weight=1)

        # Formulário de movimentação
        formulario = ttk.LabelFrame(
            principal,
            text="Nova movimentação",
            padding=12
        )
        formulario.pack(fill="x", pady=(0, 15))

        # Tipo
        ttk.Label(formulario, text="Tipo:").grid(
            row=0, column=0, sticky="w"
        )

        self.tipo = ttk.Combobox(
            formulario,
            values=["Receita", "Despesa"],
            state="readonly"
        )
        self.tipo.set("Despesa")
        self.tipo.grid(
            row=1, column=0, padx=5, pady=5, sticky="ew"
        )

        # Descrição
        ttk.Label(formulario, text="Descrição:").grid(
            row=0, column=1, sticky="w"
        )

        self.descricao = ttk.Entry(formulario)
        self.descricao.grid(
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )

        # Valor
        ttk.Label(formulario, text="Valor (R$):").grid(
            row=0, column=2, sticky="w"
        )

        self.valor = ttk.Entry(formulario)
        self.valor.grid(
            row=1, column=2, padx=5, pady=5, sticky="ew"
        )

        # Categoria
        ttk.Label(formulario, text="Categoria:").grid(
            row=2, column=0, sticky="w"
        )

        self.categoria = ttk.Combobox(
            formulario,
            values=[
                "Alimentação",
                "Transporte",
                "Moradia",
                "Estudos",
                "Lazer",
                "Trabalho",
                "Saúde",
                "Outros"
            ]
        )
        self.categoria.grid(
            row=3, column=0, padx=5, pady=5, sticky="ew"
        )

        # Data
        ttk.Label(
            formulario,
            text="Data (DD/MM/AAAA):"
        ).grid(
            row=2, column=1, sticky="w"
        )

        self.data = ttk.Entry(formulario)
        self.data.insert(
            0, date.today().strftime("%d/%m/%Y")
        )
        self.data.grid(
            row=3, column=1, padx=5, pady=5, sticky="ew"
        )

        # Botão de adicionar
        ttk.Button(
            formulario,
            text="Adicionar",
            command=self.adicionar
        ).grid(
            row=3, column=2, padx=5, pady=5, sticky="ew"
        )

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=2)
        formulario.columnconfigure(2, weight=1)

        # Histórico de movimentações
        ttk.Label(
            principal,
            text="Histórico de movimentações",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(0, 8))

        tabela_frame = ttk.Frame(principal)
        tabela_frame.pack(fill="both", expand=True)

        colunas = (
            "data",
            "tipo",
            "descricao",
            "categoria",
            "valor"
        )

        self.tabela = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings",
            selectmode="browse"
        )

        titulos = {
            "data": "Data",
            "tipo": "Tipo",
            "descricao": "Descrição",
            "categoria": "Categoria",
            "valor": "Valor"
        }

        larguras = {
            "data": 110,
            "tipo": 100,
            "descricao": 250,
            "categoria": 150,
            "valor": 130
        }

        for coluna in colunas:
            self.tabela.heading(
                coluna,
                text=titulos[coluna]
            )
            self.tabela.column(
                coluna,
                width=larguras[coluna]
            )

        barra = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela.yview
        )
        self.tabela.configure(
            yscrollcommand=barra.set
        )

        self.tabela.pack(
            side="left",
            fill="both",
            expand=True
        )
        barra.pack(side="right", fill="y")

        # Botão de excluir
        ttk.Button(
            principal,
            text="Excluir movimentação selecionada",
            command=self.excluir
        ).pack(anchor="e", pady=(12, 0))

    def adicionar(self):
        try:
            tipo = self.tipo.get()
            descricao = self.descricao.get()
            categoria = self.categoria.get()

            texto_valor = (
                self.valor.get()
                .strip()
                .replace(" ", "")
                .replace(",", ".")
            )

            valor_decimal = float(texto_valor)

            if valor_decimal <= 0:
                raise ValueError(
                    "O valor deve ser maior que zero."
                )

            valor_centavos = round(valor_decimal * 100)

            data_obj = datetime.strptime(
                self.data.get().strip(),
                "%d/%m/%Y"
            ).date()

            financeiro.adicionar_movimentacao(
                tipo,
                descricao,
                valor_centavos,
                categoria,
                data_obj.isoformat()
            )

            self.descricao.delete(0, tk.END)
            self.valor.delete(0, tk.END)

            self.atualizar_tela()

            messagebox.showinfo(
                "Sucesso",
                "Movimentação adicionada!",
                parent=self.janela
            )

        except ValueError as erro:
            messagebox.showerror(
                "Dados inválidos",
                str(erro) or "Informe um valor válido.",
                parent=self.janela
            )

        except OSError as erro:
            messagebox.showerror(
                "Erro ao salvar",
                f"Não foi possível salvar os dados:\n{erro}",
                parent=self.janela
            )

    def atualizar_tela(self):
        movimentacoes = financeiro.carregar_movimentacoes()
        resumo = financeiro.calcular_resumo(movimentacoes)

        self.label_receitas.config(
            text=f"Receitas: {formatar_dinheiro(resumo['receitas'])}"
        )

        self.label_despesas.config(
            text=f"Despesas: {formatar_dinheiro(resumo['despesas'])}"
        )

        self.label_saldo.config(
            text=f"Saldo: {formatar_dinheiro(resumo['saldo'])}"
        )

        # Limpa a tabela antes de atualizar.
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Exibe as movimentações mais recentes primeiro.
        for movimento in sorted(
            movimentacoes,
            key=lambda item: (item["data"], item["id"]),
            reverse=True
        ):
            data_formatada = datetime.strptime(
                movimento["data"],
                "%Y-%m-%d"
            ).strftime("%d/%m/%Y")

            self.tabela.insert(
                "",
                "end",
                iid=str(movimento["id"]),
                values=(
                    data_formatada,
                    movimento["tipo"],
                    movimento["descricao"],
                    movimento["categoria"],
                    formatar_dinheiro(
                        movimento["valor_centavos"]
                    )
                )
            )

    def excluir(self):
        selecionados = self.tabela.selection()

        if not selecionados:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma movimentação para excluir.",
                parent=self.janela
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir esta movimentação?",
            parent=self.janela
        )

        if confirmar:
            try:
                financeiro.excluir_movimentacao(
                    int(selecionados[0])
                )
                self.atualizar_tela()

            except (ValueError, OSError) as erro:
                messagebox.showerror(
                    "Erro",
                    str(erro),
                    parent=self.janela
                )
