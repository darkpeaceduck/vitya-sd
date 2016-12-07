### Требования : 
 
 - python 3.4.3+ lib
 - ply
 
### Запуск : 
 - add src folder to PYTHONPATH, 
 - run shell as python3 src/cli/shell.py, 
 - run sep unittest as python3 -m unittest src/cli/tst/{test}
 - run all uniitest as python3 -m unittest discover -s src/cli/tst
 
### Архитектура

 - preprocessor.py выполняет подстановку переменных окружения
 - lang.py описывает структуры языка шелла
 - parser.py парсит результат, отданный препроцессором в структуры языка
 - env.py содержит класс Env для работы с окружением
 - runtime.py инъектирует метод exec в структуры языка
 - cmd.py - Сmd.exec использует map_exec из этого модуля чтобы выполнить определенную команду.
   Чтобы добавить новую команду, нужно релизовать функцию с аргументами (args, env, input, output) под
   декоратором @cmd("cmdname"), где cmdname - имя команды, которая реализуется
 - shell.py - читает очередную строку, отдает её препроцессору, результат отдает парсеру, от результата вызывается .exec  
 