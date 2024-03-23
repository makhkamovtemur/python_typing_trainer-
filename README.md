# practicum_Python
Версия: 1.1
Автор: Махкамов Темур (makhkamovtemur@gmail.com)

## Описание
Клавиатурный тренажер, в форме игры, который поможет пользователям улучшить навыки быстрого и точного набора текста на клавиатуре.

## Реализуемый функционал
1. Интерфейс для тренировки: Пользователь видит строку, которую необходимо набрать, и поле для ввода текста. Тренажёр не допускает ввод неправильных символов.
2. Подсчет количества ошибок и скорости печати с сохранением истории результатов между сессиями.
3. Графический интерфейс (GUI), разработка приятного и интуитивно понятного графического интерфейса для удобства использования.
4. Отображение статистики во время печати, вывод текущих показателей скорости и количества ошибок на экран.
5. Анализ наиболее частых ошибок на клавиатуре, где пользователь чаще всего допускает ошибки.

## Состав
* Сама игра `TypingTrainer.py`
* Модули `src/` 
* Тесты `tests/`
* Словари `dictionaries/`

## Классы и модули:
* TextGenerator - загрузка и выбор текстов для тренировки из заданных файлов.
* TypingSession - управление сессией печати: отслеживание введенных символов, подсчет ошибок и скорости печати.
* UserStats - управление статистикой пользователя, включая сохранение и загрузку данных между сессиями.
* GUI - создание и управление графическим интерфейсом пользователя.
* HeatmapGenerator - анализ ошибок и создание визуализации heatmap для клавиш.

### Функции:

* main() - основная функция для запуска и управления приложением.


Вспомогательные функции для обработки данных и взаимодействия с пользователем.


