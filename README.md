# superkart-sales-prediction-app
SUperKart Sales Prediction — Containerized App

## Run the containers

Start the backend on `skapp-network` and expose port `7860`. In this Codespaces
Docker runtime, start the frontend with the host gateway route so it can reach
the published backend port:

```bash
docker run -d --name frontend \
	--network skapp-network \
	--add-host=host.docker.internal:host-gateway \
	-e BACKEND_URL=http://host.docker.internal:7860 \
	-p 8501:8501 frontend
```

The frontend is then available at `http://localhost:8501`.

Bash Commands (Week 2):

1. Remove old containers if they exist
bash
docker rm -f frontend backend 2>/dev/null || true


2. Create the Docker network if it does not exist
bash
docker network create rppapp-network 2>/dev/null || true


3. Build both images
bash
docker build -t frontend ./frontend
docker build -t backend ./backend


4. Start the backend container
bash
docker run -d --name backend --network rppapp-network -p 7860:7860 backend

[Wait till the "Open Browser" option is not shown]


5. Start the frontend container
bash
docker run -d --name frontend --network rppapp-network -p 8501:8501 frontend

[Wait till the "Open Browser" option is not shown]
