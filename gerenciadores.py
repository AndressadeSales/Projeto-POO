import os
from modelos import Aluno, Curso, Professor, Disciplina

class GerenciadorBase:
    """Classe base que verifica e garante a existência do arquivo de dados."""
    def __init__(self, arquivo):
        self.arquivo = arquivo
        # Se o arquivo não existir no disco, cria um vazio
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()


class GerenciadorCursos(GerenciadorBase):
    """Gerencia a persistência e operações de CRUD da entidade Curso."""
    def __init__(self, arquivo="cursos.txt"):
        super().__init__(arquivo)

    def carregar_todos(self):
        """Lê o arquivo TXT, converte cada linha em objeto Curso e retorna uma lista."""
        cursos = []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 3:
                        cursos.append(Curso(partes[0], partes[1], partes[2]))
        return cursos

    def salvar_todos(self, cursos):
        """Sobrescreve o arquivo TXT com a lista completa de objetos repassada."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for c in cursos:
                f.write(f"{c.codigo};{c.nome};{c.modalidade}\n")

    def cadastrar(self, curso):
        """Adiciona um novo Curso e salva no arquivo."""
        cursos = self.carregar_todos()
        cursos.append(curso)
        self.salvar_todos(cursos)

    def alterar(self, codigo, novo_nome, nova_modalidade):
        """Atualiza os dados de um Curso existente pelo Código."""
        cursos = self.carregar_todos()
        for c in cursos:
            if c.codigo == codigo:
                c.nome = novo_nome
                c.modalidade = nova_modalidade
                break
        self.salvar_todos(cursos)

    def excluir(self, codigo):
        """Remove um Curso do arquivo buscando pelo Código."""
        cursos = [c for c in self.carregar_todos() if c.codigo != codigo]
        self.salvar_todos(cursos)

    def buscar(self, termo):
        """Pesquisa um Curso pelo Código ou Nome."""
        return [c for c in self.carregar_todos() if termo.lower() in c.codigo.lower() or termo.lower() in c.nome.lower()]


class GerenciadorAlunos(GerenciadorBase):
    """Gerencia a persistência e operações de CRUD da entidade Aluno."""
    def __init__(self, arquivo="alunos.txt"):
        super().__init__(arquivo)

    def carregar_todos(self):
        """Lê o arquivo TXT e converte as linhas formatadas em objetos Aluno."""
        alunos = []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 5:
                        alunos.append(Aluno(partes[0], partes[1], partes[2], partes[3], partes[4]))
        return alunos

    def salvar_todos(self, alunos):
        """Salva a lista completa de Alunos no TXT delimitado por ';'."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for a in alunos:
                f.write(f"{a.matricula};{a.nome};{a.cpf};{a.email};{a.codigo_curso}\n")

    def cadastrar(self, aluno):
        """Cadastra um novo Aluno."""
        alunos = self.carregar_todos()
        alunos.append(aluno)
        self.salvar_todos(alunos)

    def alterar(self, matricula, novo_nome, novo_cpf, novo_email, novo_cod_curso):
        """Altera os dados de um Aluno existente procurando por sua Matrícula."""
        alunos = self.carregar_todos()
        for a in alunos:
            if a.matricula == matricula:
                a.nome = novo_nome
                a.cpf = novo_cpf
                a.email = novo_email
                a.codigo_curso = novo_cod_curso
                break
        self.salvar_todos(alunos)

    def excluir(self, matricula):
        """Exclui o Aluno correspondente à Matrícula informada."""
        alunos = [a for a in self.carregar_todos() if a.matricula != matricula]
        self.salvar_todos(alunos)

    def buscar(self, termo):
        """Localiza registros de Alunos por Matrícula ou Nome."""
        return [a for a in self.carregar_todos() if termo.lower() in a.matricula.lower() or termo.lower() in a.nome.lower()]


class GerenciadorProfessores(GerenciadorBase):
    """Gerencia a persistência e operações de CRUD da entidade Professor."""
    def __init__(self, arquivo="professores.txt"):
        super().__init__(arquivo)

    def carregar_todos(self):
        professores = []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 4:
                        professores.append(Professor(partes[0], partes[1], partes[2], partes[3]))
        return professores

    def salvar_todos(self, professores):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for p in professores:
                f.write(f"{p.codigo};{p.nome};{p.cpf};{p.especialidade}\n")

    def cadastrar(self, professor):
        profs = self.carregar_todos()
        profs.append(professor)
        self.salvar_todos(profs)

    def alterar(self, codigo, novo_nome, novo_cpf, nova_especialidade):
        profs = self.carregar_todos()
        for p in profs:
            if p.codigo == codigo:
                p.nome = novo_nome
                p.cpf = novo_cpf
                p.especialidade = nova_especialidade
                break
        self.salvar_todos(profs)

    def excluir(self, codigo):
        profs = [p for p in self.carregar_todos() if p.codigo != codigo]
        self.salvar_todos(profs)

    def buscar(self, termo):
        return [p for p in self.carregar_todos() if termo.lower() in p.codigo.lower() or termo.lower() in p.nome.lower()]


class GerenciadorDisciplinas(GerenciadorBase):
    """Gerencia a persistência e operações de CRUD da entidade Disciplina."""
    def __init__(self, arquivo="disciplinas.txt"):
        super().__init__(arquivo)

    def carregar_todos(self):
        disciplinas = []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 5:
                        disciplinas.append(Disciplina(partes[0], partes[1], partes[2], partes[3], partes[4]))
        return disciplinas

    def salvar_todos(self, disciplinas):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for d in disciplinas:
                f.write(f"{d.codigo};{d.nome};{d.carga_horaria};{d.codigo_professor};{d.codigo_curso}\n")

    def cadastrar(self, disciplina):
        disciplinas = self.carregar_todos()
        disciplinas.append(disciplina)
        self.salvar_todos(disciplinas)

    def alterar(self, codigo, novo_nome, nova_ch, novo_cod_prof, novo_cod_curso):
        disciplinas = self.carregar_todos()
        for d in disciplinas:
            if d.codigo == codigo:
                d.nome = novo_nome
                d.carga_horaria = nova_ch
                d.codigo_professor = novo_cod_prof
                d.codigo_curso = novo_cod_curso
                break
        self.salvar_todos(disciplinas)

    def excluir(self, codigo):
        disciplinas = [d for d in self.carregar_todos() if d.codigo != codigo]
        self.salvar_todos(disciplinas)

    def buscar(self, termo):
        return [d for d in self.carregar_todos() if termo.lower() in d.codigo.lower() or termo.lower() in d.nome.lower()]