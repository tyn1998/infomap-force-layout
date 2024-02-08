import os


def green_print(text):
    print(f"\033[92m{text}\033[0m")


def get_org_files(events_dir):
    org_files = {}
    for org in os.listdir(events_dir):
        org_path = os.path.join(events_dir, org)
        if os.path.isdir(org_path):
            files = []
            for file_name in os.listdir(org_path):
                if file_name.endswith('.gml') and not file_name.startswith('.'):
                    files.append(file_name)
            org_files[org] = files
    return org_files


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
