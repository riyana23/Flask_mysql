How to run the app?

## Step1 Build the docker image
```sudo docker build . -t student_api:latest```

## Step2 Run the docker application
```sudo docker run --network host student_api:latest python app.py```
