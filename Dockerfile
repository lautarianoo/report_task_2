FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /code
WORKDIR /code

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy local project
COPY . /code/

# Expose port 8000
EXPOSE 8080

# Use gunicorn on port 8000
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "report_task_2.wsgi"]