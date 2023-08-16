import customtkinter as CTk
from pdf_compressor import compress


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
            row=5,
            column=0,
            padx=(10, 5),
            pady=20,
            sticky="nsew",
        )
        self.compression_force_slider = CTk.CTkSlider(
            master=self.settings_frame,
            from_=0,
            to=4,
            number_of_steps=4,
            width=500
        )
        self.compression_force_slider.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=(20, 20),
            pady=(20, 20),
            sticky='ew'
        )
        self.compression_force_slider.set(0)
        self.compression_force_slider.bind(
            '<ButtonRelease-1>',
            self.update_compression_force_label
        )

        self.compression_force_label = CTk.CTkLabel(
            self,
            text='Сила сжатия:\n\nПо умолчанию'
        )
        self.compression_force_label.grid(
            row=3,
            column=0,
            columnspan=3,
            pady=(10, 0)
        )

        # кнопка сжатия
        self.info_button = CTk.CTkButton(
            master=self.settings_frame,
            text="Сжать файл",
            width=100,
            command=self.compress_file
        )
        self.info_button.grid(
            row=4,
            column=1,
            pady=60,
            sticky='ew'
        )
        self.toplevel_window = None

    def browse_file(self):
        """Функция выбора файла."""

        filename = CTk.filedialog.askopenfilename()
        self.entry_file.configure(state='normal')
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, filename)
        self.entry_file.configure(state='readonly')

    def update_compression_force_label(self, event):
        """Функция обновления значений слайдера."""

        compression_force = int(self.compression_force_slider.get())
        if compression_force == 0:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nПо умолчанию')

        elif compression_force == 1:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nДопечатная подготовка')
        elif compression_force == 2:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nПечать')
        elif compression_force == 3:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nОтправка по почте')
        elif compression_force == 4:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nМаксимальное сжатие')

    def compress_file(self):
        compress('pdf/test.pdf',
                 'pdf/compressed_test.pdf',
                 power=int(self.compression_force_slider.get()))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
