# параметры
передаются в словаре c ключами:
* host
* port
* db_name all_tables
# методы
* **drop_db** -удаляет базу
* **all_tables** -список таблиц 
* **dbstats**- статиска базы данных
* **table_exists**(*table_name*) -проверка наличия таблицы
* **get_table_cursor**(*table*,*condition*,*query*-подзапрос к таблице,*columns*-список возвращаемых колонок) -возвращает курсор на таблицу
* **agg_cursor**(*table_name*,*group*-группируемые поля,*agg_functions_list*-список агрегирующих функций -возвращает курсор на таблицу
* **merge_cursor**
* **find_one**

* **insert_into_table** (*table_name* -таблица,*data*- одна строка или несколько,*bulk* -вставка записей *пачкой*,*update_criteria*- критерий обновления существующих записей,*rewrite* -признак перезаписи табилцы целиком)

