# honor_test_task

При запуске main.py происходит: 
1. Подключение к почтовому серверу и сбор непрочитанных писем
2. Анализ непрочитанных писем на наличие вложений с нужным расширением
3. Сохранение нужных вложений в указанной директории/
4. Заполнение базы данных данными из эксель файла вложения
5. Добавление записи в таблицу связи при создании новой таблицы из файла


Для запуска скрипта main.py каждый день в 12 часов дня - можно либо:
1) Добавить в main.py бесконечный цикл с проверкой времени
2) Добавить исполнение файла через cron (для unix)
3) Добавить исполнение файла через планировщик задач (windows)

В моем представлении - вариант 1 не самый лучший

Все решение можно исполнить в одном файле, поэтому моя реализация с интерфейсами излишняя.
Также не рассмотренно множество краевых условий, вроде дублирования имени файла вложения и тд.
