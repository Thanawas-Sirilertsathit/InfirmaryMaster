## Installation Guide

1. Run these two commands

```bash
cd backend/infirmary_backend
cp sample.env .env
```

```bash
cd frontend
cp sample.env .env
```

In case you want to config anything else, you can config in .env file that we have copied.

2. Make sure your docker is running then run this command

```bash
docker-compose up --build
```

3. Access the web applications

- frontend at http://localhost:80
- backend at http://localhost:8000

4. In case you need admin user to verify the staff users, create one user by registering as patient whose username is Admin. After that running this command in the terminal.

```bash
docker compose exec -T db mysql -uinfirmary_user -p1234 infirmary_db -e "UPDATE users_user SET role='admin', verified=1, is_staff=1, is_superuser=1 WHERE username='Admin'; SELECT id, username, first_name, last_name, email, role, verified, is_staff, is_superuser FROM users_user WHERE username='Admin';"
```

5. How to stop the application

```bash
docker-compose down
```
