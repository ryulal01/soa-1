# API Gateway

## Зона ответственности
API Gateway является центральной точкой входа в систему. Он маршрутизирует запросы от UI к соответствующим сервисам.

## Границы сервиса
- Принимает HTTP-запросы от UI.
- Перенаправляет запросы в сервисы пользователей, постов и аналитики.
- Логирует запросы.
- Не хранит данные, только проксирует их.

