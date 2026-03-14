"""
rPPG生理指标检测系统 - WebView版本
使用Kivy WebView加载HTML文件
"""
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.logger import Logger

# 尝试导入WebView
try:
    from kivy.uix.webview import WebView
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False
    Logger.warning("WebView模块不可用，将使用备用方案")

import os
import webbrowser

class WebHeartRateApp(App):
    def __init__(self):
        super().__init__()
        self.webview = None
        
    def build(self):
        """构建应用界面"""
        self.title = "rPPG生理指标检测系统"
        
        # 设置窗口背景色
        Window.clearcolor = (0.1, 0.1, 0.15, 1)
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        
        # 标题栏
        title_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        
        title_label = Label(
            text='rPPG生理指标检测系统',
            size_hint=(0.7, 1),
            font_size='18sp',
            bold=True,
            color=(0.2, 0.8, 1, 1)
        )
        
        # 刷新按钮
        refresh_btn = Button(
            text='刷新',
            size_hint=(0.15, 1),
            background_color=(0.2, 0.6, 0.9, 1)
        )
        refresh_btn.bind(on_press=self.reload_page)
        
        # 退出按钮
        exit_btn = Button(
            text='退出',
            size_hint=(0.15, 1),
            background_color=(0.9, 0.3, 0.3, 1)
        )
        exit_btn.bind(on_press=self.exit_app)
        
        title_layout.add_widget(title_label)
        title_layout.add_widget(refresh_btn)
        title_layout.add_widget(exit_btn)
        
        # WebView区域
        web_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.92))
        
        if HAS_WEBVIEW:
            # 使用Kivy WebView
            self.webview = WebView()
            web_layout.add_widget(self.webview)
            
            # 加载HTML文件
            self.load_html_file()
        else:
            # 备用方案：显示提示信息
            info_label = Label(
                text='WebView不可用\n\n请使用以下方式访问:\n1. 在浏览器中打开HTML文件\n2. 或使用完整版Kivy应用',
                font_size='16sp',
                halign='center'
            )
            web_layout.add_widget(info_label)
            
            # 打开浏览器按钮
            open_btn = Button(
                text='在浏览器中打开',
                size_hint=(1, 0.1),
                background_color=(0.2, 0.7, 0.3, 1)
            )
            open_btn.bind(on_press=self.open_in_browser)
            web_layout.add_widget(open_btn)
        
        main_layout.add_widget(title_layout)
        main_layout.add_widget(web_layout)
        
        return main_layout
    
    def load_html_file(self):
        """加载HTML文件"""
        try:
            # 获取HTML文件路径
            html_file = 'heart_rate_precision_web.html'
            
            if os.path.exists(html_file):
                # 获取绝对路径
                abs_path = os.path.abspath(html_file)
                file_url = 'file://' + abs_path
                
                Logger.info(f"加载HTML文件: {file_url}")
                
                if self.webview:
                    self.webview.url = file_url
            else:
                Logger.error(f"HTML文件不存在: {html_file}")
                # 显示错误信息
                self.show_error("HTML文件不存在，请确保heart_rate_precision_web.html文件在应用目录中")
                
        except Exception as e:
            Logger.error(f"加载HTML失败: {e}")
            self.show_error(f"加载失败: {str(e)}")
    
    def reload_page(self, instance):
        """刷新页面"""
        if self.webview:
            self.load_html_file()
            Logger.info("页面已刷新")
    
    def open_in_browser(self, instance):
        """在浏览器中打开"""
        try:
            html_file = 'heart_rate_precision_web.html'
            if os.path.exists(html_file):
                abs_path = os.path.abspath(html_file)
                webbrowser.open('file://' + abs_path)
            else:
                Logger.error("HTML文件不存在")
        except Exception as e:
            Logger.error(f"打开浏览器失败: {e}")
    
    def show_error(self, message):
        """显示错误信息"""
        from kivy.uix.popup import Popup
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, halign='center'))
        
        btn = Button(text='确定', size_hint=(1, 0.3))
        popup = Popup(title='错误', content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()
    
    def exit_app(self, instance):
        """退出应用"""
        self.stop()

if __name__ == '__main__':
    WebHeartRateApp().run()
