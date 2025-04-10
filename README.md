# Python App Demo

## Setup
1. Create a Virtual Environment `python-app-demo`

```bash
conda create -n python-app-demo python==3.11.7
```

2. Use that environment

```bash
conda activate python-app-demo
```

3. Install `requirements.txt`

```bash
pip install -r requirements.txt
```

4. Building Dockerfile

Check Python images here
https://hub.docker.com/_/python/tags

Chosen version
```
3.11-slim
```

You can try if the image exists in Podman by

```bash
podman pull python:3.13-alpine
```

Check the images if it exists.

```bash
podman images
```
