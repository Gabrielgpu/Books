import flet as ft
from database.base import inserir_produto, remover_produto_por_isbn
from elgin.qr import generate_codebar
from elgin.main import PrintHandler
import pygame

ultimo_isbn_inserido = None
def main(page: ft.Page):

    page.title = "Books"
    page.padding = 10
    page.spacing = 10
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    isbn = ft.Text(value="")

    
    dialog_success_remove = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(name=ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=30),
            ft.Text("SUCESSO")
        ]),
        content=ft.Text("Produto foi removido!"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(dialog_success_remove))
        ]
    )
    
    dialog_error = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.ORANGE, size=30),
            ft.Text("Erro")
        ]),
        content=ft.Text("Não foi possível Cadastrar o Produto!"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(dialog_error))
        ]
    )

    dialog_error_remove = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.ORANGE, size=30),
            ft.Text("Erro")
        ]),
        content=ft.Text("Não foi possível remover o produto!"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(dialog_error_remove))
        ]
    )
    
    isbn_invalido = ft.AlertDialog(
        title=ft.Row([
            ft.Icon(name=ft.Icons.ERROR, color=ft.Colors.ORANGE, size=30),
            ft.Text("Erro")
        ]),
        content=ft.Text("ISBN Invalido!"),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(isbn_invalido))
        ]
    )
    

    spinner = ft.ProgressRing(visible=False)
    spinner2 = ft.ProgressRing(visible=False)


    def go_to_entrada(e):
        page.route = "/entrada"
        page.update()


    def go_to_saida(e):
        page.route = "/saida"
        page.update()

    def on_route_change(route):
        page.views.clear()
        if page.route == "/entrada":
            page.views.append(view_entrada())
        elif page.route == "/saida":
            page.views.append(view_saida())
        page.update()



    def tocar_alerta():
        pygame.mixer.init()
        pygame.mixer.music.load(r"alert.mp3")
        pygame.mixer.music.play()


    def view_entrada():
        global ultimo_isbn_inserido
        def search_click(e):
            global ultimo_isbn_inserido
            spinner.visible = True
            loading_text.visible = True
            button.disabled = True
            # isbn_input.disabled = True
            # isbn_input.focus()
            page.update()

            isbn = isbn_input.value.strip()
            if not isbn:
                page.dialog = isbn_invalido
                page.dialog.open = True

                button.disabled = False
                # isbn_input.disabled = False
                loading_text.visible = False
                spinner.visible = False
                isbn_input.value = ""
                isbn_input.focus()
                page.update()

                return
            
            if isbn == ultimo_isbn_inserido:
                print(f"Erro: O ISBN {isbn} foi inserido duas vezes consecutivas.")
                tocar_alerta()

            ultimo_isbn_inserido = isbn

            try:
                number = inserir_produto(isbn)
                generate_codebar(str(number), str(isbn))
                directory_to_search = r"C:\Users\User\Desktop\your-directory"
                printer_name = "ELGIN L42PRO FULL"
                handler = PrintHandler(printer_name)
                handler.search_and_print(directory_to_search)
                
            except Exception as err:
                print(f"Erro: {err}")
                page.overlay.append(dialog_error)
                dialog_error.open = True

            finally:
                button.disabled = False
                # isbn_input.disabled = False
                loading_text.visible = False
                spinner.visible = False
                isbn_input.value = ""
                isbn_input.focus()


            page.update()

        product_home = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Registrar Livro",
                        size=32,
                        weight="bold",
                        color="blue",
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src="icon/imagem-livro.png",
                                width=300,
                                height=350,
                            ),
                            isbn_input := ft.TextField(
                                label="Inserir ISBN",
                                on_submit=search_click,
                                color=ft.Colors.BLACK87,
                                border_color=ft.Colors.CYAN,
                                autofocus=True
                            ),
                            button := ft.ElevatedButton(
                                text="Enviar",
                                on_click=search_click,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                    ft.ControlState.HOVERED: ft.Colors.BLUE
                                },
                                bgcolor=ft.Colors.WHITE
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            spinner,
                            loading_text := ft.Text(
                                value="Registrando livro...",
                                visible=False,
                                style=ft.TextStyle(color=ft.Colors.GREEN, size=16)
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text="Registrar Saída", on_click=go_to_saida,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                    ft.ControlState.HOVERED: ft.Colors.YELLOW
                                }, bgcolor=ft.Colors.BLUE
                            )
                        ]
                    ),
                ]
            )
        )
        layout = ft.Container(
            expand=True,
            margin=ft.margin.all(30),
            content=ft.ResponsiveRow(
                columns=12,
                spacing=0,
                run_spacing=20,
                controls=[product_home]
            )
        )

        return ft.View(
            route="/entrada",
            controls=[layout]
        )
    
        

    def view_saida():
        page.update()

        def search_click(e):
            spinner2.visible = True
            loading_text2.visible = True
            button2.disabled = True
            isbn_input2.disabled = True
            page.update()

            isbn = isbn_input2.value.strip()
            if not isbn:
                page.dialog = isbn_invalido
                page.dialog.open = True

                button2.disabled = False
                isbn_input2.disabled = False
                loading_text2.visible = False
                spinner2.visible = False
                isbn_input2.value = ""
                page.update()
                return

            try:
                if not remover_produto_por_isbn(isbn):
                    raise ValueError("Não foi encontrado na tabela 'produtos' para remoção")

                button2.disabled = False
                isbn_input2.disabled = False
                loading_text2.visible = False
                spinner2.visible = False
                isbn_input2.value = ""

                page.overlay.append(dialog_success_remove) 
                dialog_success_remove.open = True
                page.update()

            except ValueError as ve:
                print(f"Erro de validação {ve}")
                page.overlay.append(dialog_error_remove) 
                dialog_error_remove.open = True

            except Exception as err:
                print(f"Erro geral: {err}")
                page.overlay.append(dialog_error_remove) 
                dialog_error_remove.open = True
            
            finally:
                button2.disabled = False
                isbn_input2.disabled = False
                loading_text2.visible = False
                spinner2.visible = False
                isbn_input2.value = ""
                page.update()


        product_home_saida = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Remover Livro",
                        size=32,
                        weight="bold",
                        color="red",
                    ),
                    
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src="icon/imagem-livro-remover.png",
                                width=300,
                                height=350,
                            ),
                            isbn_input2 := ft.TextField(
                                label="Inserir ISBN",
                                on_submit=search_click,
                                color=ft.Colors.BLACK87,
                                border_color=ft.Colors.CYAN,
                            ),
                            button2 := ft.ElevatedButton(
                                text="Remover",
                                on_click=search_click,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                                    ft.ControlState.HOVERED: ft.Colors.RED
                                },
                                bgcolor=ft.Colors.WHITE
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            spinner2,
                            loading_text2 := ft.Text(
                                value="Removendo livro...",
                                visible=False,
                                style=ft.TextStyle(color=ft.Colors.RED, size=16)
                            )
                        ]
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text="Registrar entrada", on_click=go_to_entrada,
                                color={
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                    ft.ControlState.HOVERED: ft.Colors.YELLOW
                                }, bgcolor=ft.Colors.BLUE
                            )
                        ]
                    ),
                ]
            )
        )
        layout_saida = ft.Container(
            expand=True,
            margin=ft.margin.all(30),
            content=ft.ResponsiveRow(
                columns=12,
                spacing=0,
                run_spacing=20,
                controls=[product_home_saida]
            )
        )
        return ft.View(
            route="/saida",
            bgcolor=ft.Colors.BLACK87,
            controls=[layout_saida]
        )

    page.on_route_change = on_route_change


    page.go("/entrada")


ft.app(target=main, view="web_browser", host="0.0.0.0", port="2000", assets_dir="assets")
