import io
import logging
import mimetypes
import os
import sys
import tkinter
from tkinter import messagebox

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

        # Radiobutton силы сжатия
        self.radio_var = tkinter.IntVar(value=0)
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
        self.rb_force_0 = CTk.CTkRadioButton(
            master=self.settings_frame,
            variable=self.radio_var,
            value=0,
            text='Стандартная'
        )
        self.rb_force_0.grid(
            row=0,
            column=1,
            padx=(20, 20),
            pady=(20, 20)
        )

        self.rb_force_1 = CTk.CTkRadioButton(
            master=self.settings_frame,
            variable=self.radio_var,
            value=1,
            text='Допечатная'
        )
        self.rb_force_1.grid(
            row=0,
            column=2,
        )
        self.rb_force_2 = CTk.CTkRadioButton(
            master=self.settings_frame,
            variable=self.radio_var,
            value=2,
            text='Печать'
        )
        self.rb_force_2.grid(
            row=0,
            column=3,
            padx=(20, 0),
        )
        self.rb_force_3 = CTk.CTkRadioButton(
            master=self.settings_frame,
            variable=self.radio_var,
            value=3,
            text='На почту'
        )
        self.rb_force_3.grid(
            row=0,
            column=4,
        )
        self.rb_force_4 = CTk.CTkRadioButton(
            master=self.settings_frame,
            variable=self.radio_var,
            value=4,
            text='Максимум'
        )
        self.rb_force_4.grid(
            row=0,
            column=6,
        )
        # кнопка сжатия
        self.compress_button = CTk.CTkButton(
            master=self.settings_frame,
            text="Сжать файл",
            width=100,
            command=self.compress_file
        )
        self.compress_button.grid(
            row=4,
            column=2,
            columnspan=3,
            padx=(10, 50),
            pady=100,
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

        if filename:
            mime_type, _ = mimetypes.guess_type(filename)
            if mime_type != 'application/pdf':
                messagebox.showerror(
                    "Ошибка", "Выбранный файл не является PDF.")
                return

            self.entry_file.configure(state='normal')
            self.entry_file.delete(0, 'end')
            self.entry_file.insert(0, filename)
            self.entry_file.configure(state='readonly')

    def get_compression_force_name(self):
        """Добавляет название в файл."""

        force = self. radio_var.get()
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

    def compress_file(self):
        """Функция сжатия файла."""

        input_file = str(self.entry_file.get())

        if not input_file:
            messagebox.showerror("Ошибка", "Выберите файл для сжатия.")
            # Восстанавливаем текст на кнопке после завершения операции
            self.compress_button.configure(text="Сжать файл")
            return

        mime_type, _ = mimetypes.guess_type(input_file)
        if mime_type != 'application/pdf':
            messagebox.showerror("Ошибка", "Выбранный файл не является PDF.")
            # Восстанавливаем текст на кнопке после завершения операции
            self.compress_button.configure(text="Сжать файл")
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
            self.compress_button.configure(text="Подождите...")
            self.message = messagebox.showinfo(
                "Продолжить?", "Нажмите ОК для продолжения"
            )
            console_output = io.StringIO()
            # Сохраняем текущий вывод консоли
            sys.stdout = console_output

            # Вызываем compress функцию
            compress(input_file,
                     output_file,
                     power=int(self.radio_var.get()))

            # Получаем вывод консоли в виде строки
            console_output_str = console_output.getvalue()

            # Возвращаем вывод консоли в стандартное состояние
            sys.stdout = sys.__stdout__

            # Показываем messagebox и добавляем вывод консоли в него
            messagebox.showinfo(
                "Успех", f"Файл успешно сжат.\n\nИтого:\n{console_output_str}")
        except Exception as e:
            # То же самое для случая ошибки
            console_output_str = console_output.getvalue()
            sys.stdout = sys.__stdout__
            messagebox.showerror(
                "Ошибка", f"Произошла ошибка при сжатии файла: {str(e)}\n"
                f"\nВывод консоли:\n{console_output_str}")
            logging.error(f"Ошибка при сжатии файла: {str(e)}", exc_info=True)
        finally:
            # Восстанавливаем текст на кнопке после завершения операции
            self.compress_button.configure(text="Сжать файл")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
