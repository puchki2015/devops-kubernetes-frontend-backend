1. Go to desktop and create a folder devops-kubernetes-frontend-backend.
2. Create the Git Repo with the same name
3. Create a sample file readme.md
4. .git init
5. git add README.md
6. git commit -m "first commit"
7. git branch -M main
8. git remote add origin https://github.com/puchki2015/devops-kubernetes-frontend-backend.git
9. 

10. create a folder "api" under C:\Users\agniv\OneDrive\Desktop\devops-kubernetes-frontend-backend and cd api
11. uv init
12. uv venv 
13. venv\Scripts\activate
14. create a requirements.txt and add    
        qrcode
        fastapi
        uvicorn
        python-dotenv
        Pillow

15. Create the main.py file and run "uvicorn main:app --reload"

=====================

16. Now start working on the frontend which is next js application

17. Create a folder "front-end-nextjs" under C:\Users\agniv\OneDrive\Desktop\devops-kubernetes-frontend-backend and create the necessary files

========================

18. Dockerize the application, first dockerise fastapi application.

19. Create a dockerfile under C:\Users\agniv\OneDrive\Desktop\devops-kubernetes-frontend-backend\api

20. Now build the image , api first.

21. run the below command from C:\Users\agniv\OneDrive\Desktop\devops-kubernetes-frontend-backend\api

docker build -t <image_name> .

e.g docker build -t devops-qr-code-api .

22. Now build the image for front end.

23. run the below command from C:\Users\agniv\OneDrive\Desktop\devops-kubernetes-frontend-backend\front-end-nextjs


e.g docker build -t devops-qr-code-frontend .


===================

Now to test run those 2 docker images locally

first create container from api image

docker run -d --name <container_name> -p 8000:80 <image_name>


docker run -d --name <container_name> -p 8000:80 <image_name> ---->api

docker run -d --name <container_name> -p 8000:80 <image_name> ----> front end


e.g 

docker run -d --name devops-qr-api-container -p 8000:80 devops-qr-code-api

docker run -d --name devops-qr-frontend-container -p 3000:3000 devops-qr-code-frontend

now go to localhost:3000 to acccess the frontend and localhost:8000 to access backend


==============

Now go to hub.docker.com and create repo devops-qr-code-fronend and devops-qr-code-api


Now tag the images

a. docker tag devops-qr-code-api:latest puchki2015/devops-qr-code-api:latest

b. docker tag devops-qr-code-frontend:latest puchki2015/devops-qr-code-frontend:latest

Now do docker push

docker push puchki2015/devops-qr-code-api:latest

docker push puchki2015/devops-qr-code-frontend:latest


==============================

Now the coding part is done.
Next the CI/CD pipeline
SO when any changes will happen in any codebase like api.front end it will genearate a new image and pushed to dockethub
through github actions.

There is a file under .github\workflows named "build_docker.yaml" which takes care of it automatically

Just you have to create a Personal Access Token(PAT) through hub.docker.com --> Account Settings --> Personal Access Token

Now go to github.com--> go to the repo "devops-kubernetes-frontend-backend"--> Settings --> Secrets and Variables --> Actions-->
Add a repo secret with name of "DOCKER_HUB_TOKEN" and the value of PAT.

Now to test, make a small changes in any of the files and see the workflow will be triggered automatically





==========================

Now, we are trying to spin up a EKS cluster in AWS.

1. Install aws cli
2. run command--> aws configure, it will ask for access key and secret key
3. Create the cluster with below command

eksctl create cluster --name Anirban-test --region us-east-1 --nodegroup-name linux-nodes --node-type t3.micro --nodes 2


=============================

Now as we will be deploying the deployment and services in the EKS cluster , we need to make some changes in the frontend "page.js"

Development code:

try {
      const response = await axios.post(`http://localhost:8000/generate-qr?url=${url}`);


need to replace with actual service name deployed in EKS

try {
      const response = await axios.post(`/api/generate-qr?url=${url}`);


This page.js is client side code that is coming from browser and that would not translate to the backend server from the end user.
The end user dont access our internal k8s service/network.

So api route has been created under api/genearte-qr folder ( the same path has been mentioned in page.js client side).
So if any of the request comes in page.js (that is api/genearte-qr) will be forwarded to backend cluster dns name.
So DNS transaltion will happen at the server side that is frontend container which has access to backend container. so
the fronend request will properly go to backend container

 generate-qr is the api where fast api listens on






