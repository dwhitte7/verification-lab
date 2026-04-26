# ValidationConnectionProject
=======

A small Linux-based verification lab built in WSL Ubuntu to practice API testing, asynchronous workflow validation, traffic generation, and containerization.

## What this project does

This project includes:

- A small FastAPI service
- Robot Framework API tests
- An asynchronous job workflow that is polled until completion
- iPerf3 traffic generation with JSON result parsing
- A Dockerfile to run the API in a container
- A GitHub Actions workflow to run the API tests in CI

## Project structure

```text
.
├── app
│   └── main.py
├── tests
│   └── api.robot
├── results
├── requirements.txt
├── Dockerfile
├── parse_iperf.py
├── check_iperf.py
└── .github
    └── workflows
        └── api-tests.yml
