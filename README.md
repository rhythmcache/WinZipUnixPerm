# WinZipUnixPerm
Apply Linux attributes and permissions to the contents of a ZIP file directly from a Windows environment

# WinPerm (Experimental)

 A  tool to apply Linux-style attributes and permissions to the contents of a ZIP file directly from a Windows environment.  

⚠️ **This is an experimental build**. Functionality is not guaranteed, and unexpected behavior may occur.

## Usage

### General Syntax

```
winperm <path_to_zip> <dir_perm> <file_perm>
```
###### Example 
To apply 755 permissions to directories and 644 permissions to files in a ZIP located at "C:\Users\Admin\Downloads\example.zip"

- Open Command Prompt in the directory where winperm is located.
- Run the following command:
```
winperm "C:\Users\Admin\Downloads\example.zip" 755 644
```
, now that zip when extracted on linux , it will have 644 and 755 permissions


