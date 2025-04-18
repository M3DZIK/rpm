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
* [VSCode](https://copr.fedorainfracloud.org/coprs/medzik/vscode/)

### Single Packages:

* [cloudflared](https://copr.fedorainfracloud.org/coprs/medzik/cloudflared/)
* [ktlint](https://copr.fedorainfracloud.org/coprs/medzik/ktlint/)

## VSCode Repository Packages

* `code-oss`: The Open Source version of Visual Studio Code (vscode) editor
* `codium`: Free/Libre Open Source Software Binaries of VS Code

## JetBrains Repository Packages

The JetBrains repository offers the following development tools:

* `android-studio`: Android development IDE
* `android-studio-beta`: Beta version of Android Studio
* `android-studio-canary`: Cutting-edge canary build of Android Studio (potentially unstable)
* `aqua`: A powerful IDE for test automation by JetBrains
* `clion`: C and C++ IDE
* `dategrip`: Python IDE for data scientists
* `dataspell`: Data science IDE for Python
* `goland`: Go programming IDE
* `intellij-idea-community`: Free and open-source Java IDE (Compiled from source code on Fedora COPR)
* `intellij-idea-community-bin`: Free and open-source Java IDE (Official binaries from JetBrains build)
* `intellij-idea-ultimate`: Paid, feature-rich Java IDE
* `jetbrains-fleet`: Unified IDE for multiple languages
* `jetbrains-gateway`: Development environment for creating cross-platform apps
* `pycharm-community`: Free and open-source Python IDE (Compiled from source code on Fedora COPR)
* `pycharm-community-bin`: Free and open-source Python IDE (Official binaries from JetBrains build)
* `pycharm-professional`: Paid, feature-rich Python IDE
* `rider`: .NET development IDE
* `rubymine`: Ruby and Rails IDE
* `rustrover`: Rust IDE
* `webstorm`: JavaScript and web development IDE
