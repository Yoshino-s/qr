pkg install python python-dev -y
pkg install curl wget git -y
pip install requests
wget https://raw.githubusercontent.com/Yoshino-s/qr/master/sources.list
wget https://raw.githubusercontent.com/Yoshino-s/qr/master/sop.py 
cp ~/../usr/etc/apt/sources.list ~/../usr/etc/apt/sources.list 
cp ./sources.list ~/../usr/etc/apt/sources.list 
termux-setup-storage
mkdir /sdcard/sop/
ln /sdcard/sop/ sop -s 
cp ./sop.py ~/sop/sop.py 
echo "Success"
