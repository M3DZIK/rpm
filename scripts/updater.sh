#!/bin/bash

set -e

SCRIPT_DIR="$(realpath "$(dirname "$0")")"

USER="Oskar Karpiński <karpinski.oskar@proton.me>"

source "$SCRIPT_DIR/utils.sh"

update_package() {
  local package="$1"
  local spec_file="$package/$package.spec"

  echo "Checking package: $package"

  local spec_version;
  local spec_epoch;
  local spec_build;
  # local spec_commit;
  spec_version=$(spec_get_version "$spec_file")
  spec_epoch=$(spec_get_epoch "$spec_file")
  spec_build=$(spec_get_global "$spec_file" build_ver)
  # spec_commit=$(spec_get_global "$spec_file" git_commit)

  eval "$(parse_config "$package")"

  local latest_version;
  local latest_build;
  if [ "$TYPE" == "jetbrains" ]; then
    eval "$(latest_jetbrains_version "$JETBRAINS_CODE" "$JETBRAINS_TYPE")"
  # elif [ "$TYPE" == "github" ]; then
  #   eval "$(latest_github_version "$GITHUB_REPO")"
  # elif [ "$TYPE" == "github-tag" ]; then
  #   eval "$(latest_github_tag_version "$GITHUB_REPO")"
  # elif [ "$TYPE" == "github-git" ]; then
  #   eval "$(latest_github_git_version "$GITHUB_REPO")"
  # elif [ "$TYPE" == "git" ]; then
  #   eval "$(latest_git_version "$GIT_REPO")"
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

  # if [ -n "$spec_commit" ]; then
  #   if [[ -z "$latest_hash" || "$latest_hash" == "null" ]]; then
  #     echo "[!] Failed to get latest build of $package"
  #     return 1
  #   fi
  # fi

  echo "Latest Version: $latest_version"
  if [ -n "$latest_build" ]; then
    echo "Latest Build: $latest_build"
  fi

  if [ -n "$spec_pypi_version" ]; then
    spec_version="$spec_pypi_version"
  fi

  # if [ "$TYPE" == "git" ]; then
  #   if [ "$spec_version" == "$latest_version" ] ; then
  #     return 0
  #   fi
  # else
  #   if ! eval compare_version "$spec_version" "$latest_version"; then
  #     return 0
  #   fi
  # fi

  if [ "$spec_version" == "$latest_version" ] ; then
    return 0
  fi

  # local changelog
  # if [ -z "$spec_build" ]; then
  #   changelog="$latest_version"
  # else
  #   changelog="$latest_version ($latest_build)"
  # fi

  spec_write_version "$spec_file" "$latest_version"
  if [ -n "$spec_build" ]; then
    spec_write_global "$spec_file" build_ver "$latest_build"
  fi
  # if [ -n "$spec_commit" ]; then
  #   spec_write_global "$spec_file" git_commit "$latest_hash"
  # fi

  full_version_latest="$latest_version-1"
  if [ -n "$spec_epoch" ]; then
    full_version_latest="$spec_epoch:$full_version_latest"
  fi

  # spec_write_changelog "$spec_file" "$full_version_latest" "$changelog"

  git add .
  git commit -m "$package: Update to $latest_version"
  git push

  if [ "$COPR" == "jetbrains" ]; then
    curl -X POST "$WEBHOOK_JETBRAINS/$package"
  fi

  echo "Committed"
}

latest_jetbrains_version() {
  local json;
  local version;
  local build;

  local code="$1"

  local type="$JETBRAINS_TYPE"
  if [ -z "$type" ]; then
    type="release"
  fi

  json="$(curl -s 'https://data.services.jetbrains.com/products/releases?code='"$code"'&latest=true&type='"$type"'')"
  version="$(printf "%s" "$json" | jq -r '.'"$code"'[0].version')"
  build="$(printf "%s" "$json" | jq -r '.'"$code"'[0].build')"

  echo "local latest_version=$version"
  echo "local latest_build=$build"
}

# latest_github_version() {
#   local json;
#   local tag;
#   local version;

#   local repo="$1"

#   json="$(curl -s 'https://api.github.com/repos/'"$repo"'/releases/latest')"
#   tag="$(printf "%s" "$json" | jq -r '.tag_name')"
#   version="${tag/v/}"

#   echo "local latest_version=$version"
# }

# latest_github_tag_version() {
#   local json;
#   local tag;
#   local version;

#   local repo="$1"

#   json="$(curl -s 'https://api.github.com/repos/'"$repo"'/tags')"
#   tag="$(printf "%s" "$json" | jq -r '[.[]][0].name')"
#   version="${tag/v/}"

#   echo "local latest_version=$version"
# }

# latest_github_git_version() {
#   local count;
#   local latest_sha;

#   local repo="$1"

#   count="$(curl -I -k 'https://api.github.com/repos/'"$repo"'/commits?per_page=1' | sed -n '/^[Ll]ink:/ s/.*"next".*page=\([0-9]*\).*"last".*/\1/p')"
#   latest_sha="$(curl -s 'https://api.github.com/repos/'"$repo"'/commits?per_page=1' | jq -r '[.[]][0].sha')"

#   echo "local latest_version=0.0.0.${count}.${latest_sha:0:6}"
#   echo "local latest_hash=$latest_sha"
# }

# latest_git_version() {
#   local current_dir;
#   local tmp_dir;
#   local version;

#   local repo="$1"

#   current_dir="$(pwd)"
#   tmp_dir="$(mktemp -d)"

#   git clone "$repo" "$tmp_dir"

#   cd "$tmp_dir"
#   version="$(git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g')"
#   hash=$(git rev-parse HEAD)
#   cd "$current_dir"

#   echo "local latest_version=${version/v/}"
#   echo "local latest_hash=$hash"
# }

if [ -n "$1" ]; then
  for package in "$@"; do
    if [[ ! -e "$package/updater.conf" ]]; then
      continue
    fi

    update_package "$package"
  done
else
  for package in *; do
    if [[ ! -e "$package/updater.conf" ]]; then
      continue
    fi

    update_package "$package"
  done
fi
