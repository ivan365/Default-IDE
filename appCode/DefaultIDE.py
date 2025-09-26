import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import re
import subprocess
import os
import threading
import sys

# Настраиваемый "словарь" правил для подсветки
SYNTAX_RULES = {
    'keywords': {
        'color': 'orange',
        'pattern': r'\b(def|class|import|from|as|if|else|elif|for|while|in|is|not|and|or|True|False|None)\b'
    },
    'operators': {
        'color': '#8A2BE2',
        'pattern': r'([+\-*/=><~!%^&|\[\]{}()])'
    },
    'strings': {
        'color': 'green',
        'pattern': r'(".*?"|\'.*?\')'
    },
    'comments': {
        'color': 'gray',
        'pattern': r'#.*$'
    }
}

class PowerfulEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Мощный Py-Editor")
        self.root.geometry("900x700")

        self.current_file_path = None
        self.compiler_path = None
        self.config_file = "compiler_path.cfg"
        self.process = None
        self.load_compiler_path()

        self.paned_window = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.paned_window.pack(expand=True, fill="both")

        self.editor_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.editor_frame, stretch="always")

        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<KeyRelease>", self.highlight_syntax)

        for tag_name, rule in SYNTAX_RULES.items():
            self.text_area.tag_config(f"{tag_name}_tag", foreground=rule['color'])

        self.output_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.output_frame, height=150, stretch="never")

        self.output_label = tk.Label(self.output_frame, text="Вывод:", font=("Helvetica", 12, "bold"))
        self.output_label.pack(anchor="w", padx=5)
        self.output_area = scrolledtext.ScrolledText(self.output_frame, font=("Courier", 10), state=tk.DISABLED, background="#222", foreground="#eee")
        self.output_area.pack(expand=True, fill="both", padx=5, pady=5)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)
        self.file_menu.add_command(label="Открыть...", command=self.open_file)
        self.file_menu.add_command(label="Сохранить как...", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=self.exit_app)
        
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Выполнить", menu=self.run_menu)
        self.run_menu.add_command(label="Настроить компилятор", command=self.set_compiler_path)
        self.run_menu.add_command(label="Запустить файл", command=self.run_file)
        self.run_menu.add_command(label="Остановить", command=self.stop_execution)
    
    def load_compiler_path(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                self.compiler_path = file.read().strip()

    def save_compiler_path(self):
        with open(self.config_file, "w") as file:
            file.write(self.compiler_path)

    def set_compiler_path(self):
        path = filedialog.askopenfilename(title="Выберите интерпретатор Python", filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")])
        if path:
            self.compiler_path = path
            self.save_compiler_path()
            messagebox.showinfo("Успех", f"Путь к компилятору сохранён:\n{self.compiler_path}")

    def run_file(self):
        if not self.current_file_path:
            messagebox.showwarning("Предупреждение", "Сначала сохраните файл, чтобы его запустить.")
            return

        if self.process and self.process.poll() is None:
            messagebox.showwarning("Предупреждение", "Процесс уже запущен. Сначала остановите его.")
            return

        # Проверяем, запущены ли мы из PyInstaller
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.getcwd())
            default_compiler = os.path.join(base_dir, 'Default')
        else:
            default_compiler = os.path.join(os.getcwd(), 'Default')

        # НОВАЯ ЛОГИКА: используем сохранённый путь ТОЛЬКО если он существует
        if self.compiler_path and os.path.exists(self.compiler_path):
            compiler = self.compiler_path
        else:
            compiler = default_compiler
        
        if not os.path.exists(compiler):
            messagebox.showerror("Ошибка", f"Компилятор не найден по пути:\n{compiler}")
            return

        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, f"Запуск файла: {self.current_file_path}\nИспользуется компилятор: {compiler}\n\n")

        try:
            self.process = subprocess.Popen([compiler, self.current_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            
            thread_out = threading.Thread(target=self.read_output, args=(self.process.stdout, "stdout"))
            thread_err = threading.Thread(target=self.read_output, args=(self.process.stderr, "stderr"))
            thread_out.daemon = True
            thread_err.daemon = True
            thread_out.start()
            thread_err.start()

        except FileNotFoundError:
            self.output_area.insert(tk.END, f"ОШИБКА: Компилятор не найден по пути:\n{compiler}")
            self.output_area.config(state=tk.DISABLED)

    def read_output(self, stream, stream_type):
        try:
            for line in stream:
                if stream_type == "stderr":
                    self.output_area.insert(tk.END, f"ОШИБКА: {line}", 'error_tag')
                else:
                    self.output_area.insert(tk.END, line)
                self.output_area.see(tk.END)
        except ValueError:
            pass

    def stop_execution(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            messagebox.showinfo("Готово", "Процесс остановлен.")
            self.output_area.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Предупреждение", "Процесс не запущен.")
    
    def highlight_syntax(self, event=None):
        for tag_name in SYNTAX_RULES.keys():
            self.text_area.tag_remove(f"{tag_name}_tag", "1.0", tk.END)

        text_content = self.text_area.get("1.0", tk.END)
        
        for tag_name, rule in SYNTAX_RULES.items():
            pattern = rule['pattern']
            for match in re.finditer(pattern, text_content, re.MULTILINE):
                start_index = f"1.0+{match.start()}c"
                end_index = f"1.0+{match.end()}c"
                self.text_area.tag_add(f"{tag_name}_tag", start_index, end_index)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.current_file_path = file_path
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
                self.root.title(f"Py-Editor - {os.path.basename(file_path)}")
                self.highlight_syntax()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

    def save_file(self):
        if self.current_file_path:
            file_path = self.current_file_path
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text_area.get("1.0", tk.END)
                    file.write(content)
                self.current_file_path = file_path
                self.root.title(f"Py-Editor - {os.path.basename(file_path)}")
                messagebox.showinfo("Сохранено", "Файл успешно сохранён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def exit_app(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()
    
def main():
    root = tk.Tk()
    app = PowerfulEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()