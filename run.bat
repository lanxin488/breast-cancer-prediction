@echo off
chcp 65001 >nul
echo ========================================
echo    乳腺癌预测系统 - 快速启动
echo ========================================
echo.
echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/3] 安装依赖包...
pip install -r requirements.txt

echo.
echo [3/3] 启动Flask应用...
echo.
echo ========================================
echo    系统启动中，请稍候...
echo    访问地址：http://127.0.0.1:5000
echo    按 Ctrl+C 停止服务
echo ========================================
echo.
python app.py

pause
