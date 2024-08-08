Exchange Rates Project

This project is a Flask web app using a MySQL database, containerized with Docker.

Before you start, make sure you have these tools installed:

    Docker
    Docker Compose

setup and start 
    Build and start the containers: 

    docker-compose up --build

To access the MySQL database inside the container:
    Get the container ID:

    docker ps

Connect to the MySQL container: 

    docker exec -it <container ID> mysql -u root -p

Enter the root password when asked.

Export the database
The database information is in the config file.
To export the database using mysqldump:

     docker exec -it $(docker-compose ps -q db) sh -c 'mysqldump -u root -p exchange_rates_db' > backup.sql

Import the data
    Copy the backup file into the container: 
    
    docker cp backup.sql $(docker-compose ps -q db):/backup.sql


Useful Commands
    Stop the containers: 

    docker-compose down
    
Rebuild the containers: 

    docker-compose up --build