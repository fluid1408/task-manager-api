
FROM continuumio/miniconda3:latest

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "task-api", "/bin/bash", "-c"]

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["conda", "run", "--no-capture-output", "-n", "task-api", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]