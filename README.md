# Pokemon Scouting App

## Description

This repository contains the backend api that allows users to retrieve information for
various pokemons. It utilizes the [pokeapi](https://pokeapi.co) as the primary source
of information and caches the responses on a local database for future reference.

## Endpoint

The application consists on only one simple endpoint. Here's the details:

- **GET /api/v1/pokemons?name={pokemonName}**

  This endpoint receives a pokemon name and calls the underlying pokeapi to retrieve
  the related information for the inputted pokemon. At first, it tries to find the data
  in the database and if it can't find it, it calls the api and stores the results for
  future calls.

  This is how the response looks like:

  ```json
  {
    "abilities": ["hyper-cutter", "shell-armor", "sheer-force"],
    "base_experience": 166,
    "id": "067e01c2-48be-72e6-8000-64d2ad4346aa",
    "name": "kingler",
    "weight": 600
  }
  ```

## How to run the project

If you don't have it already, you need to install
[docker and docker compose](https://docs.docker.com/engine/install/) in order to run
the project locally or deploy it into the cloud.

Also, if you have the `make` command available (via build-essential) in your system's
PATH it would be of great help to avoid typing down long commands, but it's optional.

Its also worth mentioning that in order to run the next commands as-is, you need to make
sure that you are in a unix-like OS, because the docker-compose file uses the `/tmp/`
directory to store the local sqlite database as a docker volume. In case that you aren't
in a unix-like OS, you can edit [this file](./docker/staging/docker-compose.yaml) on the
`volumes` section and change the path to one of your choosing.

### Running the server

To run the server locally, open up your terminal inside this project's directory and run
the following command:

```bash
$ docker compose -f docker/staging/docker-compose.yaml up
```

Or this one if you have `build-essential` installed

```bash
$ make up
```

Now, open up your preferred http client and start making pokemon scouting calls!

Once you are finished with the local and manual tests you can run the following command
to stop the server:

```bash
$ docker compose -f docker/staging/docker-compose.yaml down --volumes --rmi all
```

Or this one if you have `build-essential` installed

```bash
$ make down
```

In addition, `make down` will also remove the images that were just built to avoid
occupying your machine's disk space.

### Running tests

This project leverages pytest and docker to run the test suite, should it be locally or
into the cloud.

To run the test suite locally, you can run the following docker commands:

```bash
# Builds the test image
$ docker build -t pokemon-scouting-testing --file docker/testing/Dockerfile .

# Runs the container with the test suite and removes it afterwards
$ docker run --rm pokemon-scouting-testing

# Removes the newly built testing image
$ docker rmi pokemon-scouting-testing
```

Or, as mentioned before, if you have the `make` cli command available (via build-essential)
you can simply:

```bash
$ make test
```

## Video Link

Bellow you can find the google driver folder to the code explanation as well as
instructions on how to run the project:

[https://drive.google.com/file/d/1c7vH03ebMlvOuC18z9Jof2yLRaR4dGD0/view?usp=sharing](https://drive.google.com/file/d/1c7vH03ebMlvOuC18z9Jof2yLRaR4dGD0/view?usp=sharing)
