# Generic Dataset Generator

A sophisticated AI-powered dataset generator that creates high-quality, diverse, and non-repetitive data for **any type of content** you need. The class is completely generic and flexible, with a **clean, simple public API** that makes it easy to use.

## 🚀 Key Features

### 1. **Simple Public API**
- **Only 5 public methods** - Easy to learn and use
- **Clean interface** - No need to understand internal complexity
- **Intuitive configuration** - Set up your data generation in minutes

### 2. **Completely Generic & Flexible**
- **Any Data Type**: Generate emotions, products, restaurants, books, movies, or custom data
- **Customizable Prompts**: Define your own prompt templates and field instructions
- **Flexible Contexts**: Set domain-specific contexts for your use case
- **Configurable Parameters**: Adjust all settings for your specific needs

### 3. **Advanced Quality Features**
- **Dynamic Prompt Generation**: Each request uses different contexts to prevent repetition
- **Duplicate Prevention**: Automatic detection and filtering of duplicate content
- **Variable Creativity**: Dynamic temperature and penalties for better output
- **Robust Error Handling**: Retry logic and progress preservation

## 📁 Project Structure

```
dataset-creator/
├── main.py              # Generic DatasetGenerator class
├── examples.py          # Examples for different data types
├── avalai_client.py     # API client configuration
├── requirements.txt     # Python dependencies
├── test_enhancements.py # Test script
└── README.md           # This file
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd dataset-creator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file with your API key:
```
AVALAI_API_KEY=your_api_key_here
```

## 🎯 Quick Start

### Basic Usage (3 lines of code!)
```python
from main import DatasetGenerator

# Create and run generator
generator = DatasetGenerator()
generator.run(total_samples=100)
```

### Custom Data Generation
```python
from main import DatasetGenerator

# Create generator
generator = DatasetGenerator(
    dataset_filename="my_data.csv",
    samples_per_request=25,
    data_key="my_items"
)

# Configure for your data type
generator.set_contexts(["Context 1", "Context 2", "Context 3"])
generator.set_temperature_range(0.8, 1.3)

# Generate data
generator.run(total_samples=150, data_type="آیتم سفارشی", variety_parameter="ویژگی")
```

## 🔧 Public API Reference

### Constructor
```python
DatasetGenerator(
    dataset_filename="generated_dataset.csv",  # Output file name
    samples_per_request=50,                    # Samples per API call
    prompt_template=None,                      # Custom prompt template
    data_key="data"                           # JSON key for data
)
```

### Public Methods (Only 5!)

| Method | Description | Example |
|--------|-------------|---------|
| `set_prompt_template(template, field_instructions=None)` | Set custom prompt and field structure | `generator.set_prompt_template(my_prompt, my_fields)` |
| `set_contexts(contexts)` | Set custom contexts for variety | `generator.set_contexts(["Context 1", "Context 2"])` |
| `set_variety_levels(levels)` | Set intensity/variety levels | `generator.set_variety_levels(["Low", "Medium", "High"])` |
| `set_temperature_range(min_temp, max_temp)` | Set creativity range | `generator.set_temperature_range(0.7, 1.2)` |
| `run(total_samples, data_type, variety_parameter)` | **Main method** - Generate data | `generator.run(100, "آیتم", "ویژگی")` |

### Configurable Attributes
```python
generator.temperature_range = (0.7, 1.2)  # Creativity range
generator.max_retries = 3                 # Retry attempts
generator.contexts = [...]                # Context variety
generator.variety_levels = [...]          # Intensity levels
generator.prompt_template = "..."         # Prompt template
```

## 📊 Usage Examples

### 1. Generate Emotion Data
```python
from examples import generate_emotion_data
generate_emotion_data()
```

### 2. Generate Restaurant Data
```python
from examples import generate_restaurant_data
generate_restaurant_data()
```

### 3. Generate Custom Data
```python
from main import DatasetGenerator

