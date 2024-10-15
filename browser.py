import os
import json
from collections import Counter
import sqlite3
import glob
import csv
from datetime import datetime

def get_browser_history():
    history_files = {
        'chrome': os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History',
        'firefox': os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
        'edge': os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge Beta\User Data\Default\History'
    }
    
    cookie_files = {
        'chrome': os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Cookies',
        'firefox': os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
        'edge': os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge Beta\User Data\Default\Cookies'
    }
    
    cache_files = {
        'chrome': os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Cache',
        'firefox': os.path.expanduser('~') + r'\AppData\Roaming\Mozilla\Firefox\Profiles',
        'edge': os.path.expanduser('~') + r'\AppData\Local\Microsoft\Edge Beta\User Data\Default\Cache'
    }
    
    history_data = []
    cookies_data = []
    cache_data = []
    
    # Extract Chrome history
    if os.path.exists(history_files['chrome']):
        try:
            conn = sqlite3.connect(history_files['chrome'])
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM urls")
            history_data.extend([row[0] for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Chrome history: {e}")
    
    # Extract Firefox history
    if os.path.exists(history_files['firefox']):
        try:
            profile_path = glob.glob(history_files['firefox'] + r'\*\places.sqlite')[0]
            conn = sqlite3.connect(profile_path)
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM moz_places")
            history_data.extend([row[0] for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Firefox history: {e}")
    
    # Extract Edge history
    if os.path.exists(history_files['edge']):
        try:
            conn = sqlite3.connect(history_files['edge'])
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM urls")
            history_data.extend([row[0] for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Edge history: {e}")
    
    # Extract Chrome cookies
    if os.path.exists(cookie_files['chrome']):
        try:
            conn = sqlite3.connect(cookie_files['chrome'])
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value FROM cookies")
            cookies_data.extend([{'host': row[0], 'name': row[1], 'value': row[2]} for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Chrome cookies: {e}")
    
    # Extract Firefox cookies
    if os.path.exists(cookie_files['firefox']):
        try:
            profile_path = glob.glob(cookie_files['firefox'] + r'\*\cookies.sqlite')[0]
            conn = sqlite3.connect(profile_path)
            cursor = conn.cursor()
            cursor.execute("SELECT host, name, value FROM moz_cookies")
            cookies_data.extend([{'host': row[0], 'name': row[1], 'value': row[2]} for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Firefox cookies: {e}")
    
    # Extract Edge cookies
    if os.path.exists(cookie_files['edge']):
        try:
            conn = sqlite3.connect(cookie_files['edge'])
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value FROM cookies")
            cookies_data.extend([{'host': row[0], 'name': row[1], 'value': row[2]} for row in cursor.fetchall()])
            conn.close()
        except Exception as e:
            print(f"Error reading Edge cookies: {e}")
    
    # Extract Chrome cache
    if os.path.exists(cache_files['chrome']):
        try:
            for root, dirs, files in os.walk(cache_files['chrome']):
                for file in files:
                    cache_data.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error reading Chrome cache: {e}")
    
    # Extract Firefox cache
    if os.path.exists(cache_files['firefox']):
        try:
            profile_path = glob.glob(cache_files['firefox'] + r'\*\cache2\entries')[0]
            for root, dirs, files in os.walk(profile_path):
                for file in files:
                    cache_data.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error reading Firefox cache: {e}")
    
    # Extract Edge cache
    if os.path.exists(cache_files['edge']):
        try:
            for root, dirs, files in os.walk(cache_files['edge']):
                for file in files:
                    cache_data.append(os.path.join(root, file))
        except Exception as e:
            print(f"Error reading Edge cache: {e}")
    
    return history_data, cookies_data, cache_data

def save_to_csv(history_data, cookies_data, cache_data):
    # Save history data to CSV
    with open("browser_history.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])
        for url in history_data:
            writer.writerow([url])
    
    # Save cookies data to CSV
    with open("browser_cookies.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Host", "Name", "Value"])
        for cookie in cookies_data:
            writer.writerow([cookie['host'], cookie['name'], cookie['value']])
    
    # Save cache data to CSV
    with open("browser_cache.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Path"])
        for cache_file in cache_data:
            writer.writerow([cache_file])

def main():
    history_data, cookies_data, cache_data = get_browser_history()
    save_to_csv(history_data, cookies_data, cache_data)

if __name__ == "__main__":
    main()