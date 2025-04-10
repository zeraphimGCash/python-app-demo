# You can try if the image exists in Podman by
# podman pull python:3.11-slim

# Check the images if it exists.
# podman images
FROM python:3.13-alpine

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

COPY ./src src

CMD python /src/app.py