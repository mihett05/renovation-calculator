# renovation-calculator

## Описание
Калькулятор для подсчёта стоимости отделки комнаты, на основе результатов парсинга ekonomstroy.ru.

## Технологии и библиотеки

### Backend
- PostgreSQL (asyncpg) - основная СУБД
- SQLAlchemy - ORM для работы с СУБД
- alembic - миграции для ORM
- FastAPI - веб-фреймворк для REST API
- Pydantic - библиотека для сериализации
- aiohttp - библиотека для асинхронных http запросов
- BeautifulSoup4 (lxml) - библиотека для парсинга html
- adaptix - библиотека для создания мапперов
- dishka - библиотека для Dependency Injection

### Frontend
- Vite - бандлер
- SWC - транспилятор для JSX
- Typescript - типизация для JS
- React - библиотека для UI
- Mantine - библиотека для стилизации и UI компонентов
- Redux ToolKit - библиотека для стейт менеджмента и запросов к API
- React Router - библиотека для роутинга SPA
- biome - линтер и форматер
- nginx - web-сервер для раздачи статики
