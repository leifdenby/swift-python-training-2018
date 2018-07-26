# https://disc.gsfc.nasa.gov/data-access#windows_wget

wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition "$@"
