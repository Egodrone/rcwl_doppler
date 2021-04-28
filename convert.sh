cd ./records;
for f in *.h264;do
echo $f;
tmp=${f::-5};
echo $tmp;
sudo MP4Box -fps 30 -add $f $PWD/../converted/$tmp.mp4;
done;
