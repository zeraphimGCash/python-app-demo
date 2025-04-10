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

7. Using `Kind`

https://kind.sigs.k8s.io/

Setup
https://kind.sigs.k8s.io/docs/user/quick-start/


This is the command I followed for MacOS, Apple Silicon

```bash
brew install kind
```

```bash
kind create cluster
```

Check if hte kind cluster container was made

```bash
podman ps
```

Typically looks like this

```bash
e94612b5426e  docker.io/kindest/node@sha256:f226345927d7e348497136874b6d207e0b32cc52154ad8323129352923a3142f                        38 seconds ago  Up 38 seconds  127.0.0.1:59849->6443/tcp  kind-control-plane
```

8. Installing Kubectl

9. Basic Kubectl commands

```bash
kubectl version

kubectl get pods

kubectl cluster-info

kubectl get ns

```

Upon running `kubectl get ns` and `podman ps` you should see these results.

```bash
zeraphim ~/Desktop/python-app (main) ± 1 > kubectl get ns
NAME                 STATUS   AGE
default              Active   4h
kube-node-lease      Active   4h
kube-public          Active   4h
kube-system          Active   4h
local-path-storage   Active   4h
zeraphim ~/Desktop/python-app (main) ± 1 > podman ps
CONTAINER ID  IMAGE                                                                                           COMMAND               CREATED      STATUS      PORTS                      NAMES
ff36cc5c3dc7  localhost/python-app:v2                                                                         /bin/sh -c python...  7 hours ago  Up 7 hours  0.0.0.0:8080->5000/tcp     cool_hodgkin
e94612b5426e  docker.io/kindest/node@sha256:f226345927d7e348497136874b6d207e0b32cc52154ad8323129352923a3142f                        7 hours ago  Up 7 hours  127.0.0.1:59849->6443/tcp  kind-control-plane
```

10. Installing `Kind` Ingress

https://kind.sigs.k8s.io/docs/user/ingress/

Paste this in terminal to create `Kind` cluster

For DOCKER

```yaml
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

For PODMAN
```yaml
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

**Note:** If there's an existing `Kind` cluster, delete it first.

```bash
kind delete cluster
```

To use the `Kind` cluster

```bash
kubectl cluster-info --context kind-kind
```

To deploy an ingress controller

```bash
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
```

```bash
kubectl get pods -n ingress-nginx
```

Cant follow from here
https://www.udemy.com/course/from-devops-to-platform-engineering-master-backstage-idps/learn/lecture/49124395#overview

## K8S

**NOTE:** Can't run these commands, probably will work if `Kind` is working already

1. Creating `deploy.yaml` and `service.yaml`

For **DEPLOYMENT**
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

For **SERVICE**
https://kubernetes.io/docs/concepts/services-networking/service/

2. Apply `deploy.yaml`

```bash
kubectl apply -f k8s/deploy.yaml
```

3. Get Deployments

```bash
kubectl get deployments
```

## Accessing with Browser

## Bonus

It's very common to access applications on kubernetes via Ingress, as we just learned.

It's also very common to assign DNSs to these applications. For example, it is nice to access `http://python-app.example.com/api/v1/healthz` instead of just `http://localhost/api/v1/healthz`.

Following this logic, we would like to access our newly deployed application at `http://python-app.test.com/api/v1/healthz`.

## Helm

Delete `K8S` yaml files before using `Helm`

```bash
cd ~/python-app/k8s
 
# Delete the ingress
kubectl delete -f ingress.yaml
 
# Delete the service
kubectl delete -f service.yaml
 
# Delete the deployment
kubectl delete -f deploy.yaml
```

Installing `Helm`

https://helm.sh/docs/intro/install/

```bash
brew install helm
```

Check `Helm` version

```bash
helm version
```

