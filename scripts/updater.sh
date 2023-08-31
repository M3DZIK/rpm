#!/bin/bash

set -e

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

USER="M3DZIK <me@medzik.dev>"

source "$SCRIPT_DIR/utils.sh"

for pkg in *; do
    if [[ ! -e "$pkg/.updater" ]]; then
        continue
    fi

    . "$pkg/.updater"

    LATEST="$(curl -s 'https://data.services.jetbrains.com/products/releases?code='$CODE'&latest=true&type=release')"
    version="$(printf "%s" "${LATEST}" | jq -r '.'$CODE'[0].version')"
    build="$(printf "%s" "${LATEST}" | jq -r '.'$CODE'[0].build')"

    spec_version=$(spec_get_version $pkg/$pkg.spec)
    spec_build=$(spec_get_global $pkg/$pkg.spec build_vers)

    echo "$pkg: latest:  $version ($build)"
    echo "$pkg: current: $spec_version ($spec_build)"

    if [ "$spec_version $spec_build" != "$version $build" ]; then
        spec_write_version $pkg/$pkg.spec $version
        spec_write_global $pkg/$pkg.spec build_vers $build
        spec_write_changelog $pkg/$pkg.spec $version "$spec_version ($spec_build)"

        git add .
        git commit -m "$pkg: Update to ${version}"
        git push

        curl -X POST "$WEBHOOK/$pkg"
    fi
done
