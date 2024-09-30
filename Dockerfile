FROM python:3.11

ADD bot.py .

RUN pip install requests discord dotenv requests-cache urllib3

CMD ["python", "bot.py"]

