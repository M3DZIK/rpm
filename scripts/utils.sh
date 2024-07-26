#!/bin/bash

# Get version from spec file
# example: version=$(spec_get_version test.spec)
spec_get_version() {
  local version;
  version="$(cat $1 | grep Version: | awk '{print $2}')"
  echo "$version"
}

# Get epoch from spec file
# example: epoch=$(spec_get_epoch test.spec)
spec_get_epoch() {
  local epoch;
  epoch="$(cat $1 | grep Epoch: | awk '{print $2}')"
  echo "$epoch"
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
  sed -i "s/^Version: .*/Version: $2/" "$1"
  sed -i "s/^Release: .*/Release: 1%{?dist}/" "$1"
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

parse_config() {
  local package="$1"

  config=$(
    . "$package/updater.conf"
    echo "local COPR=$COPR"
    echo "local TYPE=$TYPE"
    echo "local JETBRAINS_CODE=$JETBRAINS_CODE"
    echo "local JETBRAINS_TYPE=$JETBRAINS_TYPE"
    echo "local GITHUB_REPO=$GITHUB_REPO"
    echo "local GIT_REPO=$GIT_REPO"
    echo "local PYPI_NAME=$PYPI_NAME"
    echo "local CRATE_NAME=$CRATE_NAME"
    echo "local CUSTOM=$CUSTOM"
  )
  eval "$config"

  echo "local COPR=$COPR"
  echo "local TYPE=$TYPE"
  echo "local JETBRAINS_CODE=$JETBRAINS_CODE"
  echo "local JETBRAINS_TYPE=$JETBRAINS_TYPE"
  echo "local GITHUB_REPO=$GITHUB_REPO"
  echo "local GIT_REPO=$GIT_REPO"
  echo "local PYPI_NAME=$PYPI_NAME"
  echo "local CRATE_NAME=$CRATE_NAME"
  echo "local CUSTOM=$CUSTOM"
}

# Compare two versions, return 1 if they are the same or 0 if they are different
# example: compare_version $old_version $new_version
compare_version() {
  local old="$1"
  local new="$2"

  if [[ -z "$new" || "$new" == "null" ]]; then
    echo "[!] Latest version is empty or null"
    return 0
  fi

  if eval "$SCRIPT_DIR/compare-versions.py" "$old" "$new"; then
    return 0
  else
    return 1
  fi
}
