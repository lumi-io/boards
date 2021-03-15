FROM python:alpine3.7 
COPY . /app
WORKDIR /app
EXPOSE 80
ENV FLASK_APP=manage.py
RUN pip install pipenv
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt
CMD [ "flask", "run" ] 