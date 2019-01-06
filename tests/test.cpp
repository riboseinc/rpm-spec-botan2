#include <cassert>

#include <botan/version.h>

int main(int argc, char *argv[]) {
    assert(Botan::version_major() == 2);
    assert(Botan::short_version_string()[0] == '2');
}

