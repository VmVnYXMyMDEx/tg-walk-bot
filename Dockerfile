FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "walk_bot.py"]  # Важно: имя файла должно совпадать с вашим скриптом!
