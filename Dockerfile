# docker run -it --rm --name profilemaker -v $PWD:/code -w /code python:3.8.5-alpine3.12 /bin/sh

# First stage
FROM python:3.8.5-alpine3.12 AS builder
COPY requirements.txt .

# Install dependencies to the local user directory (eg. /root/.local)
RUN pip install --no-cache-dir --user --no-warn-script-location -r requirements.txt

# Second unnamed stage
FROM python:3.8.5-alpine3.12

RUN apk add --no-cache make bash

WORKDIR /code

# Copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local

# Update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Copy sources
COPY . .

RUN make create-project

EXPOSE 8000

# Run server
CMD [ "./project/manage.py", "runserver", "0.0.0.0:8000"]
