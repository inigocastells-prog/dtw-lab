# matches the requires-python = ">=3.12,<3.13" constraint, slim keeps the image small
FROM python:3.12-slim

# sets the working directory (needed by /version which reads pyproject.toml from CWD)
WORKDIR /app

# copies only what's needed to install the package
COPY pyproject.toml .
COPY src/ src/

# installs the package and all dependencies, and registers the start-server script
RUN pip install .

# documents the port used by run_server_prod
EXPOSE 80

# runs the start-server entry point defined in pyproject.toml, which calls uvicorn on 0.0.0.0:80
CMD ["start-server"]