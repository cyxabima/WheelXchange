from typing import Optional, Sequence
import uuid
from sqlmodel import desc, select
from . import schemas
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Cars


class CarService:
    async def get_all_cars(self, session: AsyncSession) -> Sequence[Cars]:
        statement = select(Cars).order_by(desc(Cars.created_at))
        result = await session.exec(statement)
        cars = result.all()
        return cars

    async def get_car(
        self, car_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[Cars]:
        statement = select(Cars).where(Cars.uid == car_uid)
        result = await session.exec(statement)
        car = result.first()  # this will either return None or Car Object
        return car

    async def create_car(
        self, car_data: schemas.CarCreateModel, session: AsyncSession
    ) -> Optional[Cars]:

        new_car = Cars(**car_data.model_dump())
        session.add(new_car)
        await session.commit()
        await session.refresh(new_car)
        return new_car

    async def edit_car(
        self, car_uid: uuid.UUID, car_update_data, session: AsyncSession
    ) -> Optional[Cars]:

        car = await self.get_car(car_uid, session)

        if not car:
            return None

        # as it is pydantic model and exclude_unset is to remove the none value so that cars remaining
        # attribute doest set to none
        update_car_dict = car_update_data.model_dump(exclude_unset=True)
        for key, value in update_car_dict.items():
            setattr(car, key, value)

        await session.commit()
        await session.refresh(car)

        return car

    async def delete_car(
        self, car_uid: uuid.UUID, session: AsyncSession
    ) -> Optional[dict]:
        car = await self.get_car(car_uid, session)
        if not car:
            return None
        await session.delete(car)
        await session.commit()

        return {"message": "car deleted successfully"}
