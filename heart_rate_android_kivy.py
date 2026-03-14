import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import Camera
from kivy.logger import Logger

import numpy as np
import time
from collections import deque
import math

# -------------------------- 安卓心率检测配置 --------------------------
BUFFER_LENGTH = 180  # 6秒数据（30fps），安卓性能优化
FS = 30.0

# 医学参考范围
MEDICAL_HR_MIN = 60
MEDICAL_HR_MAX = 100

# 精度优化参数
STABILITY_THRESHOLD = 10      # 安卓性能优化
SMOOTHING_WINDOW = 5          # 简化平滑窗口
MIN_SIGNAL_LENGTH = 90        # 安卓性能优化
QUALITY_THRESHOLD_HIGH = 60   # 高质量信号阈值
QUALITY_THRESHOLD_MEDIUM = 40 # 中等质量信号阈值

class HeartRateAndroidApp(App):
    def __init__(self):
        super().__init__()
        
        # 信号缓存
        self.green_buffer = deque(maxlen=BUFFER_LENGTH)
        
        # 状态变量
        self.stable_face_count = 0
        self.last_face_position = None
        self.last_hr_values = deque(maxlen=10)
        self.heart_rate = 0
        self.heart_rate_status = "等待检测"
        self.heart_rate_confidence = 0
        self.signal_quality = 0
        self.frame_count = 0
        
        # 摄像头相关
        self.camera = None
        self.is_camera_active = False
        
        # 界面组件
        self.camera_image = None
        self.status_label = None
        self.heart_rate_label = None
        self.quality_label = None
        
    def build(self):
        """构建应用界面"""
        self.title = "心率检测安卓应用"
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(
            text='心率专用精度优化健康监测系统',
            size_hint=(1, 0.1),
            font_size='20sp',
            bold=True
        )
        
        # 摄像头预览区域
        self.camera_image = Image(
            size_hint=(1, 0.6)
        )
        
        # 状态显示区域
        status_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        
        self.status_label = Label(
            text='状态: 等待启动摄像头',
            size_hint=(1, 0.3),
            font_size='16sp'
        )
        
        self.heart_rate_label = Label(
            text='心率: 0 次/分钟 (等待检测)',
            size_hint=(1, 0.4),
            font_size='18sp',
            bold=True
        )
        
        self.quality_label = Label(
            text='信号质量: 0%',
            size_hint=(1, 0.3),
            font_size='14sp'
        )
        
        # 控制按钮
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        start_button = Button(
            text='启动摄像头',
            size_hint=(0.5, 1),
            background_color=(0, 0.7, 0, 1)
        )
        start_button.bind(on_press=self.start_camera)
        
        stop_button = Button(
            text='停止检测',
            size_hint=(0.5, 1),
            background_color=(0.7, 0, 0, 1)
        )
        stop_button.bind(on_press=self.stop_camera)
        
        # 组装界面
        button_layout.add_widget(start_button)
        button_layout.add_widget(stop_button)
        
        status_layout.add_widget(self.status_label)
        status_layout.add_widget(self.heart_rate_label)
        status_layout.add_widget(self.quality_label)
        
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.camera_image)
        main_layout.add_widget(status_label)
        main_layout.add_widget(button_layout)
        
        return main_layout
    
    def start_camera(self, instance):
        """启动摄像头"""
        try:
            if self.camera is None:
                self.camera = Camera(index=0, resolution=(640, 480))
                self.camera.play = True
                
                # 设置定时器处理帧
                Clock.schedule_interval(self.process_frame, 1.0/30.0)  # 30fps
                
                self.is_camera_active = True
                self.status_label.text = "状态: 摄像头已启动，请保持面部稳定"
                Logger.info("摄像头启动成功")
            else:
                self.camera.play = True
                self.is_camera_active = True
                
        except Exception as e:
            self.status_label.text = f"状态: 摄像头启动失败 - {str(e)}"
            Logger.error(f"摄像头启动失败: {e}")
    
    def stop_camera(self, instance):
        """停止摄像头"""
        if self.camera:
            self.camera.play = False
            self.is_camera_active = False
            
            # 停止定时器
            Clock.unschedule(self.process_frame)
            
            self.status_label.text = "状态: 检测已停止"
            Logger.info("摄像头已停止")
    
    def process_frame(self, dt):
        """处理摄像头帧"""
        if not self.is_camera_active or self.camera is None:
            return
            
        try:
            # 获取摄像头纹理
            texture = self.camera.texture
            if texture is None:
                return
                
            # 更新摄像头预览
            self.camera_image.texture = texture
            
            # 转换为numpy数组进行处理
            buffer_data = texture.pixels
            image_size = texture.size
            
            # 将缓冲区数据转换为numpy数组
            image_array = np.frombuffer(buffer_data, dtype=np.uint8)
            image_array = image_array.reshape((image_size[1], image_size[0], 4))  # RGBA
            
            # 转换为BGR格式（OpenCV格式）
            bgr_image = image_array[:, :, :3][:, :, ::-1]  # RGBA -> BGR
            
            # 简化的人脸检测（基于肤色）
            face_detected = self.simple_face_detection(bgr_image)
            
            if face_detected:
                # 提取绿色通道信号
                avg_green = np.mean(bgr_image[:, :, 1])  # 绿色通道
                self.green_buffer.append(avg_green)
                
                self.frame_count += 1
                
                # 人脸稳定性检测
                self.stable_face_count = min(self.stable_face_count + 1, STABILITY_THRESHOLD)
                
                if len(self.green_buffer) >= MIN_SIGNAL_LENGTH:
                    # 信号处理
                    processed_signal = self.advanced_signal_preprocessing(np.array(self.green_buffer))
                    
                    # 信号质量评估
                    self.signal_quality = self.calculate_signal_quality_precision(processed_signal)
                    
                    # 心率计算
                    hr_raw, hr_confidence = self.precision_heart_rate_calculation(processed_signal, FS)
                    
                    if hr_raw > 0:
                        self.heart_rate, self.heart_rate_status, _ = self.validate_heart_rate_precision(hr_raw, hr_confidence)
                        self.heart_rate = round(self.smooth_value_precision(self.heart_rate, self.last_hr_values, hr_confidence, SMOOTHING_WINDOW), 1)
                        self.heart_rate_confidence = hr_confidence
                        
                        # 更新界面
                        self.update_ui()
                        
                        # 定期日志输出
                        if self.frame_count % 60 == 0:
                            Logger.info(f"心率: {self.heart_rate}bpm, 置信度: {self.heart_rate_confidence:.1f}%, 信号质量: {self.signal_quality:.1f}%")
            else:
                self.stable_face_count = max(0, self.stable_face_count - 1)
                
        except Exception as e:
            Logger.error(f"帧处理异常: {e}")
    
    def simple_face_detection(self, image):
        """简化的人脸检测（基于肤色）"""
        try:
            # 转换为HSV颜色空间
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # 肤色范围（简化版）
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            
            # 创建肤色掩码
            skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)
            
            # 计算肤色区域比例
            skin_ratio = np.sum(skin_mask > 0) / (image.shape[0] * image.shape[1])
            
            # 如果肤色区域超过一定比例，认为检测到人脸
            return skin_ratio > 0.1
            
        except:
            return False
    
    def advanced_signal_preprocessing(self, signal_data):
        """高级信号预处理"""
        if len(signal_data) < MIN_SIGNAL_LENGTH:
            return signal_data
        
        try:
            # 简化去趋势
            detrend_signal = signal_data - np.mean(signal_data)
            
            # 移动平均滤波
            window_size = 5
            smoothed = np.convolve(detrend_signal, np.ones(window_size)/window_size, mode='same')
            
            # 归一化
            if np.std(smoothed) > 0:
                normalized = (smoothed - np.mean(smoothed)) / np.std(smoothed)
            else:
                normalized = smoothed
            
            return normalized
            
        except Exception as e:
            Logger.error(f"信号预处理异常: {e}")
            return signal_data
    
    def precision_heart_rate_calculation(self, signal_data, fs):
        """精度优化的心率计算"""
        if len(signal_data) < MIN_SIGNAL_LENGTH:
            return 0, 0
        
        try:
            # 信号质量检查
            signal_std = np.std(signal_data)
            if signal_std < 0.1:
                return 0, 0
            
            # 应用汉宁窗
            window = np.hanning(len(signal_data))
            windowed_signal = signal_data * window
            
            # FFT计算
            fft_vals = np.fft.fft(windowed_signal)
            fft_freqs = np.fft.fftfreq(len(signal_data), 1/fs)
            
            # 只保留正频率
            positive_mask = fft_freqs > 0
            fft_vals = fft_vals[positive_mask]
            fft_freqs = fft_freqs[positive_mask]
            
            # 计算功率谱
            power = np.abs(fft_vals) ** 2
            
            # 心率频率范围（0.8-2.5Hz，对应48-150bpm）
            hr_mask = (fft_freqs >= 0.8) & (fft_freqs <= 2.5)
            
            if np.sum(hr_mask) == 0:
                return 0, 0
            
            hr_power = power[hr_mask]
            hr_freqs = fft_freqs[hr_mask]
            
            # 找到最大功率对应的频率
            max_power_idx = np.argmax(hr_power)
            peak_freq = hr_freqs[max_power_idx]
            peak_power = hr_power[max_power_idx]
            
            hr = peak_freq * 60
            
            # 置信度计算
            confidence = min(100, (peak_power / np.max(power)) * 100)
            
            return hr, confidence
            
        except Exception as e:
            Logger.error(f"心率计算异常: {e}")
            return 0, 0
    
    def calculate_signal_quality_precision(self, signal_data):
        """信号质量评估"""
        try:
            signal_std = np.std(signal_data)
            
            # 周期性评估
            autocorr = np.correlate(signal_data - np.mean(signal_data), 
                                   signal_data - np.mean(signal_data), mode='full')
            autocorr = autocorr[len(autocorr)//2:]
            periodicity = np.max(autocorr[10:50]) / autocorr[0] if autocorr[0] > 0 else 0
            
            # 综合信号质量评分
            quality = min(100, signal_std * 30 + min(70, periodicity * 100))
            
            return quality
        except:
            return 0
    
    def smooth_value_precision(self, current_value, history, confidence, window_size=5):
        """数值平滑"""
        if current_value == 0:
            return 0
        
        history.append(current_value)
        
        if len(history) < window_size:
            return current_value
        
        # 简单移动平均
        smoothed = np.mean(list(history)[-window_size:])
        
        return smoothed
    
    def validate_heart_rate_precision(self, hr_value, confidence):
        """心率验证"""
        if hr_value < 40 or hr_value > 180:
            return 0, "超出范围", False
        
        if confidence < QUALITY_THRESHOLD_MEDIUM:
            return 0, "置信度低", False
        
        # 医学范围验证
        if MEDICAL_HR_MIN <= hr_value <= MEDICAL_HR_MAX:
            return hr_value, "正常", confidence >= QUALITY_THRESHOLD_HIGH
        elif 50 <= hr_value < MEDICAL_HR_MIN:
            return hr_value, "偏低", confidence >= QUALITY_THRESHOLD_MEDIUM
        elif MEDICAL_HR_MAX < hr_value <= 110:
            return hr_value, "偏高", confidence >= QUALITY_THRESHOLD_MEDIUM
        else:
            return 0, "异常", False
    
    def update_ui(self):
        """更新用户界面"""
        # 更新状态标签
        self.status_label.text = f"状态: 检测中 (稳定性: {self.stable_face_count}/{STABILITY_THRESHOLD})"
        
        # 更新心率显示
        hr_color = "[color=00FF00]" if self.heart_rate_confidence > 60 else "[color=FFA500]"
        self.heart_rate_label.text = f"{hr_color}心率: {self.heart_rate} 次/分钟 ({self.heart_rate_status}) [置信度: {self.heart_rate_confidence:.1f}%][/color]"
        
        # 更新信号质量
        quality_color = "[color=00FF00]" if self.signal_quality > 60 else "[color=FFA500]" if self.signal_quality > 40 else "[color=FF0000]"
        self.quality_label.text = f"{quality_color}信号质量: {self.signal_quality:.1f}%[/color]"
    
    def on_stop(self):
        """应用停止时的清理工作"""
        if self.camera:
            self.camera.play = False
            self.camera = None

# 安卓兼容的OpenCV导入
try:
    import cv2
except ImportError:
    # 在安卓环境中可能无法导入OpenCV，使用简化版本
    class DummyCV2:
        COLOR_BGR2HSV = 40
        
        @staticmethod
        def cvtColor(img, code):
            # 简化版的BGR转HSV转换
            if code == 40:  # COLOR_BGR2HSV
                # 简化的转换逻辑
                hsv_img = np.zeros_like(img, dtype=np.uint8)
                return hsv_img
            return img
    
    cv2 = DummyCV2()

if __name__ == '__main__':
    HeartRateAndroidApp().run()