#!/usr/bin/env python3
"""
使用 Microsoft PowerPoint 导出幻灯片为图片（通过 PDF 中转）
比 LibreOffice 渲染更准确，与实际 PPTX 完全一致

适用条件：
- macOS 系统
- 已安装 Microsoft PowerPoint
- 已安装 Poppler (pdftoppm)

用法：
    python screenshot-pptx.py <pptx_file> <output_image> [slide_num] [dpi]

参数：
    pptx_file: PPTX 文件路径
    output_image: 输出图片路径 (.png 或 .jpg)
    slide_num: 幻灯片编号，1-indexed（默认: 1）
    dpi: 输出分辨率（默认: 200）

示例：
    python screenshot-pptx.py presentation.pptx slide1.png 1 200
"""

import subprocess
import sys
import os
import time
from pathlib import Path


def check_requirements():
    """检查系统要求"""
    # 检查是否是 macOS
    if sys.platform != 'darwin':
        return False, "此脚本仅支持 macOS 系统"

    # 检查 PowerPoint 是否安装
    pptx_app = Path("/Applications/Microsoft PowerPoint.app")
    if not pptx_app.exists():
        return False, "未检测到 Microsoft PowerPoint，请先安装"

    # 检查 pdftoppm 是否可用
    try:
        subprocess.run(['pdftoppm', '-v'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "未检测到 pdftoppm，请安装 Poppler (brew install poppler)"

    return True, ""


def export_slide_with_powerpoint(pptx_path: str, output_path: str, slide_num: int = 1, dpi: int = 200):
    """
    使用 PowerPoint 导出指定幻灯片为图片

    Args:
        pptx_path: PPTX 文件路径
        output_path: 输出图片路径 (.png 或 .jpg)
        slide_num: 幻灯片编号 (1-indexed)
        dpi: 输出分辨率

    Returns:
        bool: 成功返回 True，失败返回 False
    """
    pptx_path = os.path.abspath(pptx_path)
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    output_name = Path(output_path).stem
    output_ext = Path(output_path).suffix.lower()

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 临时 PDF 路径
    pdf_path = os.path.join(output_dir, f"{output_name}_temp.pdf")

    # Step 1: 用 AppleScript 让 PowerPoint 导出 PDF
    applescript = f'''
    tell application "Microsoft PowerPoint"
        activate
        open POSIX file "{pptx_path}"
        delay 1

        set thePresentation to active presentation
        save thePresentation in POSIX file "{pdf_path}" as save as PDF

        delay 0.5
        close thePresentation saving no
    end tell
    '''

    try:
        # 运行 AppleScript
        result = subprocess.run(
            ['osascript', '-e', applescript],
            check=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        # 等待文件写入完成
        time.sleep(0.5)

        if not os.path.exists(pdf_path):
            print(f"Error: PDF not created at {pdf_path}")
            return False

        # Step 2: 用 pdftoppm 从 PDF 生成图片
        output_prefix = os.path.join(output_dir, output_name)

        if output_ext in ['.jpg', '.jpeg']:
            format_flag = '-jpeg'
        else:
            format_flag = '-png'

        pdftoppm_cmd = [
            'pdftoppm',
            format_flag,
            '-r', str(dpi),
            '-f', str(slide_num),
            '-l', str(slide_num),
            pdf_path,
            output_prefix
        ]

        subprocess.run(pdftoppm_cmd, check=True, capture_output=True)

        # pdftoppm 输出格式是 prefix-N.png
        generated_file = f"{output_prefix}-{slide_num}.{'jpg' if output_ext in ['.jpg', '.jpeg'] else 'png'}"

        if os.path.exists(generated_file):
            # 重命名为目标文件名
            os.rename(generated_file, output_path)
            print(f"Screenshot saved: {output_path}")
            print(f"  Slide: {slide_num} (1-indexed)")
            print(f"  DPI: {dpi}")
        else:
            print(f"Error: Generated file not found: {generated_file}")
            return False

        # 清理临时 PDF
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        return True

    except subprocess.TimeoutExpired:
        print("Error: PowerPoint operation timed out")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr if e.stderr else e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        # 确保清理临时文件
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except:
                pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python screenshot-pptx.py <pptx_file> <output_image> [slide_num] [dpi]")
        print("  slide_num: 1-indexed (default: 1)")
        print("  dpi: resolution (default: 200)")
        print("")
        print("Example: python screenshot-pptx.py presentation.pptx slide1.png 1 200")
        print("")
        print("Requirements: macOS, Microsoft PowerPoint, Poppler (pdftoppm)")
        sys.exit(1)

    # 检查系统要求
    ok, msg = check_requirements()
    if not ok:
        print(f"Error: {msg}")
        print("Falling back to screenshot-slide.py (LibreOffice)")
        sys.exit(1)

    pptx_file = sys.argv[1]
    output_file = sys.argv[2]
    slide_num = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 200

    success = export_slide_with_powerpoint(pptx_file, output_file, slide_num, dpi)
    sys.exit(0 if success else 1)
