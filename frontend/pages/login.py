import flet as ft

def main(page: ft.page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.DEEP_PURPLE_100
    loginPage = ft.Stack([
        ft.Column(
            [
                ft.Container(
                    margin=30,
                    padding=30,
                    bgcolor=ft.colors.BLACK45,
                    border_radius=10,
                    content=ft.Column([
                        ft.TextField(
                            label="Employee ID",
                            color=ft.colors.WHITE,
                        ),
                        ft.TextField(
                            label="Password",
                            password=True,
                            can_reveal_password=True,
                            color=ft.colors.WHITE,
                        )
                    ],

                    ),


                ),
                ft.Row(
                    [
                        ft.Container(
                            margin=30,
                            width=150,
                            content=ft.ElevatedButton(
                                "Signup",
                            )
                        ),
                        ft.Container(
                            margin=30,
                            width=150,
                            content=ft.ElevatedButton("Login")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ]
        )
    ],
        width=400,
    )

    page.add(loginPage)


ft.app(target=main)
