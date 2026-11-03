import os

# ==============================================================================
# EQUIPE BETA: Módulo Professor (RF08)
# ==============================================================================

class Professor:
    """
    Classe que representa a entidade Professor (apenas modelo de dados).
    Contém encapsulamento nos atributos (prefixados com '_') e métodos @property.
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
        return f"[{self._codigo}] Prof. {self._nome} | CPF: {self._cpf} | Esp: {self._especialidade}"


class GerenciadorProfessores:
    """Gerencia a persistência em professores.txt e operações de CRUD da entidade Professor."""
    def __init__(self, arquivo="professores.txt"):
        self.arquivo = arquivo
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()

    def carregar_todos(self):
        """Lê o arquivo TXT e converte as linhas em objetos Professor."""
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
        """Salva a lista completa de Professores no TXT delimitado por ';'."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for p in professores:
                f.write(f"{p.codigo};{p.nome};{p.cpf};{p.especialidade}\n")

    def cadastrar(self, professor):
        """Cadastra um novo Professor."""
        profs = self.carregar_todos()
        profs.append(professor)
        self.salvar_todos(profs)

    def alterar(self, codigo, novo_nome, novo_cpf, nova_especialidade):
        """Altera os dados de um Professor existente pelo seu Código."""
        profs = self.carregar_todos()
        for p in profs:
            if p.codigo == codigo:
                p.nome = novo_nome
                p.cpf = novo_cpf
                p.especialidade = nova_especialidade
                break
        self.salvar_todos(profs)

    def excluir(self, codigo):
        """Exclui o Professor correspondente ao Código informado."""
        profs = [p for p in self.carregar_todos() if p.codigo != codigo]
        self.salvar_todos(profs)

    def buscar(self, termo):
        """Localiza registros de Professores por Código ou Nome."""
        return [
            p for p in self.carregar_todos()
            if termo.lower() in p.codigo.lower() or termo.lower() in p.nome.lower()
        ]