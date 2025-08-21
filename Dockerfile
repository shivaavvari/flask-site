#stage 1 i need base image python 
from python:3.12.11-trixie

#stage 2 i need a folder to save my code

workdir /app

#stage 3 i need to copy the dependency file
 
copy requirements.txt .
#RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
 #   apt-get install -y build-essential python3-dev && \
  #  rm -rf /var/lib/apt/lists/



#stage 4 run this dependency file 
run pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
#stage 5 copy the entire code
copy . .

#stage 6 expose the ports 

#expose 8000



#stage 7 Run the application 

CMD ["pytest", "test.py"]