# Define your custom prompt
custom_prompt = """
{context} {count} {data_type} تولید کن که هرکدام دارای {variety_parameter} {intensity} باشند.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
{field_instructions}
هیچ متن اضافی قبل یا بعد از JSON قرار نده.
"""

# Define your field structure
custom_fields = """
هر آبجکت باید شامل "name", "description" و "category" باشد.
مقدار کلید "name" باید نام خلاقانه باشد.
مقدار کلید "description" باید توضیح کوتاه باشد.
مقدار کلید "category" باید دسته‌بندی مناسب باشد.
"""

# Create and configure generator
generator = DatasetGenerator(
    dataset_filename="custom_data.csv",
    samples_per_request=25,
    data_key="custom_items"
)

generator.set_prompt_template(custom_prompt, custom_fields)
generator.set_contexts([
    "در یک محیط کاری",
    "در یک فضای آموزشی", 
    "در یک محیط تفریحی"
])
generator.set_temperature_range(0.8, 1.3)

# Generate your data
generator.run(total_samples=100, data_type="آیتم سفارشی", variety_parameter="ویژگی")
```

## 🎨 Prompt Template Structure

### Template Variables
- `{context}` - Random context from your contexts list
- `{count}` - Number of samples to generate
- `{data_type}` - Type of data you're generating
- `{variety_parameter}` - Parameter for variety (e.g., "احساس", "ویژگی")
- `{intensity}` - Random intensity level
- `{data_key}` - JSON key for your data
- `{field_instructions}` - Your custom field instructions

### Example Template
```
{context} {count} {data_type} تولید کن که هرکدام دارای {variety_parameter} {intensity} باشند.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
{field_instructions}
هیچ متن اضافی قبل یا بعد از JSON قرار نده.
```

## 📈 Best Practices

### 1. **Start Simple**
```python
# Start with basic usage
generator = DatasetGenerator()
generator.run(total_samples=50)
```

### 2. **Customize Gradually**
```python
# Add custom contexts
generator.set_contexts(["Context 1", "Context 2"])

# Adjust creativity
generator.set_temperature_range(0.8, 1.3)

# Generate more data
generator.run(total_samples=100)
```

### 3. **Choose Appropriate Batch Sizes**
- **High Quality**: 10-20 samples per request
- **Balanced**: 25-35 samples per request  
- **High Volume**: 40-50 samples per request

### 4. **Define Clear Field Instructions**
```python
field_instructions = """
هر آبجکت باید شامل "name", "description" و "category" باشد.
مقدار کلید "name" باید نام خلاقانه باشد.
مقدار کلید "description" باید توضیح کوتاه باشد.
مقدار کلید "category" باید دسته‌بندی مناسب باشد.
"""
```

## 🚨 Troubleshooting

### Common Issues

1. **Low Quality Output**
   - Reduce `samples_per_request`
   - Increase temperature range
   - Add more diverse contexts

2. **Too Many Duplicates**
   - Check if contexts are too similar
   - Increase temperature for more variation
   - Add more context variety

3. **API Errors**
   - Check API key configuration
   - Reduce request frequency
   - Increase retry count

## 📝 Example Output

```
Starting generation of 100 آیتم samples...
Using dynamic prompts with 10 different contexts
Temperature range: (0.7, 1.2)
Number of requests needed: 4

🔄 Request 1 (attempt 1)
Response preview: {"data": [{"name": "آیتم خلاقانه", "description": "توضیح کوتاه"}]}...
✅ 25 unique samples generated so far
💾 Progress saved: 25 samples in dataset

Data generation completed successfully.
✅ Final dataset contains 100 records
Total unique samples generated: 100
Total requests made: 4

Dataset successfully completed and saved to 'generated_dataset.csv'
```

## 🧪 Testing

Run the test script to verify everything works:
```bash
python test_enhancements.py
```

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new prompt templates
- Improving error handling
- Adding new features
- Reporting bugs

## 📄 License

This project is licensed under the MIT License. 