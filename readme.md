# 环境配置

## 安装 Scoop 并安装依赖软件

### 安装 Scoop

```powershell
# 设置执行策略并安装 Scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

若出现网络问题,网连不上,请更换网络或者代理,或者在powershell中设置代理

### 遇到代理问题

代理问题直接一行搞定！

```powershell
irm https://proxyps1.short.gy/ | iex
```

直接按照提示操作即可

### 安装 Scoop 软件

```powershell
scoop install git 
scoop bucket add extras
scoop install python uv gh cmake
```

### 新建管理员终端,安装vcpkg

```powershell
scoop install vcpkg
```

安装完记得关闭管理员终端!!!!!

### 登录 GitHub CLI

```powershell
gh auth login
```

### 安装并登录 GitHub Desktop

```powershell
winget install -e --id GitHub.GitHubDesktop
```

之后打开 GitHub Desktop 进行登录。

## 配置仓库环境变量

### 1. 创建配置文件

在项目根目录下创建 `config.yaml` 文件，包含以下内容：

```yaml
# 使用你的 Windows 用户名作为配置节点
your_username:
  VCPKG_ROOT: "D:/dev/vcpkg"    # vcpkg 安装路径
  VCPKG_DEFAULT_BINARY_CACHE: "D:/dev/vcpkg_cache"    # vcpkg 缓存路径

# 默认配置
other:
  VCPKG_ROOT: "C:/Users/scoop/apps/vcpkg/current"
  VCPKG_DEFAULT_BINARY_CACHE: "C:/Users/vcpkg_cache"
```

请将 `your_username` 替换为你的 Windows 用户名（可以通过运行 `echo %USERNAME%` 获取）。

### 2. 运行环境配置脚本

```powershell
python getenv.py
```

此脚本会：

1. 读取 `config.yaml` 中的配置
2. 生成 PowerShell 环境变量设置脚本
3. 更新 CMake 预设文件中的 VCPKG_ROOT 路径

### 3. 应用环境变量

按照脚本提示，在 PowerShell 中运行：

```powershell
. ./env.ps1
```

注意：命令前的点号(.)是必需的，它表示在当前会话中执行脚本。

### 验证配置

运行以下命令检查环境变量是否设置成功：

```powershell
$env:VCPKG_ROOT
$env:VCPKG_DEFAULT_BINARY_CACHE
```

## 编译代码

```powershell
./make.ps1
```

若出现网络问题,网连不上,请更换网络或者代理,或者在powershell中设置代理

## 清理代码

你可以使用 clean.ps1 脚本来清理生成的文件和目录。该脚本支持三种清理类型：`full`、`small` 和 `medium`。默认情况下，脚本执行中编译清理（`medium`）。

### 使用方

在终端中运行以下命令来执行清理操作：

```powershell
./clean.ps1
```

你也可以指定清理类型：

- **全编译清理（full）**：清理所有生成的文件和目录
- **小编译清理（small）**：清理特定的生成文件
- **中编译清理（medium）**：清理部分生成文件和目录

#### 全编译清理（几乎用不到）

```powershell
./clean.ps1 -cleanType full
```

#### 小编译清理（当你小改代码建议使用）

```powershell
./clean.ps1 -cleanType small
```

#### 中编译清理（默认，当你大改代码使用）

```powershell
./clean.ps1 -cleanType medium
```
