import os
# Set env var for GCP
os.environ['GCP_PROJECT_ID'] = 'k-trend-autobot'

from src.storage_manager import StorageManager
print("Initializing StorageManager...")
storage = StorageManager()
print("Initialized!")

print("Calling get_edit_session...")
try:
    session = storage.get_edit_session('Ubd61e83e61bbe07d8df7c6a2a62c0a72')
    print("Session:", session)
except Exception as e:
    print("Exception thrown:", repr(e))
