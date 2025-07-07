# ChatOps Telegram Bot

**Версия 0.1.0**

**Telegram-бот для управления GitHub Issues и CI/CD из чата по модели ChatOps**

---

## 📋 Описание

ChatOps Telegram Bot — это простой и расширяемый бот на Python, который позволяет:
- Получать список открытых Issue из репозитория GitHub  
- Добавлять комментарии к Issue  
- Запускать сборки и получать статусы из CI (GitHub Actions)  
- Управлять проектом, не выходя из Telegram  
- Использовать безопасное хранение токенов через JWT  

---

## 🗂 Структура проекта

```
.
├── bot/
│   ├── main.py
│   ├── handlers/
│   │   └── commands.py
│   └── services/
│       ├── github_api.py
│       └── ci_api.py
├── config/
│   ├── config.example.yaml
│   └── config.yaml
├── tests/
│   └── test_github_client.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Развёртывание и эксплуатация

### 1. Предварительные требования
- Python ≥3.11  
- Docker & docker-compose  
- Учетные данные:
  - Telegram Bot Token  
  - GitHub Personal Access Token  
  - JWT Secret  
  - `SETTINGS.github_repo` (формат `username/repo`)

### 2. Настройка конфигурации
1. Скопируйте пример конфига:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```
2. Откройте `config/config.yaml` и заполните поля:
   ```yaml
   telegram_token: "ВАШ_TELEGRAM_TOKEN"
   github_token:  "ВАШ_GITHUB_TOKEN"
   jwt_secret:    "ВАШ_JWT_SECRET"
   github_repo:   "username/repo"

   api:
     base_url: "https://api.github.com"
   timeout:
     telegram: 5
     github: 10
   ```

### 3. Локальный запуск через Docker
```bash
docker-compose up --build
```
- Сервис `bot` автоматически подхватит переменные из `.env`, если они заданы  
- Bot запускается в режиме long-polling: `skip_updates=True`  

### 4. Запуск без Docker
1. Создайте виртуальное окружение и активируйте:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите бота:
   ```bash
   python bot/main.py
   ```

### 5. Команды бота
- `/start` — приветствие  
- `/help` — список команд  
- `/issues` — получить список открытых Issue  
- `/comment <jwt> <номер> <текст>` — добавить комментарий к Issue  
- `/build <jwt> <workflow_id>` — запустить workflow  
- `/status <jwt> <workflow_id>` — получить статус последнего запуска  
- `/workflows` — список доступных workflows  

### 6. Тестирование
```bash
pytest --maxfail=1 -q
```

### 7. CI/CD
Файл: `.github/workflows/ci.yml`  
Шаги:
- flake8  
- pytest  
- docker build

---

## 🔜 В разработке

В следующих версиях планируется:
1. **Управление документами** в Telegram: загрузка, хранение и поиск файлов проекта.  
2. **Webhook + HTTPS**: переход на вебхуки для снижения задержек и повышения надёжности, с автоматическим получением SSL-сертификатов.  
3. **Метрики и мониторинг**: интеграция с Prometheus и построение дашборда Grafana для отслеживания производительности бота.  

---

*Спасибо за использование ChatOps Telegram Bot!*