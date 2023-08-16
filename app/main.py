import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Главное окно
        h, w = 585, 400
        self.title("Сжать PDF")
        self.geometry(f'{h}x{w}')
        self.resizable(False, False)
        CTk.set_default_color_theme("blue")

        self.file_frame = CTk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.file_frame.grid(
            row=1,
            column=0,
            padx=(20, 20),
            pady=(20, 20),
            sticky="nsew"
        )
        # Окно ввода пароля
        self.entry_file = CTk.CTkEntry(
            master=self.file_frame,
            width=400
        )
        self.entry_file.grid(
            row=0,
            column=0,
            padx=(20, 20),
            pady=(40, 20)
        )
        self.btn_choice = CTk.CTkButton(
            master=self.file_frame,
            text="Выбрать файл",
            width=100,
            command=self.browse_file
        )
        self.btn_choice.grid(
            row=0,
            column=1,
            pady=(40, 20)
        )
        # слайдер силы сжатия
        self.settings_frame = CTk.CTkFrame(
            master=self,
            fg_color="transparent"
        )
        self.settings_frame.grid(
            row=2,
            column=0,
            padx=(10, 5),
            sticky="nsew",
        )
        self.compression_force_slider = CTk.CTkSlider(
            master=self.settings_frame,
            from_=0,
            to=4,
            number_of_steps=4,
            width=500
            # command=self.slider_event
        )
        self.compression_force_slider.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=(20, 20),
            pady=(20, 20),
            sticky='ew'
        )

    def browse_file(self):
        """Функция выбора файла."""
        filename = CTk.filedialog.askopenfilename()
        self.entry_file.configure(state='normal')
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, filename)
        self.entry_file.configure(state='readonly')


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
