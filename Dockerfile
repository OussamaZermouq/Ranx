FROM python:3.11

ADD bot.py .

RUN pip install requests 
RUN pip install discord 
RUN pip install python-dotenv
RUN pip install requests-cache 
RUN pip install urllib3

CMD ["python", "bot.py"]

