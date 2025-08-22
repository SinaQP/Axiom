#!/usr/bin/env python3
"""
Chatbot Training Data Generator About System
Uses the existing DatasetGenerator to create system-related questions for chatbot training.
Generates questions that users might ask about a system, similar to the provided example.
"""

import json
import pandas as pd
from main import DatasetGenerator

def generate_chatbot_training_data():
    """Generate chatbot training data with system-related questions"""
    
    # Create generator with chatbot-specific settings
    generator = DatasetGenerator(
        dataset_filename="chatbot_training_dataset.csv",  # Keep CSV for processing
        samples_per_request=25,  # Moderate batch size for quality
        data_key="questions"
    )
    
    # Set up system-specific prompt template
    system_prompt = """
    {context} {count} سوال مختلف تولید کن که کاربران ممکنه درباره سیستم بپرسند.

    این سوالات می‌تونن شامل موارد زیر و حتی موضوعات بیشتری باشند:
    - سوالات مربوط به ورود و خروج از سیستم
    - سوالات مربوط به ناوبری و استفاده از منوها
    - سوالات مربوط به جستجو و فیلتر کردن داده‌ها
    - سوالات مربوط به وارد کردن و ویرایش اطلاعات
    - سوالات مربوط به گزارش‌گیری و چاپ
    - سوالات مربوط به تنظیمات شخصی و پروفایل
    - سوالات مربوط به امنیت و رمز عبور
    - سوالات مربوط به داشبورد و آمار
    - سوالات مربوط به مدیریت فایل‌ها و اسناد
    - سوالات مربوط به ارتباط با پشتیبانی

    خروجی را فقط و فقط در فرمت JSON خالص ارائه بده (بدون markdown یا کد بلوک).
    کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
    {field_instructions}

    مثال فرمت خروجی:
    {{"{data_key}": [{{"question": "چگونه وارد سیستم شوم؟"}}]}}

    هیچ متن اضافی، توضیح، یا کد بلوک قبل یا بعد از JSON قرار نده.
    فقط JSON خالص ارائه بده.
    """
    
    # Set up field instructions for simple question format
    system_fields = """
    هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
    مثال: {{"question": "چگونه وارد سیستم شوم؟"}}
    فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
    """
        
    # Configure the generator
    generator.set_prompt_template(system_prompt, system_fields)
    
    # Set system-specific contexts for different user scenarios
    system_contexts = [
        # Login and authentication contexts
        "در حال ورود به سیستم",
        "در حال تنظیم رمز عبور",
        "در حال بازیابی رمز عبور",
        "در حال تغییر اطلاعات شخصی",
        "در حال تنظیم امنیت حساب کاربری",
        
        # Navigation and interface contexts
        "در حال استفاده از منوی اصلی",
        "در حال ناوبری در داشبورد",
        "در حال استفاده از نوار ابزار",
        "در حال تغییر زبان سیستم",
        "در حال تنظیم تم و ظاهر",
        
        # Data management contexts
        "در حال وارد کردن داده‌ها",
        "در حال ویرایش اطلاعات",
        "در حال حذف رکوردها",
        "در حال آپلود فایل",
        "در حال دانلود گزارش",
        
        # Search and filter contexts
        "در حال جستجو در سیستم",
        "در حال فیلتر کردن نتایج",
        "در حال مرتب‌سازی داده‌ها",
        "در حال استفاده از جستجوی پیشرفته",
        "در حال ذخیره جستجوهای مورد علاقه",
        
        # Reporting contexts
        "در حال تهیه گزارش",
        "در حال چاپ اسناد",
        "در حال ارسال گزارش به ایمیل",
        "در حال تنظیم فرمت گزارش",
        "در حال برنامه‌ریزی گزارش‌های خودکار",
        
        # Dashboard and analytics contexts
        "در حال مشاهده آمار",
        "در حال تحلیل داده‌ها",
        "در حال تنظیم نمودارها",
        "در حال مشاهده داشبورد",
        "در حال شخصی‌سازی نمایش",
        
        # File management contexts
        "در حال مدیریت فایل‌ها",
        "در حال آرشیو کردن اسناد",
        "در حال اشتراک‌گذاری فایل",
        "در حال پشتیبان‌گیری",
        "در حال بازیابی فایل‌های حذف شده",
        
        # Communication contexts
        "در حال ارسال پیام",
        "در حال تماس با پشتیبانی",
        "در حال ارسال درخواست",
        "در حال مشاهده اعلان‌ها",
        "در حال تنظیم تنظیمات اعلان",
        
        # Settings and configuration contexts
        "در حال تنظیم سیستم",
        "در حال تغییر تنظیمات",
        "در حال شخصی‌سازی محیط",
        "در حال تنظیم مجوزها",
        "در حال مدیریت کاربران",
        
        # Troubleshooting contexts
        "در حال حل مشکل",
        "در حال بررسی خطاها",
        "در حال بازنشانی تنظیمات",
        "در حال پاک کردن کش",
        "در حال به‌روزرسانی سیستم"
    ]
    
    generator.set_contexts(system_contexts)
    
    # Set variety levels for system scenarios
    system_variety_levels = [
        "ساده",
        "متوسط", 
        "پیچیده",
        "پیشرفته"
    ]
    
    generator.set_variety_levels(system_variety_levels)
    
    # Set temperature range for creativity
    generator.set_temperature_range(0.5, 1.1)
    
    # Generate chatbot training data
    print("🤖 Starting Chatbot Training Data Generation...")
    print("📊 This will generate system-related questions for chatbot training")
    print("🎯 Target: 1000 system questions")
    
    generator.run(
        total_samples=1000,  # 1000 questions total
        data_type="سوال سیستم", 
        variety_parameter="پیچیدگی"
    )
    
    print("\n✅ Chatbot training data generation completed!")
    print("📁 Data saved to: chatbot_training_dataset.json")

