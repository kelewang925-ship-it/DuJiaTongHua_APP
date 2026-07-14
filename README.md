"# DuJiaTongHua_APP"  

如果你正在使用代理软件

例如 Clash、V2Ray、Nekoray 等，先查看代理软件的 HTTP 端口。

假设 HTTP 端口是 7890：

git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

然后测试：

git ls-remote https://github.com/kelewang925-ship-it/DuJiaTongHua_APP.git

如果能输出 commit 和分支信息，再执行：

git push

注意，不同软件端口不一定是 7890，也可能是 10809、1080 或其他端口。