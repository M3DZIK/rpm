# Automatically Updated RPM Repositories

This guide outlines how to add and utilize automatically updated RPM repositories from the COPR project (Community Owned Package Repositories).

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
