# crowd-counting-api
API using Phyton, FastAPI and NiceGUI for crowd counting analysis. [SOLID Principles]

- [x] Run uvicorn server `uvicorn app.main:app --reload`

## Migrations
- [x] Generate: `alembic revision --autogenerate -m "deskripsi_migrasi"`
- [x] Deploy to Database `alembic upgrade head`

## Requirements
```
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
pydantic
python-jose
passlib[bcrypt]
pyjwt

# Training Dataset
torch 
torchvision 
numpy 
opencv-python 
matplotlib 
tqdm
```