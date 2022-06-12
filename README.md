## Requirements
1. Redis (version used 7.0.0)
2. ElasticMq (https://github.com/softwaremill/elasticmq)
3. Python (version used 3.8.9)

## Getting Started

1. Start Redis server
2. Start ElasticMq (queue name used is "process")
3. Clone the repo
4. Create Virtual env
5. use requirement.txt to install packages


        pip install -r requirement.txt

6. Start gunicorn server using following command


        export FLASK_ENV=dev; gunicorn --timeout 120 run:APP -b 0.0.0.0:8989 -w 1

7. Access API using 



        localhost:8989/api/crypto/sign?message=random

8. Sample Request and Response 

Request:

    curl -vH "User-Authorization:SYNTHESIA_DEMO" -XGET "http://localhost:8989/crypto/sign?message=abcde

Response (on success):

    [
        {
            "success": true, 
            "data": "d5RYxgxPG-A_mpsIyvNUvrEz5aZZBzNsER2F7Xl0VsvAtfHVMIsfpgGdoLMy35Uy17VzzwpRLg921gZxsG6GqkghX6d9O-OzB6cNay4-MnkSNfIFvut7GImb4d5g4FkHOazzINUMh0ln9EMI9eEyAwUoXDp48ABzen8VMLLs8QbyawK6Jk1HwfAuNWFBzMQCvNnr2MSrzYaGjS5StjEUasNnxs8cJjJhNmlDvlC3RuE1dBOo1T0RzcVXDdfbcgMCE1QMVV4edkNmJHvj9kIRaB4kOesnK8MbBAtBMs2p8C4weh-cX0_sUQ8TX16ecS3JIYdXEO6PeU9fasjZgKnZfw==", 
            "msg": "Messaged signed successfully"
        }
    ]

Response (on Failure):

    [
        {
            "success": true, 
            "data": "", 
            "msg": "Sit back and relax, You will get an email when your signed message is ready"
        }
    ]

9. Start workers (from repo root directory) to process queue data

        python3 workers/worker.py
## Authors

- [@sa35t](https://github.com/sa35t/)

