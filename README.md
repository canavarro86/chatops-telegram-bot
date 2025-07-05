# ChatOps Telegram Bot

**Telegram-бот для управления GitHub Issues и CI/CD из чата по модели ChatOps**

---

## 📋 Описание

ChatOps Telegram Bot — это простой и расширяемый бот на Python, который позволяет:
- Получать список открытых Issue из репозитория GitHub  
- Создавать комментарии, назначать ответственных и управлять лейблами  
- Триггерить сборки и получать статусы из CI (GitHub Actions или Jenkins)  
- Отправлять ежедневные/еженедельные дайджесты по активности  
- Работать с безопасным хранением токенов через JWT  

Проект демонстрирует навыки DevOps-интеграции, Python-разработки, Docker и GitHub Actions.

---

## 🚀 Возможности

- **Интеграция с GitHub API**  
- **Интеграция с CI/CD API** (GitHub Actions / Jenkins)  
- **Команды бота**: `/start`, `/issues`, `/build <workflow>`, `/comment <#issue> <text>` и т.д.  
- **JWT-аутентификация** пользователей  
- **Docker + docker-compose** для локального запуска  
- **CI-pipeline**: линтинг, тесты, сборка образа в GitHub Actions  

---

## ⚙️ Технологии

- Python 3.11  
- [aiogram](https://docs.aiogram.dev/) или python-telegram-bot  
- GitHub REST API v3  
- JWT (PyJWT)  
- Docker, docker-compose  
- GitHub Actions  

---

## 📦 Предварительные требования

- Python ≥3.11  
- Docker & docker-compose  
- Аккаунт GitHub с правами на репозиторий  
- Telegram-бот (BotFather)  

---

## 🛠 Установка и настройка

1. **Клонируем репозиторий**  
   ```bash
   git clone git@github.com:YOUR_USERNAME/chatops-telegram-bot.git
   cd chatops-telegram-bot

2. **Создаём виртуальное окружение и устанавливаем зависимости**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3. **Копируем пример конфига и правим**
    ```bash
    cp config/config.yaml.example config/config.yaml
    ```

    В config/config.yaml задайте:
    ```yaml
    telegram_token: "ВАШ_TELEGRAM_TOKEN"
    github_token:  "ВАШ_GITHUB_TOKEN"
    jwt_secret:    "ВАШ_JWT_SECRET"
    github_repo:   "username/repo"
    ```


4. **Запускаем локально**
    ```bash
    docker-compose up --build
    ```

    или без Docker:
    ```bash
    python bot/main.py
    ```

5. **Проверяем бота**
    В Telegram отправьте /start — бот должен ответить приветствием.

🔧 **Использование**

    /issues — список открытых задач
    /build <workflow> — запустить указанный workflow
    /comment <#номер> <текст> — добавить комментарий к issue
    /assign <#номер> @user — назначить пользователя
    и др.

🧪 **Тестирование**

    ```bash
    source venv/bin/activate
    pytest --maxfail=1 -q
    ```

🔄 **CI/CD**
    Файл: .github/workflows/ci.yml

    Lint: flake8
    Tests: pytest
    Build: Docker image

🤝 Вклад

    1. Форкните репозиторий
    2. Создайте ветку feature/<имя>
    3. Внесите изменения и напишите тесты
    4. Сделайте PR в main



