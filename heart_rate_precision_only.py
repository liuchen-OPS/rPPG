import cv2
import numpy as np
import time
import math
from collections import deque
from PIL import Image, ImageDraw, ImageFont
import warnings
import traceback
warnings.filterwarnings('ignore')

# -------------------------- 心率专用精度优化配置 --------------------------
BUFFER_LENGTH = 240  # 8秒数据（30fps），增加数据量提高精度
FS = 30.0

# 医学参考范围
MEDICAL_HR_MIN = 60
MEDICAL_HR_MAX = 100

# 精度优化参数
STABILITY_THRESHOLD = 15      # 提高稳定性要求
SMOOTHING_WINDOW = 7          # 优化平滑窗口
MIN_SIGNAL_LENGTH = 120       # 增加最小信号长度
QUALITY_THRESHOLD_HIGH = 60   # 高质量信号阈值
QUALITY_THRESHOLD_MEDIUM = 40 # 中等质量信号阈值

# -------------------------- 心率专用精度优化初始化 --------------------------

def safe_face_cascade_init():
    """安全的人脸检测器初始化"""
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        return face_cascade
    except Exception as e:
        print(f"人脸检测器初始化异常: {e}")
        return None

def safe_camera_init():
    """安全的摄像头初始化"""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("摄像头初始化失败")
            return None
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("摄像头初始化成功")
        return cap
    except Exception as e:
        print(f"摄像头初始化异常: {e}")
        return None

# 安全初始化
face_cascade = safe_face_cascade_init()
cap = safe_camera_init()

if cap is None:
    print("系统启动失败：摄像头不可用")
    exit(1)

# 信号缓存（心率专用版本）
green_buffer = deque(maxlen=BUFFER_LENGTH)

# 精度优化相关变量
stable_face_count = 0
last_face_position = None
last_hr_values = deque(maxlen=15)
signal_quality_history = deque(maxlen=20)
hr_confidence_history = deque(maxlen=10)

# -------------------------- 心率专用精度优化核心函数 --------------------------

def advanced_signal_preprocessing(signal_data):
    """高级信号预处理（专注于心率检测）"""
    if len(signal_data) < MIN_SIGNAL_LENGTH:
        return signal_data
    
    try:
        # 1. 精确去趋势（去除基线漂移）
        detrend_signal = signal_data - np.polyval(np.polyfit(range(len(signal_data)), signal_data, 1), range(len(signal_data)))
        
        # 2. 带通滤波优化（0.8-4Hz，对应48-240bpm）
        # 低通滤波（去除高频噪声）
        window_size_low = 9
        low_pass = np.convolve(detrend_signal, np.ones(window_size_low)/window_size_low, mode='same')
        
        # 高通滤波（去除低频漂移）
        window_size_high = 31
        high_pass = low_pass - np.convolve(low_pass, np.ones(window_size_high)/window_size_high, mode='same')
        
        # 3. 信号平滑（保留心率信息）
        window_size_smooth = 5
        smoothed = np.convolve(high_pass, np.ones(window_size_smooth)/window_size_smooth, mode='same')
        
        # 4. 归一化处理（提高信号质量）
        if np.std(smoothed) > 0:
            normalized = (smoothed - np.mean(smoothed)) / np.std(smoothed)
        else:
            normalized = smoothed
        
        return normalized
        
    except Exception as e:
        print(f"信号预处理异常: {e}")
        return signal_data

def precision_heart_rate_calculation(signal_data, fs):
    """精度优化的心率计算"""
    if len(signal_data) < MIN_SIGNAL_LENGTH:
        return 0, 0  # 心率值, 置信度
    
    try:
        # 1. 信号质量评估
        signal_std = np.std(signal_data)
        if signal_std < 0.15:  # 提高信号质量要求
            return 0, 0
        
        # 2. 应用汉宁窗（减少频谱泄漏）
        window = np.hanning(len(signal_data))
        windowed_signal = signal_data * window
        
        # 3. 零填充FFT（提高频率分辨率）
        n_fft = max(1024, len(signal_data))
        fft_vals = np.fft.fft(windowed_signal, n=n_fft)
        fft_freqs = np.fft.fftfreq(n_fft, 1/fs)
        
        # 4. 只保留正频率
        positive_mask = fft_freqs > 0
        fft_vals = fft_vals[positive_mask]
        fft_freqs = fft_freqs[positive_mask]
        
        # 5. 计算功率谱密度
        power = np.abs(fft_vals) ** 2
        
        # 6. 心率频率范围（0.8-2.5Hz，对应48-150bpm）
        hr_mask = (fft_freqs >= 0.8) & (fft_freqs <= 2.5)
        
        if np.sum(hr_mask) == 0:
            return 0, 0
        
        hr_power = power[hr_mask]
        hr_freqs = fft_freqs[hr_mask]
        
        # 7. 多峰值检测（提高准确性）
        peak_indices = np.argsort(hr_power)[-5:][::-1]  # 前5个最大峰值
        
        valid_peaks = []
        for idx in peak_indices:
            peak_freq = hr_freqs[idx]
            peak_power = hr_power[idx]
            hr = peak_freq * 60
            
            # 心率范围验证
            if 45 <= hr <= 180:
                # 功率阈值检查
                power_threshold = np.max(hr_power) * 0.3
                if peak_power > power_threshold:
                    valid_peaks.append((hr, peak_power, peak_freq))
        
        if not valid_peaks:
            return 0, 0
        
        # 8. 心率选择策略（基于功率加权）
        if len(valid_peaks) >= 2:
            # 多峰值加权平均
            total_power = sum(power for _, power, _ in valid_peaks)
            weighted_hr = sum(hr * power for hr, power, _ in valid_peaks) / total_power
            
            # 置信度计算
            max_power = max(power for _, power, _ in valid_peaks)
            confidence = min(100, (max_power / np.max(power)) * 100)
            
            return weighted_hr, confidence
        else:
            # 单峰值
            hr, power, freq = valid_peaks[0]
            confidence = min(100, (power / np.max(power)) * 100)
            return hr, confidence
            
    except Exception as e:
        print(f"心率计算异常: {e}")
        return 0, 0

