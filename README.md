# NokiaOCR


## Getting Started


### Database Setup

If this is the first time you are setting up the project, you will need to initialize the database migrations. Follow these steps:

1. Access the web container:
    ```sh
    docker-compose exec web bash
    ```

2. Initialize the database migration folder:
    ```sh
    flask db init
    ```

3. Generate the initial migration:
    ```sh
    flask db migrate -m "Initial migration."
    ```

4. Apply the migration to the database:
    ```sh
    flask db upgrade
    ```

### Usage

```sh
docker-compose up
```

