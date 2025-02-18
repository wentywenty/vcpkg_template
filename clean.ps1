# 主函数，根据参数调用不同的清理函数
param (
    [string]$cleanType = "medium"  # 默认是中编译清理
)

# 大编译清理
function Clean-FullBuild {
    Write-Host "Performing full build clean..."
    # 清理所有生成的文件和目录
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build/*
    Write-Host "Full build clean completed."
}

# 小编译清理
function Clean-SmallBuild {
    Write-Host "Performing small build clean..."
    # 清理特定的生成文件
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build/Debug/*
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build/Win32/*
    Write-Host "Small build clean completed."
}

# 中编译清理
function Clean-MediumBuild {
    Write-Host "Performing medium build clean..."
    # 清理部分生成文件和目录
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ./build/CMakeFiles/*
    Write-Host "Medium build clean completed."
}

switch ($cleanType) {
    "full" { Clean-FullBuild }
    "small" { Clean-SmallBuild }
    "medium" { Clean-MediumBuild }
    default { Write-Host "Unknown clean type: $cleanType" }
}