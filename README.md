# Kinamic ETL

A Scrapy-based web scraping solution with Apache Airflow orchestration for crawling and extracting artwork data from [http://pstrial-2019-12-16.toscrape.com/browse/](http://pstrial-2019-12-16.toscrape.com/browse/)

## Project Structure
---------------

The project consists of the following directories and files:

* `dags/`: Contains the Airflow DAGs (Directed Acyclic Graphs) for workflow orchestration.
	+ `scrapy_dag.py`: The DAG for running the Scrapy spider.
* `scrapinghub/`: Contains the Scrapy project files.
	+ `spiders/`: Contains the Scrapy spiders.
		- `artwork_spider.py`: The spider for crawling artwork data.
	+ `items.py`: Defines the Scrapy items for artwork data.
	+ `pipelines.py`: Defines the Scrapy pipelines for processing artwork data.
	+ `settings.py`: Contains the Scrapy project settings.
* `docker-compose.yml`: Defines the Docker services for the project.
* `requirements.txt`: Lists the Python dependencies for the project.
* `README.md`: This file.


## Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/juanjosezap/kinamic-etl.git
   cd kinamic-etl
   ```

2. **Python Environment Setup**
   ```bash
   python3.11 -m venv py311
   source py311/bin/activate  # Linux/MacOS
   # py311\Scripts\activate  # Windows
   pip install -r airflow/requirements.txt
   ```

3. **Docker Setup with Automation Scripts**
   ```bash
   # Make scripts executable
   chmod +x setup.sh cleanup.sh

   # Start containers
   ./setup.sh

   # When finished, clean up resources
   ./cleanup.sh
   ```


### Running Spider Directly

To run the Scrapy spider directly, use the following command:
```bash
scrapy crawl artworkspider 
```
This will crawl the artwork data and save it to the MySQL database.
Add `-O output.csv` to export the data into a `csv` file.

### Airflow Orchestration

To run the Scrapy spider using Airflow orchestration, follow these steps:

1. Access the Airflow UI at [http://localhost:8080](http://localhost:8080).
2. Enable the `artwork_scraping_pipeline` DAG.
3. Monitor the runs through the Airflow interface.

### MySQL Configuration

The MySQL database configuration is as follows:

* Host: `mysql`
* Port: `3306`
* Database: `scrapinghub_db`
* User: `root`
* Password: `rootpassword`

## Docker Services
--------------

The project uses the following Docker services:

| Service       | Port    | Description                  |
|---------------|---------|------------------------------|
| Airflow Web   | 8080    | Airflow web interface        |
| MySQL         | 3306    | Database service             |
| Airflow Worker| 8793    | Celery worker                |

## Database Schema
The project uses the following database schema:

### Table: artworks
The following columns are used to store artwork data:

| Column Name   | Type            | Description                                |
|---------------|-----------------|--------------------------------------------|
| id            | INT             | Primary key                                |
| url           | VARCHAR(255)    | URL of the artwork                         |
| artist        | VARCHAR(255)    | Artist name                                |
| title         | VARCHAR(255)    | Artwork title                              |
| description   | TEXT            | Artwork description                        |
| image         | VARCHAR(255)    | URL to artwork image                       |
| categories    | VARCHAR(255)    | Artwork categories                         |
| price         | DECIMAL(10, 2)  | Artwork price                              |
| dated         | VARCHAR(50)     | Artwork dated                              |
| date_added    | VARCHAR(50)     | Date artwork was added                     |
| location      | VARCHAR(50)     | Artwork location                           |
| width         | DECIMAL(10, 2)  | Artwork width                              |
| height        | DECIMAL(10, 2)  | Artwork height                             |
| medium        | VARCHAR(100)    | Artwork medium                             |
| dimensions    | VARCHAR(255)    | Artwork dimensions                         |
| created_at    | TIMESTAMP       | Timestamp when artwork was created         |
| updated_at    | TIMESTAMP       | Timestamp when artwork was updated         |

### Running Streamlit Application

To run the Streamlit application for visualizing the artwork data, use the following steps:

1. **Run Streamlit Application**

   Execute the Streamlit application with the following command:
   ```bash
   streamlit run streamlit/scrapinghub.py
   ```

2. **Access the Application**

   Open your web browser and go to [http://localhost:8501](http://localhost:8501) to access the Streamlit application interface and interact with the visualizations.

## Acknowledgments
--------------

* Scrapy community for robust web scraping framework
* Apache Airflow for workflow orchestration
* Docker for containerization solutions