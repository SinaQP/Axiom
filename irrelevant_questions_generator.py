#!/usr/bin/env python3
"""
Irrelevant Questions Data Generator
Uses the existing DatasetGenerator to create irrelevant questions that users might ask
but are not relevant to the system's purpose.
Generates simple question format with only "question" field.
"""

import json
from main import DatasetGenerator

def generate_irrelevant_questions_data():
    """Generate irrelevant questions data using the existing DatasetGenerator"""
    
    # Create generator with settings for irrelevant questions
    generator = DatasetGenerator(
        dataset_filename="irrelevant_questions_dataset.csv",  # Keep CSV for processing
        samples_per_request=25,  # Good batch size for quality
        data_key="questions"
    )
    
    # Set up prompt template for irrelevant questions
    irrelevant_prompt = """
    {context} {count} سوال مختلف تولید کن که کاربران ممکنه بپرسن اما مربوط به سیستم نیست.

این سوالات می‌تونن شامل موارد زیر و حتی موضوعات بیشتری باشند:
    - سوالات فلسفی و وجودی
    - سوالات علمی و تئوری
    - سوالات مربوط به طبیعت و جهان
    - سوالات مربوط به آینده و تکنولوژی
    - سوالات مربوط به احساسات و روابط انسانی
    - سوالات مربوط به تاریخ و فرهنگ
    - سوالات مربوط به هنر و خلاقیت
    - سوالات مربوط به اخلاق و ارزش‌ها
    - سوالات مربوط به زندگی روزمره
    - سوالات مربوط به تخیل و داستان‌سرایی

    خروجی را فقط و فقط در فرمت JSON خالص ارائه بده (بدون markdown یا کد بلوک).
    کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
    {field_instructions}

    مثال فرمت خروجی:
    {{"{data_key}": [{{"question": "چرا آسمان آبی است؟"}}]}}

    هیچ متن اضافی، توضیح، یا کد بلوک قبل یا بعد از JSON قرار نده.
    فقط JSON خالص ارائه بده.
    """
    
    # Set up field instructions for simple question format
    irrelevant_fields = """
    هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
    مثال: {{"question": "چرا آسمان آبی است؟"}}
    فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
    """
        
    # Configure the generator
    generator.set_prompt_template(irrelevant_prompt, irrelevant_fields)
    
    # Set contexts for different types of irrelevant questions
    irrelevant_contexts = [
        # Philosophical contexts
        "در حال تفکر فلسفی",
        "در یک بحث وجودی",
        "در حال پرسش از معنای زندگی",
        "در یک گفتگوی عمیق",
        "در حال تأمل در طبیعت",
        
        # Scientific contexts
        "در حال مطالعه علمی",
        "در یک آزمایشگاه تخیلی",
        "در حال کشف اسرار جهان",
        "در یک کنفرانس علمی",
        "در حال تحقیق در مورد فضا",
        
        # Nature and universe contexts
        "در حال تماشای ستاره‌ها",
        "در یک جنگل اسرارآمیز",
        "در حال کوهنوردی",
        "در کنار دریا",
        "در حال تماشای طلوع آفتاب",
        
        # Future and technology contexts
        "در آینده‌ای دور",
        "در یک دنیای تکنولوژیک",
        "در حال تصور آینده",
        "در یک شهر هوشمند",
        "در حال سفر در زمان",
        
        # Human emotions and relationships contexts
        "در حال تجربه عشق",
        "در یک رابطه پیچیده",
        "در حال درک احساسات",
        "در یک موقعیت اجتماعی",
        "در حال رشد شخصی",
        
        # History and culture contexts
        "در یک دوره تاریخی",
        "در حال مطالعه فرهنگ‌ها",
        "در یک موزه باستانی",
        "در حال سفر به گذشته",
        "در یک تمدن قدیمی",
        
        # Art and creativity contexts
        "در حال خلق هنر",
        "در یک گالری نقاشی",
        "در حال نوشتن داستان",
        "در یک کنسرت موسیقی",
        "در حال تجربه خلاقیت",
        
        # Ethics and values contexts
        "در حال تصمیم‌گیری اخلاقی",
        "در یک موقعیت دشوار",
        "در حال درک ارزش‌ها",
        "در یک بحث اخلاقی",
        "در حال انتخاب بین خوب و بد",
        
        # Daily life contexts
        "در حال زندگی روزمره",
        "در یک صبح آرام",
        "در حال پیاده‌روی",
        "در یک کافه دنج",
        "در حال استراحت",
        
        # Imagination and storytelling contexts
        "در یک دنیای خیالی",
        "در حال داستان‌سرایی",
        "در یک ماجراجویی",
        "در حال رویاپردازی",
        "در یک قصه‌ی پریان"
    ]
    
    generator.set_contexts(irrelevant_contexts)
    
    # Set variety levels for different types of questions
    variety_levels = [
        "ساده",
        "متوسط", 
        "پیچیده",
        "عمیق"
    ]
    
    generator.set_variety_levels(variety_levels)
    
    # Set temperature range for creativity
    generator.set_temperature_range(0.9, 1.4)
    
    # Generate irrelevant questions data
    print("🚀 Starting Irrelevant Questions Data Generation...")
    print("📊 This will generate general, philosophical, and unrelated questions")
    print("🎯 Target: 1000 irrelevant questions")
    
    generator.run(
        total_samples=1000,  # 1000 questions total
        data_type="سوال نامربوط", 
        variety_parameter="پیچیدگی"
    )
    
    print("\n✅ Irrelevant questions data generation completed!")
    print("📁 Data saved to: irrelevant_questions_dataset.csv")


