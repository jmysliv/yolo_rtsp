# YOLO RTSP

This is a project for running a yolo object detection on a continuous stream of data read with the RTSP protocol
and sending the result data on an MQTT topic.

## Project structure

The project consists of:
* **app** - the application that analyzes the stream and detects objects using yolo library.
* **mosquitto** - an open source (EPL/EDL licensed) message broker that implements the MQTT protocol
* **server** - a simple flask server that displays detected objects
  
## Running the project

### Locally

```shell
docker-compose up
```

The flask page should be visible at port 8000.

### YOLO network

To use the YOLO object detection please place the following files in the `app/res/files` directory:
* https://pjreddie.com/media/files/yolov3.weights
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.cfg
* https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.txt


