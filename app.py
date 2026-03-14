"""
科学级rPPG心率检测系统 - Flask后端
基于Web的远程光电容积描记（rPPG）心率检测
"""

from flask import Flask, render_template, jsonify, request
import json
import time
from datetime import datetime
import os

app = Flask(__name__)

# 存储检测数据（生产环境应使用数据库）
detection_sessions = {}


@app.route('/')
def index():
    """主页 - 返回心率检测页面"""
    return render_template('index.html')


@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    """开始新的检测会话"""
    session_id = str(int(time.time()))
    detection_sessions[session_id] = {
        'start_time': datetime.now().isoformat(),
        'data_points': [],
        'status': 'active'
    }
    return jsonify({
        'success': True,
        'session_id': session_id,
        'message': '检测会话已启动'
    })


@app.route('/api/save_data', methods=['POST'])
def save_data():
    """保存检测数据点"""
    data = request.json
    session_id = data.get('session_id')
    
    if session_id not in detection_sessions:
        return jsonify({'success': False, 'error': '会话不存在'}), 404
    
    detection_sessions[session_id]['data_points'].append({
        'timestamp': datetime.now().isoformat(),
        'heart_rate': data.get('heart_rate'),
        'hrv': data.get('hrv'),
        'spo2': data.get('spo2'),
        'distance': data.get('distance'),
        'snr': data.get('snr'),
        'quality': data.get('quality')
    })
    
    return jsonify({'success': True})


@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """生成检测报告"""
    data = request.json
    session_id = data.get('session_id')
    
    if session_id not in detection_sessions:
        return jsonify({'success': False, 'error': '会话不存在'}), 404
    
    session = detection_sessions[session_id]
    data_points = session['data_points']
    
    if len(data_points) == 0:
        return jsonify({'success': False, 'error': '没有足够的数据'}), 400
    
    # 计算统计数据
    hr_values = [dp['heart_rate'] for dp in data_points if dp['heart_rate']]
    hrv_values = [dp['hrv'] for dp in data_points if dp['hrv']]
    spo2_values = [dp['spo2'] for dp in data_points if dp['spo2']]
    distance_values = [dp['distance'] for dp in data_points if dp['distance']]
    snr_values = [dp['snr'] for dp in data_points if dp['snr']]
    
    def safe_avg(values):
        return round(sum(values) / len(values), 1) if values else 0
    
    def safe_min(values):
        return min(values) if values else 0
    
    def safe_max(values):
        return max(values) if values else 0
    
    def safe_std(values):
        if len(values) < 2:
            return 0
        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        return round(variance ** 0.5, 1)
    
    # 生成结论
    avg_hr = safe_avg(hr_values)
    hr_stability = safe_std(hr_values)
    avg_hrv = safe_avg(hrv_values)
    avg_spo2 = safe_avg(spo2_values)
    avg_snr = safe_avg(snr_values)
    
    conclusion_parts = []
    
    # 心率结论
    if 60 <= avg_hr <= 100:
        conclusion_parts.append(f"平均心率{avg_hr:.0f}bpm处于正常静息范围")
    elif avg_hr > 100:
        conclusion_parts.append(f"平均心率{avg_hr:.0f}bpm偏高，可能处于活动状态")
    else:
        conclusion_parts.append(f"平均心率{avg_hr:.0f}bpm偏低，可能是运动员体质")
    
    # 稳定性结论
    if hr_stability < 3:
        conclusion_parts.append("，心率非常稳定")
    elif hr_stability < 6:
        conclusion_parts.append("，心率较为稳定")
    else:
        conclusion_parts.append("，心率波动较大")
    
    # HRV结论
    if avg_hrv > 0:
        if avg_hrv > 100:
            conclusion_parts.append("；HRV优秀，自主神经功能健康")
        elif avg_hrv >= 50:
            conclusion_parts.append("；HRV正常")
        else:
            conclusion_parts.append("；HRV偏低，可能存在疲劳或压力")
    
    # 信号质量结论
    if avg_snr >= 10:
        conclusion_parts.append("；信号质量良好，结果可信度高")
    elif avg_snr >= 5:
        conclusion_parts.append("；信号质量一般，结果可供参考")
    else:
        conclusion_parts.append("；信号质量较差，建议重新测量")
    
    report = {
        'success': True,
        'session_id': session_id,
        'duration': len(data_points),
        'avgHR': round(avg_hr),
        'minHR': safe_min(hr_values),
        'maxHR': safe_max(hr_values),
        'hrStability': round(hr_stability, 1),
        'avgHRV': round(avg_hrv),
        'avgSpO2': round(avg_spo2),
        'avgDistance': round(safe_avg(distance_values)),
        'avgSNR': round(avg_snr, 1),
        'signalQuality': '良好' if avg_snr >= 10 else ('一般' if avg_snr >= 5 else '较差'),
        'conclusion': ''.join(conclusion_parts)
    }
    
    session['status'] = 'completed'
    session['report'] = report
    
    return jsonify(report)


@app.route('/api/export_report', methods=['POST'])
def export_report():
    """导出检测报告为JSON"""
    data = request.json
    session_id = data.get('session_id')
    
    if session_id not in detection_sessions:
        return jsonify({'success': False, 'error': '会话不存在'}), 404
    
    session = detection_sessions[session_id]
    
    export_data = {
        'export_time': datetime.now().isoformat(),
        'session': session
    }
    
    return jsonify(export_data)


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len([s for s in detection_sessions.values() if s['status'] == 'active'])
    })


if __name__ == '__main__':
    # 确保templates目录存在
    os.makedirs('templates', exist_ok=True)
    
    print("=" * 50)
    print("科学级rPPG心率检测系统")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
