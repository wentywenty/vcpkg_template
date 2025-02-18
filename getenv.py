#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import os
import json
import getpass
import sys
from typing import Dict, List, Optional
from pathlib import Path

class ConfigurationError(Exception):
    """配置相关的异常基类"""
    pass

class ConsoleHelper:
    @staticmethod
    def setup_encoding():
        """设置控制台编码"""
        if sys.platform == 'win32':
            if sys.stdout.encoding != 'utf-8':
                sys.stdout.reconfigure(encoding='utf-8')
            if os.environ.get('CI'):
                os.system('chcp 65001')

    @staticmethod
    def safe_print(message: str):
        """安全打印，处理编码问题"""
        try:
            print(message)
        except UnicodeEncodeError:
            print(message.encode('ascii', 'replace').decode())

class ConfigManager:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.config_path = base_path / 'config.yaml'
        self.script_path = base_path / 'env.ps1'
        self.cmake_presets_path = base_path / 'CMakeUserPresets.json'
        self.user_config: Dict = {}

    def load_config(self) -> None:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            current_user = getpass.getuser()
            self.user_config = config.get(current_user, config.get('other', {}))
            if not self.user_config:
                raise ConfigurationError(f"No configuration found for user {current_user}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load config: {str(e)}")

    def generate_ps_commands(self) -> List[str]:
        """生成PowerShell命令"""
        commands = [
            '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8',
            '$OutputEncoding = [System.Text.Encoding]::UTF8'
        ]
        
        for key, value in self.user_config.items():
            commands.append(f'$env:{key}="{value}"')
            ConsoleHelper.safe_print(f'Setting environment variable: {key}={value}')
        
        return commands

    def write_ps_script(self, commands: List[str]) -> None:
        """写入PowerShell脚本"""
        try:
            with open(self.script_path, 'w', encoding='utf-8-sig') as f:
                f.write('\n'.join(commands))
        except Exception as e:
            raise ConfigurationError(f"Failed to write PowerShell script: {str(e)}")

    def update_cmake_presets(self) -> None:
        """更新CMake预设文件"""
        if 'VCPKG_ROOT' not in self.user_config:
            return

        if not self.cmake_presets_path.exists():
            ConsoleHelper.safe_print('Warning: CMakeUserPresets.json not found')
            return

        try:
            with open(self.cmake_presets_path, 'r', encoding='utf-8') as f:
                content = json.load(f)

            vcpkg_root = os.path.normpath(self.user_config['VCPKG_ROOT'])
            for preset in content.get('configurePresets', []):
                if 'VCPKG_ROOT' in preset.get('environment', {}):
                    preset['environment']['VCPKG_ROOT'] = vcpkg_root

            with open(self.cmake_presets_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=4)

            ConsoleHelper.safe_print(f'Updated VCPKG_ROOT to: {vcpkg_root}')
        except Exception as e:
            raise ConfigurationError(f"Failed to update CMake presets: {str(e)}")

def main() -> int:
    """主函数"""
    try:
        ConsoleHelper.setup_encoding()
        
        config_manager = ConfigManager(Path(__file__).parent)
        config_manager.load_config()
        
        ps_commands = config_manager.generate_ps_commands()
        config_manager.write_ps_script(ps_commands)
        config_manager.update_cmake_presets()
        
        ConsoleHelper.safe_print("\nRun the following command in PowerShell to set environment variables:")
        ConsoleHelper.safe_print(f". {config_manager.script_path}")
        ConsoleHelper.safe_print("\nConfiguration completed!")
        return 0
        
    except ConfigurationError as e:
        print(f"Configuration error: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())