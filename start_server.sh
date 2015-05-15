current_dir=$(pwd)
echo 'Enter the number of servers'
read servers
for i in `seq 1 $servers`
do
	osascript -e 'tell application "Terminal" to do script "python '$current_dir'/server.py '$i'"'
done  
