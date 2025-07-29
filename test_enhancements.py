#!/usr/bin/env python3
"""
Test script for the Generic Dataset Generator
Demonstrates key improvements and allows testing of features
"""

import os
import json
from main import DatasetGenerator

def test_public_interface():
    """Test the public interface methods"""
    print("🧪 Testing Public Interface...")
    
    generator = DatasetGenerator(samples_per_request=5)
    
    # Test configuration methods
    print("1. Testing set_prompt_template...")
    custom_prompt = "Test prompt with {context} and {count}"
    generator.set_prompt_template(custom_prompt)
    print("✅ set_prompt_template works")
    
    print("2. Testing set_contexts...")
    custom_contexts = ["Context 1", "Context 2", "Context 3"]
    generator.set_contexts(custom_contexts)
    print("✅ set_contexts works")
    
    print("3. Testing set_variety_levels...")
    custom_levels = ["Low", "Medium", "High"]
    generator.set_variety_levels(custom_levels)
    print("✅ set_variety_levels works")
    
    print("4. Testing set_temperature_range...")
    generator.set_temperature_range(0.5, 1.0)
    print("✅ set_temperature_range works")
    
    return True

def test_duplicate_detection():
    """Test duplicate detection functionality"""
    print("\n🧪 Testing Duplicate Detection...")
    
    generator = DatasetGenerator()
    
    # Create some test items
    test_items = [
        {"text": "در یک روز آفتابی، کودک خوشحالانه بازی می‌کرد", "emotion": "شادی"},
        {"text": "در یک روز آفتابی، کودک خوشحالانه بازی می‌کرد", "emotion": "شادی"},  # Duplicate
        {"text": "در یک شب بارانی، صدای رعد و برق ترسناک بود", "emotion": "ترس"},
        {"text": "در یک شب بارانی، صدای رعد و برق ترسناک بود", "emotion": "ترس"},  # Duplicate
        {"text": "در یک مهمانی خانوادگی، همه خوشحال بودند", "emotion": "شادی"}
    ]
    
    # Test duplicate detection (using private method for testing)
    unique_items = generator._filter_duplicates(test_items)
    
    print(f"Original items: {len(test_items)}")
    print(f"Unique items: {len(unique_items)}")
    print(f"Duplicates filtered: {len(test_items) - len(unique_items)}")
    
    return len(unique_items) < len(test_items)

def test_temperature_variation():
    """Test that temperature varies dynamically"""
    print("\n🧪 Testing Temperature Variation...")
    
    generator = DatasetGenerator()
    
    temperatures = []
    for i in range(10):
        temp = generator._get_dynamic_temperature()
        temperatures.append(temp)
        print(f"Temperature {i+1}: {temp:.3f}")
    
    # Check if temperatures vary
    temp_range = max(temperatures) - min(temperatures)
    print(f"Temperature range: {min(temperatures):.3f} - {max(temperatures):.3f}")
    print(f"Variation: {temp_range:.3f}")
    
    return temp_range > 0.1

def test_context_variety():
    """Test context variety in prompts"""
    print("\n🧪 Testing Context Variety...")
    
    generator = DatasetGenerator()
    
    contexts_used = set()
    for i in range(20):
        prompt = generator._get_generation_prompt(5)
        # Extract context from prompt (simple method)
        if "در یک" in prompt:
            context_start = prompt.find("در یک")
            context_end = prompt.find("،", context_start)
            if context_end == -1:
                context_end = prompt.find(" ", context_start + 10)
            context = prompt[context_start:context_end]
            contexts_used.add(context)
    
    print(f"Unique contexts used: {len(contexts_used)}")
    print("Sample contexts:", list(contexts_used)[:5])
    
    return len(contexts_used) > 1

def test_small_quality_dataset():
    """Test generating a small high-quality dataset"""
    print("\n🧪 Testing Small Quality Dataset Generation...")
    
    # Create a generator with high-quality settings
    generator = DatasetGenerator(
        dataset_filename="test_quality_dataset.csv",
        samples_per_request=5  # Very small for testing
    )
    
    # Use diverse contexts
    generator.set_contexts([
        "در یک فضاپیما",
        "در یک قلعه قرون وسطایی", 
        "در یک جنگل آمازون",
        "در یک شهر زیرزمینی",
        "در یک جزیره دورافتاده"
    ])
    
    generator.set_temperature_range(0.8, 1.3)
    
    try:
        # Generate a small dataset
        generator.run(total_samples=10)
        print("✅ Small dataset generation completed successfully")
        
        # Check if file was created
        if os.path.exists("test_quality_dataset.csv"):
            print("✅ Output file created successfully")
            return True
        else:
            print("❌ Output file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 Generic Dataset Generator - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Public Interface", test_public_interface),
        ("Duplicate Detection", test_duplicate_detection),
        ("Temperature Variation", test_temperature_variation),
        ("Context Variety", test_context_variety),
        ("Small Quality Dataset", test_small_quality_dataset)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        except Exception as e:
            print(f"❌ ERROR - {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The generic generator is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

def demonstrate_features():
    """Demonstrate key features with examples"""
    print("\n🎯 Feature Demonstration")
    print("=" * 30)
    
    generator = DatasetGenerator(samples_per_request=3)
    
    print("1. Public Configuration Methods:")
    print("   - set_prompt_template() - Set custom prompts")
    print("   - set_contexts() - Set custom contexts")
    print("   - set_variety_levels() - Set variety levels")
    print("   - set_temperature_range() - Set creativity range")
    print("   - run() - Main method to generate data")
    
    print("\n2. Simple Usage Example:")
    print("   generator = DatasetGenerator()")
    print("   generator.set_contexts(['Context 1', 'Context 2'])")
    print("   generator.set_temperature_range(0.8, 1.3)")
    print("   generator.run(total_samples=100)")
    
    print("\n3. Advanced Usage Example:")
    print("   generator.set_prompt_template(custom_prompt, custom_fields)")
    print("   generator.run(total_samples=100, data_type='آیتم سفارشی', variety_parameter='ویژگی')")

def show_public_api():
    """Show the clean public API"""
    print("\n🔧 Public API Reference")
    print("=" * 25)
    
    print("""
DatasetGenerator(dataset_filename, samples_per_request, prompt_template, data_key)

PUBLIC METHODS:
├── set_prompt_template(template, field_instructions=None)
├── set_contexts(contexts)
├── set_variety_levels(levels)
├── set_temperature_range(min_temp, max_temp)
└── run(total_samples, data_type="آیتم", variety_parameter="ویژگی")

CONFIGURABLE ATTRIBUTES:
├── temperature_range = (0.7, 1.2)
├── max_retries = 3
├── contexts = [list of contexts]
├── variety_levels = ["کم", "متوسط", "زیاد"]
└── prompt_template = "template string"
""")

if __name__ == "__main__":
    # Show the clean public API
    show_public_api()
    
    # Run demonstration
    demonstrate_features()
    
    # Ask user if they want to run tests
    print("\n" + "=" * 50)
    response = input("Do you want to run the full test suite? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        run_all_tests()
    else:
        print("Skipping tests. You can run them later with: python test_enhancements.py") 