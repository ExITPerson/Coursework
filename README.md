![b3a5a00f-6e6b-488f-9ac1-5623c31cb0d1.jpg](design_tools%2Fb3a5a00f-6e6b-488f-9ac1-5623c31cb0d1.jpg)

# <p align="center"> Проект 1 </p>


## <p align="center">Описание</p>

**<p align="center">Проект 1 - это программа для анализа транзакций и вывода их пользователю в виде JSON-ответа</p>**

---

## <p align="center">Функции программы</p>


- **Формирование отчетов за 3 месяца по категориям, дням недели, выходным и будним дням**
- **Формирование JSON-ответов с данными о транзакциях, курсе валют, цене по тикерам для дальнейшего вывода пользователю**
- **Вычисление возможного кэшбэка по месяцам, для вывода в предложении "Повышенный кэшбэк"**


----

## <p align="center">Установка</p>

1. **Клонируйте репозиторий:**
````
git clone https://github.com/ExITPerson/Coursework.git
````

2. **Установите зависимости:**
````
pip install -r requirements.txt
````
---

## <p align="center">Информация о тестировании проекта</p>

- **Запустите тестирование**
````
pytest --cov src --cov-report term-missing
````

- **Увидите информацию о тестах папки scr в терминале**

````
========================= test session starts =========================
platform win32 -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: C:\Users\eliab\my_prj\Coursework
configfile: pytest.ini
plugins: cov-6.0.0, pytest_freezer-0.4.8, xdist-3.6.1
collected 35 items                                                                                                  

tests\test_decorators.py ..                                     [  5%]
tests\test_reports.py ...                                       [ 14%]
tests\test_services.py .....                                    [ 28%]
tests\test_utils.py .....                                       [ 42%]
tests\test_views\test_exchange_rate.py ...                      [ 51%]
tests\test_views\test_get_top_five_transactions.py .....        [ 65%]
tests\test_views\test_greeting.py ....                          [ 77%]
tests\test_views\test_info_on_the_card.py .....                 [ 91%]
tests\test_views\test_stock_quotes.py ...                       [100%]

---------- coverage: platform win32, python 3.12.6-final-0 -----------
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
src\__init__.py        0      0   100%
src\decorator.py      18      0   100%
src\reports.py        89      6    93%   46-48, 118-120
src\services.py       32      0   100%
src\utils.py          21      0   100%
src\views.py         109     10    91%   163-180
------------------------------------------------
TOTAL                269     16    94%


========================= 35 passed in 2.92s ==========================
````
