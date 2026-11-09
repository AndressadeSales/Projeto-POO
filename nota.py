import os


class Nota:
    """
    Classe que representa a entidade Nota / Desempenho Académico.
    Contém as notas, os pesos e a regra de cálculo da média ponderada[cite: 22].
    """
    def __init__(self, matricula: str, codigo_disciplina: str, nota1: float, peso1: float, nota2: float, peso2: float, nota3: float, peso3: float):
        self._matricula = matricula
        self._codigo_disciplina = codigo_disciplina
        self._nota1 = float(nota1)
        self._peso1 = float(peso1)
        self._nota2 = float(nota2)
        self._peso2 = float(peso2)
        self._nota3 = float(nota3)
        self._peso3 = float(peso3)

    @property
    def matricula(self): return self._matricula
    @matricula.setter
    def matricula(self, valor): self._matricula = valor

    @property
    def codigo_disciplina(self): return self._codigo_disciplina
    @codigo_disciplina.setter
    def codigo_disciplina(self, valor): self._codigo_disciplina = valor

    @property
    def nota1(self): return self._nota1
    @property
    def peso1(self): return self._peso1
    @property
    def nota2(self): return self._nota2
    @property
    def peso2(self): return self._peso2
    @property
    def nota3(self): return self._nota3
    @property
    def peso3(self): return self._peso3

    def calcular_media(self):
        """Calcula a média ponderada respeitando o teto máximo de 10.0 (RF21, RF22)[cite: 22]."""
        soma_pesos = self._peso1 + self._peso2 + self._peso3
        if soma_pesos == 0:
            return 0.0
        
        soma_notas = (self._nota1 * self._peso1) + (self._nota2 * self._peso2) + (self._nota3 * self._peso3)
        media = soma_notas / soma_pesos
        
        # Garante que a média nunca ultrapasse o teto de 10.0[cite: 22]
        return min(round(media, 2), 10.0)

    def obter_status(self):
        """Retorna o status académico: Aprovado se média >= 7.0, Reprovado se < 7.0 (RF23)[cite: 22]."""
        return "Aprovado" if self.calcular_media() >= 7.0 else "Reprovado"

    def __str__(self):
        return (
            f"Matrícula: {self._matricula} | Disc: {self._codigo_disciplina} | "
            f"N1: {self._nota1} (P{self._peso1}) | N2: {self._nota2} (P{self._peso2}) | "
            f"N3: {self._nota3} (P{self._peso3}) | Média: {self.calcular_media()} | Status: {self.obter_status()}"
        )


class GerenciadorNotas:
    """Gerencia a persistência no ficheiro notas.txt e operações de CRUD (RF20, RF24)[cite: 22]."""
    def __init__(self, arquivo="notas.txt"):
        self.arquivo = arquivo
        if not os.path.exists(self.arquivo):
            open(self.arquivo, 'w', encoding='utf-8').close()

    def carregar_todos(self):
        """Lê o ficheiro notas.txt e converte as linhas em objetos Nota, recalculando em tempo de execução (RF24)[cite: 22]."""
        notas = []
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 8:
                        notas.append(Nota(
                            partes[0], partes[1],
                            float(partes[2]), float(partes[3]),
                            float(partes[4]), float(partes[5]),
                            float(partes[6]), float(partes[7])
                        ))
        return notas

    def salvar_todos(self, notas):
        """Salva a lista completa de notas no formato delimitado por ';' (RF20)[cite: 22]."""
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            for n in notas:
                f.write(f"{n.matricula};{n.codigo_disciplina};{n.nota1};{n.peso1};{n.nota2};{n.peso2};{n.nota3};{n.peso3}\n")

    def cadastrar(self, nota):
        """Cadastra um novo registo de notas após validação estrita (RF22)[cite: 22]."""
        for n_val in [nota.nota1, nota.nota2, nota.nota3]:
            if not (0.0 <= n_val <= 10.0):
                raise ValueError("As notas inseridas devem estar obrigatoriamente no intervalo entre 0.0 e 10.0 (RF22)[cite: 22].")
        
        notas = self.carregar_todos()
        notas.append(nota)
        self.salvar_todos(notas)

    def alterar(self, matricula, codigo_disciplina, n1, p1, n2, p2, n3, p3):
        """Altera notas e pesos, permitindo o recálculo automático na leitura (RF24)[cite: 22]."""
        for n_val in [n1, n2, n3]:
            if not (0.0 <= float(n_val) <= 10.0):
                raise ValueError("As notas inseridas devem estar obrigatoriamente no intervalo entre 0.0 e 10.0 (RF22)[cite: 22].")

        notas = self.carregar_todos()
        encontrado = False
        for n in notas:
            if n.matricula == matricula and n.codigo_disciplina == codigo_disciplina:
                n._nota1, n._peso1 = float(n1), float(p1)
                n._nota2, n._peso2 = float(n2), float(p2)
                n._nota3, n._peso3 = float(n3), float(p3)
                encontrado = True
                break
        if encontrado:
            self.salvar_todos(notas)
        return encontrado

    def excluir(self, matricula, codigo_disciplina):
        """Remove um registo de notas pelo aluno e disciplina."""
        notas = self.carregar_todos()
        novas_notas = [n for n in notas if not (n.matricula == matricula and n.codigo_disciplina == codigo_disciplina)]
        self.salvar_todos(novas_notas)

    def buscar(self, termo):
        """Pesquisa registos de notas por Matrícula ou Código da Disciplina."""
        return [
            n for n in self.carregar_todos()
            if termo.lower() in n.matricula.lower() or termo.lower() in n.codigo_disciplina.lower()
        ]