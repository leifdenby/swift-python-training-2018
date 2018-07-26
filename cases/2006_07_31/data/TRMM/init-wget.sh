# https://disc.gsfc.nasa.gov/data-access#windows_wget

TEST_URL=https://acdisc.gesdisc.eosdis.nasa.gov/data//Aqua_AIRS_Level3/AIRX3STD.006/2006/AIRS.2006.12.31.L3.RetStd001.v6.0.9.0.G13155192744.hdf
USER=$1
PASSWORD=$2

cd $HOME
echo "machine urs.earthdata.nasa.gov login $USER password $PASSWORD" >> .netrc
chmod 0600 .netrc

touch .urs_cookies
#wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition $TEST_URL
