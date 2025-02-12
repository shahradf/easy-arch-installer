import subprocess
from time import sleep

class Color:
    green = '\033[92m'
    red = '\033[91m'
    white = '\033[0m'

# Clear screen function
def clear_screen():
    subprocess.run("clear", shell=True)

# Display a message with a specific color
def print_message(message, color=Color.white):
    print(color + message + Color.white)

# Wait for a certain amount of time
def wait(seconds=3):
    sleep(seconds)

# Install packages with pacman and handle errors
def install_package(package):
    try:
        subprocess.run(f"sudo pacman -S {package} --noconfirm", shell=True, check=True)
    except subprocess.CalledProcessError:
        print_message(f"Error installing {package}", Color.red)

# Handle GPU driver installation
def install_gpu_driver(gpu_type):
    if gpu_type == "a":
        install_package("xf86-video-amdgpu")
    elif gpu_type == "i":
        install_package("xf86-video-intel")
    elif gpu_type == "n":
        install_package("xf86-video-nouveau")
    else:
        print_message("Invalid GPU option", Color.red)

# Install desktop environment packages
def install_desktop_environment(desktop):
    if desktop == "gnome":
        install_package("gnome gnome-extra")
        install_package("gdm")
        subprocess.run("sudo systemctl enable gdm", shell=True)
    elif desktop == "kde":
        install_package("plasma konsole dolphin")
        install_package("sddm")
        subprocess.run("sudo systemctl enable sddm", shell=True)
    elif desktop == "xfce":
        install_package("xfce4 xfce4-goodies")
        install_package("lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings")
        subprocess.run("sudo systemctl enable lightdm", shell=True)
    elif desktop == "i3":
        install_package("i3")
        install_package("sddm")
        subprocess.run("sudo systemctl enable sddm", shell=True)
    elif desktop == "mate":
        install_package("mate mate-extra")
        install_package("lightdm lightdm-gtk-greeter")
        subprocess.run("sudo systemctl enable lightdm", shell=True)
    else:
        print_message("Invalid desktop environment", Color.red)

# Main function to drive the installer
def main():
    clear_screen()

    print_message("Welcome to the Arch Linux Desktop Environment Installer", Color.green)
    wait(3)

    # Ask user to confirm password entry
    print_message("Please enter your password when prompted (for 'y' to continue)", Color.red)
    wait(10)

    # Update system
    install_package("xorg-server")

    print_message("Step 1: GPU driver installation", Color.green)
    wait(5)

    # Ask the user about the GPU
    print_message("Select your GPU type:", Color.green)
    print_message("[a] AMD, [i] Intel, [n] Nvidia", Color.red)
    gpu = input("Enter your GPU type (a/i/n): ").strip().lower()

    install_gpu_driver(gpu)

    print_message("Step 2: Select your desired desktop environment", Color.green)
    wait(3)

    # Ask user for the desktop environment
    print_message("Available Desktop Environments:", Color.red)
    print_message("[+] - gnome", Color.green)
    print_message("[+] - kde", Color.red)
    print_message("[+] - xfce", Color.green)
    print_message("[+] - i3", Color.red)
    print_message("[+] - mate", Color.green)

    desktop = input("Please type the desktop environment you'd like to install (gnome/kde/xfce/i3/mate): ").strip().lower()

    install_desktop_environment(desktop)

    # Reboot prompt
    reboot = input("If installation is complete, type 'y' to reboot: ").strip().lower()
    if reboot == "y":
        subprocess.run("reboot", shell=True)

if __name__ == "__main__":
    main()
