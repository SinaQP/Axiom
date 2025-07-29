import os
import json
import pandas as pd
from tqdm import tqdm
import time
from dotenv import load_dotenv
from avalai_client import AvalaiClient

class DatasetGenerator:
    def __init__(self, dataset_filename="generated_products_dataset.csv", samples_per_request=50, prompt_template=None, data_key="products"):
        self.dataset_filename = dataset_filename
        self.samples_per_request = samples_per_request
        self.data_key = data_key
        self.client = AvalaiClient(model_name="gpt-4o-mini")
        self.dataset = []
        
        # Default prompt template for products
        self.prompt_template = prompt_template or """
{count} متن فارسی کوتاه تولید کن که هرکدام دارای یک احساس مشخص باشند.
خروجی را فقط و فقط در فرمت JSON ارائه بده. کلیدهای JSON باید شامل "{data_key}" باشد که یک آرایه از آبجکت‌ها است.
هر آبجکت باید شامل "text" و "emotion" باشد.
مقدار کلید "text" باید یک جمله‌ی کوتاه فارسی باشد.
مقدار کلید "emotion" باید یکی از این موارد باشد: "غم"، "خشم"، "شگفتی"، "شادی"، "تنفر"، "ترس".
هیچ متن اضافی قبل یا بعد از JSON قرار نده.
"""
        
    def get_generation_prompt(self, count):
        return self.prompt_template.format(count=count, data_key=self.data_key)
    
    def calculate_required_requests(self, total_samples):
        return (total_samples + self.samples_per_request - 1) // self.samples_per_request
    
    def calculate_samples_for_request(self, total_samples):
        return min(self.samples_per_request, total_samples - len(self.dataset))
    
    def call_api_for_data(self, samples_count):
        response = self.client.client.chat.completions.create(
            model=self.client.model_name,
            messages=[
                {"role": "user", "content": self.get_generation_prompt(samples_count)}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def parse_api_response(self, response_text):
        cleaned_json = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_json)
    
    def extract_data_from_response(self, response_data):
        if self.data_key in response_data:
            return response_data[self.data_key]
        return [response_data]
    
    def load_existing_dataset(self):
        if not os.path.exists(self.dataset_filename):
            return None
        
        try:
            return pd.read_csv(self.dataset_filename, encoding='utf-8-sig')
        except Exception as e:
            print(f"Error reading existing file: {e}")
            return None
    
    def save_dataset(self, final_dataframe):
        final_dataframe.to_csv(self.dataset_filename, index=False, encoding='utf-8-sig')
    
    def generate_data(self, total_samples):
        print(f"Starting generation of {total_samples} data samples...")
        
        required_requests = self.calculate_required_requests(total_samples)
        print(f"Number of requests needed: {required_requests}")
        
        for request_number in tqdm(range(required_requests)):
            self._process_single_request(request_number, total_samples)
        
        print("Data generation completed successfully.")
    
    def _process_single_request(self, request_number, total_samples):
        try:
            samples_for_this_request = self.calculate_samples_for_request(total_samples)
            
            response_text = self.call_api_for_data(samples_for_this_request)
            print(f"Request {request_number + 1}: {response_text[:100]}...")
            
            response_data = self.parse_api_response(response_text)
            new_items = self.extract_data_from_response(response_data)
            
            self.dataset.extend(new_items)
            print(f"✅ {len(self.dataset)} samples generated so far")
            
            # Save after each successful request
            self.save_progress()
            
            time.sleep(1)
            
        except json.JSONDecodeError:
            print("Error: Received response does not have valid JSON format. This sample was ignored.")
        except Exception as e:
            print(f"Another error occurred: {e}")
            # Save progress even on error to preserve what we have
            self.save_progress()
    
    def save_progress(self):
        """Save current progress to avoid losing data"""
        if not self.dataset:
            return
            
        try:
            current_dataframe = pd.DataFrame(self.dataset)
            existing_dataset = self.load_existing_dataset()
            
            if existing_dataset is not None:
                final_dataframe = pd.concat([existing_dataset, current_dataframe], ignore_index=True)
            else:
                final_dataframe = current_dataframe
            
            self.save_dataset(final_dataframe)
            print(f"💾 Progress saved: {len(self.dataset)} samples in dataset")
            
        except Exception as e:
            print(f"Warning: Could not save progress: {e}")
    
    def merge_and_save_dataset(self):
        """Final save and summary - data is already saved after each request"""
        if not self.dataset:
            print("No data was generated to save.")
            return
        
        existing_dataset = self.load_existing_dataset()
        
        if existing_dataset is not None:
            print(f"✅ Final dataset contains {len(existing_dataset)} total records")
        else:
            print(f"✅ Final dataset contains {len(self.dataset)} records")
        
        print(f"\nDataset successfully completed and saved to '{self.dataset_filename}'")
        print("\nSample of generated data:")
        new_dataframe = pd.DataFrame(self.dataset)
        print(new_dataframe.head())
    
    def run(self, total_samples):
        load_dotenv()
        self.generate_data(total_samples)
        self.merge_and_save_dataset()

def main():
    generator = DatasetGenerator()
    generator.run(total_samples=100)

if __name__ == "__main__":
    main()
