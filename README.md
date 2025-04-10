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

5. Building the Docker Image

```bash
podman build -t python-app:v1 .
```

Check the new list of images

```bash
podman images
```

6. Run the image

This is not working as intended

```bash
podman run -p 8080:5000 python-app:v1
```

```bash
podman ps
```

```bash
podman exec -ti [CONTAINER_ID] sh
```

Install CURL if not available

```bash
apk update  # if the container is based on Alpine Linux
apk add curl  # if the container is based on Alpine Linux
apt update  # if the container is based on Debian or Ubuntu
apt install curl  # if the container is based on Debian or Ubuntu
```

```bash
curl http://127.0.0.1:5000/api/v1/healthz
```

Upon running the command above, we can see that the API is running, we can access the endpoints inside of the container but we cannot access it outside.

```bash
/ # curl http://127.0.0.1:5000/api/v1/healthz
{"status":"up"}
```

The reason is that only the local interface is exposed, answer
https://stackoverflow.com/questions/7023052/configure-flask-dev-server-to-be-visible-across-the-network

```
/ # curl http://127.0.0.1:5000/api/v1/healthz
{"status" : "up"}
/ #
/ # curl http://127.0.0.1:5000/api/v1/healthz
{"status" : "up" }
/ # ip a
1: Lo: <LOOPBACK, UP, LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
く
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
11: etho@if12: <BROADCAST, MULTICAST, UP, LOWER_UP, M-DOWN> mtu 1500 qdisc noqueue state UP link/ether 02:42:ac: 11:00:02 brd ff:ff:ff: ff: ff: ff inet 172.17.0.2/16 brd 172.17.255.255 scope global etho
valid_lft forever preferred_lft forever
/ # curl http://172.17.0.2:5000/api/v1/healthz
curl: (7) Failed to connect to 172.17.0.2 port 5000 after 0 ms: Could not connect to server / # curl http://localhost: 5000/api/v1/healthz
{"status" : "up" }
/ #
```

Modify `app.run`

```python
if __name__ == '__main__':
    app.run(host="0.0.0.0"
```


With the new changes build a new image with tag `v2`

```bash
podman build -t python-app:v2 .
```

```bash
podman run -p 8080:5000 python-app:v2
```

You can now access these endpoints in your browser or in Postman

```
http://127.0.0.1:8080/api/v1/details
http://127.0.0.1:8080/api/v1/healthz
```

## Registry and Personal Auth Token

Upon running `podman images` you can see all of the application images you have along with their different tags, an application image can have multiple tags so as time passes by it might get difficult deploying in an external system like K8S.

Hence we use Docker Registry

Like this
https://hub.docker.com/


1. Login to your account

2. Navigate to `Repositories` page and click `Create a repository` button

3. You can see this command to push your image to Docker Registry but before that.

```bash
docker push jcdiamantegcash/python-app-demo:tagname
```

4. Navigate to `Account Settings` -> `Personal Access Tokens` -> `Generate a new Token`

**Name:** Python-App
**Access Permissions:** Read & Write

5. You will see a `login` command, copy the token and login using that credentials.

Use this instead, paste the token in the password

```bash
podman login docker.io -u jcdiamantegcash
```

6. Tag the image to be pushed, and push the image to the Docker Repository

```bash
podman tag python-app:v2 jcdiamantegcash/python-app-demo:v2
```

Run this, code was copied from Docker Hub, replace `docker` with `podman`

```bash
podman push jcdiamantegcash/python-app-demo:v2
```