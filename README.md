```markdown
# sbornik-vless

Автоматический сборщик подписок для протоколов **VLESS, VMess, Trojan, Shadowsocks, Hysteria, Hysteria2, HY2, TUIC**.

Репозиторий работает как «витрина готовых подписок»: GitHub Actions ежедневно собирает и проверяет конфигурации, разбивает их на части и публикует в виде RAW-ссылок, пригодных для подключения в любом клиенте.

---

## ⚠️ Дисклеймер

> Проект создан **исключительно в образовательных целях** — для изучения сетевых протоколов и принципов работы VPN.
>
> - Автор **не призывает** к нарушению законодательства.
> - Автор **не гарантирует** работоспособность конфигураций.
> - Все данные получены из **публичных источников**.
> - **Любое использование — на ваш собственный риск.**

---

## Как это работает

Каждый день в 03:00 UTC (06:00 МСК) запускается workflow `.github/workflows/sbornik-vless.yml`. Пайплайн состоит из трёх шагов.

### 1. Сбор и проверка — `main.py`

- Загружает актуальные конфигурации из публичных источников (`mirror.py`).
- Проверяет доступность узлов: DNS-резолвинг и TCP-коннект с агрессивными таймаутами.
- Сохраняет только валидные конфиги в `configs/final/`:

```
configs/final/vless.txt
configs/final/vmess.txt
configs/final/trojan.txt
configs/final/ss.txt
configs/final/hysteria.txt
configs/final/hysteria2.txt
configs/final/hy2.txt
configs/final/tuic.txt
```

### 2. Формирование подписок — `build_subscriptions.py`

- Читает `configs/final/*.txt`.
- Разбивает каждый протокол на части по `CHUNK_SIZE` строк (по умолчанию 1000).
- Кладёт чанки в `subs/`:

```
subs/vless_001.txt
subs/vless_002.txt
subs/vmess_001.txt
...
```

- Генерирует итоговый файл `subscriptions` со ссылками на RAW:

```text
=== VLESS ===
https://raw.githubusercontent.com/kort0881/sbornik-vless/refs/heads/main/subs/vless_001.txt
https://raw.githubusercontent.com/kort0881/sbornik-vless/refs/heads/main/subs/vless_002.txt

=== VMESS ===
https://raw.githubusercontent.com/kort0881/sbornik-vless/refs/heads/main/subs/vmess_001.txt
...
```

### 3. Фиксация изменений

Workflow коммитит `subscriptions` и `subs/` обратно в репозиторий. Так RAW-ссылки всегда указывают на актуальные файлы.

---

## Использование

### Для пользователей

1. Откройте файл [`subscriptions`](https://github.com/kort0881/sbornik-vless/blob/main/subscriptions).
2. Найдите блок нужного протокола (`=== VLESS ===`, `=== VMESS ===` и т.д.).
3. Скопируйте любую RAW-ссылку из блока, например:
   ```
   https://raw.githubusercontent.com/kort0881/sbornik-vless/refs/heads/main/subs/vless_001.txt
   ```
4. Вставьте её в клиент как URL подписки:
   - **Android**: v2rayNG, Hiddify, NekoBox
   - **iOS**: Shadowrocket, Streisand, FoXray
   - **Windows / macOS / Linux**: Clash, Hiddify, v2rayN

Клиент сам скачает список узлов и покажет их как обычные конфигурации.

### Для разработчиков

Локальный запуск:

```bash
git clone https://github.com/kort0881/sbornik-vless.git
cd sbornik-vless

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install requests

python main.py
python build_subscriptions.py
```

После запуска появятся `configs/final/*.txt`, `subs/*.txt` и `subscriptions`.

---

## Структура репозитория

```
.
├── .github/workflows/
│   └── sbornik-vless.yml     # CI: сборка и коммит подписок
├── configs/final/            # Проверенные конфиги по протоколам
├── subs/                     # Чанки подписок (по CHUNK_SIZE строк)
├── reports/                  # Отчёты о проверке (fast_report.txt)
├── githubmirror/             # Сырые зеркала и промежуточные файлы
├── main.py                   # Сбор и проверка узлов
├── mirror.py                 # Загрузка исходных конфигов
├── build_subscriptions.py    # Формирование чанков и subscriptions
└── subscriptions             # Итоговый список RAW-ссылок
```

---

## Настройка

### Лимит строк на подписку

Открой `build_subscriptions.py` и измени константу:

```python
CHUNK_SIZE = 1000
```

### Список источников

Источники задаются в `mirror.py` (список `URLS_BASE`) и могут дополняться через `config_sources.json` в корне репозитория — по одному URL на строку.

### Расписание запуска

Редактируется в `.github/workflows/sbornik-vless.yml`:

```yaml
on:
  schedule:
    - cron: "0 3 * * *"   # 03:00 UTC = 06:00 МСК
```

---

## FAQ

**Почему не все узлы рабочие?**  
Проверка отсеивает заведомо мёртвые хосты, но стабильность соединения зависит от вашего провайдера, региона и нагрузки на сервер. Список узлов обновляется ежедневно.

**Можно ли использовать ссылки для своего клиента/бота?**  
Да, `subscriptions` и `subs/*.txt` — это обычные RAW-файлы, доступные публично.

**Что делать, если подписка пустая?**  
Значит, на момент прогона ни один узел не прошёл проверку. Смотрите `reports/fast_report.txt`, там указано, сколько конфигов отсеялось и на каком этапе.

**Как добавить свой источник?**  
Добавьте URL в `config_sources.json` или в список `URLS_BASE` в `mirror.py`.

---

## Лицензия и правовая информация

Проект распространяется **исключительно в образовательных и исследовательских целях**. Автор не даёт гарантий, явных или подразумеваемых, и не несёт ответственности за любые последствия использования материалов репозитория.

Используя проект, вы подтверждаете, что:

- соблюдаете законодательство своей юрисдикции;
- не применяете материалы для противоправных действий;
- принимаете на себя всю ответственность за результат.
```

Это README. Кладёшь его в файл `README.md` в корне репозитория. **YAML-workflow — отдельный файл** `.github/workflows/sbornik-vless.yml`, его содержимое я присылал в предыдущем сообщении — это другой файл, не путай.
