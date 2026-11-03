import os

# ==============================================================================
# EQUIPE ALFA: Módulo Curso (RF07)
# ==============================================================================

class Curso:
    """
    Classe que representa a entidade Curso (apenas modelo de dados).
    Contém encapsulamento nos atributos (prefixados com '_') e métodos @property.
    """
    def __init__(self, codigo: str, nome: str, modalidade: str):
        self._codigo = codigo
        self._nome = nome
        self._modalidade = modalidade

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
        return f"[{self._codigo}] {self._nome} ({self._modalidade})"


class GerenciadorCursos:
    """Gerencia a persistência em cursos.txt e operações de CRUD da entidade Curso."""
    def __init__(self, arquivo="cursos.txt"):
        self.arquivo = arquivo
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()

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
        return [
            c for c in self.carregar_todos()
            if termo.lower() in c.codigo.lower() or termo.lower() in c.nome.lower()
        ]