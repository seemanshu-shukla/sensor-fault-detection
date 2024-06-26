# <p align="center"><ins>Sensor-Fault-Detection</ins></p>

## <ins>Problem Statement</ins>:
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class
indicates that the failure was caused by something else.

## <ins>Solution Proposed</ins>:
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.
## <ins>Tech Stack Used</ins>:
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## <ins>Infrastructure Required</ins>:

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform

## <ins>How to run?<ins>
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## <ins>Data Collections</ins>:
### Source Code-
```
https://github.com/seemanshu-shukla/sensor-fault-detection-big-data-pipeline
``` 
![image](https://user-images.githubusercontent.com/57321948/193536736-5ccff349-d1fb-486e-b920-02ad7974d089.png)


## <ins>Project Archietecture</ins>:
![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)


## <ins>Deployment Archietecture</ins>:
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)


## <ins>Setup Project Locally</ins>:
### Step 1: Clone the repository
```bash
git clone https://github.com/seemanshu-shukla/sensor-fault-detection.git
```

### Step 2- Create and activate a conda environment after opening the repository

```bash
conda create -n sensor python=3.7.6 -y
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Create .env file and set up following secrets
```bash
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

MONGODB_URL="<Your MongoDB connection key>"

```

### Step 5 - Run the application server
```bash
python main.py
```

### Step 6. Train application
```bash
http://localhost:8080/train

```

### Step 7. Prediction application
```bash
http://localhost:8080/predict

```

## <ins>Running project locally using Docker</ins>:

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> . 

```

3. Run the Docker image
```
docker run -d -p 8080:8080 <IMAGE_NAME>
```