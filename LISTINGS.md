# Соответствие листингов и файлов

| Листинг | Файл | Название |
|---|---|---|
| 1.1 | [access_gate.py](access_gate.py) | Проверка объекта, версии и разрешённой операции |
| 1.2 | [resume_memory.py](resume_memory.py) | Возобновление после потери ответа в локальной памяти |
| 2.1 | [validate_request.py](validate_request.py) | Ограниченная валидация запроса проекта |
| 2.2 | [search_adapter.py](search_adapter.py) | Нормализация результата поиска с признаком полноты |
| 2.3 | [intent_store.py](intent_store.py) | Транзакция SQLite для ключа и локального эффекта |
| 2.4 | [canonical_profile.py](canonical_profile.py) | Отпечаток ограниченного профиля JSON |
| 2.5 | [retry_budget.py](retry_budget.py) | Расписание повторов и бюджет ожидания |
| 2.6 | [versioned_write.py](versioned_write.py) | Запись с атомарным предусловием версии |
| 3.1 | [repeat_guard.py](repeat_guard.py) | Контроль повторного чтения на неизменном снимке |
| 3.2 | [plan_order.py](plan_order.py) | Топологический порядок и выявление цикла |
| 3.3 | [shortest_path.py](shortest_path.py) | Кратчайший путь с неотрицательной стоимостью |
| 3.4 | [reasoning_cost.py](reasoning_cost.py) | Условная экономика выбора режима по семейству |
| 3.5 | [invalidate.py](invalidate.py) | Аннулирование зависимых результатов |
| 4.1 | [snapshot_fields.py](snapshot_fields.py) | Проверка обязательных полей снимка задания |
| 4.2 | [memory_filter.py](memory_filter.py) | Фильтрация области доступа перед ранжированием |
| 4.3 | [memory_checks.py](memory_checks.py) | Контрольные сценарии памяти |
| 5.1 | [handoff_check.py](handoff_check.py) | Проверка пакета результата исполнителя |
| 5.2 | [orchestration_cost.py](orchestration_cost.py) | Расчёт условного времени и цены оркестрации |
| 5.3 | [schedule.py](schedule.py) | Расписание с ограниченным числом рабочих мест |
| 5.4 | [delivery.py](delivery.py) | Повторная доставка без повторной обработки |
| 5.5 | [outbox.py](outbox.py) | Локальная фиксация результата и уведомления |
| 6.1 | [short_runner.py](short_runner.py) | Запуск короткой проверки без оболочки |
| 6.2 | [batch_before.py](batch_before.py) | Исходный обработчик |
| 6.3 | [batch_after.py](batch_after.py) | Исправленный обработчик |
| 6.4 | [batch_checks.py](batch_checks.py) | Проверки контракта и отрицательный контроль |
| 6.5 | [batch_properties.py](batch_properties.py) | Полный перебор коротких пакетов |
| 6.6 | [batch_manifest.py](batch_manifest.py) | Манифест исходников учебного кейса |
| 6.7 | [allowed_path.py](allowed_path.py) | Проверка целевого пути в рабочей области |
| 7.1 | [stale_action.py](stale_action.py) | Отклонение действия по устаревшему наблюдению |
| 7.2 | [ui_model.py](ui_model.py) | Учебный автомат |
| 7.3 | [ui_checks.py](ui_checks.py) | Проверки повторной отправки и версии формы |
| 7.4 | [coordinates.py](coordinates.py) | Проверка координатного преобразования |
| 8.1 | [qlearning.py](qlearning.py) | Q-обучение и контроль неверной награды |
| 8.2 | [learning.py](learning.py) | Сравнение покрытия демонстрациями |
| 8.3 | [learning_checks.py](learning_checks.py) | Отрицательный контроль покрытия состояний |
| 9.1 | [audit_chain.py](audit_chain.py) | Проверка целостности учебного журнала |
| 9.2 | [security.py](security.py) | Проверка внешнего допуска |
| 9.3 | [fault_matrix.py](fault_matrix.py) | Размещение отказа и согласование |
| 10.1 | [economics.py](economics.py) | Расчёт затрат условного проекта |
| 10.2 | [enterprise_case.py](enterprise_case.py) | Конечный стенд промышленного маршрута |
| 10.3 | [framework_checks.py](framework_checks.py) | Повтор, конфликт и восстановление |
| А.1 | [framework.py](framework.py) | Полный конечный каркас агента |
| А.2 | [run_examples.sh](run_examples.sh) | Команды запуска учебных примеров |
| Б.1 | [read_schema.json](read_schema.json) | Схема чтения документа |
| Б.2 | [draft_schema.json](draft_schema.json) | Схема подготовки черновика |
| Б.3 | [publish_schema.json](publish_schema.json) | Схема публикации |
| Б.4 | [operation_schema.json](operation_schema.json) | Схема поиска операции |
