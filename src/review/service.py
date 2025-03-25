from . import schemas, models
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

class ReviewService:

    async def create_review(self, 
                            review: schemas.ReviewCreateModel,
                            session: AsyncSession):
        """
        Creates a new review for a vendor (via a car).
        """
        # Check if customer exists
        result = await session.execute(select(models.Customers).where(
                                        models.Customers.uid == review.customer_id))
        customer = result.scalars().first()
        if not customer:
            return

        # Check if car exists and get its vendor
        result = await session.execute(select(models.Cars).where(
                                         models.Cars.uid == review.car_id))
        car = result.scalars().first()
        if not car:
            return 
        
        # check if already reviewed
        result = await session.execute(select(models.Reviews).where(
                                        models.Reviews.customer_id == review.customer_id,
                                        models.Reviews.car_id == review.car_id))
        is_reviewed = result.scalars().first()
        if is_reviewed:
            return 
                                        

        vendor_id = car.vendor_id  # ✅ Get vendor from car

        # Create a new review instance((
        review_data= review.model_dump()
        review_data["vendor_id"] = vendor_id  # ✅ Add vendor_id dynamically
        new_review = models.Reviews(**review_data)
            

        # Add to session and commit
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)

        return new_review

    async def edit_review(self,
                            review_uid: str,
                            edited_review,
                            session: AsyncSession):
    # Check if review exists
        result = await session.execute(
            select(models.Reviews).where(models.Reviews.uid == review_uid)
        )
        existing_review = result.scalars().first()
        
        if not existing_review:
            return None  # raise an HTTPException

        # Update fields that were set in edited_review
        update_review_dict = edited_review.model_dump(exclude_unset=True)
        for key, value in update_review_dict.items():
            setattr(existing_review, key, value)

        await session.commit()
        await session.refresh(existing_review)

        return existing_review
