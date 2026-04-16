import os
import shutil
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import logging

logging.getLogger().setLevel(logging.CRITICAL)

def scrape_with_icrawler(query, target_folder="open", max_num=100):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "data", "raw", target_folder)
    os.makedirs(output_dir, exist_ok=True)
    
    temp_dir = os.path.join(output_dir, f"temp_{query.replace(' ', '_')}")
    os.makedirs(temp_dir, exist_ok=True)
    
    crawler = BingImageCrawler(storage={'root_dir': temp_dir}, downloader_threads=4)
    print(f"Scraping up to {max_num} images for '{query}' ...")
    
    crawler.crawl(keyword=query, filters=None, max_num=max_num)
    
    if os.path.exists(temp_dir):
        existing_files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
        count = len(existing_files)
        
        for f in os.listdir(temp_dir):
            src = os.path.join(temp_dir, f)
            if not os.path.isfile(src): continue
            
            ext = os.path.splitext(f)[1]
            if not ext: ext = ".jpg"
            new_name = f"more_open_{query.replace(' ', '_')}_{count}{ext}"
            dst = os.path.join(output_dir, new_name)
            
            shutil.move(src, dst)
            count += 1
            
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

if __name__ == "__main__":
    print("Initiating targeted scrape for Open Carabiners...\n")
    
    scrape_with_icrawler("carabiner with gate held open", max_num=100)
    scrape_with_icrawler("carabiner unlatched open loop", max_num=100)
    scrape_with_icrawler("open gate carabiner hooked onto rope", max_num=100)
    scrape_with_icrawler("carabiner clip mechanism open", max_num=100)
    scrape_with_icrawler("climbing quickdraw carabiner open", max_num=100)
    
    print("\n✅ Finished Phase 2 of Scraping!")
