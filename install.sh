#!/bin/bash
echo "Creating output directory"
mkdir -p ~/Desktop/bunny-bone-results
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
BASEDIR=$(dirname "$SCRIPT")

echo "Creating start script"
echo "#!/bin/bash" > ./start.sh
echo "source $BASEDIR/bluetooth/bin/activate" >> ./start.sh
echo "python3 $BASEDIR/main.py $BASEDIR//conf.cfg" >> ./start.sh
echo "sleep 3" >> ./start.sh
chmod +x ./start.sh


echo "Creating desktop entry.."
echo "[Desktop Entry]" > ~/Desktop/bunny-bone.desktop
echo "Name=Bunny Bone" >> ~/Desktop/bunny-bone.desktop
echo "Exec=$BASEDIR/start.sh" >> ~/Desktop/bunny-bone.desktop
echo "Icon=$BASEDIR/icon.png" >> ~/Desktop/bunny-bone.desktop
echo "Terminal=true" >> ~/Desktop/bunny-bone.desktop
echo "Type=Application" >> ~/Desktop/bunny-bone.desktop

chmod +x ~/Desktop/bunny-bone.desktop



echo "Installation complete"