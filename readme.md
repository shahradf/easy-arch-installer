# Arch Linux Desktop Installer Script

## Overview

This script automates the installation of a desktop environment on Arch Linux, streamlining the setup process for users. It supports multiple desktop environments and ensures that necessary drivers and packages are installed.

## Features

- **Desktop Environment Support**: Choose from KDE, GNOME, XFCE, i3, or MATE.
- **Graphics Driver Installation**: Automatically installs the appropriate graphics driver based on user input.
- **System Updates**: Performs system updates before installation.

## Prerequisites

- A running Arch Linux system.
- Sudo privileges.

## Installation

1. **Clone the Repository**:


   git clone https://github.com/shahradf/easy-arch-installer

    Navigate to the Script Directory:

cd easy-arch-installer

Usage

    Run the Script:

    python3 arch_installer.py

Follow the On-Screen Prompts:

    Password Prompt: Enter your password when prompted.
    Graphics Driver Selection: Choose your GPU type (AMD, Intel, or NVIDIA).
    Desktop Environment Selection: Choose your preferred desktop environment.

Reboot:

After installation, reboot your system to apply the changes.