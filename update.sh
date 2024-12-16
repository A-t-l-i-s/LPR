
cd /root/LPR/

systemctl stop LPR
systemctl disable LPR


git fetch --all
git reset --hard
git pull


cp LPR.service /etc/systemd/systemd/

systemctl enable LPR
systemctl start LPR
