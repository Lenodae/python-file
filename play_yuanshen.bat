@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 原神 — 一键启动 / 下载安装

echo ==========================================
echo   原神 — 一键启动 / 下载安装
echo ==========================================
echo.

:: ============================================================
::  第零步：检测是否已安装原神，有就直接打开
:: ============================================================
set "GAME_FOUND="

:: 搜索常见安装路径（多盘符、多目录模式）
for %%D in (C D E F G H) do (
    for %%P in (
        "%%D:\Program Files\Genshin Impact\Genshin Impact Game"
        "%%D:\Genshin Impact\Genshin Impact Game"
        "%%D:\Program Files (x86)\Genshin Impact\Genshin Impact Game"
    ) do (
        if exist "%%~P\YuanShen.exe" (
            set "GAME_PATH=%%~P\YuanShen.exe"
            set "GAME_FOUND=1"
        )
    )
)

:: 找到了 — 直接启动游戏
if defined GAME_FOUND (
    echo [√] 检测到原神已安装！
    echo     路径: !GAME_PATH!
    echo.
    echo 正在启动原神，祝你游戏愉快！
    start "" "!GAME_PATH!"
    timeout /t 3 >nul
    exit /b 0
)

:: ============================================================
::  第一步：没找到游戏，检查启动器是否已安装
:: ============================================================
set "LAUNCHER_FOUND="
set "LAUNCHER_PATH=C:\Program Files\miHoYo Launcher\launcher.exe"

if exist "!LAUNCHER_PATH!" set "LAUNCHER_FOUND=1"
if not defined LAUNCHER_FOUND (
    if exist "C:\Program Files\Genshin Impact\launcher.exe" (
        set "LAUNCHER_PATH=C:\Program Files\Genshin Impact\launcher.exe"
        set "LAUNCHER_FOUND=1"
    )
)

if defined LAUNCHER_FOUND (
    echo [√] 未找到原神游戏，但启动器已安装
    echo     路径: !LAUNCHER_PATH!
    echo.
    set /p SKIP="是否打开启动器下载原神？(Y/n): "
    if /i "!SKIP!"=="" set "SKIP=y"
    if /i "!SKIP!"=="y" (
        echo 正在打开启动器...
        start "" "!LAUNCHER_PATH!"
        echo 请在启动器中登录并下载原神（约 70GB+）。
    )
    pause
    exit /b 0
)

:: ============================================================
::  第二步：什么都没有，下载安装启动器
:: ============================================================
echo [!] 未检测到原神或启动器，开始下载安装...
echo.

set "OUTPUT=%USERPROFILE%\Downloads\mihoyo_launcher_setup.exe"
set "URL=https://hyp-webstatic.mihoyo.com/hyp-client/hyp_cn_setup_1.4.5.exe"
set "FALLBACK_URL=https://launcher.mihoyo.com/"

echo [*] 下载地址: !URL!
echo [*] 保存位置: !OUTPUT!
echo [*] 文件大小: 约 169 MB
echo.
echo 正在下载米哈游启动器，请耐心等待...
echo.

powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'Continue'; try { Invoke-WebRequest -Uri '!URL!' -OutFile '!OUTPUT!' } catch { Write-Host 'FAILED'; exit 1 }"

if !ERRORLEVEL! NEQ 0 (
    echo.
    echo 下载失败，正在打开官方下载页面...
    start "" "!FALLBACK_URL!"
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   下载完成，正在静默安装启动器...
echo ==========================================
echo.

"!OUTPUT!" /S

:: 等待安装完成（最多 60 秒）
set /a COUNT=0
:WAIT_LOOP
timeout /t 2 /nobreak >nul
set /a COUNT+=2
if exist "!LAUNCHER_PATH!" goto :INSTALL_DONE
if !COUNT! LSS 60 goto :WAIT_LOOP

:INSTALL_DONE
if exist "!LAUNCHER_PATH!" (
    echo [√] 安装成功！
    echo.
    echo ==========================================
    echo   正在打开米哈游启动器...
    echo ==========================================
    echo.
    echo 请在启动器中：
    echo   1. 登录你的米哈游账号
    echo   2. 在原神右侧点击「下载」
    echo   3. 等待游戏下载完成（约 70GB+）
    echo.
    start "" "!LAUNCHER_PATH!"
) else (
    echo [!] 自动安装可能未完成。
    echo     请检查开始菜单中的「米哈游启动器」并手动打开。
)

:: 清理
echo.
set /p DEL="是否删除安装包以释放空间？(Y/n): "
if /i "!DEL!"=="" set "DEL=y"
if /i "!DEL!"=="y" (
    del "!OUTPUT!"
    echo [√] 已删除安装包
)

echo.
echo 全部完成！
pause
