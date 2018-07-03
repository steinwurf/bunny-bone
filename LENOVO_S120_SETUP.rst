Installation and setup of Ubuntu 18.04 on Lenovo s120
=====================================================
1. Create a bootable usb stick for Ubuntu 18.04.
2. Connect the USB stick to the laptop.
3. Press laptop's power button and press and hold the FN and F12 key until the UEFI boot options appears.
4. Select the Ubuntu USB Stick.
5. Wait for the installation options to appear and choose "Install Ubuntu".
6. Pick Language (English).
7. Choose the appropriate keyboard (Danish)
8. Choose "Minimal installation"
	- Tick the Download updates while installing
	- Tick Install Third-party software
	- Write a password you can remember for the secure boot (this will only be used once during the installation).
9. Pick name and laptop name (I used bunny-bone-laptop-1) username (bunny) and password.
10. Choose Erase disk and Install Ubuntu
11. Pick the correct timezone.
12. Wait for the installation to complete.
13. Once complete click the reboot button and unplug the USB stick once asked.
14. When the installation completes you can install openssh-server to continue the installation remotely.
15. Go to settings and search for Power. From here disable the Wifi and Bluetooth power save.
15. Go to settings and search for Privacy. From here you can disable the Screen Lock.
16. If you don't want the laptop to suspend when closing the lid:
    - open Ubuntu software
    - find and install GNOME Tweaks
    - launch GNOME Tweaks
    - search for "lid" and un-tick Suspend when laptop lid is closed.
17.  If you want the right click to be in the right side of the mouse pad, use GNOME Tweaks to fix this as well. Otherwise two fingered clicks will perform right click.

You are now ready to setup the bunny bone python application.

