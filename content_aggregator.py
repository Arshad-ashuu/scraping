# import time
# from categories import main

# def get_part_details(part_name, part_cat):
#     part_name = part_name.strip().lower()
#     start_time = time.time()
#     part_list = main.get_part_list(part_name, part_cat)
#     print("Time Taken", time.time()-start_time)
#     return part_list

import time
from categories import main

def get_part_details(part_name, part_cat):
    """
    Fetches part details from relevant websites based on the category.

    Args:
        part_name: The name of the part to search for.
        part_cat: The category of the part (e.g., "cloths").

    Returns:
        A list of Part objects containing product details.
    """
    part_name = part_name.strip().lower()
    start_time = time.time()

    try:
        part_list = main.get_part_list(part_name, part_cat)
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []  # Return an empty list on error

    elapsed_time = time.time() - start_time
    print(f"Time Taken: {elapsed_time:.2f} seconds") 

    return part_list