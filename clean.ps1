param (
    [ValidateSet("full", "small", "medium")]
    [string]$cleanType = "medium"
)

# 公共函数：输出彩色日志
function Write-ColorLog {
    param (
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 公共函数：验证目录是否存在
function Test-DirectoryExists {
    param (
        [string]$Path
    )
    if (!(Test-Path $Path)) {
        Write-ColorLog "Directory not found: $Path" "Yellow"
        return $false
    }
    return $true
}

# 公共函数：执行清理操作
function Remove-BuildFiles {
    param (
        [string]$Path
    )
    try {
        if (Test-Path $Path) {
            Remove-Item -Recurse -Force -ErrorAction Stop $Path
            Write-ColorLog "Successfully cleaned: $Path" "Green"
        }
    }
    catch {
        Write-ColorLog "Failed to clean: $Path. Error: $_" "Red"
        return $false
    }
    return $true
}

# 完整清理
function Clear-FullBuild {
    Write-ColorLog "Starting full build clean..." "Cyan"
    
    $success = Remove-BuildFiles "./build/*"
    
    if ($success) {
        Write-ColorLog "Full build clean completed successfully." "Green"
    }
    else {
        Write-ColorLog "Full build clean completed with errors." "Yellow"
    }
}

# 小规模清理
function Clear-SmallBuild {
    Write-ColorLog "Starting small build clean..." "Cyan"
    
    $success = $true
    $success = $success -and (Remove-BuildFiles "./build/Debug/*")
    $success = $success -and (Remove-BuildFiles "./build/Win32/*")
    
    if ($success) {
        Write-ColorLog "Small build clean completed successfully." "Green"
    }
    else {
        Write-ColorLog "Small build clean completed with errors." "Yellow"
    }
}

# 中等规模清理
function Clear-MediumBuild {
    Write-ColorLog "Starting medium build clean..." "Cyan"
    
    $success = Remove-BuildFiles "./build/CMakeFiles/*"
    
    if ($success) {
        Write-ColorLog "Medium build clean completed successfully." "Green"
    }
    else {
        Write-ColorLog "Medium build clean completed with errors." "Yellow"
    }
}

# 主执行逻辑
try {
    if (!(Test-DirectoryExists "./build")) {
        Write-ColorLog "Build directory does not exist. Nothing to clean." "Yellow"
        exit 0
    }

    Write-ColorLog "Starting clean operation with type: $cleanType" "White"
    
    switch ($cleanType) {
        "full" { Clear-FullBuild }
        "small" { Clear-SmallBuild }
        "medium" { Clear-MediumBuild }
    }
}
catch {
    Write-ColorLog "An unexpected error occurred: $_" "Red"
    exit 1
}