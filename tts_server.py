# tts_server.py - 简单的 TTS HTTP 服务
import http.server
import asyncio
import subprocess
import tempfile
import os
import base64
import json
from urllib.parse import urlparse, parse_qs

class TTSHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/tts':
            params = parse_qs(parsed.query)
            text = params.get('text', [''])[0]
            if not text:
                self.send_error(400, 'Missing text')
                return
            
            try:
                # 用 edge-tts 生成音频
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                    tmp_path = tmp.name
                
                # 运行 edge-tts
                result = subprocess.run([
                    'edge-tts',
                    '--voice', 'zh-CN-XiaoxiaoNeural',
                    '--rate', '-15%',
                    '--text', text,
                    '--write-media', tmp_path
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    self.send_error(500, f'TTS failed: {result.stderr}')
                    return
                
                # 读取音频并返回
                with open(tmp_path, 'rb') as f:
                    audio_data = f.read()
                os.unlink(tmp_path)
                
                self.send_response(200)
                self.send_header('Content-Type', 'audio/mpeg')
                self.send_header('Content-Length', len(audio_data))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(audio_data)
                
            except Exception as e:
                self.send_error(500, str(e))
        else:
            super().do_GET()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.end_headers()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8889
    server = http.server.HTTPServer(('', port), TTSHandler)
    print(f'TTS server running on port {port}')
    server.serve_forever()
