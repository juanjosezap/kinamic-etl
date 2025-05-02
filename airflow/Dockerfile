FROM apache/airflow:2.7.1

USER root

# Install additional dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libglib2.0-0\               
    libnss3\                                     
    libnspr4\                                    
    libdbus-1-3\                                 
    libatk1.0-0\                                 
    libatk-bridge2.0-0\                          
    libcups2\                                    
    libdrm2\                                     
    libxcb1\                                     
    libxkbcommon0\                               
    libx11-6\                                    
    libxcomposite1\                              
    libxdamage1\                                 
    libxext6\                                    
    libxfixes3\                                  
    libxrandr2\                                  
    libgbm1\                                     
    libpango-1.0-0\                              
    libcairo2\                                   
    libasound2\                                  
    libatspi2.0-0 \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages for Scrapy and database connectors
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN playwright install

WORKDIR /opt/airflow