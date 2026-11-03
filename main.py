
import tkinter as tk
from tkinter import ttk, messagebox
from aluno import Aluno, GerenciadorAlunos
from curso import Curso, GerenciadorCursos
from professor import Professor, GerenciadorProfessores
from disciplina import Disciplina, GerenciadorDisciplinas

class SistemaAcademicoGUI:
    """Classe principal que constrói e controla a Interface Gráfica (GUI) em Tkinter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integrado de Gestão Acadêmica")
        self.root.geometry("850x650")

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

        # Botão de encerramento controlado (RF18)
        rodape = ttk.Frame(self.root)
        rodape.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(rodape, text="Encerrar Programa", command=self.root.destroy).pack(side="right")

    # ==========================================================================
    # INTERFACE DE CURSOS (EQUIPE ALFA)
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
        ttk.Button(btn_frame, text="Pesquisar (Cód/Nome)", command=self.pesquisar_curso).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_cursos).pack(side="left", padx=5)

        self.list_cursos = tk.Listbox(self.aba_cursos)
        self.list_cursos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_cursos()

    def cadastrar_curso(self):
        cod = self.ent_curso_cod.get().strip()
        nome = self.ent_curso_nome.get().strip()
        mod = self.cb_curso_mod.get().strip()
        if not all([cod, nome, mod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios do Curso!")
            return
        self.g_cursos.cadastrar(Curso(cod, nome, mod))
        self.atualizar_cursos()
        messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")

    def alterar_curso(self):
        cod = self.ent_curso_cod.get().strip()
        nome = self.ent_curso_nome.get().strip()
        mod = self.cb_curso_mod.get().strip()
        if not all([cod, nome, mod]):
            messagebox.showwarning("Aviso", "Preencha todos os campos para alterar o Curso!")
            return
        self.g_cursos.alterar(cod, nome, mod)
        self.atualizar_cursos()
        messagebox.showinfo("Sucesso", "Curso atualizado!")

    def excluir_curso(self):
        cod = self.ent_curso_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código do Curso para excluir!")
            return
        self.g_cursos.excluir(cod)
        self.atualizar_cursos()

    def pesquisar_curso(self):
        termo = self.ent_curso_cod.get().strip() or self.ent_curso_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um Código ou Nome para pesquisar!")
            return
        self.list_cursos.delete(0, tk.END)
        for c in self.g_cursos.buscar(termo):
            self.list_cursos.insert(tk.END, str(c))

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
        ttk.Button(btn_frame, text="Pesquisar (Mat/Nome)", command=self.pesquisar_aluno).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_alunos).pack(side="left", padx=5)

        self.list_alunos = tk.Listbox(self.aba_alunos)
        self.list_alunos.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_alunos()

    def cadastrar_aluno(self):
        mat = self.ent_aluno_mat.get().strip()
        nome = self.ent_aluno_nome.get().strip()
        cpf = self.ent_aluno_cpf.get().strip()
        email = self.ent_aluno_email.get().strip()
        cod_curso = self.ent_aluno_codcurso.get().strip()

        if not all([mat, nome, cpf, email, cod_curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios do Aluno!")
            return

        self.g_alunos.cadastrar(Aluno(mat, nome, cpf, email, cod_curso))
        self.atualizar_alunos()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

    def alterar_aluno(self):
        mat = self.ent_aluno_mat.get().strip()
        nome = self.ent_aluno_nome.get().strip()
        cpf = self.ent_aluno_cpf.get().strip()
        email = self.ent_aluno_email.get().strip()
        cod_curso = self.ent_aluno_codcurso.get().strip()

        if not all([mat, nome, cpf, email, cod_curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos para alterar o Aluno!")
            return

        self.g_alunos.alterar(mat, nome, cpf, email, cod_curso)
        self.atualizar_alunos()
        messagebox.showinfo("Sucesso", "Aluno atualizado!")

    def excluir_aluno(self):
        mat = self.ent_aluno_mat.get().strip()
        if not mat:
            messagebox.showwarning("Aviso", "Informe a Matrícula para excluir!")
            return
        self.g_alunos.excluir(mat)
        self.atualizar_alunos()

    def pesquisar_aluno(self):
        termo = self.ent_aluno_mat.get().strip() or self.ent_aluno_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite uma Matrícula ou Nome para pesquisar!")
            return
        self.list_alunos.delete(0, tk.END)
        for a in self.g_alunos.buscar(termo):
            self.list_alunos.insert(tk.END, str(a))

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
        ttk.Button(btn_frame, text="Pesquisar (Cód/Nome)", command=self.pesquisar_professor).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todos", command=self.atualizar_professores).pack(side="left", padx=5)

        self.list_profs = tk.Listbox(self.aba_professores)
        self.list_profs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_professores()

    def cadastrar_professor(self):
        cod = self.ent_prof_cod.get().strip()
        nome = self.ent_prof_nome.get().strip()
        cpf = self.ent_prof_cpf.get().strip()
        esp = self.ent_prof_esp.get().strip()

        if not all([cod, nome, cpf, esp]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios do Professor!")
            return

        self.g_professores.cadastrar(Professor(cod, nome, cpf, esp))
        self.atualizar_professores()
        messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")

    def alterar_professor(self):
        cod = self.ent_prof_cod.get().strip()
        nome = self.ent_prof_nome.get().strip()
        cpf = self.ent_prof_cpf.get().strip()
        esp = self.ent_prof_esp.get().strip()

        if not all([cod, nome, cpf, esp]):
            messagebox.showwarning("Aviso", "Preencha todos os campos para alterar o Professor!")
            return

        self.g_professores.alterar(cod, nome, cpf, esp)
        self.atualizar_professores()
        messagebox.showinfo("Sucesso", "Professor atualizado!")

    def excluir_professor(self):
        cod = self.ent_prof_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código do Professor para excluir!")
            return
        self.g_professores.excluir(cod)
        self.atualizar_professores()

    def pesquisar_professor(self):
        termo = self.ent_prof_cod.get().strip() or self.ent_prof_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um Código ou Nome para pesquisar!")
            return
        self.list_profs.delete(0, tk.END)
        for p in self.g_professores.buscar(termo):
            self.list_profs.insert(tk.END, str(p))

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
        ttk.Button(btn_frame, text="Pesquisar (Cód/Nome)", command=self.pesquisar_disciplina).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Listar Todas", command=self.atualizar_disciplinas).pack(side="left", padx=5)

        self.list_discs = tk.Listbox(self.aba_disciplinas)
        self.list_discs.pack(fill="both", expand=True, padx=10, pady=5)
        self.atualizar_disciplinas()

    def cadastrar_disciplina(self):
        cod = self.ent_disc_cod.get().strip()
        nome = self.ent_disc_nome.get().strip()
        ch = self.ent_disc_ch.get().strip()
        cod_prof = self.ent_disc_codprof.get().strip()
        cod_curso = self.ent_disc_codcurso.get().strip()

        if not all([cod, nome, ch, cod_prof, cod_curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios da Disciplina!")
            return

        self.g_disciplinas.cadastrar(Disciplina(cod, nome, ch, cod_prof, cod_curso))
        self.atualizar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")

    def alterar_disciplina(self):
        cod = self.ent_disc_cod.get().strip()
        nome = self.ent_disc_nome.get().strip()
        ch = self.ent_disc_ch.get().strip()
        cod_prof = self.ent_disc_codprof.get().strip()
        cod_curso = self.ent_disc_codcurso.get().strip()

        if not all([cod, nome, ch, cod_prof, cod_curso]):
            messagebox.showwarning("Aviso", "Preencha todos os campos para alterar a Disciplina!")
            return

        self.g_disciplinas.alterar(cod, nome, ch, cod_prof, cod_curso)
        self.atualizar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina atualizada!")

    def excluir_disciplina(self):
        cod = self.ent_disc_cod.get().strip()
        if not cod:
            messagebox.showwarning("Aviso", "Informe o Código da Disciplina para excluir!")
            return
        self.g_disciplinas.excluir(cod)
        self.atualizar_disciplinas()

    def pesquisar_disciplina(self):
        termo = self.ent_disc_cod.get().strip() or self.ent_disc_nome.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um Código ou Nome para pesquisar!")
            return
        self.list_discs.delete(0, tk.END)
        for d in self.g_disciplinas.buscar(termo):
            self.list_discs.insert(tk.END, str(d))

    def atualizar_disciplinas(self):
        self.list_discs.delete(0, tk.END)
        for d in self.g_disciplinas.carregar_todos():
            self.list_discs.insert(tk.END, str(d))

    # ==========================================================================
    # RELATÓRIO INTEGRADO (SÍNTESE DOS MÓDULOS ALFA E BETA)
    # ==========================================================================
    def setup_aba_relatorio(self):
        btn_frame = ttk.Frame(self.aba_relatorio)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Gerar Relatório Completo", command=self.gerar_relatorio).pack(side="left", padx=5)

        self.txt_relatorio = tk.Text(self.aba_relatorio, wrap="word")
        self.txt_relatorio.pack(fill="both", expand=True, padx=10, pady=10)

    def gerar_relatorio(self):
        self.txt_relatorio.delete("1.0", tk.END)

        alunos = self.g_alunos.carregar_todos()
        cursos = {c.codigo: c for c in self.g_cursos.carregar_todos()}
        professores = {p.codigo: p for p in self.g_professores.carregar_todos()}
        disciplinas = self.g_disciplinas.carregar_todos()

        if not alunos:
            self.txt_relatorio.insert(tk.END, "Nenhum aluno encontrado nos dados persistidos.\n")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAcademicoGUI(root)
    root.mainloop()