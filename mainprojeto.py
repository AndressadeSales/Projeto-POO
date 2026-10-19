import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Aluno, Curso, Professor, Disciplina
from gerenciadores import (
    GerenciadorAlunos,
    GerenciadorCursos,
    GerenciadorProfessores,
    GerenciadorDisciplinas
)

class SistemaAcademicoGUI:
    """Classe principal que constrói e controla a Interface Gráfica (GUI) em Tkinter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integrado de Gestão Acadêmica")
        self.root.geometry("850x600")

        # Inicialização dos gerenciadores que tratam a gravação/leitura nos arquivos TXT
        self.g_alunos = GerenciadorAlunos()
        self.g_cursos = GerenciadorCursos()
        self.g_professores = GerenciadorProfessores()
        self.g_disciplinas = GerenciadorDisciplinas()

        # Criação dos separadores por abas (Notebook Tkinter)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Definição das abas da interface
        self.aba_cursos = ttk.Frame(self.notebook)
        self.aba_alunos = ttk.Frame(self.notebook)
        self.aba_professores = ttk.Frame(self.notebook)
        self.aba_disciplinas = ttk.Frame(self.notebook)
        self.aba_relatorio = ttk.Frame(self.notebook)

        # Adição das abas ao Notebook
        self.notebook.add(self.aba_cursos, text="Cursos")
        self.notebook.add(self.aba_alunos, text="Alunos")
        self.notebook.add(self.aba_professores, text="Professores")
        self.notebook.add(self.aba_disciplinas, text="Disciplinas")
        self.notebook.add(self.aba_relatorio, text="Relatório Integrado")

        # Métodos para montar os formulários de cada aba
        self.setup_aba_cursos()
        self.setup_aba_alunos()
        self.setup_aba_professores()
        self.setup_aba_disciplinas()
        self.setup_aba_relatorio()

    # ==========================================================================
    # INTERFACE DE CURSOS (EQUIPE ALFA)
    # ==========================================================================
    def setup_aba_cursos(self):
        # Formulário de entrada de dados
        frame = ttk.LabelFrame(self.aba_cursos, text="Gerenciar Curso")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_curso_cod = ttk.Entry(frame)
        self.ent_curso_cod.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_curso_nome = ttk.Entry(frame)
        self.ent_curso_nome.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Modalidade:").grid(row=1, column=0, padx=5, pady=5)
        self.cb_curso_mod = ttk.Combobox(frame, values=["Presencial", "EAD"], state="readonly")
        self.cb_curso_mod.grid(row=1, column=1, padx=5, pady=5)
        self.cb_curso_mod.current(0)

        # Botões de Ações (CRUD)
        btn_frame = ttk.Frame(self.aba_cursos)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_curso).pack(side="left", padx=5)

        # Listbox para exibição dos dados
        self.list_cursos = tk.Listbox(self.aba_cursos)
        self.list_cursos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_cursos()

    def cadastrar_curso(self):
        c = Curso(self.ent_curso_cod.get(), self.ent_curso_nome.get(), self.cb_curso_mod.get())
        if not c.codigo or not c.nome:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        self.g_cursos.cadastrar(c)
        self.atualizar_cursos()
        messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")

    def alterar_curso(self):
        self.g_cursos.alterar(self.ent_curso_cod.get(), self.ent_curso_nome.get(), self.cb_curso_mod.get())
        self.atualizar_cursos()

    def excluir_curso(self):
        self.g_cursos.excluir(self.ent_curso_cod.get())
        self.atualizar_cursos()

    def atualizar_cursos(self):
        self.list_cursos.delete(0, tk.END)
        for c in self.g_cursos.carregar_todos():
            self.list_cursos.insert(tk.END, str(c))

    # ==========================================================================
    # INTERFACE DE ALUNOS (EQUIPE ALFA)
    # ==========================================================================
    def setup_aba_alunos(self):
        frame = ttk.LabelFrame(self.aba_alunos, text="Gerenciar Aluno")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Matrícula:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_aluno_mat = ttk.Entry(frame)
        self.ent_aluno_mat.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_aluno_nome = ttk.Entry(frame)
        self.ent_aluno_nome.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_aluno_cpf = ttk.Entry(frame)
        self.ent_aluno_cpf.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="E-mail:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_aluno_email = ttk.Entry(frame)
        self.ent_aluno_email.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Cód. Curso:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_aluno_codcurso = ttk.Entry(frame)
        self.ent_aluno_codcurso.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self.aba_alunos)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_aluno).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar_aluno).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_aluno).pack(side="left", padx=5)

        self.list_alunos = tk.Listbox(self.aba_alunos)
        self.list_alunos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_alunos()

    def cadastrar_aluno(self):
        a = Aluno(
            self.ent_aluno_mat.get(),
            self.ent_aluno_nome.get(),
            self.ent_aluno_cpf.get(),
            self.ent_aluno_email.get(),
            self.ent_aluno_codcurso.get()
        )
        self.g_alunos.cadastrar(a)
        self.atualizar_alunos()

    def alterar_aluno(self):
        self.g_alunos.alterar(
            self.ent_aluno_mat.get(),
            self.ent_aluno_nome.get(),
            self.ent_aluno_cpf.get(),
            self.ent_aluno_email.get(),
            self.ent_aluno_codcurso.get()
        )
        self.atualizar_alunos()

    def excluir_aluno(self):
        self.g_alunos.excluir(self.ent_aluno_mat.get())
        self.atualizar_alunos()

    def atualizar_alunos(self):
        self.list_alunos.delete(0, tk.END)
        for a in self.g_alunos.carregar_todos():
            self.list_alunos.insert(tk.END, str(a))

    # ==========================================================================
    # INTERFACE DE PROFESSORES (EQUIPE BETA)
    # ==========================================================================
    def setup_aba_professores(self):
        frame = ttk.LabelFrame(self.aba_professores, text="Gerenciar Professor")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_prof_cod = ttk.Entry(frame)
        self.ent_prof_cod.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_prof_nome = ttk.Entry(frame)
        self.ent_prof_nome.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="CPF:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_prof_cpf = ttk.Entry(frame)
        self.ent_prof_cpf.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Especialidade:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_prof_esp = ttk.Entry(frame)
        self.ent_prof_esp.grid(row=1, column=3, padx=5, pady=5)

        btn_frame = ttk.Frame(self.aba_professores)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_professor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar_professor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_professor).pack(side="left", padx=5)

        self.list_profs = tk.Listbox(self.aba_professores)
        self.list_profs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_professores()

    def cadastrar_professor(self):
        p = Professor(
            self.ent_prof_cod.get(),
            self.ent_prof_nome.get(),
            self.ent_prof_cpf.get(),
            self.ent_prof_esp.get()
        )
        self.g_professores.cadastrar(p)
        self.atualizar_professores()

    def alterar_professor(self):
        self.g_professores.alterar(
            self.ent_prof_cod.get(),
            self.ent_prof_nome.get(),
            self.ent_prof_cpf.get(),
            self.ent_prof_esp.get()
        )
        self.atualizar_professores()

    def excluir_professor(self):
        self.g_professores.excluir(self.ent_prof_cod.get())
        self.atualizar_professores()

    def atualizar_professores(self):
        self.list_profs.delete(0, tk.END)
        for p in self.g_professores.carregar_todos():
            self.list_profs.insert(tk.END, str(p))

    # ==========================================================================
    # INTERFACE DE DISCIPLINAS (EQUIPE BETA)
    # ==========================================================================
    def setup_aba_disciplinas(self):
        frame = ttk.LabelFrame(self.aba_disciplinas, text="Gerenciar Disciplina")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_disc_cod = ttk.Entry(frame)
        self.ent_disc_cod.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Nome:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_disc_nome = ttk.Entry(frame)
        self.ent_disc_nome.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Carga Horária:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_disc_ch = ttk.Entry(frame)
        self.ent_disc_ch.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Cód. Professor:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_disc_codprof = ttk.Entry(frame)
        self.ent_disc_codprof.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Cód. Curso:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_disc_codcurso = ttk.Entry(frame)
        self.ent_disc_codcurso.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self.aba_disciplinas)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_disciplina).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar_disciplina).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_disciplina).pack(side="left", padx=5)

        self.list_discs = tk.Listbox(self.aba_disciplinas)
        self.list_discs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_disciplinas()

    def cadastrar_disciplina(self):
        d = Disciplina(
            self.ent_disc_cod.get(),
            self.ent_disc_nome.get(),
            self.ent_disc_ch.get(),
            self.ent_disc_codprof.get(),
            self.ent_disc_codcurso.get()
        )
        self.g_disciplinas.cadastrar(d)
        self.atualizar_disciplinas()

    def alterar_disciplina(self):
        self.g_disciplinas.alterar(
            self.ent_disc_cod.get(),
            self.ent_disc_nome.get(),
            self.ent_disc_ch.get(),
            self.ent_disc_codprof.get(),
            self.ent_disc_codcurso.get()
        )
        self.atualizar_disciplinas()

    def excluir_disciplina(self):
        self.g_disciplinas.excluir(self.ent_disc_cod.get())
        self.atualizar_disciplinas()

    def atualizar_disciplinas(self):
        self.list_discs.delete(0, tk.END)
        for d in self.g_disciplinas.carregar_todos():
            self.list_discs.insert(tk.END, str(d))

    # ==========================================================================
    # RELATÓRIO INTEGRADO (SINTESE DOS MÓDULOS ALFA E BETA)
    # ==========================================================================
    def setup_aba_relatorio(self):
        btn_frame = ttk.Frame(self.aba_relatorio)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Gerar Relatório Completo", command=self.gerar_relatorio).pack(side="left", padx=5)

        # Caixa de Texto multilinha para apresentar o resultado final
        self.txt_relatorio = tk.Text(self.aba_relatorio, wrap="word")
        self.txt_relatorio.pack(fill="both", expand=True, padx=10, pady=10)

    def gerar_relatorio(self):
        """
        Gera o relatório integrado mapeando os IDs de Curso e Professor entre as entidades
        conforme especificado na Seção 5 dos requisitos do projeto.
        """
        self.txt_relatorio.delete("1.0", tk.END)

        # Carrega todas as informações salvas dos arquivos TXT
        alunos = self.g_alunos.carregar_todos()
        cursos = {c.codigo: c for c in self.g_cursos.carregar_todos()}
        professores = {p.codigo: p for p in self.g_professores.carregar_todos()}
        disciplinas = self.g_disciplinas.carregar_todos()

        if not alunos:
            self.txt_relatorio.insert(tk.END, "Nenhum aluno encontrado nos dados persistidos.\n")
            return

        # Itera sobre cada aluno para montar a frase relacionando as entidades
        for aluno in alunos:
            curso = cursos.get(aluno.codigo_curso)
            nome_curso = curso.nome if curso else f"[Curso ID '{aluno.codigo_curso}' Desconhecido]"

            # Localiza todas as disciplinas do mesmo curso do aluno
            discs_aluno = [d for d in disciplinas if d.codigo_curso == aluno.codigo_curso]

            if discs_aluno:
                for disc in discs_aluno:
                    prof = professores.get(disc.codigo_professor)
                    nome_prof = prof.nome if prof else f"[Prof ID '{disc.codigo_professor}' Desconhecido]"

                    # Formatação da frase padrão solicitada no documento
                    frase = (
                        f"O Aluno {aluno.nome} está matriculado no curso {nome_curso}, "
                        f"assistindo a disciplina {disc.nome} com o professor {nome_prof}.\n\n"
                    )
                    self.txt_relatorio.insert(tk.END, frase)
            else:
                frase = (
                    f"O Aluno {aluno.nome} está matriculado no curso {nome_curso}, "
                    f"mas não há disciplinas vinculadas a este curso no momento.\n\n"
                )
                self.txt_relatorio.insert(tk.END, frase)


# Ponto de entrada da aplicação Python
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAcademicoGUI(root)
    root.mainloop()