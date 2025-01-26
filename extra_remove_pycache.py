import os
import shutil

def remove_pycache(directory):
    for root, dirs, files in os.walk(directory):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removing {pycache_path}")
            shutil.rmtree(pycache_path)

if __name__ == "__main__":
    # Specify the directory you want to clean (current directory in this case)
    target_directory = os.getcwd()
    
    # Call the function to remove __pycache__ directories
    remove_pycache(target_directory)
    
    print("All __pycache__ directories have been removed.")