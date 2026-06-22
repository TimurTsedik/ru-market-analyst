# Заготовка для подачи в awesome-списки

Цель — попасть в часто-крауленные кураторские списки. Это лучший единичный рычаг
discoverability для skill-репо (их же активно цитируют LLM при вопросах «какие есть
Claude-скиллы для X»).

> ⚠️ Перед PR **открой `CONTRIBUTING.md` целевого репо** — формат строки, раздел,
> алфавитный порядок и требования к описанию у каждого списка свои. Ниже — заготовки;
> подгони под их шаблон.

## Готовая строка-entry (подгони формат под список)

```md
- [RU Market Analyst](https://github.com/TimurTsedik/ru-market-analyst) - Skill suite for end-to-end Russian bond portfolio analysis: parses broker statements (Tinkoff/Alfa/Sber), researches instruments on cbonds, builds risk buckets, duration & tax (IIS/LDV) analysis, and outputs a verified swap plan.
```

RU-вариант (для русскоязычных списков):

```md
- [RU Market Analyst](https://github.com/TimurTsedik/ru-market-analyst) — набор скиллов Claude Code: сквозной разбор портфеля облигаций РФ (парсинг отчётов ТБанк/Альфа/Сбер, ресёрч на cbonds, риск-корзины, дюрация, налоги ИИС/ЛДВ, план замен).
```

## Куда подавать (проверь актуальность и формат)

| Список | Репозиторий (проверь, что живой) | Раздел-кандидат |
|---|---|---|
| awesome-claude-code | `hesreallyhim/awesome-claude-code` | Skills / Workflows |
| awesome-claude-skills | поиск по GitHub `awesome claude skills` | Finance / Domain skills |
| awesome-claude (general) | поиск `awesome claude` | Tools / Skills |
| awesome-ai-agents | `e2b-dev/awesome-ai-agents` и аналоги | Domain-specific / Finance |

## Шаги (типовой flow awesome-PR)

1. Форкни целевой репо.
2. Прочитай `CONTRIBUTING.md` — формат строки, нужный раздел, алфавитный порядок.
3. Добавь entry в нужную секцию (часто строго по алфавиту).
4. Если есть линтер/скрипт (`npm run lint`, `make`) — прогони.
5. Коммит → PR. В описании PR: одна строка что это + почему уместно в этом списке.
6. Будь готов к правкам мейнтейнера по формату описания.

## Мини-чеклист качества (что смотрят кураторы)

- [x] У репо есть **описание** и **topics** (уже проставлено).
- [x] Есть **LICENSE** (MIT).
- [x] README объясняет «что/для кого/как поставить» в первом экране.
- [ ] Есть хотя бы пара ⭐ и видимая активность (релиз/коммиты).
- [ ] Нет битых ссылок в README.
