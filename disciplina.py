import os

# ==============================================================================
# EQUIPE BETA: Módulo Disciplina (RF09 e RF14)
# ==============================================================================

class Disciplina:
    """
    Classe que representa a entidade Disciplina (apenas modelo de dados).
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
        return (
            f"[{self._codigo}] {self._nome} ({self._carga_horaria}h) | "
            f"Cód. Prof: {self._codigo_professor} | Cód. Curso: {self._codigo_curso}"
        )


class GerenciadorDisciplinas:
    """Gerencia a persistência em disciplinas.txt e operações de CRUD da entidade Disciplina."""
    def __init__(self, arquivo="disciplinas.txt"):
        self.arquivo = arquivo
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()

    def carregar_todos(self):
        """Lê o arquivo TXT e converte as linhas em objetos Disciplina."""
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
        """Salva a lista completa de Disciplinas no TXT delimitado por ';'."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for d in disciplinas:
                f.write(f"{d.codigo};{d.nome};{d.carga_horaria};{d.codigo_professor};{d.codigo_curso}\n")

    def cadastrar(self, disciplina):
        """Cadastra uma nova Disciplina."""
        disciplinas = self.carregar_todos()
        disciplinas.append(disciplina)
        self.salvar_todos(disciplinas)

    def alterar(self, codigo, novo_nome, nova_ch, novo_cod_prof, novo_cod_curso):
        """Altera os dados de uma Disciplina existente pelo seu Código."""
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
        """Exclui a Disciplina correspondente ao Código informado."""
        disciplinas = [d for d in self.carregar_todos() if d.codigo != codigo]
        self.salvar_todos(disciplinas)

    def buscar(self, termo):
        """Localiza registros de Disciplinas por Código ou Nome."""
        return [
            d for d in self.carregar_todos()
            if termo.lower() in d.codigo.lower() or termo.lower() in d.nome.lower()
        ]