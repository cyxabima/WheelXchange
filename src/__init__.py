from fastapi import Depends, FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.Dependencies import get_logged_user
from src.config import Config
from src.db.main import get_async_session, init_db
from src.users.routes import customer_router, vendor_router
from src.vehicles.routes import vehicles_router
from src.review.routes import review_router
from contextlib import asynccontextmanager
from src.booking_table.routes import booking_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server starts")
    await init_db()
    yield
    print("Server ends")


VERSION = "v1"
app = FastAPI(
    title="WheelXchange",
    version=VERSION,
    description="A Rest API for Vehicle Rental system or Market Place",
    lifespan=life_span,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(session: AsyncSession = Depends(get_async_session)):
    return {
        "title": "WheelXchange",
        "moto": "List. Rent. Ride. Repeat!",
        "subtitle": "Where Owners Earn & Renters Roll!",
        "DB_URI": Config.DB_URI,
    }


@app.get("/me")
async def me(user=Depends(get_logged_user)):
    return user


app.include_router(
    vehicles_router, prefix=f"/api/{VERSION}/vehicles", tags=["Vehicles"]
)
app.include_router(
    customer_router, prefix=f"/api/{VERSION}/customers", tags=["Customers"]
)
app.include_router(vendor_router, prefix=f"/api/{VERSION}/vendors", tags=["Vendors"])
app.include_router(review_router, prefix=f"/api/{VERSION}/reviews", tags=["Reviews"])
app.include_router(booking_router, prefix=f"/api/{VERSION}/booking", tags=["Booking"])
