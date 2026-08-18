from library import Biblioteca


def menu():
    print("\n=== Biblioteca ===")
    print("1. Cadastrar Livro")
    print("2. Cadastrar Usuário")
    print("3. Emprestar Livro")
    print("4. Devolver Livro")
    print("5. Listar Livros Disponíveis")
    print("6. Listar Livros Emprestados")
    print("7. Listar Livros de um Usuário")
    print("8 Salvar e Sair")


def main():
    bib = Biblioteca()

    while True:
        menu()
        op = input("Escolha uma opção: ").strip()

        if op == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            livro = bib.cadastrar_livros(titulo, autor, isbn)
            if livro:
                print("Livro cadastrado com sucesso!")
            else:
                print("ISBN já cadastrado.")

        elif op == "2":
            nome = input("Nome: ")
            email = input("E-mail: ")
            usuario = bib.cadastrar_usuario(nome, email)
            if usuario:
                print("Usuário cadastrado com sucesso!")
            else:
                print("E-mail já cadastrado.")

        elif op == "3":
            isbn = input("ISBN do livro: ")
            email = input("E-mail do usuário: ")
            if bib.emprestar_livro(isbn, email):
                print("Empréstimo realizado!")
            else:
                print("Não foi possível realizar o empréstimo.")

        elif op == "4":
            isbn = input("ISBN do livro: ")
            email = input("E-mail do usuário: ")
            if bib.devolver_livro(isbn, email):
                print("Devolução realizada!")
            else:
                print("Não foi possível realizar a devolução.")

        elif op == "5":
            livros = bib.listar_livros_disponiveis()
            if not livros:
                print("Nenhum livro disponível.")
            else:
                for book in livros:
                    print(f"- {book.titulo} ({book.autor})"
                          f"[ISBN: {book.isbn}]")

        elif op == "6":
            livros = bib.listar_livros_emprestados()
            if not livros:
                print("Nenhum livro emprestado.")
            else:
                for book in livros:
                    print(f"- {book.titulo} ({book.autor})"
                          f"[ISBN: {book.isbn}]"
                          f"- Emprestado para: {book.emprestado_para}")

        elif op == "7":
            email = input("E-mail do usuário: ")
            livros = bib.listar_livros_por_usuario(email)
            if not livros:
                print("Usuário não encontrado ou sem livros emprestados.")
            else:
                for book in livros:
                    print(f"- {book.titulo} ({book.autor})"
                          f"[ISBN: {book.isbn}]")

        elif op == "8":
            bib.salvar_dados()
            print("Dados salvos. Até logo!")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
