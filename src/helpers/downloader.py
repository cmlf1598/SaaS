import requests
from pathlib import Path

def download_to_local(url:str, out_path:Path,
parent_mkdir:bool=True):
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be a valid pathlib.Path object")
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises an exception if status code is 4xx/5xx    
        out_path.write_bytes(response.content)  # use write_text() if it's plain text/utf-8
        return True
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False 