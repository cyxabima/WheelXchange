from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
import uuid
from src.db.models import Reviews, Cars
from sqlmodel import select
from pydantic import EmailStr
from src.booking_table.service import BookingService
from src.users.service import CustomerService, VendorService
from src.vehicles.service import CarService
from typing import Sequence
from src.db.models import Customers, Vendors

admin_password = Config.ADMIN_PANEL_PASSWORD
admin_name = Config.ADMIN_NAME


class AdminService(CustomerService, VendorService, CarService):
    async def login_admin(
        self,
        password: str,
        session: AsyncSession,
    ):

        if password != admin_password:
            return

        return {"message": f"Welcome {admin_name} to Admin Panel!"}

    async def delete_review(
        self,
        review_uid: uuid.UUID,
        session: AsyncSession,
    ):
        """
        Delete the any review of any customer
        """
        statement = select(Reviews).where(
            Reviews.uid == review_uid,
        )
        result = await session.exec(statement).first()
        if not result:
            return
        await session.delete(result)
        await session.commit()
        return {"message": "review deleted successfully"}

    async def get_all_cars(self, session: AsyncSession) -> tuple[Sequence[Cars], int]:
        cars = await super().get_all_cars(session)  # call parent
        total_cars = len(cars)
        return cars, total_cars

    async def get_all_customers(self, session: AsyncSession):
        all_customers = await super().get_all_users(Customers, session)
        total_customers = len(all_customers)
        return all_customers, total_customers

    async def get_all_vendors(self, session: AsyncSession):
        all_vendors = await super().get_all_users(Vendors, session)
        total_vendors = len(all_vendors)
        return all_vendors, total_vendors

    async def delete_account(self, user_email: EmailStr, session: AsyncSession):
        vendor = await self.get_vendor_by_email(user_email, session)
        if not vendor:
            customer = await self.get_customer_by_email(user_email, session)
            if not customer:
                return
            await session.delete(customer)
            await session.commit()
            return 200

        await session.delete(vendor)
        await session.commit()
        return 200
