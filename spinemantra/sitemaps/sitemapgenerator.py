import logging
import mysql.connector
from mysql.connector import Error
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="spinemantra"
        )
        if conn.is_connected():
            logging.info("Successfully connected to the database")
        return conn
    except Error as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

def generate_sitemap(url_prefix, table, slug_column, lastmod_column=None, include_id=False):
    try:
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        
        if lastmod_column:
            query = f"SELECT {slug_column}, id, {lastmod_column} FROM {table}"
        else:
            query = f"SELECT {slug_column}, id FROM {table}"
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for entry in data:
            sitemap_content += '  <url>\n'
            if include_id:
                sitemap_content += f'    <loc>{url_prefix}/{entry[slug_column]}/{entry["id"]}</loc>\n'
            else:
                sitemap_content += f'    <loc>{url_prefix}/{entry[slug_column]}</loc>\n'
            if lastmod_column and lastmod_column in entry:
                sitemap_content += f'    <lastmod>{entry[lastmod_column]}</lastmod>\n'
            sitemap_content += '  </url>\n'
        
        sitemap_content += '</urlset>'
        return sitemap_content
    except Error as e:
        logging.error(f"Error generating sitemap: {e}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_sitemap(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Sitemap saved: {filename}")
    except IOError as e:
        logging.error(f"Error saving sitemap {filename}: {e}")
        raise

def generate_sitemap_index(sitemaps):
    sitemap_index_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_index_content += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for sitemap in sitemaps:
        sitemap_index_content += '  <sitemap>\n'
        sitemap_index_content += f'    <loc>{sitemap["loc"]}</loc>\n'
        if "lastmod" in sitemap:
            sitemap_index_content += f'    <lastmod>{sitemap["lastmod"]}</lastmod>\n'
        sitemap_index_content += '  </sitemap>\n'
    
    sitemap_index_content += '</sitemapindex>'
    return sitemap_index_content

if __name__ == "__main__":
    try:
        domain = "https://spinemantra.com"
        
        sitemaps = [
            # ("blog_posts", f"{domain}/blog-details", "blog_posts", "slug", None, False),
            ("video_details", f"{domain}/videos", "video_details", "slug", None, False),
            # ("case_studies", f"{domain}/case-study-details", "case_studies", "slug", None, False),
            ("career_models", f"{domain}/careers", "career_models", "slug", None, False),
            ("services", f"{domain}/service", "services", "slug", "updated_at", True),
            ("contacts", f"{domain}/contact", "contacts", "slug", None, False),
            ("infographic_models", f"{domain}/infographics", "infographic_models", "slug", None, False),
            ("location_pages", f"{domain}/location/kolkata", "location_pages", "slug", None, False),
            ("quiz_categories", f"{domain}/quizzes", "quiz_categories", "slug", None, False),
        ]
        
        sitemap_files = []
        
        for name, url_prefix, table, slug_column, lastmod_column, include_id in sitemaps:
            sitemap_content = generate_sitemap(url_prefix, table, slug_column, lastmod_column, include_id)
            sitemap_filename = f"sitemap_{name}.xml"
            save_sitemap(sitemap_filename, sitemap_content)
            sitemap_files.append({
                "loc": f"{domain}/{sitemap_filename}",
                "lastmod": datetime.now().strftime("%Y-%m-%d")
            })
        
        sitemap_index_content = generate_sitemap_index(sitemap_files)
        save_sitemap("sitemap_index.xml", sitemap_index_content)
        
        logging.info("All sitemaps and sitemap index generated successfully")
    except Exception as e:
        logging.error(f"An error occurred during sitemap generation: {e}")