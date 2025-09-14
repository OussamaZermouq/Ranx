FROM python:3.11

ADD * .

RUN pip install requests 
RUN pip install discord 
RUN pip install python-dotenv
RUN pip install requests-cache 
RUN pip install urllib3
RUN pip install py_hot_reload

CMD ["python", "bot.py"]
