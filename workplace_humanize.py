#!/usr/bin/env python3
"""
Workplace Humanization Data Generator
Uses the existing DatasetGenerator to create workplace-specific humanization data
for different job roles and workplace scenarios.
Generates simple question format similar to humanize.json
"""

import json
from main import DatasetGenerator

def generate_workplace_humanize_data():
    """Generate workplace humanization data using the existing DatasetGenerator"""
    
    # Create generator with workplace-specific settings
    generator = DatasetGenerator(
        dataset_filename="workplace_humanize_dataset.csv",  # Keep CSV for processing
        samples_per_request=20,  # Smaller batches for better quality
        data_key="questions"
    )
    
    # Set up workplace-specific prompt template - simplified format
    workplace_prompt = """
    {context} {count} سوال مختلف تولید کن که یک  ممکنه در محیط کار با آن‌ها مواجه بشه.

این سوالات می‌تونن شامل موارد زیر و حتی موضوعات بیشتری باشند:
    - سوالات مربوط به کار و وظایف روزانه
    - سوالات مربوط به ارتباط با همکاران و مدیران
    - سوالات مربوط به مدیریت استرس و فشار کاری
    - سوالات مربوط به پیشرفت شغلی و یادگیری
    - سوالات مربوط به تعادل کار و زندگی شخصی
    - سوالات مربوط به چالش‌های تکنیکی و فنی
    - سوالات مربوط به تصمیم‌گیری و حل مشکل
    - سوالات مربوط به کار تیمی و همکاری

    خروجی را فقط و فقط در فرمت JSON خالص ارائه بده (بدون markdown یا کد بلوک).
    کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
    {field_instructions}

    مثال فرمت خروجی:
    {{"{data_key}": [{{"question": "چطور می‌تونم با استرس کار کنار بیام؟"}}]}}

    هیچ متن اضافی، توضیح، یا کد بلوک قبل یا بعد از JSON قرار نده.
    فقط JSON خالص ارائه بده.
    """
    
    # Set up field instructions for simple question format
    workplace_fields = """
    هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
    مثال: {{"question": "چطور می‌تونم با استرس کار کنار بیام؟"}}
    فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
    """
        
    # Configure the generator
    generator.set_prompt_template(workplace_prompt, workplace_fields)
    
    # Set workplace-specific contexts for different job roles
    workplace_contexts = [
        # Manager contexts
        "در یک جلسه مدیریتی",
        "در حال برنامه‌ریزی پروژه",
        "در حال ارزیابی عملکرد کارکنان",
        "در یک مذاکره تجاری",
        "در حال حل مشکل تیم",
        "در یک ارائه به هیئت مدیره",
        "در حال تصمیم‌گیری استراتژیک",
        "در یک جلسه توجیهی",
        "در حال مدیریت بحران",
        "در یک مصاحبه استخدامی",
        
        # Programmer contexts
        "در حال کدنویسی",
        "در یک جلسه کد ریویو",
        "در حال دیباگ کردن",
        "در یک جلسه تیم توسعه",
        "در حال طراحی معماری نرم‌افزار",
        "در حال تست کردن کد",
        "در یک جلسه اسکرام",
        "در حال مستندسازی کد",
        "در حال حل مشکل تکنیکی",
        "در یک جلسه آموزش تیم",
        
        # Sales contexts
        "در حال ارائه محصول",
        "در یک جلسه فروش",
        "در حال مذاکره قیمت",
        "در حال پیگیری مشتری",
        "در یک نمایشگاه تجاری",
        "در حال حل مشکل مشتری",
        "در یک جلسه توجیهی فروش",
        "در حال تحلیل بازار",
        "در حال برنامه‌ریزی فروش",
        "در یک جلسه با تیم فروش",
        
        # Accountant contexts
        "در حال تهیه گزارش مالی",
        "در یک جلسه حسابرسی",
        "در حال بررسی اسناد مالی",
        "در یک جلسه با مدیر مالی",
        "در حال تهیه بودجه",
        "در یک جلسه با مشاور مالیاتی",
        "در حال تحلیل صورت‌های مالی",
        "در یک جلسه توجیهی مالی",
        "در حال حل مشکل حسابداری",
        "در یک جلسه با بانک",
        
        # Teacher contexts
        "در حال تدریس",
        "در یک جلسه اولیا و مربیان",
        "در حال تصحیح امتحان",
        "در یک جلسه شورای معلمان",
        "در حال برنامه‌ریزی درسی",
        "در یک جلسه مشاوره دانش‌آموز",
        "در حال تهیه محتوای آموزشی",
        "در یک جلسه با مدیر مدرسه",
        "در حال حل مشکل کلاسی",
        "در یک جلسه آموزش ضمن خدمت",
        
        # Doctor contexts
        "در حال معاینه بیمار",
        "در یک جلسه کنفرانس پزشکی",
        "در حال مطالعه پرونده بیمار",
        "در یک جلسه با تیم درمانی",
        "در حال انجام عمل جراحی",
        "در یک جلسه با خانواده بیمار",
        "در حال نوشتن نسخه",
        "در یک جلسه آموزش پزشکی",
        "در حال حل مشکل درمانی",
        "در یک جلسه با مدیر بیمارستان",
        
        # Engineer contexts
        "در حال طراحی پروژه",
        "در یک جلسه مهندسی",
        "در حال نظارت بر ساخت",
        "در یک جلسه با پیمانکار",
        "در حال محاسبات فنی",
        "در یک جلسه با مشاور",
        "در حال تهیه نقشه",
        "در یک جلسه با کارفرما",
        "در حال حل مشکل فنی",
        "در یک جلسه با تیم مهندسی",
        
        # Secretary contexts
        "در حال پاسخگویی تلفن",
        "در یک جلسه برنامه‌ریزی",
        "در حال تنظیم قرار ملاقات",
        "در یک جلسه با مدیر",
        "در حال تهیه گزارش",
        "در یک جلسه با مراجعین",
        "در حال مدیریت تقویم",
        "در یک جلسه با تیم اداری",
        "در حال حل مشکل اداری",
        "در یک جلسه با کارمندان"
    ]
    
    generator.set_contexts(workplace_contexts)
    
    # Set variety levels for workplace scenarios
    workplace_variety_levels = [
        "کم",
        "متوسط", 
        "زیاد",
        "بسیار زیاد"
    ]
    
    generator.set_variety_levels(workplace_variety_levels)
    
    # Set temperature range for creativity
    generator.set_temperature_range(0.8, 1.3)
    
    # Generate workplace humanization data
    print("🚀 Starting Workplace Humanization Data Generation...")
    print("📊 This will generate questions for different job roles and workplace scenarios")
    print("🎯 Target: 800 workplace questions (100 per job role)")
    
    generator.run(
        total_samples=800,  # 800 questions total
        data_type="سوال کاری", 
        variety_parameter="چالش"
    )
    

    print("\n✅ Workplace humanization data generation completed!")
    print("📁 Data saved to: workplace_humanize_dataset.json")


