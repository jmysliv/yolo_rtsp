# YOLO RTSP

This is a project for running a yolo object detection on a continuous stream of data read with the RTSP protocol
and sending the result data on an MQTT topic.

## Project structure

The project consists of:
* **app** - the application that analyzes the stream and detects objects using yolo library.
  
For the system to work there needs to be exactly one instance of balancer and at least one instance of the app running.
## Running the project

### Locally

```shell
docker-compose up
python -m app
python -m server
```

### In Docker container

Use the files provided in the `docker` directory to build the container images.

For building on the arm64 architecture first use:
```shell
sudo apt install -y qemu-user-static binfmt-support
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx create --name profile
docker buildx use profile
docker buildx inspect --bootstrap
```
Build the balancer:
```shell
sudo docker buildx build --platform linux/arm64 -t tequilac/balancer -f docker/balancer/Dockerfile --push .
```
Build the app:
```shell
sudo docker buildx build --platform linux/arm64 -t tequilac/app -f docker/app/Dockerfile --push .
```

### On Kubernetes cluster

Use the files provided in the `deployment` directory.
Note that the images specified for the deployments were built for arm64 architecture.


### YOLO network

To use the YOLO object detection please place the following files in the `app/res/files` directory:
* https://pjreddie.com/media/files/yolov3.weights
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.cfg
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.txt


