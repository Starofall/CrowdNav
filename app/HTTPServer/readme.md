In order to run the HTTP server:

pip install fastapi
pip install "uvicorn[standard]"
python -m uvicorn main:app --reload


after building the docker image: 

docker run -p 3000:5000 -it --link kafka:kafka <image-name>
"then access the port 3000"