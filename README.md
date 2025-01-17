FastApi + SQLite апи для хранения заметок.

Как использовать Docker:
Создать образ:

`docker build -t notes-api .`

Запустить контейнер:

`docker run -d -p 8000:8000 notes-api`

Теперь API будет доступно по адресу http://localhost:8000

Как использовать API:
Создать заметку (POST /notes/):

`curl -X POST "http://localhost:8000/notes/" -H "Content-Type: application/json" -d '{"title":"Заголовок","content":"Содержание"}'`
Получить все заметки (GET /notes/):

`curl "http://localhost:8000/notes/"`
Получить заметку по ID (GET /notes/{id}):

`curl "http://localhost:8000/notes/1"`
Обновить заметку (PUT /notes/{id}):

`curl -X PUT "http://localhost:8000/notes/1" -H "Content-Type: application/json" -d '{"title":"Новый заголовок","content":"Новое содержание"}'`
Удалить заметку (DELETE /notes/{id}):

`curl -X DELETE "http://localhost:8000/notes/1"`

Также вы можете использовать автоматическую документацию API по адресу http://localhost:8000/docs, где можно тестировать все эндпоинты через веб-интерфейс.

Все тесты проходит успешно:)
![image](https://github.com/user-attachments/assets/991b19e0-4c82-49a8-804a-abde5e316fca)

