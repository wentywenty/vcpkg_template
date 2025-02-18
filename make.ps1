# 设置 PowerShell 输出编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

.\.venv\Scripts\activate    # 激活虚拟环境
python getenv.py    # 获取环境变量
.\env.ps1    # 加载环境变量
############################################################
# 开始编译
############################################################

# 生成 Visual Studio 项目
cmake -G "Visual Studio 17 2022" -A Win32 --preset=default .

# cmake --build build --config Release -- /p:Platform=Win32   
cmake --build build --config Debug -- /p:Platform=Win32   
