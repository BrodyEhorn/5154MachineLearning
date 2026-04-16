import os
import shutil
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import logging

# Disable verbose icrawler logging
logging.getLogger().setLevel(logging.CRITICAL)

def scrape_with_icrawler(query, target_folder, max_num=100):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "raw", target_folder)
    os.makedirs(output_dir, exist_ok=True)
    
    temp_dir = os.path.join(output_dir, f"temp_{query.replace(' ', '_')}")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Using BingImageCrawler which is often more lenient than Google without API keys
    crawler = BingImageCrawler(storage={'root_dir': temp_dir}, downloader_threads=4)
    
    print(f"Scraping up to {max_num} images for '{query}' -> {target_folder}/ ...")
    crawler.crawl(keyword=query, filters=None, max_num=max_num)
    
    # Move and systematically rename to prevent file collision
    if os.path.exists(temp_dir):
        existing_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
        count = len(existing_files)
        
        for f in os.listdir(temp_dir):
            src = os.path.join(temp_dir, f)
            if not os.path.isfile(src): continue
            
            ext = os.path.splitext(f)[1]
            if not ext: ext = ".jpg"
            new_name = f"{query.replace(' ', '_')}_{count}{ext}"
            dst = os.path.join(output_dir, new_name)
            
            shutil.move(src, dst)
            count += 1
            
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == "__main__":
    print("Initiating dataset scraping pipeline via icrawler...\n")
    
    scrape_with_icrawler("locked carabiner climbing gear", "closed", 100)
    scrape_with_icrawler("closed climbing carabiner", "closed", 100)
    
    scrape_with_icrawler("open gate carabiner climbing", "open", 100)
    scrape_with_icrawler("unlocked open carabiner", "open", 100)
    
    print("\n✅ Scraping complete! Next step: Validate images in data/raw/ and remove any false positives.")
