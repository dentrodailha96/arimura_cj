#image to download
FROM python:3.12

#Set where is the root of the project
WORKDIR /sushiproject

#Dependency of the project (Libraries necessary to the project) // . = current working directory
COPY requirements.txt .

#RUN Install the libraries necessary
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Define the port in which Flask will run
EXPOSE 80

# CMD start to run as soon as the image is created
CMD ["python3", "site.py"]