def generate_simple_test_dataset():
    """Generate a simple test dataset with just irrelevant questions"""
    
    generator = DatasetGenerator(
        dataset_filename="test_irrelevant_questions.csv",
        samples_per_request=15,
        data_key="questions"
    )
    
    # Simple prompt for just irrelevant questions
    simple_prompt = """
{context} {count} سوال مختلف تولید کن که کاربران ممکنه بپرسن اما مربوط به سیستم نیست.

این سوالات می‌تونن شامل موارد زیر باشند:
- سوالات فلسفی و وجودی
- سوالات علمی و تئوری
- سوالات مربوط به طبیعت و جهان
- سوالات مربوط به آینده و تکنولوژی
- سوالات مربوط به احساسات و روابط انسانی

خروجی را فقط و فقط در فرمت JSON خالص ارائه بده.
کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
{field_instructions}

مثال فرمت خروجی:
{{"{data_key}": [{{"question": "چرا آسمان آبی است؟"}}]}}

فقط JSON خالص ارائه بده.
"""
    
    # Simple field instructions
    simple_fields = """
هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
مثال: {{"question": "چرا آسمان آبی است؟"}}
فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
"""
    
    generator.set_prompt_template(simple_prompt, simple_fields)
    
    generator.set_contexts([
        "در حال تفکر فلسفی",
        "در یک بحث علمی",
        "در حال تماشای طبیعت",
        "در حال تصور آینده",
        "در حال تجربه احساسات"
    ])
    
    generator.set_temperature_range(0.9, 1.3)
    
    print("🧪 Generating test dataset...")
    generator.run(total_samples=75, data_type="سوال نامربوط", variety_parameter="پیچیدگی")
    
    print("✅ Test dataset completed!")

def main():
    """Main function to run irrelevant questions data generation"""
    
    print("🤔 Irrelevant Questions Data Generator")
    print("=" * 50)
    print("This script generates general, philosophical, and unrelated questions")
    print("that users might ask but are not relevant to your system.")
    print("Output format: Simple JSON array of questions")
    print()
    
    # Ask user what they want to generate
    print("Choose an option:")
    print("1. Generate full dataset (1000 questions)")
    print("2. Generate a small test dataset (75 questions)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        generate_irrelevant_questions_data()
                
    elif choice == "2":
        generate_simple_test_dataset()          
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
