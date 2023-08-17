import io
import sys
import os
import customtkinter as CTk
from pdf_compressor import compress
from tkinter import messagebox
import logging
import mimetypes


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
        # Окно ввода пути файла
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
        # Лейбл силы сжатия
        self.compression_force_label = CTk.CTkLabel(
            self,
            text='Сила сжатия:\n\nСтандартная',
            font=("Arial", 20, "bold")
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

        logging.basicConfig(
            level=logging.ERROR,
            filename="error_log.txt",
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def browse_file(self):
        """Функция выбора файла."""

        filename = CTk.filedialog.askopenfilename()
        self.entry_file.configure(state='normal')
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, filename)
        self.entry_file.configure(state='readonly')

    def get_compression_force_name(self):
        """Добавляет название для лейбла."""

        force = self.compression_force_slider.get()
        if force == 0:
            return "стандартная"
        elif force == 1:
            return "допечатная"
        elif force == 2:
            return "печать"
        elif force == 3:
            return "на_почту"
        elif force == 4:
            return "максимальное_сжатие"

    def update_compression_force_label(self, event):
        """Функция обновления значений слайдера."""

        compression_force = int(self.compression_force_slider.get())
        if compression_force == 0:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nСтандартная')

        elif compression_force == 1:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nДопечатная')
        elif compression_force == 2:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nПечать')
        elif compression_force == 3:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nНа почту')
        elif compression_force == 4:
            self.compression_force_label.configure(
                text='Сила сжатия:\n\nМаксимальное сжатие')

    def browse_file(self):
        """Функция выбора файла."""
        filename = CTk.filedialog.askopenfilename()

        if filename:
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type != 'application/pdf':
                messagebox.showerror("Ошибка", "Выбранный файл не является PDF.")
                return

            self.entry_file.configure(state='normal')
            self.entry_file.delete(0, 'end')
            self.entry_file.insert(0, filename)
            self.entry_file.configure(state='readonly')

    def compress_file(self):
        """Функция сжатия файла."""

        input_file = str(self.entry_file.get())

        if not input_file:
            messagebox.showerror("Ошибка", "Выберите файл для сжатия.")
            return

        mime_type, _ = mimetypes.guess_type(input_file)
        if mime_type != 'application/pdf':
            messagebox.showerror("Ошибка", "Выбранный файл не является PDF.")
            return

        if not input_file:
            messagebox.showerror("Ошибка", "Выберите файл для сжатия.")
            return

        file_name, file_extension = os.path.splitext(input_file)
        output_file = "{}_{}_{}{}".format(
            file_name, "сжатый",
            self.get_compression_force_name(),
            file_extension
        )

        if os.path.exists(output_file):
            response = messagebox.askyesno(
                "Файл уже существует",
                "Файл сжатия уже существует. Перезаписать?"
            )
            if not response:
                return

        try:
            # Создаем объект StringIO для перехвата вывода консоли
            console_output = io.StringIO()
            # Сохраняем текущий вывод консоли
            sys.stdout = console_output

            # Вызываем compress функцию
            compress(input_file,
                     output_file,
                     power=int(self.compression_force_slider.get()))

            # Получаем вывод консоли в виде строки
            console_output_str = console_output.getvalue()
            
            # Возвращаем вывод консоли в стандартное состояние
            sys.stdout = sys.__stdout__

            # Показываем messagebox и добавляем вывод консоли в него
            messagebox.showinfo("Успех", f"Файл успешно сжат.\n\nИтого:\n{console_output_str}")
        except Exception as e:
            # То же самое для случая ошибки
            console_output_str = console_output.getvalue()
            sys.stdout = sys.__stdout__
            messagebox.showerror("Ошибка", f"Произошла ошибка при сжатии файла: {str(e)}\n\nВывод консоли:\n{console_output_str}")
            logging.error(f"Ошибка при сжатии файла: {str(e)}", exc_info=True)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
