from main import DatasetGenerator

# Example 1: Products (default)
def generate_products():
    generator = DatasetGenerator(
        dataset_filename="products_dataset.csv",
        samples_per_request=50
    )
    generator.run(total_samples=150)

# Example 2: Restaurants
def generate_restaurants():
    restaurant_prompt = """
{count} نام رستوران خلاقانه به همراه توضیح کوتاه (حدود ۲۰ کلمه) و لیستی از سه ویژگی کلیدی برای رستوران‌های جدید تولید کن.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
هر آبجکت باید شامل "restaurant_name", "description" و "features" باشند.
مقدار کلید "features" باید یک لیست از رشته‌ها باشد. هیچ متن اضافی قبل یا بعد از JSON قرار نده.
"""
    
    generator = DatasetGenerator(
        dataset_filename="restaurants_dataset.csv",
        samples_per_request=30,
        prompt_template=restaurant_prompt,
        data_key="restaurants"
    )
    generator.run(total_samples=100)

# Example 3: Books
def generate_books():
    book_prompt = """
{count} عنوان کتاب خلاقانه به همراه توضیح کوتاه (حدود ۲۰ کلمه) و لیستی از سه ویژگی کلیدی برای کتاب‌های جدید تولید کن.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
هر آبجکت باید شامل "book_title", "description" و "features" باشند.
مقدار کلید "features" باید یک لیست از رشته‌ها باشد. هیچ متن اضافی قبل یا بعد از JSON قرار نده.
"""
    
    generator = DatasetGenerator(
        dataset_filename="books_dataset.csv",
        samples_per_request=25,
        prompt_template=book_prompt,
        data_key="books"
    )
    generator.run(total_samples=75)

# Example 4: Movies
def generate_movies():
    movie_prompt = """
{count} عنوان فیلم خلاقانه به همراه توضیح کوتاه (حدود ۲۰ کلمه) و لیستی از سه ویژگی کلیدی برای فیلم‌های جدید تولید کن.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
هر آبجکت باید شامل "movie_title", "description" و "features" باشند.
مقدار کلید "features" باید یک لیست از رشته‌ها باشد. هیچ متن اضافی قبل یا بعد از JSON قرار نده.
"""
    
    generator = DatasetGenerator(
        dataset_filename="movies_dataset.csv",
        samples_per_request=20,
        prompt_template=movie_prompt,
        data_key="movies"
    )
    generator.run(total_samples=60)

if __name__ == "__main__":
    # Uncomment the function you want to run:
    # generate_products()
    # generate_restaurants()
    # generate_books()
    # generate_movies()
    
    print("Examples ready! Uncomment the function you want to run.") 