from pathlib import Path
import json


class Livro:
    def __init__(self, titulo: str, autor: str, isbn: str):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self._disponivel = True
        self._emprestado_para: str | None = None

    def emprestar(self, user_name: str) -> bool:
        if not self._disponivel:
            print(f"\n{self.titulo} já foi emprestado")
            return False

        self._disponivel = False
        self._emprestado_para = user_name
        return True

    def devolver(self) -> bool:
        if self._disponivel:
            print(f"\n{self.titulo} não foi emprestado")
            return False

        self._disponivel = True
        self._emprestado_para = None
        return True

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    @property
    def emprestado_para(self) -> str | None:
        return self._emprestado_para

    def to_dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "disponivel": self._disponivel,
            "emprestado_para": self._emprestado_para,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Livro":
        livro = cls(data["titulo"], data["autor"], data["isbn"])
        livro._disponivel = data["disponivel"]
        livro._emprestado_para = data["empretado_para"]
        return livro


if __name__ == '__main__':
    livro = Livro(
        "Python Fluente", "Luciano Ramalho", "798-5649878654"
    )

    print("Título:", livro.titulo)
    print("Autor:", livro.autor)
    print("ISBN:", livro.isbn)
    print("Disponível:", livro.disponivel)
    print("Emprestado para:", livro.emprestado_para)

    emprestimo = livro.devolver()

    emprestimo = livro.emprestar("Rafael")

    print("\nEmpréstimo realizado:", emprestimo)
    print("Disponível:", livro.disponivel)
    print("Emprestado para:", livro.emprestado_para)

    emprestimo = livro.emprestar("João")

    emprestimo = livro.devolver()

    print("\nDevolução realizada:", emprestimo)
    print("Disponível:", livro.disponivel)
    print("Emprestado para:", livro.emprestado_para)

    print(f"\n{livro}")


class Usuario:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
        self._livros_emprestados: list[str] = []  # guarda ISBNs

    def adicionar_livro(self, isbn: str) -> None:
        if isbn not in self._livros_emprestados:
            self._livros_emprestados.append(isbn)

    def remover_livro(self, isbn: str) -> None:
        if isbn in self._livros_emprestados:
            self._livros_emprestados.remove(isbn)

    @property
    def livros_emprestados(self) -> list[str]:
        return list(self._livros_emprestados)

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "email": self.email,
            "livros_emprestados": self._livros_emprestados
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        usuario = cls(data["nome"], data["email"])
        usuario._livros_emprestados = list(data["livros_emprestados"])
        return usuario


class Biblioteca:
    def __init__(self, arquivo_livros: str = "livros.json",
                 arquivo_usuarios: str = "usuarios.json"):
        self.arquivo_livros = Path(arquivo_livros)
        self.arquivo_usuarios = Path(arquivo_usuarios)
        self.livros: list[Livro] = []
        self.usuarios: list[Usuario] = []
        self.carregar_dados()

    # --- Operações com Livros ---
    def cadastrar_livros(
            self, titulo: str, autor: str, isbn: str
    ) -> Livro | None:
        if any(book.isbn == isbn for book in self.livros):
            return None
        livro = Livro(titulo, autor, isbn)
        self.livros.append(livro)
        return livro

    def buscar_livro_por_isbn(self, isbn: str) -> Livro | None:
        for book in self.livros:
            if book.isbn == isbn:
                return book
        return None

    # --- Operações com Usuários ---
    def cadastrar_usuario(self, nome: str, email: str) -> Usuario | None:
        if any(u.email == email for u in self.usuarios):
            return None
        usuario = Usuario(nome, email)
        self.usuarios.append(usuario)
        return usuario

    def buscar_usuario_por_email(self, email: str) -> Usuario | None:
        for u in self.usuarios:
            if u.email == email:
                return u
        return None

    # --- Empréstimo e Devolução ---
    def emprestar_livro(self, isbn: str, email_usuario: str) -> bool:
        livro = self.buscar_livro_por_isbn(isbn)
        usuario = self.buscar_usuario_por_email(email_usuario)
        if not livro or not usuario:
            return False
        if not livro.emprestar(usuario.nome):
            return False
        usuario.adicionar_livro(isbn)
        return True

    def devolver_livro(self, isbn: str, email_usuario: str) -> bool:
        livro = self.buscar_livro_por_isbn(isbn)
        usuario = self.buscar_usuario_por_email(email_usuario)
        if not livro or not usuario:
            return False
        if not livro.devolver():
            return False
        usuario.remover_livro(isbn)
        return True

    # --- Persistência ---
    def salvar_dados(self) -> None:
        livros_data = [book.to_dict() for book in self.livros]
        usuarios_data = [u.to_dict() for u in self.usuarios]

        with self.arquivo_livros.open("w", encoding="utf-8") as f:
            json.dump(livros_data, f, indent=2, ensure_ascii=False)

        with self.arquivo_usuarios.open("w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=2, ensure_ascii=False)

    def carregar_dados(self) -> None:
        if self.arquivo_livros.exists():
            with self.arquivo_livros.open("r", encoding="utf-8") as f:
                dados = json.load(f)
                self.livros = [Livro.from_dict(d) for d in dados]

        if self.arquivo_usuarios.exists():
            with self.arquivo_usuarios.open("r", encoding="utf-8") as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(d) for d in dados]

    # --- Consultas Úteis ---
    def listar_livros_disponiveis(self) -> list[Livro]:
        return [book for book in self.livros if book.disponivel]

    def listar_livros_emprestados(self) -> list[Livro]:
        return [book for book in self.livros if not book.disponivel]

    def listar_livros_por_usuario(self, email: str) -> list[Livro]:
        usuario = self.buscar_usuario_por_email(email)
        if not usuario:
            return []
        isbns = usuario.livros_emprestados
        return [book for book in self.livros if book.isbn in isbns]
