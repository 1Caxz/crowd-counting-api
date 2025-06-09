# crowd-counting-api
API using Phyton, FastAPI and NiceGUI for crowd counting analysis. [SOLID Principles]

- [x] Run uvicorn server `uvicorn app.main:app --reload`

## Migrations
- [x] Generate: `alembic revision --autogenerate -m "initial migration"`
- [x] Deploy to Database `alembic upgrade head`

## Requirements
```
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
pydantic
pydantic-settings
python-jose
passlib[bcrypt]
pyjwt
alembic

# For data model
torch
python-multipart
pillow
opencv-python
matplotlib
torchvision
h5py
scipy
```