import os
import sys
import zipfile
import stat

def set_permissions_single(zip_path, target, perm):
    """
    Apply permissions to a single file or folder in the ZIP without altering others.
    """
    perm = int(perm, 8)
    temp_zip_path = zip_path + ".temp"
    target = target.replace("\\", "/")  # Normalize path for ZIP
    
    with zipfile.ZipFile(zip_path, 'r') as zip_read:
        with zipfile.ZipFile(temp_zip_path, 'w') as zip_write:
            for zip_info in zip_read.infolist():
                # Retain original attributes for non-target entries
                if zip_info.filename == target:
                    # Ensure the entry is marked as created on UNIX
                    zip_info.create_system = 3  # UNIX
                    
                    is_dir = zip_info.is_dir()
                    
                    # Set permissions
                    if is_dir:
                        zip_info.external_attr = (perm << 16) | stat.S_IFDIR
                    else:
                        zip_info.external_attr = (perm << 16) | stat.S_IFREG
                    
                    print(f"Applied permissions {oct(perm)} to {target}")
                
                # Write back to the new ZIP archive
                zip_write.writestr(zip_info, zip_read.read(zip_info.filename))
    
    os.replace(temp_zip_path, zip_path)
    print(f"Permissions updated successfully for {zip_path}")

def set_unix_permissions(zip_path, dir_perm, file_perm):
    """
    Apply permissions to all files and folders in the ZIP.
    """
    dir_perm = int(dir_perm, 8)
    file_perm = int(file_perm, 8)
    temp_zip_path = zip_path + ".temp"
    
    with zipfile.ZipFile(zip_path, 'r') as zip_read:
        with zipfile.ZipFile(temp_zip_path, 'w') as zip_write:
            for zip_info in zip_read.infolist():
                # Ensure the entry is marked as created on UNIX
                zip_info.create_system = 3  # UNIX
                
                # Determine if the item is a file or directory
                is_dir = zip_info.is_dir()
                
                # Set permissions
                if is_dir:
                    zip_info.external_attr = (dir_perm << 16) | stat.S_IFDIR
                else:
                    zip_info.external_attr = (file_perm << 16) | stat.S_IFREG
                
                # Write back to the new ZIP archive
                zip_write.writestr(zip_info, zip_read.read(zip_info.filename))
    
    os.replace(temp_zip_path, zip_path)
    print(f"Permissions updated successfully for {zip_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  winzipunixperm <zip_path> <dir_perm> <file_perm>")
        print("  winzipunixperm -s <zip_path> <path_in_zip> <perm>")
        sys.exit(1)
    
    if sys.argv[1] == "-s":
        # Single file/folder mode
        if len(sys.argv) != 5:
            print("Usage: winzipunixperm -s <zip_path> <path_in_zip> <perm>")
            sys.exit(1)
        
        zip_path = sys.argv[2]
        target = sys.argv[3]
        perm = sys.argv[4]
        
        if not os.path.exists(zip_path):
            print(f"Error: File {zip_path} does not exist.")
            sys.exit(1)
        if not perm.isdigit():
            print("Error: Permission should be numeric (e.g., 755, 644).")
            sys.exit(1)
        
        set_permissions_single(zip_path, target, perm)
    
    else:
        # Apply permissions to entire ZIP
        if len(sys.argv) != 4:
            print("Usage: winzipunixperm <zip_path> <dir_perm> <file_perm>")
            sys.exit(1)
        
        zip_path = sys.argv[1]
        dir_perm = sys.argv[2]
        file_perm = sys.argv[3]
        
        if not os.path.exists(zip_path):
            print(f"Error: File {zip_path} does not exist.")
            sys.exit(1)
        if not dir_perm.isdigit() or not file_perm.isdigit():
            print("Error: Permissions should be numeric (e.g., 755, 644).")
            sys.exit(1)
        
        set_unix_permissions(zip_path, dir_perm, file_perm)
