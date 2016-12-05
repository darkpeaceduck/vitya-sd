## Архитектура

Ecть три части : Bus, View, ConnectionManager (для каждой части есть абстрактные классы).
ConnectionManager отвечает за пересылку сообщений. Юзер сначала должен зарегистрироваться(addListener), затем должен переключится в режим listen или
connect, а затем ему начнут приходить уведомления.

View - отвечает за отрисовку информации.

Так как в основном в реализациях View и ConnectionManager свои системы тредов, то вводится промежуточная 
сущность Bus (в основном все же сделано для удобства сбора информации из UI тредов - то есть во время обновления UI делаются poll в Bus).
В принципе в реализациях UI можно обойтись без bus, в таком случае класс UI должен реализовывать и Abstract Bus.

## Расширяемость 
Для добавление Ui интерфейса нужно реализовать AbstractView
Для добавления протокола соединения нужно реализовать AbstractConnectionManager

## Реализация

Есть реализация ConnectionManager на socket + asyncore, View на Tkinter (запуск - добавить src/python в PYTHONPATH , затем python3 chat/run_trUI_sockets.py (логгирование включено на DEBUG(логируются реализиции connection managerов)); тесты - python3 -m unittest discover -s chat/tst)

