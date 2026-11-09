import tkinter as tk
from tkinter import ttk, messagebox
from aluno import Aluno, GerenciadorAlunos
from curso import Curso, GerenciadorCursos
from professor import Professor, GerenciadorProfessores
from disciplina import Disciplina, GerenciadorDisciplinas
from nota import Nota, GerenciadorNotas

class SistemaAcademicoGUI:
    """Classe principal que constrói e controla a Interface Gráfica (GUI) em Tkinter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integrado de Gestão Acadêmica")
        self.root.geometry("900x700")

        # Inicialização dos gerenciadores de persistência em TXT
        self.g_alunos = GerenciadorAlunos()
        self.g_cursos = GerenciadorCursos()
        self.g_professores = GerenciadorProfessores()
        self.g_disciplinas = GerenciadorDisciplinas()
        self.g_notas = GerenciadorNotas()

        # Criação do sistema de abas (Notebook Tkinter)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Definição das abas
        self.aba_cursos = ttk.Frame(self.notebook)
        self.aba_alunos = ttk.Frame(self.notebook)
        self.aba_professores = ttk.Frame(self.notebook)
        self.aba_disciplinas = ttk.Frame(self.notebook)
        self.aba_notas = ttk.Frame(self.notebook)
        self.aba_relatorio = ttk.Frame(self.notebook)

        # Adição das abas ao Notebook
        self.notebook.add(self.aba_cursos, text="Cursos")
        self.notebook.add(self.aba_alunos, text="Alunos")
        self.notebook.add(self.aba_professores, text="Professores")
        self.notebook.add(self.aba_disciplinas, text="Disciplinas")
        self.notebook.add(self.aba_notas, text="Notas")
        self.notebook.add(self.aba_relatorio, text="Relatórios")

        # Montagem dos formulários de cada aba
        self.setup_aba_cursos()
        self.setup_aba_alunos()
        self.setup_aba_professores()
        self.setup_aba_disciplinas()
        self.setup_aba_notas()
        self.setup_aba_relatorio()

        # Botão de encerramento controlado (RF18)
        rodape = ttk.Frame(self.root)
        rodape.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(rodape, text="Encerrar Programa", command=self.root.destroy).pack(side="right")

    # ==========================================================================
    # INTERFACE DE CURSOS
    # ==========================================================================
    def setup_aba_cursos(self):
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

        btn_frame = ttk.Frame(self.aba_cursos)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar", command=self.cadastrar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar", command=self.alterar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Pesquisar", command=self.pesquisar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_cursos).pack(side="left", padx=5)

        self.list_cursos = tk.Listbox(self.aba_cursos)
        self.list_cursos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_cursos()

    def cadastrar_curso(self):
        cod, nome, mod = self.ent_curso_cod.get().strip(), self.ent_curso_nome.get().strip(), self.cb_curso_mod.get().strip()
        if not all([cod, nome, mod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return
        self.g_cursos.cadastrar(Curso(cod, nome, mod))
        self.atualizar_cursos()
        messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")

    def alterar_curso(self):
        cod, nome, mod = self.ent_curso_cod.get().strip(), self.ent_curso_nome.get().strip(), self.cb_curso_mod.get().strip()
        if not all([cod, nome, mod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_cursos.alterar(cod, nome, mod)
        self.atualizar_cursos()
        messagebox.showinfo("Sucesso", "Curso atualizado!")

    def excluir_curso(self):
        cod = self.ent_curso_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código!")
            return
        self.g_cursos.excluir(cod)
        self.atualizar_cursos()

    def pesquisar_curso(self):
        termo = self.ent_curso_cod.get().strip() or self.ent_curso_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para pesquisar!")
            return
        self.list_cursos.delete(0, tk.END)
        for c in self.g_cursos.buscar(termo):
            self.list_cursos.insert(tk.END, str(c))

    def atualizar_cursos(self):
        self.list_cursos.delete(0, tk.END)
        for c in self.g_cursos.carregar_todos():
            self.list_cursos.insert(tk.END, str(c))

    # ==========================================================================
    # INTERFACE DE ALUNOS
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
        ttk.Button(btn_frame, text="Pesquisar", command=self.pesquisar_aluno).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_alunos).pack(side="left", padx=5)

        self.list_alunos = tk.Listbox(self.aba_alunos)
        self.list_alunos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_alunos()

    def cadastrar_aluno(self):
        mat, nome, cpf, email, cod = self.ent_aluno_mat.get().strip(), self.ent_aluno_nome.get().strip(), self.ent_aluno_cpf.get().strip(), self.ent_aluno_email.get().strip(), self.ent_aluno_codcurso.get().strip()
        if not all([mat, nome, cpf, email, cod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_alunos.cadastrar(Aluno(mat, nome, cpf, email, cod))
        self.atualizar_alunos()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

    def alterar_aluno(self):
        mat, nome, cpf, email, cod = self.ent_aluno_mat.get().strip(), self.ent_aluno_nome.get().strip(), self.ent_aluno_cpf.get().strip(), self.ent_aluno_email.get().strip(), self.ent_aluno_codcurso.get().strip()
        if not all([mat, nome, cpf, email, cod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_alunos.alterar(mat, nome, cpf, email, cod)
        self.atualizar_alunos()
        messagebox.showinfo("Sucesso", "Aluno atualizado!")

    def excluir_aluno(self):
        mat = self.ent_aluno_mat.get().strip()
        if not mat:
            messagebox.showwarning("Aviso", "Informe a Matrícula!")
            return
        self.g_alunos.excluir(mat)
        self.atualizar_alunos()

    def pesquisar_aluno(self):
        termo = self.ent_aluno_mat.get().strip() or self.ent_aluno_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para pesquisar!")
            return
        self.list_alunos.delete(0, tk.END)
        for a in self.g_alunos.buscar(termo):
            self.list_alunos.insert(tk.END, str(a))

    def atualizar_alunos(self):
        self.list_alunos.delete(0, tk.END)
        for a in self.g_alunos.carregar_todos():
            self.list_alunos.insert(tk.END, str(a))

    # ==========================================================================
    # INTERFACE DE PROFESSORES
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
        ttk.Button(btn_frame, text="Pesquisar", command=self.pesquisar_professor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_professores).pack(side="left", padx=5)

        self.list_profs = tk.Listbox(self.aba_professores)
        self.list_profs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_professores()

    def cadastrar_professor(self):
        cod, nome, cpf, esp = self.ent_prof_cod.get().strip(), self.ent_prof_nome.get().strip(), self.ent_prof_cpf.get().strip(), self.ent_prof_esp.get().strip()
        if not all([cod, nome, cpf, esp]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_professores.cadastrar(Professor(cod, nome, cpf, esp))
        self.atualizar_professores()
        messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")

    def alterar_professor(self):
        cod, nome, cpf, esp = self.ent_prof_cod.get().strip(), self.ent_prof_nome.get().strip(), self.ent_prof_cpf.get().strip(), self.ent_prof_esp.get().strip()
        if not all([cod, nome, cpf, esp]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_professores.alterar(cod, nome, cpf, esp)
        self.atualizar_professores()
        messagebox.showinfo("Sucesso", "Professor atualizado!")

    def excluir_professor(self):
        cod = self.ent_prof_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código!")
            return
        self.g_professores.excluir(cod)
        self.atualizar_professores()

    def pesquisar_professor(self):
        termo = self.ent_prof_cod.get().strip() or self.ent_prof_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para pesquisar!")
            return
        self.list_profs.delete(0, tk.END)
        for p in self.g_professores.buscar(termo):
            self.list_profs.insert(tk.END, str(p))

    def atualizar_professores(self):
        self.list_profs.delete(0, tk.END)
        for p in self.g_professores.carregar_todos():
            self.list_profs.insert(tk.END, str(p))

    # ==========================================================================
    # INTERFACE DE DISCIPLINAS
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
        ttk.Button(btn_frame, text="Pesquisar", command=self.pesquisar_disciplina).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todas", command=self.atualizar_disciplinas).pack(side="left", padx=5)

        self.list_discs = tk.Listbox(self.aba_disciplinas)
        self.list_discs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_disciplinas()

    def cadastrar_disciplina(self):
        cod, nome, ch, prof, curso = self.ent_disc_cod.get().strip(), self.ent_disc_nome.get().strip(), self.ent_disc_ch.get().strip(), self.ent_disc_codprof.get().strip(), self.ent_disc_codcurso.get().strip()
        if not all([cod, nome, ch, prof, curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_disciplinas.cadastrar(Disciplina(cod, nome, ch, prof, curso))
        self.atualizar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")

    def alterar_disciplina(self):
        cod, nome, ch, prof, curso = self.ent_disc_cod.get().strip(), self.ent_disc_nome.get().strip(), self.ent_disc_ch.get().strip(), self.ent_disc_codprof.get().strip(), self.ent_disc_codcurso.get().strip()
        if not all([cod, nome, ch, prof, curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        self.g_disciplinas.alterar(cod, nome, ch, prof, curso)
        self.atualizar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina atualizada!")

    def excluir_disciplina(self):
        cod = self.ent_disc_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código!")
            return
        self.g_disciplinas.excluir(cod)
        self.atualizar_disciplinas()

    def pesquisar_disciplina(self):
        termo = self.ent_disc_cod.get().strip() or self.ent_disc_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para pesquisar!")
            return
        self.list_discs.delete(0, tk.END)
        for d in self.g_disciplinas.buscar(termo):
            self.list_discs.insert(tk.END, str(d))

    def atualizar_disciplinas(self):
        self.list_discs.delete(0, tk.END)
        for d in self.g_disciplinas.carregar_todos():
            self.list_discs.insert(tk.END, str(d))

    # ==========================================================================
    # INTERFACE DE NOTAS (NOVO MÓDULO RF19 - RF24)
    # ==========================================================================
    def setup_aba_notas(self):
        frame = ttk.LabelFrame(self.aba_notas, text="Gerenciar Notas e Pesos")
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text="Matrícula Aluno:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_nota_mat = ttk.Entry(frame)
        self.ent_nota_mat.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Cód. Disciplina:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_nota_disc = ttk.Entry(frame)
        self.ent_nota_disc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Nota 1:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_n1 = ttk.Entry(frame, width=8)
        self.ent_n1.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame, text="Peso 1:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.ent_p1 = ttk.Entry(frame, width=8)
        self.ent_p1.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Nota 2:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_n2 = ttk.Entry(frame, width=8)
        self.ent_n2.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame, text="Peso 2:").grid(row=2, column=1, sticky="e", padx=5, pady=5)
        self.ent_p2 = ttk.Entry(frame, width=8)
        self.ent_p2.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Nota 3:").grid(row=3, column=0, padx=5, pady=5)
        self.ent_n3 = ttk.Entry(frame, width=8)
        self.ent_n3.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame, text="Peso 3:").grid(row=3, column=1, sticky="e", padx=5, pady=5)
        self.ent_p3 = ttk.Entry(frame, width=8)
        self.ent_p3.grid(row=3, column=2, sticky="w", padx=5, pady=5)

        btn_frame = ttk.Frame(self.aba_notas)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Cadastrar Nota", command=self.cadastrar_nota).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Alterar Nota", command=self.alterar_nota).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Excluir Nota", command=self.excluir_nota).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Pesquisar", command=self.pesquisar_nota).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todas", command=self.atualizar_notas).pack(side="left", padx=5)

        self.list_notas = tk.Listbox(self.aba_notas)
        self.list_notas.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_notas()

    def cadastrar_nota(self):
        try:
            mat = self.ent_nota_mat.get().strip()
            disc = self.ent_nota_disc.get().strip()
            n1, p1 = float(self.ent_n1.get()), float(self.ent_p1.get())
            n2, p2 = float(self.ent_n2.get()), float(self.ent_p2.get())
            n3, p3 = float(self.ent_n3.get()), float(self.ent_p3.get())

            if not all([mat, disc]):
                messagebox.showwarning("Aviso", "Preencha a Matrícula e o Código da Disciplina!")
                return

            nova_nota = Nota(mat, disc, n1, p1, n2, p2, n3, p3)
            self.g_notas.cadastrar(nova_nota)
            self.atualizar_notas()
            messagebox.showinfo("Sucesso", f"Notas cadastradas! Média calculada: {nova_nota.calcular_media()}")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))

    def alterar_nota(self):
        try:
            mat = self.ent_nota_mat.get().strip()
            disc = self.ent_nota_disc.get().strip()
            n1, p1 = float(self.ent_n1.get()), float(self.ent_p1.get())
            n2, p2 = float(self.ent_n2.get()), float(self.ent_p2.get())
            n3, p3 = float(self.ent_n3.get()), float(self.ent_p3.get())

            sucesso = self.g_notas.alterar(mat, disc, n1, p1, n2, p2, n3, p3)
            if sucesso:
                self.atualizar_notas()
                messagebox.showinfo("Sucesso", "Notas atualizadas e recalculadas com sucesso!")
            else:
                messagebox.showwarning("Aviso", "Registo de notas não encontrado para alteração.")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))

    def excluir_nota(self):
        mat = self.ent_nota_mat.get().strip()
        disc = self.ent_nota_disc.get().strip()
        if not all([mat, disc]):
            messagebox.showwarning("Aviso", "Informe a Matrícula e o Código da Disciplina para excluir!")
            return
        self.g_notas.excluir(mat, disc)
        self.atualizar_notas()
        messagebox.showinfo("Sucesso", "Registo de notas excluído!")

    def pesquisar_nota(self):
        termo = self.ent_nota_mat.get().strip() or self.ent_nota_disc.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite uma Matrícula ou Cód. Disciplina para pesquisar!")
            return
        self.list_notas.delete(0, tk.END)
        for n in self.g_notas.buscar(termo):
            self.list_notas.insert(tk.END, str(n))

    def atualizar_notas(self):
        self.list_notas.delete(0, tk.END)
        for n in self.g_notas.carregar_todos():
            self.list_notas.insert(tk.END, str(n))

    # ==========================================================================
    # RELATÓRIOS (INTEGRADO + RENDIMENTO ESCOLAR - RF23)
    # ==========================================================================
    def setup_aba_relatorio(self):
        btn_frame = ttk.Frame(self.aba_relatorio)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Gerar Relatório Integrado", command=self.gerar_relatorio_integrado).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Relatório de Rendimento Escolar (RF23)", command=self.gerar_relatorio_rendimento).pack(side="left", padx=5)

        self.txt_relatorio = tk.Text(self.aba_relatorio, wrap="word")
        self.txt_relatorio.pack(fill="both", expand=True, padx=10, pady=10)

    def gerar_relatorio_integrado(self):
        self.txt_relatorio.delete("1.0", tk.END)
        alunos = self.g_alunos.carregar_todos()
        cursos = {c.codigo: c for c in self.g_cursos.carregar_todos()}
        professores = {p.codigo: p for p in self.g_professores.carregar_todos()}
        disciplinas = self.g_disciplinas.carregar_todos()

        if not alunos:
            self.txt_relatorio.insert(tk.END, "Nenhum aluno encontrado.\n")
            return

        for aluno in alunos:
            curso = cursos.get(aluno.codigo_curso)
            nome_curso = curso.nome if curso else f"[Curso ID '{aluno.codigo_curso}' Desconhecido]"
            discs_aluno = [d for d in disciplinas if d.codigo_curso == aluno.codigo_curso]

            if discs_aluno:
                for disc in discs_aluno:
                    prof = professores.get(disc.codigo_professor)
                    nome_prof = prof.nome if prof else f"[Prof ID '{disc.codigo_professor}' Desconhecido]"
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

    def gerar_relatorio_rendimento(self):
        """Gera o Relatório de Rendimento Escolar exigido no RF23[cite: 22]."""
        self.txt_relatorio.delete("1.0", tk.END)
        notas = self.g_notas.carregar_todos()
        alunos = {a.matricula: a for a in self.g_alunos.carregar_todos()}
        disciplinas = {d.codigo: d for d in self.g_disciplinas.carregar_todos()}

        if not notas:
            self.txt_relatorio.insert(tk.END, "Nenhum registo de notas encontrado em notas.txt[cite: 22].\n")
            return

        self.txt_relatorio.insert(tk.END, "=== RELATÓRIO DE RENDIMENTO ESCOLAR (RF23) ===\n\n")
        for n in notas:
            aluno = alunos.get(n.matricula)
            nome_aluno = aluno.nome if aluno else f"[Aluno Matrícula '{n.matricula}' Desconhecido]"

            disc = disciplinas.get(n.codigo_disciplina)
            nome_disc = disc.nome if disc else f"[Disciplina ID '{n.codigo_disciplina}' Desconhecida]"

            media = n.calcular_media()
            status = n.obter_status()

            texto = (
                f"• Aluno: {nome_aluno} (Matrícula: {n.matricula})\n"
                f"  Disciplina: {nome_disc}\n"
                f"  Notas e Pesos: N1={n.nota1} (Peso {n.peso1}) | N2={n.nota2} (Peso {n.peso2}) | N3={n.nota3} (Peso {n.peso3})\n"
                f"  Média Final: {media} | Status: {status}\n"
                f"------------------------------------------------------------\n\n"
            )
            self.txt_relatorio.insert(tk.END, texto)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAcademicoGUI(root)
    root.mainloop()