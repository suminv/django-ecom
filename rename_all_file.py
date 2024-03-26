import os
import re

def rename_files(directory):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            match = re.search(r'ECommerce\s*#?(\d+)', filename)
            if match:
                number = match.group(1)
                new_filename = f"{number}_{filename}"
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                print(f"File renamed: {filename} -> {new_filename}")

directory = '/Users/vsumin/Downloads/python-lessons/django/ecom/'
rename_files(directory)
