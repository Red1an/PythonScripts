#set page(margin: (left: 3cm, right: 1cm, y: 2cm))
#set text(size: 14pt, font: "Times New Roman", lang: "ru")
#set par(justify: true)

#import "../../title.typ": title
#import "../../template.typ": template, struct-heading

#title( 
  "41", // кафедра
  "РЕКУРРЕНТНЫЕ НЕЙРОННЫЕ СЕТИ", // название лабы 
  "МАШИННОЕ ОБУЧЕНИЕ И БОЛЬШИЕ ДАННЫЕ", // название предмета
  "4316", // группа
  "М.С. Пронь", // студент
  "А.С. Раскопина", // ФИО препода
  "ассистент" // должность
)

#show: doc => template(doc)

#show raw.where(block: true): it => {
  set text(font: "Courier New", size: 11pt)
  set par(leading: 0.45em, justify: false)
  block(
    width: 100%,
    fill: none,
    stroke: 0.5pt + black,
    inset: 8pt,
    radius: 2pt,
    breakable: true,
    it
  )
}


#outline()

#pagebreak()

= Цель работы
Изучить принципы работы рекуррентных нейронных сетей для прогнозирования временных рядов.


= Описание датасета
В работе был использован датасет Traffic Time Series Dataset для 20 варианта, содержащий почасовые наблюдения дорожного трафика, погодных условий и событий. Была выполнена загрузка данных из открытого источника Kaggle и была проверена структура таблицы (рис. @fig:source-ds).

#figure(
  image("Pictures/1)Исходный датасет.png", width: 80%),
  caption: [Исходный датасет]
) <fig:source-ds>

Был выведен первичный анализ данных: информация о типах столбцов, статистические характеристики, наличие пропусков и базовые свойства признаков (рис. @fig:eda-ds). На данном этапе было установлено, что данные пригодны для построения моделей после стандартной предобработки.

#figure(
  image("Pictures/2)Анализ датасета.png", width: 80%),
  caption: [Анализ датасета]
) <fig:eda-ds>

Был построен и проанализирован график временного ряда для оценки динамики и возможной сезонности (рис. @fig:ts-plot). Было показано, что ряд обладает выраженной изменчивостью, что обосновывает применение рекуррентных архитектур.

#figure(
  image("Pictures/3)Временые ряды трафика.png", width: 100%),
  caption: [Временные ряды трафика]
) <fig:ts-plot>

= Описание обученных моделей и их адаптация
В рамках лабораторной работы были реализованы и исследованы три архитектуры рекуррентных сетей: классическая RNN, LSTM и GRU. Для всех моделей была использована единая схема адаптации: одинаковая длина входного окна, сопоставимое число скрытых слоев, одинаковый размер скрытого состояния и единый выходной блок регрессии. Такой подход позволил выполнить корректное сравнение моделей в одинаковых условиях.

Ниже приведен листинг реализации моделей, использованный в работе.

#figure(
```python
class RNNModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )


class LSTMModel(nn.Module):
    """LSTM - Long Short-Term Memory"""
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )


class GRUModel(nn.Module):
    """GRU - Gated Recurrent Unit"""
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )


for ModelClass, name in [(RNNModel, 'RNN'), (LSTMModel, 'LSTM'), (GRUModel, 'GRU')]:
    model = ModelClass().to(DEVICE)
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f'{name}: {n_params:,} обучаемых параметров')
    del model
```,
  caption: [Листинг реализации RNN, LSTM и GRU]
) <lst:models>

Была выполнена предварительная инженерия признаков и формирование многомерного входа модели: к целевому признаку трафика были добавлены погодные и календарные признаки. Было выполнено масштабирование признаков и было сформировано скользящее окно фиксированной длины (рис. @fig:preproc).

#figure(
  image("Pictures/4)Предобработка данных.png", width: 80%),
  caption: [Предобработка данных]
) <fig:preproc>

= Процесс обучения
Было выполнено обучение трех моделей на одинаковых обучающей, валидационной и тестовой выборках. В процессе обучения была использована оптимизация Adam, функция потерь MSE и механизм ранней остановки по валидационной ошибке. Такой протокол позволил снизить риск переобучения и обеспечить сопоставимость результатов.

Был выведен сводный результат этапа обучения моделей (рис. @fig:train-summary), после чего была выполнена визуализация кривых обучения для анализа сходимости (рис. @fig:train-curves).

#figure(
  image("Pictures/5)Обучение моделей.png", width: 100%),
  caption: [Обучение моделей]
) <fig:train-summary>

#figure(
  image("Pictures/6)Графики процесса обучения.png", width: 100%),
  caption: [Графики процесса обучения]
) <fig:train-curves>

= Сравнение моделей, анализ результатов
Было выполнено сравнение качества моделей по метрикам MSE, MAE и $R^2$ (рис. @fig:metrics-compare). Было установлено, что модели LSTM и GRU демонстрируют более высокое качество прогнозирования по сравнению с классической RNN, что согласуется с их архитектурными особенностями и лучшей способностью учитывать долгосрочные зависимости.

#figure(
  image("Pictures/7)Сравнение метрик качества.png", width: 100%),
  caption: [Сравнение метрик качества]
) <fig:metrics-compare>

Дополнительно было выполнено сравнение предсказаний моделей с реальными значениями временного ряда (рис. @fig:preds-compare). Было показано, что современные gated-архитектуры (LSTM, GRU) лучше повторяют динамику целевого сигнала и формируют более устойчивый прогноз.

#figure(
  image("Pictures/8)Сравнение предсказаний моделей.png", width: 100%),
  caption: [Сравнение предсказаний моделей]
) <fig:preds-compare>

= Выводы
В ходе лабораторной работы была исследована задача прогнозирования временного ряда трафика с использованием рекуррентных нейронных сетей. Был выполнен полный цикл работ: загрузка и анализ датасета, предобработка признаков, обучение трех моделей (RNN, LSTM, GRU), оценка качества и интерпретация результатов.

По итогам сравнения было установлено, что модели LSTM и GRU обеспечивают более точный прогноз по метрикам MSE, MAE и $R^2$ по сравнению с базовой RNN. Полученные результаты соответствуют цели работы и подтверждают целесообразность применения gated-рекуррентных архитектур для задач прогнозирования трафика.


Код лабораторной работы приведен в ноутбуке: https://colab.research.google.com/drive/1QRQkVEfiyLFfpJ1WjRFh6HMPyUuZWAA7?usp=sharing
