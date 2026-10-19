# ==============================================================================
# EQUIPE ALFA: Módulos Aluno e Curso
# ==============================================================================

class Curso:
    """
    Classe que representa a entidade Curso.
    Contém encapsulamento nos atributos (prefixados com '_') e métodos @property.
    """
    def __init__(self, codigo: str, nome: str, modalidade: str):
        # Atributos protegidos
        self._codigo = codigo
        self._nome = nome
        self._modalidade = modalidade

    # Getters e Setters utilizando decorators do Python (@property)
    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def modalidade(self):
        return self._modalidade

    @modalidade.setter
    def modalidade(self, valor):
        self._modalidade = valor

    def __str__(self):
        # Representação em formato legível de texto
        return f"[{self._codigo}] {self._nome} ({self._modalidade})"


class Aluno:
    """
    Classe que representa a entidade Aluno.
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
        return f"Matrícula: {self._matricula} | Nome: {self._nome} | CPF: {self._cpf} | Email: {self._email} | Cód. Curso: {self._codigo_curso}"


# ==============================================================================
# EQUIPE BETA: Módulos Professor e Disciplina
# ==============================================================================

class Professor:
    """
    Classe que representa a entidade Professor.
    """
    def __init__(self, codigo: str, nome: str, cpf: str, especialidade: str):
        self._codigo = codigo
        self._nome = nome
        self._cpf = cpf
        self._especialidade = especialidade

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor

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
    def especialidade(self):
        return self._especialidade

    @especialidade.setter
    def especialidade(self, valor):
        self._especialidade = valor

    def __str__(self):
        return f"[{self._codigo}] Prof. {self._nome} - {self._especialidade}"


class Disciplina:
    """
    Classe que representa a entidade Disciplina.
    Possui ligações com as classes Professor (codigo_professor) e Curso (codigo_curso).
    """
    def __init__(self, codigo: str, nome: str, carga_horaria: str, codigo_professor: str, codigo_curso: str):
        self._codigo = codigo
        self._nome = nome
        self._carga_horaria = carga_horaria
        self._codigo_professor = codigo_professor  # Chave de ligação com Professor
        self._codigo_curso = codigo_curso          # Chave de ligação com Curso

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        self._carga_horaria = valor

    @property
    def codigo_professor(self):
        return self._codigo_professor

    @codigo_professor.setter
    def codigo_professor(self, valor):
        self._codigo_professor = valor

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @codigo_curso.setter
    def codigo_curso(self, valor):
        self._codigo_curso = valor

    def __str__(self):
        return f"[{self._codigo}] {self._nome} ({self._carga_horaria}h) | Cód. Prof: {self._codigo_professor} | Cód. Curso: {self._codigo_curso}"