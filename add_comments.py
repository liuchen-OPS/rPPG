#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML文件自动注释工具
为heart_rate_precision_web.html添加逐行中文注释
"""

import re

def add_comments_to_html(input_file, output_file):
    """
    为HTML文件添加逐行注释
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    commented_lines = []
    in_style = False
    in_script = False
    in_html_comment = False
    
    # 文件头部说明
    header = '''<!-- 
================================================================================
科学级rPPG心率检测系统 - 零基础逐行详细注释版
================================================================================
本文档专为零基础学生设计，每一行代码都有详细中文注释
rPPG = remote Photoplethysmography (远程光电容积描记法)
通过摄像头捕捉面部微小颜色变化来检测心率

文件结构：
1. HTML头部（字符编码、视口设置、标题）
2. CSS样式（页面布局、颜色、动画效果）
3. HTML结构（页面内容、按钮、显示区域）
4. JavaScript代码（核心算法、心率检测逻辑）
================================================================================
-->
'''
    commented_lines.append(header)
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        original_line = line  # 保留原始行（包括缩进）
        
        # 跳过空行，但保留换行
        if not stripped:
            commented_lines.append(line)
            continue
        
        # 检测进入/退出不同区域
        if '<style>' in stripped:
            in_style = True
            commented_lines.append('    <!-- ==================== CSS样式部分开始 ==================== -->\n')
        elif '</style>' in stripped:
            in_style = False
        elif '<script>' in stripped or '<script ' in stripped:
            in_script = True
            commented_lines.append('    <!-- ==================== JavaScript代码部分开始 ==================== -->\n')
        elif '</script>' in stripped:
            in_script = False
        
        # 根据当前区域添加相应注释
        comment = generate_comment(stripped, i, in_style, in_script)
        
        if comment:
            # 添加注释（保持原始缩进）
            indent = len(line) - len(line.lstrip())
            commented_lines.append(' ' * indent + '<!-- ' + comment + ' -->\n')
        
        # 添加原始代码行
        commented_lines.append(original_line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(commented_lines)
    
    print(f"注释完成！已保存到: {output_file}")
    print(f"总行数: {len(commented_lines)}")

def generate_comment(line, line_num, in_style, in_script):
    """
    根据代码内容生成注释
    """
    # HTML标签注释
    if line.startswith('<!DOCTYPE'):
        return '文档类型声明，告诉浏览器这是HTML5文档'
    elif line.startswith('<html'):
        return 'HTML根元素，lang="zh-CN"表示页面语言是中文'
    elif line.startswith('<head>'):
        return '头部区域，包含元数据（不显示在页面上）'
    elif line.startswith('<meta charset'):
        return '设置字符编码为UTF-8，确保中文正常显示'
    elif line.startswith('<meta name="viewport"'):
        return '视口设置：width=device-width自适应设备宽度，initial-scale=1.0初始不缩放'
    elif line.startswith('<title>'):
        return '页面标题，显示在浏览器标签页上'
    elif line.startswith('<body>'):
        return '页面主体开始，这里面的内容会显示在浏览器中'
    
    # CSS注释
    elif in_style and '*' in line and '{' in line:
        return '通配符选择器*，匹配所有HTML元素'
    elif in_style and 'margin:' in line:
        return 'margin设置外边距（元素外部的空白）'
    elif in_style and 'padding:' in line:
        return 'padding设置内边距（元素内部的空白）'
    elif in_style and 'box-sizing:' in line:
        return 'box-sizing: border-box让宽高计算包含padding和border'
    elif in_style and 'body {' in line:
        return 'body选择器，设置整个页面的基础样式'
    elif in_style and 'font-family:' in line:
        return 'font-family设置字体，按优先级从左到右尝试'
    elif in_style and 'background:' in line:
        return 'background设置背景，可以是颜色、渐变或图片'
    elif in_style and 'linear-gradient' in line:
        return 'linear-gradient创建线性渐变背景，135deg是从左上到右下的角度'
    elif in_style and 'min-height:' in line:
        return 'min-height设置最小高度，100vh是视口高度的100%'
    elif in_style and 'display: flex' in line:
        return 'display: flex启用Flexbox弹性布局，便于元素排列'
    elif in_style and 'justify-content:' in line:
        return 'justify-content设置主轴（水平方向）对齐方式'
    elif in_style and 'align-items:' in line:
        return 'align-items设置交叉轴（垂直方向）对齐方式'
    elif in_style and 'color:' in line and '#' in line:
        return 'color设置文字颜色，#ffffff是白色的十六进制代码'
    elif in_style and 'border-radius:' in line:
        return 'border-radius设置圆角，值越大角越圆'
    elif in_style and 'box-shadow:' in line:
        return 'box-shadow添加阴影：水平偏移 垂直偏移 模糊半径 颜色'
    elif in_style and 'position:' in line:
        return 'position设置定位方式，relative相对定位，absolute绝对定位'
    elif in_style and 'width:' in line:
        return 'width设置宽度，100%表示占满父容器'
    elif in_style and 'height:' in line:
        return 'height设置高度'
    elif in_style and 'text-align:' in line:
        return 'text-align设置文字对齐方式'
    elif in_style and 'font-size:' in line:
        return 'font-size设置字体大小'
    elif in_style and 'font-weight:' in line:
        return 'font-weight设置字体粗细，bold是粗体'
    elif in_style and 'border:' in line:
        return 'border设置边框：宽度 样式 颜色'
    elif in_style and 'cursor:' in line:
        return 'cursor设置鼠标样式，pointer是手型'
    elif in_style and 'transition:' in line:
        return 'transition设置过渡动画，让属性变化更平滑'
    elif in_style and 'animation:' in line:
        return 'animation应用动画效果'
    elif in_style and '@keyframes' in line:
        return '@keyframes定义动画的关键帧（动画各阶段的状态）'
    elif in_style and 'grid-template-columns:' in line:
        return 'grid-template-columns定义网格列数和宽度'
    elif in_style and 'gap:' in line:
        return 'gap设置网格项之间的间距'
    elif in_style and '@media' in line:
        return '@media是媒体查询，根据屏幕尺寸应用不同样式（响应式设计）'
    elif in_style and '}' in line and len(line.strip()) == 1:
        return 'CSS规则块结束'
    
    # HTML结构注释
    elif '<div' in line and 'class="container"' in line:
        return '主容器div，包裹整个页面内容'
    elif '<div' in line and 'class="header"' in line:
        return '页面头部区域，包含标题和副标题'
    elif '<h1>' in line:
        return 'h1是一级标题，页面最重要的标题'
    elif '<p>' in line:
        return 'p是段落标签，用于显示文字'
    elif '<button' in line:
        return 'button是按钮元素，用户可以点击'
    elif '<video' in line:
        return 'video是视频元素，用于显示摄像头画面'
    elif '<canvas' in line:
        return 'canvas是画布元素，用于绘制图形和波形'
    elif 'id="' in line:
        return 'id是给元素的唯一标识，JavaScript可以通过id获取元素'
    elif 'class="' in line:
        return 'class是给元素的类名，用于应用CSS样式'
    elif 'onclick="' in line:
        return 'onclick是点击事件属性，点击时执行指定函数'
    elif '<!--' in line:
        return 'HTML注释，不会显示在页面上'
    
    # JavaScript注释（简单模式）
    elif in_script:
        if line.startswith('const ') or line.startswith('let ') or line.startswith('var '):
            return '声明变量，用于存储数据'
        elif 'function ' in line or 'async function' in line:
            return '定义函数，封装可重复使用的代码块'
        elif 'class ' in line:
            return '定义类，创建对象的模板'
        elif 'constructor(' in line:
            return '构造函数，创建对象时自动执行'
        elif 'this.' in line:
            return 'this指向当前对象，访问对象的属性和方法'
        elif 'if (' in line:
            return 'if条件语句，条件为真时执行代码块'
        elif 'else' in line and '{' in line:
            return 'else分支，if条件不满足时执行'
        elif 'for (' in line:
            return 'for循环，重复执行代码块指定次数'
        elif 'while (' in line:
            return 'while循环，条件为真时重复执行'
        elif 'return ' in line:
            return 'return返回函数的结果'
        elif 'await ' in line:
            return 'await等待异步操作完成'
        elif 'try {' in line:
            return 'try块，包裹可能出错的代码'
        elif 'catch (' in line:
            return 'catch捕获并处理错误'
        elif 'new ' in line:
            return 'new创建对象实例'
        elif '.' in line and '(' in line and not line.startswith('//'):
            return '调用对象的方法（函数）'
        elif '=' in line and not '==' in line and not '===' in line:
            return '赋值操作，将右边的值赋给左边'
        elif '==' in line or '===' in line:
            return '比较操作，判断两边是否相等'
        elif '+' in line or '-' in line or '*' in line or '/' in line:
            return '算术运算：+加 -减 *乘 /除'
        elif '}' in line and len(line.strip()) == 1:
            return '代码块结束'
    
    # 默认返回None表示不添加注释
    return None

if __name__ == '__main__':
    add_comments_to_html(
        'heart_rate_precision_web.html',
        'heart_rate_precision_web_零基础注释版.html'
    )
