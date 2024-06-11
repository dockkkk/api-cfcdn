1，先安装pythone3

   sudo apt update

   sudo apt install python3

   sudo apt install python3-pip

2，上传py文件到服务器，windows，或者家用小主机支持py的都可以

   只需填写CF的api token，zone id，和解析域名

3，python3运行***.py文件

4，设置自动运行

   crontab -e
   
   0 */6 * * * /usr/bin/python3 /root/*****.py   #6小时运行一次



对接的api为https://api.345673.xyz/get_data
![image](https://github.com/dockkkk/api-cfcdn/assets/102992310/f99c5628-d88f-4e65-8e58-2185786ed142)


感谢isJielin大佬 ymyuuu大佬 提供的免费优选
