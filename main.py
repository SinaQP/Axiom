import os
import json
import pandas as pd
from tqdm import tqdm
import time
import random
import hashlib
from dotenv import load_dotenv
from avalai_client import AvalaiClient

class DatasetGenerator:
    def __init__(self, dataset_filename="generated_dataset.csv", samples_per_request=50, prompt_template=None, data_key="data"):
        self.dataset_filename = dataset_filename
        self.samples_per_request = samples_per_request
        self.data_key = data_key
        self.client = AvalaiClient(model_name="gpt-4o-mini")
        self.dataset = []
        
        # Track generated content to prevent duplicates
        self._generated_hashes = set()
        self._request_count = 0
        
        # Diversity parameters
        self.temperature_range = (0.7, 1.2)
        self.max_retries = 3
        
        # Generic context variety for different scenarios
        self.contexts = [
            "در یک روز آفتابی",
            "در یک شب بارانی", 
            "در یک سفر کاری",
            "در یک مهمانی خانوادگی",
            "در یک رستوران شلوغ",
            "در یک پارک آرام",
            "در یک مرکز خرید",
            "در یک کتابخانه",
            "در یک بیمارستان"
        ]
        
        # Generic intensity/variety levels
        self.variety_levels = ["کم", "متوسط", "زیاد"]
        
        # Default generic prompt template
        self.prompt_template = prompt_template or """
            {context} {count} {data_type} تولید کن که هرکدام دارای {variety_parameter} {intensity} باشند.

            خروجی را فقط و فقط در فرمت JSON خالص ارائه بده (بدون markdown یا کد بلوک).
            کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
            {field_instructions}

            مثال فرمت خروجی:
            {{"{data_key}": [{{"field1": "value1", "field2": "value2"}}]}}

            هیچ متن اضافی، توضیح، یا کد بلوک قبل یا بعد از JSON قرار نده.
            فقط JSON خالص ارائه بده.
            """
                
                # Default field instructions for generic data
        self.field_instructions = """
        هر آبجکت باید شامل فیلدهای مورد نیاز باشد که در دستورالعمل‌های خاص تعریف شده‌اند.
        """
    
    # ==================== PUBLIC METHODS ====================
    
    def set_prompt_template(self, template, field_instructions=None):
        """Set a custom prompt template and field instructions"""
        self.prompt_template = template
        if field_instructions:
            self.field_instructions = field_instructions
    
    def set_contexts(self, contexts):
        """Set custom contexts for your specific use case"""
        self.contexts = contexts
    
    def set_variety_levels(self, levels):
        """Set custom variety/intensity levels"""
        self.variety_levels = levels
    
    def set_temperature_range(self, min_temp, max_temp):
        """Set custom temperature range for creativity control"""
        self.temperature_range = (min_temp, max_temp)
    
    def run(self, total_samples, data_type="آیتم", variety_parameter="ویژگی"):
        """Main method to run the dataset generation process"""
        load_dotenv()
        self._generate_data(total_samples, data_type, variety_parameter)
        self._merge_and_save_dataset()
    
    # ==================== PRIVATE METHODS ====================
    
    def _get_generation_prompt(self, count, data_type="آیتم", variety_parameter="ویژگی", custom_context=None):
        """Generate a dynamic prompt with random context and variety"""
        context = custom_context or random.choice(self.contexts)
        intensity = random.choice(self.variety_levels)
        
        return self.prompt_template.format(
            count=count, 
            data_key=self.data_key,
            context=context,
            intensity=intensity,
            data_type=data_type,
            variety_parameter=variety_parameter,
            field_instructions=self.field_instructions
        )
    
    def _get_dynamic_temperature(self):
        """Get a random temperature within the range to vary creativity"""
        return random.uniform(*self.temperature_range)
    
    def _calculate_required_requests(self, total_samples):
        return (total_samples + self.samples_per_request - 1) // self.samples_per_request
    
    def _calculate_samples_for_request(self, total_samples):
        return min(self.samples_per_request, total_samples - len(self.dataset))
    
    def _generate_content_hash(self, item):
        """Generate a hash for content to detect duplicates"""
        content_str = json.dumps(item, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(content_str.encode('utf-8')).hexdigest()
    
    def _is_duplicate(self, item):
        """Check if an item is a duplicate"""
        content_hash = self._generate_content_hash(item)
        return content_hash in self._generated_hashes
    
    def _add_to_generated_set(self, items):
        """Add items to the generated set to track duplicates"""
        for item in items:
            content_hash = self._generate_content_hash(item)
            self._generated_hashes.add(content_hash)
    
    def _call_api_for_data(self, samples_count, data_type="آیتم", variety_parameter="ویژگی", custom_context=None):
        """Call API with dynamic parameters"""
        temperature = self._get_dynamic_temperature()
        
        prompt = self._get_generation_prompt(samples_count, data_type, variety_parameter, custom_context)
        
        response = self.client.client.chat.completions.create(
            model=self.client.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=2000,  # Ensure enough tokens for creative responses
            presence_penalty=0.1,  # Slightly penalize repetition
            frequency_penalty=0.1   # Slightly penalize frequent tokens
        )
        return response.choices[0].message.content
    
    def _parse_api_response(self, response_text):
        """Parse API response and extract JSON, handling various response formats"""
        try:
            # First, try to clean the response
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text.replace("```", "").strip()
            
            # Try to find JSON content between curly braces
            start_brace = cleaned_text.find("{")
            end_brace = cleaned_text.rfind("}")
            
            if start_brace != -1 and end_brace != -1 and end_brace > start_brace:
                json_content = cleaned_text[start_brace:end_brace + 1]
                return json.loads(json_content)
            
            # If no braces found, try parsing the entire cleaned text
            return json.loads(cleaned_text)
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response: {response_text[:200]}...")
            
            # Try to extract JSON from the response more aggressively
            try:
                # Look for any JSON-like structure
                import re
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                matches = re.findall(json_pattern, response_text)
                
                if matches:
                    # Try the longest match
                    longest_match = max(matches, key=len)
                    return json.loads(longest_match)
                    
            except Exception as nested_e:
                print(f"❌ Secondary JSON extraction also failed: {nested_e}")
            
            raise e
    
    def _extract_data_from_response(self, response_data):
        """Extract and flatten data from API response into individual items"""
        if self.data_key in response_data:
            items = response_data[self.data_key]
        else:
            items = [response_data]
        
        # Ensure items is a list
        if not isinstance(items, list):
            items = [items]
        
        # Flatten the data into individual records
        flattened_items = []
        for item in items:
            if isinstance(item, dict):
                flattened_items.append(item)
            elif isinstance(item, str):
                # Try to parse string as JSON
                try:
                    parsed_item = json.loads(item)
                    if isinstance(parsed_item, list):
                        flattened_items.extend(parsed_item)
                    else:
                        flattened_items.append(parsed_item)
                except (json.JSONDecodeError, TypeError):
                    # If it's not JSON, treat as text
                    flattened_items.append({"text": item, "emotion": "unknown"})
        
        return flattened_items
    
    def _filter_duplicates(self, items):
        """Filter out duplicate items"""
        unique_items = []
        for item in items:
            if not self._is_duplicate(item):
                unique_items.append(item)
            else:
                print(f"⚠️ Duplicate detected and filtered out")
        return unique_items
    
    def _load_existing_dataset(self):
        if not os.path.exists(self.dataset_filename):
            return None
        
        try:
            return pd.read_csv(self.dataset_filename, encoding='utf-8-sig')
        except Exception as e:
            print(f"Error reading existing file: {e}")
            return None
    
    def _save_dataset(self, final_dataframe):
        """Save dataset to CSV with proper formatting"""
        try:
            # Ensure the dataframe has the expected structure
            if not final_dataframe.empty:
                # If the dataframe has a single column with JSON strings, parse them
                if len(final_dataframe.columns) == 1 and self.data_key in final_dataframe.columns:
                    # Parse the JSON strings into proper columns
                    parsed_data = []
                    for _, row in final_dataframe.iterrows():
                        try:
                            # Parse the JSON string
                            json_data = json.loads(row[self.data_key])
                            if isinstance(json_data, list):
                                parsed_data.extend(json_data)
                            else:
                                parsed_data.append(json_data)
                        except:
                            continue
                    
                    # Create new dataframe from parsed data
                    if parsed_data:
                        final_dataframe = pd.DataFrame(parsed_data)
                
                # Save with proper encoding
                final_dataframe.to_csv(self.dataset_filename, index=False, encoding='utf-8-sig')
            else:
                print("Warning: No data to save")
                
        except Exception as e:
            print(f"Error saving dataset: {e}")
            # Fallback: save as is
            final_dataframe.to_csv(self.dataset_filename, index=False, encoding='utf-8-sig')
    
    def _generate_data(self, total_samples, data_type="آیتم", variety_parameter="ویژگی"):
        print(f"Starting generation of {total_samples} {data_type} samples...")
        print(f"Using dynamic prompts with {len(self.contexts)} different contexts")
        print(f"Temperature range: {self.temperature_range}")
        
        required_requests = self._calculate_required_requests(total_samples)
        print(f"Number of requests needed: {required_requests}")
        
        for request_number in tqdm(range(required_requests)):
            self._process_single_request(request_number, total_samples, data_type, variety_parameter)
        
        print("Data generation completed successfully.")
    
    def _process_single_request(self, request_number, total_samples, data_type="آیتم", variety_parameter="ویژگی"):
        """Process a single API request with retry logic and duplicate filtering"""
        self._request_count += 1
        
        for attempt in range(self.max_retries):
            try:
                samples_for_this_request = self._calculate_samples_for_request(total_samples)
                
                print(f"\n🔄 Request {request_number + 1} (attempt {attempt + 1})")
                response_text = self._call_api_for_data(samples_for_this_request, data_type, variety_parameter)
                print(f"Response preview: {response_text[:100]}...")
                
                try:
                    response_data = self._parse_api_response(response_text)
                    new_items = self._extract_data_from_response(response_data)
                except json.JSONDecodeError:
                    print("⚠️ JSON parsing failed, creating fallback data...")
                    # Create fallback data if JSON parsing completely fails
                    new_items = self._create_fallback_data(samples_for_this_request, data_type)
                
                # Filter duplicates
                unique_items = self._filter_duplicates(new_items)
                
                if len(unique_items) < len(new_items):
                    print(f"⚠️ Filtered out {len(new_items) - len(unique_items)} duplicates")
                
                # Add to dataset and tracking set
                self.dataset.extend(unique_items)
                self._add_to_generated_set(unique_items)
                
                print(f"✅ {len(self.dataset)} unique samples generated so far")
                
                # Save after each successful request
                self._save_progress()
                
                # Variable delay to prevent rate limiting and add randomness
                delay = random.uniform(1.0, 2.5)
                time.sleep(delay)
                
                break  # Success, exit retry loop
                
            except Exception as e:
                print(f"❌ Error on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries - 1:
                    print("❌ Max retries reached for this request")
                    # Save progress even on error to preserve what we have
                    self._save_progress()
                time.sleep(1)
    
    def _create_fallback_data(self, count, data_type):
        """Create fallback data when API response is malformed"""
        fallback_items = []
        for i in range(count):
            fallback_item = {
                "id": len(self.dataset) + i + 1,
                "name": f"{data_type} {len(self.dataset) + i + 1}",
                "description": f"Fallback {data_type} description",
                "created_at": "fallback"
            }
            fallback_items.append(fallback_item)
        
        return fallback_items
    
    def _save_progress(self):
        """Save current progress to avoid losing data"""
        if not self.dataset:
            return
            
        try:
            current_dataframe = pd.DataFrame(self.dataset)
            existing_dataset = self._load_existing_dataset()
            
            if existing_dataset is not None:
                final_dataframe = pd.concat([existing_dataset, current_dataframe], ignore_index=True)
            else:
                final_dataframe = current_dataframe
            
            self._save_dataset(final_dataframe)
            print(f"💾 Progress saved: {len(self.dataset)} samples in dataset")
            
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def _merge_and_save_dataset(self):
        """Final save and summary - data is already saved after each request"""
        if not self.dataset:
            print("No data was generated to save.")
            return
        
        existing_dataset = self._load_existing_dataset()
        
        if existing_dataset is not None:
            print(f"✅ Final dataset contains {len(existing_dataset)} total records")
        else:
            print(f"✅ Final dataset contains {len(self.dataset)} records")
        
        print(f"\nDataset successfully completed and saved to '{self.dataset_filename}'")
        print(f"Total unique samples generated: {len(self.dataset)}")
        print(f"Total requests made: {self._request_count}")
        print("\nSample of generated data:")
        new_dataframe = pd.DataFrame(self.dataset)
        print(new_dataframe.head())

# def main():
#     generator = DatasetGenerator(
#         dataset_filename="emotion_dataset.csv",
#         samples_per_request=25,
#         data_key="samples"
#     )
    
#     # Set up the emotion prompt template
#     emotion_prompt = """
#     {context} {count} نمونه‌ی متن فارسی کوتاه تولید کن که هرکدام بیانگر یکی از احساسات انسانی باشند.

#     خروجی را فقط و فقط در فرمت JSON خالص ارائه بده (بدون markdown یا کد بلوک).
#     کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
#     {field_instructions}

#     مثال فرمت خروجی:
#     {{"{data_key}": [{{"text": "من امروز خوشحالم", "emotion": "شادی"}}]}}

#     هیچ متن اضافی، توضیح، یا کد بلوک قبل یا بعد از JSON قرار نده.
#     فقط JSON خالص ارائه بده.
#     """
    
#     # Set up field instructions for emotions
#     emotion_fields = """
#     هر آبجکت باید شامل "text" و "emotion" باشد.
#     مقدار "text" باید یک جمله‌ی کوتاه فارسی باشد (مثلاً «من امروز برنده شدم»).
#     مقدار "emotion" باید یکی از این موارد باشد: "غم"، "خشم"، "شگفتی"، "شادی"، "تنفر"، "ترس".
#     """
    
#     # Configure the generator
#     generator.set_prompt_template(emotion_prompt, emotion_fields)
#     generator.set_contexts([
#         "در یک روز آفتابی",
#         "در یک شب بارانی", 
#         "در یک مهمانی خانوادگی",
#         "در یک سفر کاری",
#         "در یک کلاس درس",
#         "در یک رستوران شلوغ",
#         "در یک پارک آرام",
#         "در یک مرکز خرید",
#         "در یک کتابخانه",
#         "در یک بیمارستان"
#     ])
#     generator.set_temperature_range(0.7, 1.2)
    
#     generator.run(total_samples=5000, data_type="متن احساسی", variety_parameter="احساس")

# if __name__ == "__main__":
#     main()
