import os
import time

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{Color.RESET}")

def run_command(command, description=""):
    if description:
        print_colored(description, Color.GREEN)
    os.system(command)

def input_colored(prompt, color):
    return input(f"{color}{prompt}{Color.RESET}")

def setup_partitions():
    print("Please create your partitions as follows:")
    time.sleep(2)
    print("1. Create a SWAP partition twice the size of your RAM.")
    time.sleep(5)
    print("2. Create a BOOT partition of 1GB and set its type to EFI System.")
    time.sleep(5)
    print_colored("Note: If your system is NOT UEFI, do NOT create a boot partition.", Color.RED)
    time.sleep(5)
    print("3. Create a ROOT partition with the remaining space.")
    time.sleep(5)
    print("Proceeding to the partitioning interface...")
    time.sleep(3)

    run_command("sudo cfdisk /dev/sda", "Opening partitioning tool...")
    input_colored("Press Enter when you've finished partitioning: ", Color.RED)
    
    run_command("clear")
    run_command("lsblk", "Displaying your partitions...")

def format_partitions():
    boot = input_colored("Enter the BOOT partition (e.g., /dev/sda1): ", Color.GREEN)
    swap = input("Enter the SWAP partition (e.g., /dev/sda2): ")
    root = input_colored("Enter the ROOT partition (e.g., /dev/sda3): ", Color.RED)
    
    run_command(f"mkfs.fat -F32 {boot}", "Formatting BOOT partition...")
    run_command(f"mkswap {swap} && swapon {swap}", "Setting up SWAP partition...")
    run_command(f"mkfs.ext4 {root}", "Formatting ROOT partition...")

    run_command(f"mount {root} /mnt", "Mounting ROOT partition...")
    run_command("clear")

def install_base_system():
    configure_mirrors = input("Do you want to configure the mirror list? (y/n): ")
    if configure_mirrors.lower() == "y":
        run_command("sudo pacman -S nano --noconfirm", "Installing Nano editor...")
        run_command("clear")
        print_colored("Comment out slow/distant servers by adding '#' before 'Server' lines.", Color.RED)
        input("Press Enter to edit the mirror list: ")
        run_command("sudo nano /etc/pacman.d/mirrorlist")
        input_colored("Finished editing? Press Enter to continue: ", Color.GREEN)

    print_colored("Installing base system...", Color.GREEN)
    run_command("sudo pacstrap /mnt base base-devel linux linux-firmware")
    
    run_command("sudo genfstab -U /mnt >> /mnt/etc/fstab", "Generating fstab...")

def configure_system():
    run_command("sudo arch-chroot /mnt", "Entering chroot environment...")
    run_command('echo "arch-pc" | sudo tee /mnt/etc/hostname', "Setting hostname...")

    print("In the next editor, uncomment:")
    print_colored("en_US.UTF-8 UTF-8", Color.RED)
    input("Press Enter to edit locale settings: ")
    run_command("sudo nano /etc/locale.gen")
    run_command("locale-gen")
    run_command('echo "LANG=en_US.UTF-8" | sudo tee /etc/locale.conf')
    run_command("export LANG=en_US.UTF-8")

    run_command("sudo ln -sf /usr/share/zoneinfo/Asia/Tehran /etc/localtime", "Setting timezone...")
    run_command("hwclock --systohc --utc")

    run_command("sudo pacman -Syu --noconfirm", "Updating system...")
    input_colored("Press Enter to set ROOT password: ", Color.RED)
    run_command("sudo passwd")

def create_user():
    username = input_colored("Enter a new username: ", Color.RED)
    run_command(f"sudo useradd -m -G wheel,storage,power -s /bin/bash {username}", f"Creating user {username}...")
    run_command(f"sudo passwd {username}", f"Setting password for {username}...")

    print("Next, uncomment:")
    print_colored("%wheel ALL=(ALL) ALL", Color.RED)
    input("Press Enter to edit sudoers file: ")
    run_command("sudo nano /etc/sudoers")

def install_grub():
    is_uefi = input("Is your system UEFI? (y/n): ").lower()
    
    if is_uefi == "y":
        run_command("sudo pacman -S grub efibootmgr os-prober --noconfirm", "Installing GRUB for UEFI...")
        run_command("sudo mkdir /boot/EFI")
        boot_partition = input("Enter the BOOT partition (e.g., /dev/sda1): ")
        run_command(f"mount {boot_partition} /boot/EFI", "Mounting BOOT partition...")
        run_command("sudo grub-install --target=x86_64-efi --bootloader-id=GRUB --recheck")
    else:
        run_command("sudo pacman -S grub --noconfirm", "Installing GRUB for Legacy BIOS...")
        run_command("sudo grub-install --target=i386-pc --recheck /dev/sda")

    run_command("sudo grub-mkconfig -o /boot/grub/grub.cfg", "Generating GRUB configuration...")

def finalize_installation():
    run_command("sudo pacman -S networkmanager --noconfirm", "Installing Network Manager...")
    run_command("sudo systemctl enable NetworkManager", "Enabling Network Manager...")
    run_command("exit", "Exiting chroot...")
    run_command("sudo umount -a", "Unmounting partitions...")

    print_colored("Installation complete! Your system will reboot in 20 seconds...", Color.GREEN)
    time.sleep(20)
    run_command("sudo reboot")

def main():
    run_command("clear")
    print_colored("Welcome to the Arch Linux Installer!", Color.GREEN)
    
    setup_partitions()
    format_partitions()
    install_base_system()
    configure_system()
    create_user()
    install_grub()
    finalize_installation()

if __name__ == "__main__":
    main()
