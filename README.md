# WinZipUnixPerm
Apply Linux attributes and permissions to the contents of a ZIP file directly from a Windows environment

# WinZipUnixPerm (Experimental)

 A  simpl tool to apply Linux-style attributes and permissions to the contents of a ZIP file directly from a Windows environment.  

⚠️ **This is an experimental build**. Functionality is not guaranteed, and unexpected behavior may occur.

## Usage

### General Syntax
- to apply permissions to every file and folder of zip
```
winzipunixperm <zip_path> <dir_perm> <file_perm>
```
- to apply permission to a single file/folder of zip
```
winzipunixperm -s <zip_path> <path_in_zip> <perm>
```

###### Example 
To apply 755 permissions to directories and 644 permissions to files in a ZIP located at "C:\Users\Admin\Downloads\example.zip"

- Open Command Prompt in the directory where winperm is located.
- Run the following command:
```
winperm "C:\Users\Admin\Downloads\example.zip" 755 644
```
, now that zip when extracted on linux , it will have 644 and 755 permissions

- To set permissions on a single file, here is an example command
```
python uniwinperm.py -s "zipfile.zip" "folder1/folder2/folder3/file.txt" 755
```
(Download Exe)[https://github.com/rhythmcache/WinZipUnixPerm/releases/download/v1/winzipunixperm.exe]




