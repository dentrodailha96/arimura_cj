#image to download (slim because it is smaller)
FROM python:3.12-slim

#Set where is the root of the project
WORKDIR /sushiproject

#Dependency of the project (Libraries necessary to the project) // . = current working directory
COPY requirements.txt .

#RUN Install the libraries necessary
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy app code LAST (rebuilds on every push, but pip is already cached)
COPY routes/ routes/
COPY sql/ sql/
COPY templates/ templates/
COPY site.py .

# CMD start to run as soon as the image is created
CMD ["python3", "site.py"]