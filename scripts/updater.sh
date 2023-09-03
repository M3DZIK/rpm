#!/bin/bash

set -e

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

USER="M3DZIK <me@medzik.dev>"

source "$SCRIPT_DIR/utils.sh"

update_package() {
  local package="$1"
  local spec_file="$package/$package.spec"

  echo "Checking package: $package"

  local spec_version;
  local spec_build;
  spec_version=$(spec_get_version "$spec_file")
  spec_build=$(spec_get_global "$spec_file" build_ver)

  eval "$(parse_config "$package")"

  local latest_version;
  local latest_build;
  if [ "$TYPE" == "jetbrains" ]; then
    eval "$(latest_jetbrains_version "$JETBRAINS_CODE")"
  elif [ "$TYPE" == "custom" ]; then
    latest_version=$("$package/$CUSTOM")
  fi

  if [[ -z "$latest_version" || "$latest_version" == "null" ]]; then
    echo "[!] Failed to get latest version of $package"
    return 1
  fi

  if [ -n "$spec_build" ]; then
    if [[ -z "$latest_build" || "$latest_build" == "null" ]]; then
      echo "[!] Failed to get latest build of $package"
      return 1
    fi
  fi

  echo "Latest Version: $latest_version"
  if [ -n "$latest_build" ]; then
    echo "Latest Build: $latest_build"
  fi

  if ! eval compare_version "$spec_version" "$latest_version"; then
    return 0
  fi

  local changelog
  if [ -z "$spec_build" ]; then
    changelog="$latest_version"
  else
    changelog="$latest_version ($latest_build)"
  fi

  spec_write_version "$spec_file" "$latest_version"
  if [ -n "$spec_build" ]; then
    spec_write_global "$spec_file" build_ver "$latest_build"
  fi
  spec_write_changelog "$spec_file" "$latest_version" "$changelog"

  git add .
  git commit -m "$package: Update to $latest_version"
  git push

  if [ "$COPR" == "jetbrains" ]; then
    curl -X POST "$WEBHOOK_JETBRAINS/$package"
  fi

  echo "Committed"
}

latest_jetbrains_version() {
  local latest_version;
  local latest_build;

  local code="$1"

  json="$(curl -s 'https://data.services.jetbrains.com/products/releases?code='"$code"'&latest=true&type=release')"
  version="$(printf "%s" "$json" | jq -r '.'"$code"'[0].version')"
  build="$(printf "%s" "$json" | jq -r '.'"$code"'[0].build')"

  echo "local latest_version=$version"
  echo "local latest_build=$build"
}

for package in *; do
  if [[ ! -e "$package/updater.conf" ]]; then
    continue
  fi

  update_package "$package"
done
