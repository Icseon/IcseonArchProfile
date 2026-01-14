from archinstall import Install, Profile, hardware

class IcseonArchProfile(Profile):

    def __init__(self):

        # Base packages.
        base_packages = [
            "base",
            "base-devel",
            "linux",
            "linux-firmware",
            "sudo",
            "git"
        ]

        # Will be populated dynamically.
        driver_packages = []

        # Only install nvidia drivers if we have the hardware for it.
        if hardware.has_nvidia():

            # Nvidia drivers.
            driver_packages += [
                "nvidia-utils",
                "lib32-nvidia-utils",
                "nvidia",
                "nvidia-settings"
            ]

        # Desktop environment.
        desktop_env_packages = [
            "gnome",
            "gdm"
        ]

        # Audio playback.
        audio_packages = [
            "pipewire",
            "pipewire-alsa",
            "pipewire-pulse",
            "wireplumber"
        ]

        # Fonts, including emojis and CJK.
        font_packages = [
            "noto-fonts",
            "noto-fonts-cjk",
            "noto-fonts-emoji"
        ]

        # Networking. Bluetooth included.
        networking_packages = [
            "networkmanager",
            "bluez",
            "bluez-utils"
        ]

        # Applications I prefer to have pre-installed.
        applications = [
            "micro",
            "nano",
            "chromium",
            "firefox",
            "wine",
            "openssh",
            "ntfs-3g"
        ]

        # Construct superclass.
        super().__init__(

            # Metadata.
            name="IcseonArch",
            description="Icseon's Arch Linux installation",

            # Target packages.
            packages=(
                base_packages
                + driver_packages
                + desktop_env_packages
                + audio_packages
                + font_packages
                + networking_packages
                + applications
            ),

            # Default enabled services.
            services=[
                "NetworkManager",
                "gdm",
                "bluetooth"
            ]

        )

    def post_install(self, install_session):
        """
        Post installation script.
        :param install_session:
        :return:
        """

        # Set default editor to micro.
        install_session.arch_chroot("echo 'export EDITOR=micro' > /etc/profile.d/editor.sh")

        # Enable multilib (32 bit packages) - and install wine32.
        install_session.arch_chroot("sed -i \"/\[multilib\]/,/Include/\"'s/^#//' /etc/pacman.conf")
        install_session.arch_chroot("pacman -Syu wine32")

profile = IcseonArchProfile()
installer = Install(profile)
installer.run()