def calculate_signal_quality_precision(signal_data):
    """精度优化的信号质量评估"""
    try:
        signal_std = np.std(signal_data)
        
        # 信噪比估计
        noise_std = np.std(signal_data - np.convolve(signal_data, np.ones(7)/7, mode='same'))
        snr = signal_std / noise_std if noise_std > 0 else 0
        
        # 周期性评估
        autocorr = np.correlate(signal_data - np.mean(signal_data), 
                               signal_data - np.mean(signal_data), mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        periodicity = np.max(autocorr[10:50]) / autocorr[0] if autocorr[0] > 0 else 0
        
        # 综合信号质量评分
        quality = min(100, signal_std * 20 + min(40, snr * 10) + min(40, periodicity * 100))
        
        return quality
    except:
        return 0

def smooth_value_precision(current_value, history, confidence, window_size=7):
    """精度优化的数值平滑"""
    if current_value == 0:
        return 0
    
    history.append(current_value)
    
    if len(history) < window_size:
        return current_value
    
    # 基于置信度的加权平滑
    weights = np.array([0.1, 0.15, 0.2, 0.25, 0.2, 0.15, 0.1])
    
    # 调整权重基于置信度
    confidence_factor = confidence / 100.0
    weights = weights * (0.5 + 0.5 * confidence_factor)
    weights = weights / np.sum(weights)
    
    smoothed = np.average(list(history)[-window_size:], weights=weights[:len(history)])
    
    return smoothed

def validate_heart_rate_precision(hr_value, confidence):
    """精度优化的心率验证"""
    if hr_value < 40 or hr_value > 180:
        return 0, "超出人体生理范围", False
    
    if confidence < QUALITY_THRESHOLD_MEDIUM:
        return 0, "置信度不足", False
    
    # 医学范围验证
    if MEDICAL_HR_MIN <= hr_value <= MEDICAL_HR_MAX:
        return hr_value, "正常范围", confidence >= QUALITY_THRESHOLD_HIGH
    elif 50 <= hr_value < MEDICAL_HR_MIN:
        return hr_value, "偏低（运动员或体质较好）", confidence >= QUALITY_THRESHOLD_MEDIUM
    elif MEDICAL_HR_MAX < hr_value <= 110:
        return hr_value, "偏高（需关注）", confidence >= QUALITY_THRESHOLD_MEDIUM
    else:
        return 0, "异常值", False

def safe_text_display_precision(img, text, position, font_size=20, color=(255, 255, 255)):
    """安全的文本显示"""
    try:
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        try:
            font = ImageFont.truetype("simhei.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("msyh.ttc", font_size)
            except:
                font = ImageFont.load_default()
        
        draw.text(position, text, font=font, fill=color)
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    except:
        try:
            cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size/20, color, 2)
            return img
        except:
            return img

# -------------------------- 心率专用精度优化主循环 --------------------------

def main():
    global stable_face_count, last_face_position
    
    frame_count = 0
    start_time = time.time()
    
    print("=== 心率专用精度优化健康监测系统 ===")
    print("专注于心率检测，移除HRV测量部分")
    print("=" * 60)
    
    try:
        cv2.namedWindow('Heart Rate Precision Only', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Heart Rate Precision Only', 1000, 600)
        
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("无法读取摄像头画面")
                    time.sleep(0.1)
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.05, 6, minSize=(120, 120))
                
                heart_rate = 0
                heart_rate_status = "计算中"
                heart_rate_confidence = 0
                heart_rate_reliable = False
                signal_quality = 0
                
                current_face = None
                face_stable = False
                
                if len(faces) > 0:
                    current_face = max(faces, key=lambda f: f[2] * f[3])
                    x, y, w, h = current_face
                    
                    # 人脸稳定性检查
                    if last_face_position is not None:
                        x2, y2, w2, h2 = last_face_position
                        face_stable = (abs(x - x2) < 25 and abs(y - y2) < 25)
                    
                    if face_stable:
                        stable_face_count += 1
                    else:
                        stable_face_count = 0
                    
                    last_face_position = current_face
                    
                    # 精度优化测量条件
                    if stable_face_count >= STABILITY_THRESHOLD:
                        roi_y = max(0, y + int(h * 0.2))
                        roi_h = min(int(h * 0.15), frame.shape[0] - roi_y)
                        roi_x = max(0, x + int(w * 0.3))
                        roi_w = min(int(w * 0.4), frame.shape[1] - roi_x)
                        
                        roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
                        
                        if roi.size > 0:
                            avg_green = np.mean(roi[:, :, 1])
                            
                            green_buffer.append(avg_green)
                            
                            frame_count += 1
                            
                            if len(green_buffer) >= BUFFER_LENGTH:
                                green_signal = np.array(green_buffer)
                                
                                # 精度优化的信号处理
                                processed_signal = advanced_signal_preprocessing(green_signal)
                                
                                # 信号质量评估
                                signal_quality = calculate_signal_quality_precision(processed_signal)
                                
                                # 精度优化的心率计算
                                hr_raw, hr_confidence = precision_heart_rate_calculation(processed_signal, FS)
                                
                                if hr_raw > 0:
                                    heart_rate, heart_rate_status, heart_rate_reliable = validate_heart_rate_precision(hr_raw, hr_confidence)
                                    heart_rate = round(smooth_value_precision(heart_rate, last_hr_values, hr_confidence, SMOOTHING_WINDOW), 1)
                                    heart_rate_confidence = hr_confidence
                            
                            # 绘制检测区域
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (255, 0, 0), 2)
                            
                            # 心率专用精度优化显示
                            y_offset = 40
                            line_height = 22
                            
                            title_text = "心率专用精度优化健康监测系统"
                            frame = safe_text_display_precision(frame, title_text, (200, 10), 20, (255, 255, 255))
                            
                            # 稳定性状态
                            stability_text = f"稳定性: {stable_face_count}/{STABILITY_THRESHOLD}"
                            frame = safe_text_display_precision(frame, stability_text, (10, y_offset), 16, 
                                                               (0, 255, 0) if face_stable else (255, 165, 0))
                            
                            # 心率显示（带置信度）
                            hr_color = (0, 255, 0) if heart_rate_reliable else (255, 165, 0)
                            hr_text = f"心率: {heart_rate} 次/分钟 ({heart_rate_status}) [置信度: {heart_rate_confidence:.1f}%]"
                            frame = safe_text_display_precision(frame, hr_text, (10, y_offset + line_height*1), 18, hr_color)
                            
                            # 信号质量
                            quality_text = f"信号质量: {signal_quality:.1f}%"
                            quality_color = (0, 255, 0) if signal_quality > 60 else \
                                           (255, 255, 0) if signal_quality > 40 else \
                                           (255, 0, 0)
                            frame = safe_text_display_precision(frame, quality_text, (10, y_offset + line_height*2), 16, quality_color)
                            
                            # 医学参考范围
                            medical_text = f"医学参考范围: {MEDICAL_HR_MIN}-{MEDICAL_HR_MAX} 次/分钟"
                            frame = safe_text_display_precision(frame, medical_text, (10, y_offset + line_height*3), 14, (200, 200, 200))
                            
                            # 精度优化特性说明
                            explanation_texts = [
                                "心率专用精度优化特性:",
                                "• 高级信号预处理",
                                "• 零填充FFT提高频率分辨率", 
                                "• 多峰值检测算法",
                                "• 实时置信度评估",
                                "• 专注于心率检测（无HRV）"
                            ]
                            
                            for i, text in enumerate(explanation_texts):
                                frame = safe_text_display_precision(frame, text, (10, y_offset + line_height*(4+i)), 12, (200, 200, 200))
                            
                            # 操作提示
                            hint_text = "保持面部稳定 | 心率专用系统 | ESC退出 | R重置"
                            frame = safe_text_display_precision(frame, hint_text, (10, frame.shape[0] - 30), 14, (200, 200, 200))
                            
                            # 控制台输出心率信息
                            if frame_count % 30 == 0 and heart_rate > 0:
                                print(f"心率专用系统 - 心率: {heart_rate}bpm[置信度:{heart_rate_confidence:.1f}%], "
                                      f"信号质量: {signal_quality:.1f}%")
                
                else:
                    stable_face_count = 0
                    hint_text = "请将面部对准摄像头，保持稳定姿势"
                    frame = safe_text_display_precision(frame, hint_text, (150, frame.shape[0]//2), 20, (255, 255, 255))
                
                # 显示帧
                cv2.imshow('Heart Rate Precision Only', frame)
                
                # 键盘控制
                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    print("心率专用系统正常退出")
                    break
                elif key == ord('r') or key == ord('R'):
                    print("系统重置")
                    green_buffer.clear()
                    last_hr_values.clear()
                    stable_face_count = 0
                
            except Exception as e:
                print(f"主循环异常: {e}")
                time.sleep(0.1)
        
    except Exception as e:
        print(f"系统启动异常: {e}")
        traceback.print_exc()
    
    finally:
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print("心率专用精度优化健康监测系统已关闭")

if __name__ == "__main__":
    main()