# crowd-counting-api
API using Phyton, FastAPI and NiceGUI for crowd counting analysis. [SOLID Principles]

- [x] Run uvicorn server `uvicorn app.main:app --reload` or `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## WSL Port Forwarding
- [x] Check WLS IP from WSL terminal: `ip addr show eth0`
- [x] Forward IP from CMD Windows 
```
- netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8000 connectaddress=172.21.131.76 connectport=8000

- netsh interface portproxy add v4tov4 listenaddress=127.0.0.1 listenport=8000 connectaddress=172.21.131.76 connectport=8000
```
- [x] Access from other devices in same network `http:192.168.xx.xx:8000`

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