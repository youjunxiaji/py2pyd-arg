@echo off

REM 切换到 UTF-8 编码
chcp 65001

REM 获取当前批处理文件所在的目录
set "current_dir=%~dp0"

REM 创建输出目录（如果不存在）
if not exist "%current_dir%output" mkdir "%current_dir%output"

REM 执行PyInstaller命令
pyinstaller ^
    --noconfirm ^
    --onedir ^
    --console ^
    --icon "E:\desktop\TOOLS\py2pyd-ui\window\transform.ico" ^
    --name "py2pyd" ^
    --add-data "%current_dir%module;module/" ^
    --distpath "%current_dir%output" ^
    "%current_dir%main.py"

REM 删除 build 文件夹（如果存在）
if exist "build" rmdir /s /q "build"

REM 删除以spec结尾的文件
del /f /s /q *.spec

REM 加密代码
python main.py -f "%current_dir%output\main\_internal" -d

REM 打包成安装文件
"D:\Inno Setup 6\ISCC.exe" "%current_dir%py2pyd.iss"
