# AI BookCreator

**AI BookCreator** — веб-платформа для создания, редактирования и публикации книг с использованием искусственного интеллекта Google Gemini.

## 🚀 Возможности

- **Генерация контента с помощью AI**: Создавайте книги на основе краткого сюжета с помощью Google Gemini
- **Notion-подобный редактор**: Удобный блочный редактор для создания и редактирования книг
- **Витрина книг**: Публикуйте свои книги и делитесь ими с миром
- **Система комментариев и лайков**: Взаимодействуйте с другими авторами
- **Подписки и платежи**: Монетизация через подписки и дополнительные пакеты генераций
- **Челленджи и достижения**: Участвуйте в конкурсах и получайте награды

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
