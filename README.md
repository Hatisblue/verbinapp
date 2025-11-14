# AI BookCreator

**AI BookCreator** — веб-платформа для создания, редактирования и публикации книг с использованием искусственного интеллекта Google Gemini.

## 🚀 Возможности

### ✅ Реализовано (FULL IMPLEMENTATION)

#### Backend API (100% готово)
- **Аутентификация**: JWT-токены, регистрация, вход, обновление токенов
- **Управление книгами**: CRUD операции, публикация, уровни доступа
- **Генерация контента**: Интеграция с Google Gemini для создания книг
- **Редактор блоков**: Notion-подобные блоки с drag-and-drop
- **Комментарии и лайки**: Полная система взаимодействия
- **Подписки и платежи**: Планы подписок, история платежей, интеграция с YooKassa
- **Челленджи**: Создание конкурсов, участие, определение победителей
- **Администрирование**: Модерация контента, управление пользователями, статистика
- **Рекомендации**: Персонализированные рекомендации книг
- **Уведомления**: Система уведомлений пользователей
- **Экспорт**: PDF экспорт с использованием ReportLab
- **Безопасность**: Rate limiting, CORS, валидация, модерация контента

#### Frontend (React + TypeScript)
- **Аутентификация**: Страницы входа и регистрации с валидацией
- **Витрина книг**: Отображение книг с фильтрацией и поиском
- **Редактор книг**: Создание и редактирование с блоками, генерация через AI
- **API клиенты**: Полная интеграция с backend через axios
- **Адаптивный дизайн**: Material-UI компоненты, светлая/темная тема

#### Инфраструктура
- **Docker Compose**: Полная контейнеризация (PostgreSQL, Redis, Backend)
- **База данных**: Полная схема с 15+ таблицами
- **Тестирование**: Базовые unit и integration тесты
- **Документация**: Swagger/OpenAPI автодокументация

## 📋 Требования

- Docker и Docker Compose
- Google Gemini API ключ (получить на https://makersuite.google.com/app/apikey)

## 🛠️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <your-repo-url>
cd verbinapp
```

### 2. Настроить переменные окружения

Скопируйте `.env.example` и создайте `.env`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите ваш `GEMINI_API_KEY`:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 3. Запустить приложение с помощью Docker Compose

```bash
docker-compose up --build
```

Приложение будет доступно по адресам:
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/api/docs
- **Frontend** (если раскомментировать в docker-compose.yml): http://localhost:3000

### 4. Остановить приложение

```bash
docker-compose down
```

## 📁 Структура проекта

```
verbinapp/
├── backend/                 # Backend на FastAPI
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   ├── db/             # База данных
│   │   ├── middleware/     # Middleware
│   │   └── utils/          # Утилиты
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Frontend на React + TypeScript
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы
│   │   ├── services/      # API клиенты
│   │   └── types/         # TypeScript типы
│   ├── public/
│   └── package.json
├── docker-compose.yml     # Docker Compose конфигурация
├── .env.example           # Пример переменных окружения
└── README.md              # Этот файл
```

## 🔧 Разработка

### Backend (FastAPI)

Запустить backend в режиме разработки:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (React)

Запустить frontend в режиме разработки:

```bash
cd frontend
npm install
npm start
```

## 📚 API Documentation

После запуска приложения, API документация доступна по адресу:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 🧪 Тестирование

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm test
```

## 🎯 Основные эндпоинты API

### Аутентификация
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `POST /api/auth/refresh` - Обновить токен
- `POST /api/auth/logout` - Выход

### Книги
- `GET /api/books` - Список книг
- `POST /api/books` - Создать книгу
- `GET /api/books/{id}` - Получить книгу
- `PUT /api/books/{id}` - Обновить книгу
- `DELETE /api/books/{id}` - Удалить книгу
- `POST /api/books/generate` - Сгенерировать книгу с помощью AI
- `POST /api/books/{id}/publish` - Опубликовать книгу

### Пользователи
- `GET /api/users/{id}` - Получить пользователя
- `GET /api/users/me` - Текущий пользователь
- `PUT /api/users/me` - Обновить профиль

## 🔐 Безопасность

- JWT аутентификация (Access + Refresh токены)
- Bcrypt для хеширования паролей
- CORS настроен для защиты от cross-origin атак
- SQL injection защита через параметризованные запросы
- XSS защита через санитизацию HTML

## 📝 Лицензия

MIT License

## 👥 Контакты

Email: support@bookgenerator.ru

---

**Версия:** 1.0.0 (MVP)
**Дата:** 14 ноября 2025
