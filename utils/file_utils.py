"""
File utility functions for downloading and cleaning up files
"""
import os
import shutil
import urllib.request


def download_static_files(github_raw_base, github_files):
    """Download missing static files from GitHub"""
    missing_files = []

    # Check which files are missing
    for github_path, local_path in github_files.items():
        if not os.path.exists(local_path):
            missing_files.append((github_path, local_path))

    if not missing_files:
        print("✓ All static files present")
        return True

    print(f"Downloading {len(missing_files)} missing file(s) from GitHub...")

    for github_path, local_path in missing_files:
        try:
            url = f"{github_raw_base}/{github_path}"
            print(f"  Downloading: {github_path}")

            # Download file
            with urllib.request.urlopen(url) as response:
                content = response.read()

            # Save file
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(content)

            print(f"  ✓ Saved: {local_path}")
        except Exception as e:
            print(f"  ✗ Error downloading {github_path}: {e}")
            return False

    print("✓ All static files downloaded successfully")
    return True


def update_static_files(github_raw_base, github_files):
    """Force update all static files from GitHub"""
    print("Updating all static files from GitHub...")

    for github_path, local_path in github_files.items():
        try:
            url = f"{github_raw_base}/{github_path}"
            print(f"  Updating: {github_path}")

            # Download file
            with urllib.request.urlopen(url) as response:
                content = response.read()

            # Save file
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(content)

            print(f"  ✓ Updated: {local_path}")
        except Exception as e:
            print(f"  ✗ Error updating {github_path}: {e}")
            return False

    print("✓ All static files updated successfully")
    return True


def cleanup_temp_directory(temp_dir):
    """Clean up temporary directory to prevent accumulation of orphaned files"""
    try:
        if os.path.exists(temp_dir):
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error deleting {item_path}: {e}")
            print(f"Cleaned up temp directory: {temp_dir}")
    except Exception as e:
        print(f"Error cleaning temp directory: {e}")
