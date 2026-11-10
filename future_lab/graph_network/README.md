# Graph & Network Methods — Future Lab

Статус: **DESIGNED / DISCOVERED**.

Назначение: общий математический пакет для AU-01, FATHER Factory, ALINA BOOK 2, OSINT, Security, Business, Logistics и инфраструктурных агентов.

## Базовая модель

Граф задаётся как множество вершин и рёбер. Для сетевых задач рёбра могут иметь направление и веса:
- время;
- стоимость;
- риск;
- пропускную способность;
- задержку;
- вероятность;
- confidence loss.

## Методы, зафиксированные в пакете

| ID | Метод | Класс | Статус |
|---|---|---|---|
| GRAPH-SP-01 | Shortest Path | graph optimization | DISCOVERED |
| GRAPH-MST-01 | Minimum Spanning Tree | graph optimization | DISCOVERED |
| GRAPH-FLOW-01 | Maximum Flow / Minimum Cut | network optimization | DISCOVERED |
| GRAPH-TSP-01 | Travelling Salesman Problem | combinatorial optimization | DISCOVERED |
| GRAPH-CPM-01 | Critical Path Method | project network | DISCOVERED |
| GRAPH-PERT-01 | PERT | stochastic project network | DISCOVERED |
| GRAPH-GERT-01 | GERT | probabilistic network | DISCOVERED |

## FATHER-применение

### Shortest Path
Поиск минимального пути через цепочку действий, инструментов, API или источников.

### Maximum Flow
Поиск bottleneck, throughput и предельной пропускной способности между агентами, очередями, API, GPU, БД и storage.

### TSP
Оптимизация порядка обхода объектов, источников, задач, инспекций и маршрутов.

### CPM
Вычисление критического пути производственного процесса FATHER.

### PERT
Работа с неопределёнными сроками выполнения работ.

### GERT
Графы с вероятностными переходами, ветвлениями и возможными возвратами — особенно полезны для agent workflow.

## Qualification rule

Ни один метод не становится RUNNABLE только потому, что он описан в учебном материале.

Для RUNNABLE нужны:
1. авторитетный первичный/академический источник;
2. формализованный алгоритм;
3. код;
4. unit/contract tests;
5. граничные случаи;
6. benchmark/backtest;
7. паспорт метода.

## Источники discovery

- Пользовательский материал по теории графов, сетям и задаче коммивояжера.
- Пользовательский материал по СПУ, PERT и CPM.
- Studfile используется только как discovery/source-navigation слой и не заменяет authoritative source для квалификации метода.
