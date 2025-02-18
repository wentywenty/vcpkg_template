# 环境配置

## 安装 Scoop 并安装依赖软件

### 安装 Scoop

```powershell
# 设置执行策略并安装 Scoop
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

若出现网络问题,网连不上,请更换网络或者代理,或者在powershell中设置代理

[代理设置](doc\env\proxy.md)

### 安装 Scoop 软件

```powershell
scoop bucket add extras
scoop install git python uv gh powershell-yaml cmake lua luarocks ninja
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

#### 全编译清理（你们几乎用不到）

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