def generate_simple_test_dataset():
    """Generate a simple test dataset with just questions"""
    
    generator = DatasetGenerator(
        dataset_filename="test_workplace_humanize.csv",
        samples_per_request=10,
        data_key="questions"
    )
    
    # Simple prompt for just questions
    simple_prompt = """
{context} {count} سوال مختلف تولید کن که یک فرد شاغل ممکنه در محیط کار با آن‌ها مواجه بشه.

این سوالات می‌تونن شامل موارد زیر و حتی موضوعات بیشتری باشند:
- سوالات مربوط به کار و وظایف روزانه
- سوالات مربوط به ارتباط با همکاران
- سوالات مربوط به مدیریت استرس
- سوالات مربوط به پیشرفت شغلی
- سوالات مربوط به تعادل کار و زندگی

خروجی را فقط و فقط در فرمت JSON خالص ارائه بده.
کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
{field_instructions}

مثال فرمت خروجی:
{{"{data_key}": [{{"question": "چطور می‌تونم با استرس کار کنار بیام؟"}}]}}

فقط JSON خالص ارائه بده.
"""
    
    # Simple field instructions
    simple_fields = """
هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
مثال: {{"question": "چطور می‌تونم با استرس کار کنار بیام؟"}}
فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
"""
    
    generator.set_prompt_template(simple_prompt, simple_fields)
    
    generator.set_contexts([
        "در یک جلسه کاری",
        "در حال حل مشکل",
        "در یک جلسه تیم",
        "در حال برنامه‌ریزی",
        "در حال ارائه گزارش"
    ])
    
    generator.set_temperature_range(0.8, 1.2)
    
    print("🧪 Generating test dataset...")
    generator.run(total_samples=50, data_type="سوال کاری", variety_parameter="چالش")
    
    # Convert to JSON
    print("✅ Test dataset completed!")

def main():
    """Main function to run workplace humanization data generation"""
    
    print("🏢 Workplace Humanization Data Generator")
    print("=" * 50)
    print("This script generates workplace-specific questions for chatbots")
    print("that can interact with different types of workers.")
    print("Output format: Simple JSON array of questions (like humanize.json)")
    print()
    
    # Ask user what they want to generate
    print("Choose an option:")
    print("1. Generate data for all job roles (800 questions)")
    print("2. Generate a small test dataset (50 questions)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        generate_workplace_humanize_data()
                
    elif choice == "2":
        generate_simple_test_dataset()
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
