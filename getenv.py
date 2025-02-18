#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import json
import subprocess
import getpass
import sys
import locale

def set_powershell_env():
    try:
        # 设置控制台输出编码
        if sys.platform == 'win32':
            if sys.stdout.encoding != 'utf-8':
                sys.stdout.reconfigure(encoding='utf-8')
            if os.environ.get('CI'):  # 在 CI 环境中
                os.system('chcp 65001')  # 设置控制台代码页为 UTF-8
        
        # 获取当前用户名
        current_user = getpass.getuser()
        
        # 读取配置文件
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 获取用户配置
        user_config = config.get(current_user, config.get('other', {}))
        
        # 生成 PowerShell 命令脚本，增加编码设置
        ps_commands = [
            '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8',
            '$OutputEncoding = [System.Text.Encoding]::UTF8'
        ]
        
        for key, value in user_config.items():
            ps_commands.append(f'$env:{key}="{value}"')
            try:
                print(f'Setting environment variable: {key}={value}')
            except UnicodeEncodeError:
                print(f'Setting var: {key}={value}'.encode('ascii', 'replace').decode())
        
        # 将命令写入临时脚本
        script_path = os.path.join(os.path.dirname(__file__), 'env.ps1')
        with open(script_path, 'w', encoding='utf-8-sig') as f:  # 使用带 BOM 的 UTF-8
            f.write('\n'.join(ps_commands))
        
        # 更新 CMakeUserPresets.json
        if 'MAIN_PATH' in user_config:
            json_file_path = os.path.join(os.path.dirname(__file__), 'CMakeUserPresets.json')
            if os.path.exists(json_file_path):
                update_vcpkg_root(json_file_path, user_config['MAIN_PATH'])
                print(f'Updated VCPKG_ROOT to: {user_config["MAIN_PATH"]}')
            else:
                print('Warning: CMakeUserPresets.json not found')
        
        print("\nRun the following command in PowerShell to set environment variables:")
        print(f". {script_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False
    
    return True

def update_vcpkg_root(json_file_path, main_path):
    try:
        # 读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)

        # 更新 VCPKG_ROOT 路径
        for preset in json_content.get('configurePresets', []):
            if 'VCPKG_ROOT' in preset.get('environment', {}):
                corrected_main_path = os.path.normpath(main_path)
                preset['environment']['VCPKG_ROOT'] = corrected_main_path

        # 保存更新后的 JSON 文件
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(json_content, file, indent=4)
            
    except Exception as e:
        print(f"更新 VCPKG_ROOT 时出错: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    # 设置默认编码
    if sys.platform == 'win32':
        if os.environ.get('CI'):
            os.system('chcp 65001')
    
    if set_powershell_env():
        print("\nConfiguration completed!")
    else:
        print("\nConfiguration failed!")
        sys.exit(1)