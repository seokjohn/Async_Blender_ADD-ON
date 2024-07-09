import requests
import traceback
from . import update_global_status_msg


async def download_file(url, save_file_path):
    try:
        update_global_status_msg("Downloading File")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=2048): 
                    file.write(chunk)
        update_global_status_msg("Downloaded File")
    except Exception:
        traceback.print_exc()
    else:
        update_global_status_msg("Failed to Download File")
