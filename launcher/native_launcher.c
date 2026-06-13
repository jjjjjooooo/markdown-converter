#include <mach-o/dyld.h>
#include <libgen.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    char executable_path[PATH_MAX];
    uint32_t size = sizeof(executable_path);

    if (_NSGetExecutablePath(executable_path, &size) != 0) {
        return 1;
    }

    char real_executable_path[PATH_MAX];
    if (realpath(executable_path, real_executable_path) == NULL) {
        return 1;
    }

    char *macos_dir = dirname(real_executable_path);
    char script_path[PATH_MAX];
    if (snprintf(script_path, sizeof(script_path), "%s/launcher", macos_dir) >= (int)sizeof(script_path)) {
        return 1;
    }

    execl("/bin/zsh", "zsh", script_path, NULL);
    return 1;
}
