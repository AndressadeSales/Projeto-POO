import os

# ==============================================================================
# EQUIPE ALFA: Módulo Aluno (RF06 e RF13)
# ==============================================================================

class Aluno:
    """
    Classe que representa a entidade Aluno (apenas modelo de dados).
    Possui vínculo com a entidade Curso através do atributo 'codigo_curso'.
    """
    def __init__(self, matricula: str, nome: str, cpf: str, email: str, codigo_curso: str):
        self._matricula = matricula
        self._nome = nome
        self._cpf = cpf
        self._email = email
        self._codigo_curso = codigo_curso  # Chave de ligação com a classe Curso

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, valor):
        self._matricula = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        self._cpf = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, valor):
        self._codigo_curso = valor

    def __str__(self):
        return (
            f"Matrícula: {self._matricula} | Nome: {self._nome} | "
            f"CPF: {self._cpf} | Email: {self._email} | Cód. Curso: {self._codigo_curso}"
        )


class GerenciadorAlunos:
    """Gerencia a persistência em alunos.txt e operações de CRUD da entidade Aluno."""
    def __init__(self, arquivo="alunos.txt"):
        self.arquivo = arquivo
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()

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
        return [
            a for a in self.carregar_todos()
            if termo.lower() in a.matricula.lower() or termo.lower() in a.nome.lower()
        ]