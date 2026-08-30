from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 웹앱(프론트엔드)에서 보내는 요청을 서버가 차단하지 않도록 허용해주는 설정

# 숲나들e 조회 기능을 흉내 내는 백엔드 API 라우트
@app.route('/api/vacancies', methods=['GET'])
def get_vacancies():
    # 웹앱에서 보낸 날짜와 지역 파라미터 받기
    target_date = request.args.get('date', '날짜 미지정')
    region = request.args.get('region', 'all')
    
    print(f"[요청 수신] 날짜: {target_date}, 지역: {region}")

    # 실제 숲나들e 데이터 연동 영역 (현재는 시뮬레이션 데이터 반환)
    mock_data = [
        {"name": "거제 자연휴양림", "room": "숲속의집 101호", "status": "예약가능"},
        {"name": "남해 편백휴양림", "room": "휴양관 302호", "status": "예약가능"},
        {"name": "지리산 자연휴양림", "room": "카라반 B구역", "status": "잔여 1개"}
    ]
    
    # JSON 형태로 웹앱에 응답 데이터 전송
    return jsonify(mock_data)

import os

if __name__ == '__main__':
    # 클라우드가 지정해주는 포트가 있으면 그곳을 쓰고, 없으면 5000번을 씀
    port = int(os.environ.get("PORT", 5000))
    print(f"🌲 숲나들e 백엔드 서버가 포트 {port}에서 시작됩니다!")
    app.run(host='0.0.0.0', port=port)