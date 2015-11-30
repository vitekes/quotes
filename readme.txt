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
 - env\env\Scripts\activate.bat
возможно потребуется установка visual studio

7) модуль pycurl устанавливается в ручную. Короткий путь установки: 
   установить pycurl в систему, затем из папки python/Lib/Site-packages скопироваь файл в наше виртуальное окружение
   env/venv/Lib/Site-packages файл pycurl-7.19.5.3-py2.7.egg-info

8) установить зависимости проекта (из папки intranet_py)
 - pip install -r deps

9) python runner.py --help для получения информации по запуску тестов

* при первом запуске будут установлены все зависимости для отчетов allure из мавена