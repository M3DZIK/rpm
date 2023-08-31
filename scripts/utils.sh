#!/bin/bash

# Get version from spec file
# example: version=$(spec_get_version test.spec)
spec_get_version() {
    local version;
    version="$(cat $1 | grep Version: | awk '{print $2}')"
    echo "$version"
}

# Get value of global variable from spec file
# example: value=$(spec_get_global test.spec build_vers)
spec_get_global() {
    local value;
    value="$(cat $1 | grep "%global $2" | awk '{print $3}')"
    echo "$value"
}

# Write version to spec file
# example: spec_write_version test.spec 1.0.0
spec_write_version() {
    sed -i "s/^Version: .*/Version:       $2/" "$1"
}

# Write global variable to spec file
# example: spec_write_version test.spec build_vers 100
spec_write_global() {
    sed -i "s/^%global *$2 .*/%global $2 $3/" "$1"
}

# Write changelog to spec file
# example: spec_write_changelog test.spec 1.0.0 "1.0.0 (100)"
spec_write_changelog() {
    DATE="$(date "+%a %b %d %Y")"
    sed -i "s/^%changelog/%changelog\n\* $DATE $USER - $2\n- Update to $3\n/" "$1"
}
