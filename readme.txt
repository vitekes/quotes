Подготовка окружения

1 Установить python version 2.7.x

2) скачать allure-cli и разархивировать
 https://github.com/allure-framework/allure-cli/releases/tag/allure-cli-2.3
 для упрощения работы содержимое архива (папки bin/ и lib/) можно разархивировать в папку intranet_py/env/allure

3) Установить virtualenv
 - pip install virtualenv

4) Открыть папку проекта в консоли

5) Создать окружение
 - virtualenv env\venv

6) активировать окружение
 - env\venv\Scripts\activate.bat
возможно потребуется установка visual studio

7) модуль pycurl устанавливается в ручную. Короткий путь установки: 
   Скачать pycurl http://pycurl.sourceforge.net/download/pycurl-7.19.5.win32-py2.7.zip
   Разархивировать скачанный архив в папку env\venv\Lib\site-packages

8) установить зависимости проекта (из папки intranet_py)
 - pip install -r deps

9) python runner.py --help для получения информации по запуску тестов

* при первом запуске будут установлены все зависимости для отчетов allure из мавена