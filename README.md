# Angle Health E-Commerce Backend Project

To get this project up and running, simply run `docker compose up`. This will both build the image and start a container with the Django webserver running at `127.0.0.1:8000`.

## API

Two API endpoints have been implemented, as per the project requirements:

1. `<BASE_URL>/api/post/` for posting products (POST)
2. `<BASE_URL>/api/search/` for searching for products (GET)

## Known Limitations

### POST

1. Even though each request is an atomic transaction, all posted objects are processed when submitted (even after one fails to pass validation), which can be made more efficient by failing more quickly.

### SEARCH

1. `search` endpoint allows for extraneous URL params.
2. Pagination could improve search performance at scale.

### GENERAL

1. Unit tests can be written to more rigorously test the endpoints.

## Assumptions

For expediency, simplifying assumptions were made in building this project.

1. Negative prices are not allowed for products.
2. Empty lists are valid input for the `post` endpoint. No objects will be created.
3. Django admin is not yet required; can be configured easily.
