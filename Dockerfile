FROM python:3.6
COPY src /app/src
WORKDIR /app/src
RUN pip install -r requirements.txt
ENV FLASK_APP=task.py
ENV FLASK_ENV=production
ENV DATABASE_URL=sqlite:////app/src/app.db
ENTRYPOINT ["flask","run", "--host=0.0.0.0"]
