class Livro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self._disponivel = True
        self._emprestado_para = None

    def emprestar(self, user_name):
        if not self._disponivel:
            print(f"\n{self.titulo} já foi emprestado")
            return False

        self._disponivel = False
        self._emprestado_para = user_name
        return True

    def devolver(self):
        if self._disponivel:
            print(f"\n{self.titulo} não foi emprestado")
            return False

        self._disponivel = True
        self._emprestado_para = None
        return True

    @property
    def disponivel(self):
        return self._disponivel

    @property
    def emprestado_para(self):
        return self._emprestado_para

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    def esta_emprestado(self):
        return bool(self.emprestado_para)


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
