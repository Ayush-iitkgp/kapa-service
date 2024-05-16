# kapa-service

This repository contains the kapa.ai backend service. It is built on Django + DRF with celery and stores data in both Postgres and Weaviate. The service is composed of three main apps `Org`, `Query` and `Ingestion`. 

`Org` contains the data models needed to organize teams, users and projects (kapa instances). It handles token and API key based authentication as well as permissions.

`Query` contains the kapa RAG pipeline as well as all analytics functionality. 

`Ingestion` contains all knowledge source integrations and data ingestion logic.

## Getting Started

### Prerequisites

To get started with `kapa-service`, you need to install Docker and Docker Compose on your system

1. Clone `kapa-dev-workspace`:

```bash
git clone https://github.com/kapa-ai/kapa-dev-workspace
```

2. Clone `kapa-service` inside `kapa-dev-workspace`:

```bash
cd kapa-dev-workspace && git clone https://github.com/kapa-ai/kapa-service
```  

3. Open `kapa-dev-workspace` project in VS Code.

4. Make sure you have the Docker extension installed. If not, you can install it from the VS Code Marketplace.

5. Right-click on the `docker-compose.yaml` file and select `Compose Restart` from the context menu. This will start the containers specified in the `docker-compose.yaml` file.

6. Once the containers are running, you can attach a shell to the `kapa-service` container by right-clicking on the container in the Docker extension and selecting `Attach Shell`. You can find running container by clicking on the docker icon in the left side bar. You can also attach VS Code to the container (`CTRL` + `SHIFT` + `P`, `Dev Container: Attach to Running Container`).

### Set up Postgres and Weaviate

When you run `kapa-service` for the first time you need to execute multiple migrations to get the Postgres database ready. You also need to create a collection in Weaviate which holds all embeddings. Execute

```bash
make bootstrap
```  

### Create Superuser

Create yourself a super user for the Django admin panel

```bash
make create-superuser
```

## Local Development


### Running the service


To run the project locally, attach a shell to the `kapa-service` container and run:
  

```bash
make run
```

### Running tests

To run all tests execute

```bash
make test
```

To run a single test execute

```bash
make test <NAME OF TEST FILE>
```

### Migrations

To create new migrations for a model change execute

```bash
make create-migration
```

To apply migrations execute:
  
```bash
make migrate
```

### Admin panel

You can access the admin panel at `http://0.0.0.0:8003/admin` once the project is running. To be able to login you need to have created a superuser.