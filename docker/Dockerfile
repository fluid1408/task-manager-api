# docker/Dockerfile
FROM continuumio/miniconda3:latest

WORKDIR /app

# Копируем environment.yml
COPY environment.yml .

# Создаем окружение из environment.yml
RUN conda env create -f environment.yml

# Активируем окружение в SHELL и добавляем в PATH
SHELL ["conda", "run", "-n", "task-api", "/bin/bash", "-c"]

# Копируем код (после установки зависимостей)
COPY . .

# Создаем non-root пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Запускаем приложение (указываем полный путь или активируем env)
CMD ["conda", "run", "--no-capture-output", "-n", "task-api", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]