def generate_simple_test_dataset():
    """Generate a simple test dataset with just system questions"""
    
    generator = DatasetGenerator(
        dataset_filename="test_chatbot_training.csv",
        samples_per_request=15,
        data_key="questions"
    )
    
    # Simple prompt for system questions
    simple_prompt = """
    {context} {count} سوال مختلف تولید کن که کاربران ممکنه درباره سیستم بپرسند.

    این سوالات می‌تونن شامل موارد زیر باشند:
    - سوالات مربوط به ورود و خروج از سیستم
    - سوالات مربوط به ناوبری و استفاده از منوها
    - سوالات مربوط به جستجو و فیلتر کردن
    - سوالات مربوط به وارد کردن و ویرایش اطلاعات
    - سوالات مربوط به گزارش‌گیری و چاپ
    - سوالات مربوط به تنظیمات شخصی

    خروجی را فقط و فقط در فرمت JSON خالص ارائه بده.
    کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
    {field_instructions}

    مثال فرمت خروجی:
    {{"{data_key}": [{{"question": "چگونه وارد سیستم شوم؟"}}]}}

    فقط JSON خالص ارائه بده.
    """
    
    # Simple field instructions
    simple_fields = """
    هر آبجکت باید شامل فیلد "question" باشد که یک متن ساده به فارسی است.
    مثال: {{"question": "چگونه وارد سیستم شوم؟"}}
    فقط فیلد "question" را استفاده کن، بدون فیلدهای اضافی.
    """
    
    generator.set_prompt_template(simple_prompt, simple_fields)
    
    generator.set_contexts([
        "در حال ورود به سیستم",
        "در حال استفاده از منوها",
        "در حال جستجو",
        "در حال وارد کردن داده",
        "در حال تهیه گزارش"
    ])
    
    generator.set_temperature_range(0.5, 1.0)
    
    print("🧪 Generating test dataset...")
    generator.run(total_samples=100, data_type="سوال سیستم", variety_parameter="پیچیدگی")
    
    # Convert to JSON
    print("✅ Test dataset completed!")

def main():
    """Main function to run chatbot training data generation"""
    
    print("🤖 Chatbot Training Data Generator")
    print("=" * 50)
    print("This script generates system-related questions for chatbot training")
    print("Output format: Simple JSON array of questions")
    print()
    
    # Ask user what they want to generate
    print("Choose an option:")
    print("1. Generate full dataset (1000 questions)")
    print("2. Generate test dataset (100 questions)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == "1":
        generate_chatbot_training_data()
                
    elif choice == "2":
        generate_simple_test_dataset()
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
