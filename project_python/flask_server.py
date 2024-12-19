from flask import Flask, Response
from flask_cors import CORS

def run_flask_server(latest_frame, stop_event):
    """Flask 서버 실행 및 최신 프레임 제공"""
    app = Flask(__name__)
    CORS(app)

    @app.route('/video_feed')
    def video_feed():
        """비디오 프레임을 반환하는 엔드포인트"""
        def generate():
            while not stop_event.is_set():
                if latest_frame.value:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + latest_frame.value + b'\r\n')
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

    print("Flask server running on http://0.0.0.0:6001")
    app.run(host='0.0.0.0', port=6001, debug=False, use_reloader=False)
