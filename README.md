# Image Search from Video

## To Run on local machine

### Activate the virtual environment
- For Windows
```
myenv/bin/activate
```
- For Mac
```
source myenv/bin/activate
```
### Or
### Install the Dependencies from requirement.txt
```
pip install -r requirements.txt
```
### Use the following command to start the local server
```
 uvicorn main:app --reload 
```
### Create a .env file 
with this variables QDRANT_URL, QDRANT_API_KEY and COLLECTION_NAME

### For API Docs 
- visit : http://localhost:8000/docs
- or http://localhost:8000/redocs
