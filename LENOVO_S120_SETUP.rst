Installation and setup of Ubuntu 18.04 on Lenovo s120
=====================================================
#. Create a bootable usb stick for Ubuntu 18.04.
#. Connect the USB stick to the laptop.
#. Press laptop's power button and press and hold the FN and F12 key until the
   UEFI boot options appears.
#. Select the Ubuntu USB Stick.
#. Wait for the installation options to appear and choose "Install Ubuntu".
#. Pick Language (English).
#. Choose the appropriate keyboard (Danish)
#. Choose "Minimal installation"
	- Tick the Download updates while installing
	- Tick Install Third-party software
	- Write a password you can remember for the secure boot (this will only be
      used once during the installation).
#. Pick name and laptop name (I used bunny-bone-laptop-1) username (bunny) and
   password.
#. Choose Erase disk and Install Ubuntu
#. Pick the correct timezone.
#. Wait for the installation to complete.
#. Once complete click the reboot button and unplug the USB stick once asked.
#. When the installation completes you can install openssh-server to continue
   the installation remotely.
#. Go to settings and search for Power. From here disable the Wifi and Bluetooth
   power save.
#. Go to settings and search for Privacy. From here you can disable the Screen
   Lock.
#. If you don't want the laptop to suspend when closing the lid:
   - open Ubuntu software
   - find and install GNOME Tweaks
   - launch GNOME Tweaks
   - search for "lid" and un-tick Suspend when laptop lid is closed.
#. If you want the right click to be in the right side of the mouse pad, use
   GNOME Tweaks to fix this as well. Otherwise two fingered clicks will perform
   right click.

You are now ready to setup the bunny bone python application.

Setup Scheduled Reboots
-----------------------
When running the application it was discovered that occasionally the machine's
bluetooth would stop working.
A reboot fixes the issue until it appears again.

The root to this issue haven't been found, so instead the issue is fixed
with scheduled reboots every 6 hours, at 00:00, 06:00, 12:00, 18:00.

This section will explain how to set this up.

Run the following command to open a cron tab for the root user::

    sudo crontab -e

Go to the buttom of the file and insert this::

    0 */6 * * * sudo shutdown -r

The machine will now reboot every 6 hours.

To make the appliaction start with the laptop do as follows:

#. Open "Startup Applications"
#. Click Add
#. For Name: Bunny Bone
#. For Command: /usr/bin/gnome-terminal -- $BASEDIR/start.sh, Where `$BASEDIR`
   is replaced with this directory, i.e., the directory of the start.sh script
   after running install.sh.
#. For Comment: Starts Bunny Bone
#. Click Add
#. Click Close

The machine will now start the bunny bone application on startup.
