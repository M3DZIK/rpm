# Automatically Updated RPM Repositories

This repository provides configuration files to automatically update RPM packages hosted on the COPR (Community Owned Package Repositories) project using GitHub Actions. 

By leveraging GitHub Actions, these configurations enable you to keep your development environment up-to-date with the latest versions of the packages you rely on. 

**The auto-update task is scheduled to run every 6 hours, ensuring that all packages remains up-to-date.**

## Adding a Repository

1. **Open a terminal window.**
2. **Execute the following command, replacing `<repository name>` with the desired repository name:**

   ```bash
   sudo dnf copr enable medzik/<repository name>
   ```

    **Example**: To enable the JetBrains repository, use:

    ```bash
    sudo dnf copr enable medzik/jetbrains
    ```

## Installing Packages

Once a repository is enabled, you can install packages using the dnf install command:

```bash
sudo dnf install <package name>
```

**Example**: To install Android Studio from the JetBrains repository:

```bash
sudo dnf install android-studio
```

## Available Repositories

### Multiple Packages:

* [JetBrains](https://copr.fedorainfracloud.org/coprs/medzik/jetbrains/)

### Single Packages:

* [cloudflared](https://copr.fedorainfracloud.org/coprs/medzik/cloudflared/)
* [ktlint](https://copr.fedorainfracloud.org/coprs/medzik/ktlint/)
* [librepass](https://copr.fedorainfracloud.org/coprs/medzik/librepass/)
