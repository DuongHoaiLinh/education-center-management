FROM python:3.12
WORKDIR /app
# Cài đặt phụ thuộc hệ thống và ODBC driver
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    gnupg \
    g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install -y unixodbc-dev
# Nâng cấp pip
RUN pip install --upgrade pip
# Cài đặt pyodbc riêng biệt
RUN pip install pyodbc==5.2.0
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "education_center.wsgi:application", "--bind", "0.0.0.0:8000"]