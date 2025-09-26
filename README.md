# Default_IDE
This is repository of Default IDE for Default programming language created by idiot

# Руководство по сборке программы DefaultIDE на macOS

## Команда сборки

Для создания исполняемого файла используется **PyInstaller**.  
Полная команда для сборки выглядит так (одной строкой):

```bash
pyinstaller --name DefaultIDE --noconsole --windowed --onefile ./appCode/DefaultIDE.py --add-binary "./compiler/Default:." \
--add-binary "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13:." \
--add-binary "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload:." \
--add-binary "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages:." \
--add-binary "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/setuptools/_vendor:."
```

## Объяснение параметров

- `--name DefaultIDE` — имя итоговой программы.
- `--noconsole` — отключает вывод консоли при запуске.
- `--windowed` — делает приложение графическим (GUI) для macOS.
- `--onefile` — собирает всё в один исполняемый файл.

### Добавляемые бинарные файлы (`--add-binary`)
- `"Default:."` — файл `Default`, который программа использует как «компилятор» по умолчанию.
- `.../lib/python3.13` — стандартные библиотеки Python 3.13.
- `.../lib-dynload` — динамически подгружаемые расширения Python.
- `.../site-packages` — установленные внешние пакеты Python.
- `.../setuptools/_vendor` — встроенные зависимости setuptools, которые иногда нужны при работе.

Каждый `--add-binary "путь:."` означает:  
- **путь** — что именно добавляется в сборку.  
- `:.` — куда именно в bundle кладётся (в корень временной директории `_MEIPASS`).

## Результат

После выполнения команды в папке `dist/` появится файл:

- `DefaultIDE` (исполняемый бинарь для macOS).

Его можно запускать напрямую или упаковать в `.app`.  

Если при запуске macOS выдаёт предупреждение «неизвестный разработчик», нужно открыть приложение через контекстное меню → **Открыть**.

