# pull python base image
FROM python:3.10-slim

# set work directory
WORKDIR /app

# copy project
COPY . /app

# install dependencies
# Assuming requirements.txt is in the root, if it's elsewhere, adjust the path.
RUN pip install --no-cache-dir -r requirements/requirements.txt


# expose port
EXPOSE 8000

# run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]