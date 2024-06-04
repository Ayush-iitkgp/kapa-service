# kapa-interview-service

This repository contains a monolithic RAG application. This service is not real but it was written with the real `kapa.ai` system in mind. It is identical in its technologies used but it is much smaller in scale and all its core implementations have been replaced by dummy code to reduce external dependencies.

You can see some deployed examples of the real kapa [here](https://docs.kapa.ai/examples).

## Introduction

The project introduction and the problem statement can be found at [docs/problem_statement.md](docs/problem_statement.md)

## Solution
1. Set up the local development as described [here](https://github.com/Ayush-iitkgp/django-service/blob/dev/docs/problem_statement.md#local-development)
2. Modify and create new tables in the database. Shell into the `service` container. You can use the VSCode Plugin for docker for this. Simply right click on the service and click `Attach Shell`.
```
make migrate
```
3. Initialize the query_backfillstatus table with default values
```
make initialize-backfill-table
```


## TODO
1. Add test for the constraint that the thread would be classified in one of the labels defined in the associated class.
2. Check if the label constraint on the thread exist at the database level or at the application code level.
3. Add tests for thread classification service
4. Add tests for thread backfill service
5. Add test for backfill threads task
6. Add test for caching during the backfill thread task
7. Add test for v1/projects/<uuid:project_id>/labels endpoint to create, update and delete the labels
8. Add endpoint foe modifying the thread label by the user.
