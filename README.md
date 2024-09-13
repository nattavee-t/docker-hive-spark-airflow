# Docker-Hive-Spark-Airflow

A Docker-based setup for running Apache Hive, Apache Spark, and Apache Airflow seamlessly. This project provides an integrated environment to perform data processing, scheduling, and analytics using Docker containers.

## Table of Contents
1. [About](#about)
2. [Announcements & Updates](#announcements--updates)
3. [Services](#services)
4. [Instructions](#instructions)
6. [Known Issues](#known-issues)

## About

This project combines Apache Hive, Apache Spark, and Apache Airflow within Docker containers, providing a ready-to-use environment for data processing, analysis, and orchestration. It allows users—whether beginners or experienced data engineers—to quickly set up and run their first ETL/ELT pipeline with minimal configuration.

## Announcements & Updates

**[2024-09-13]**
- Added multiple sections in README.
- Added Postgres init script and mount folder to container.

**[Upcoming]**: 
- Integration with Hadoop File System.

## Services
| Service                  | Version | Ports        |
|--------------------------|---------|--------------|
| pgAdmin                  | 8.11.0  | 8888         |
| Postgres                 | 13      | 5433         |
| Airflow with spark-providers | 2.10.0  | 8080 (webserver) |
| Spark                    | 3.5.2   | 8081         |
| Hive metastore                | 4.0.0   | 9083         |
| Hive                     | 4.0.0   | 10000, 10002 |

## Instructions

### Prerequisites

- Docker installed on your system. Check out how to install Docker [here](#https://docs.docker.com/engine/install/).
- [Docker Compose](#https://docs.docker.com/compose/install/) installed. However, if you've installed Docker Desktop, it should be included.
- (Optional) [Git](#https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your machine.

### Installation

1. **Clone the repository**:

Open terminal in your folder. Run the following command line.
```bash
git clone https://github.com/nattavee-t/docker-hive-spark-airflow.git
```

2. **Buiid Airflow extended image**:
```bash
cd docker-hive-spark-airflow
docker build -t airflow-spark-providers .
```

3. **Run Docker Compose**:
```bash
docker compose up -d
```
_Note: If you don'e want to run in backgroud, remove the option **-d**_

4. **Setup Connection on Airflow**:

On your browser, login to Airflow webserver on http://localhost:8080 with default user and password: **airflow**. Go to the tab **Admin>Connections** then add a new connection with the following config.

- Connection Id: postgres_docker
- Connection Type: Postgres
- Host: postgres
- Database: my_db
- Login: airflow
- Password: airflow

Save, then add another record for Spark connection.

- Connection Id: spark_default
- Connection Type: Spark
- Host: spark://spark
- Port: 7077

5. **(HOTFIX) Change warehouse folder permission**

Due to current [known issues](#known-issues), we will have to give permission to warehouse folder in Hive metastore service.

First, run the following command in termainal.
```bash
docker exec -it hive-metastore bash
```
Run the following command to give permission.
```bash
cd /opt/hive/data/
chmod -R 777 warehouse/
```

**(Optional) Use pgadmin to manage your Postgres database**

[pgAdmin](#https://www.pgadmin.org/) is an interface tool that allows users to manage their Postgres. To login to this service on the container, go to http://localhost:8888/. Login with: 

- user: **admin@example.com**
- password: **password**

## Known Issues
**Issue**: Any operation involving creating or renaming files in hive metastore can't be accomplished. This is due to permission issue or service not running on Hadoop file system (to be investigated)

**Hotfix**:
- Extra installation steps to give permission to folder(s)
- Config spark.master = local (executed in script)