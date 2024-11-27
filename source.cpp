#include <iostream>
#include <string>
#include <cstdlib>
#include <zip.h> // Requires libzip

#include <windows.h>

bool is_admin() {
    // Check if the program is running with administrator privileges
    BOOL isAdmin = FALSE;
    HANDLE token = NULL;

    if (OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY, &token)) {
        TOKEN_ELEVATION elevation;
        DWORD size;
        if (GetTokenInformation(token, TokenElevation, &elevation, sizeof(elevation), &size)) {
            isAdmin = elevation.TokenIsElevated;
        }
        CloseHandle(token);
    }

    return isAdmin;
}

void set_unix_attributes(const std::string &zip_path, uint32_t dir_mode, uint32_t file_mode) {
    int error = 0;
    zip_t *zip = zip_open(zip_path.c_str(), ZIP_CREATE, &error);

    if (!zip) {
        std::cerr << "Failed to open ZIP archive: " << zip_path << std::endl;
        return;
    }

    zip_int64_t num_entries = zip_get_num_entries(zip, ZIP_FL_UNCHANGED);

    for (zip_uint64_t i = 0; i < num_entries; ++i) {
        struct zip_stat st;
        zip_stat_init(&st);

        if (zip_stat_index(zip, i, ZIP_FL_UNCHANGED, &st) != 0) {
            std::cerr << "Failed to get file stats for index " << i << std::endl;
            continue;
        }

        std::string name = st.name;
        bool is_directory = (name.back() == '/');

        uint32_t mode = is_directory ? dir_mode : file_mode;
        uint32_t external_attributes = (mode << 16);

        if (zip_file_set_external_attributes(zip, i, ZIP_FL_UNCHANGED, ZIP_OPSYS_UNIX, external_attributes) != 0) {
            std::cerr << "Failed to set attributes for: " << name << std::endl;
        }
    }

    if (zip_close(zip) != 0) {
        std::cerr << "Failed to close ZIP archive: " << zip_path << std::endl;
    }
}

int main(int argc, char *argv[]) {
    if (!is_admin()) {
        std::cerr << "This program must be run with administrative privileges." << std::endl;
        return 1;
    }

    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <path_to_zip> <dir_mode> <file_mode>" << std::endl;
        std::cerr << "Example: " << argv[0] << " archive.zip 755 644" << std::endl;
        return 1;
    }

    std::string zip_path = argv[1];
    uint32_t dir_mode = std::stoi(argv[2], nullptr, 8);
    uint32_t file_mode = std::stoi(argv[3], nullptr, 8);

    set_unix_attributes(zip_path, dir_mode, file_mode);

    std::cout << "Successfully applied permissions to all entries in " << zip_path << std::endl;
    return 0;
}
