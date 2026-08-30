from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests

app = Flask(__name__)
# 모든 도메인과 출처에서의 접근을 완전 허용
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['JSON_AS_ASCII'] = False  # 한글 깨짐 방지

def validate_inputs(target_date, region):
    """[검증 레이어] 필수 파라미터 및 날짜 포맷 확인"""
    if not target_date or not region:
        return False, "필수 파라미터(date 또는 region)가 누락되었습니다."
    try:
        datetime.strptime(target_date, '%Y-%m-%d')
    except ValueError:
        return False, "날짜 형식은 YYYY-MM-DD여야 합니다."
    return True, ""

def fetch_foresttrip_data(target_date, region):
    """[수집 레이어] 실제 통신 규격 모방 및 안티봇 헤더 적용"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.foresttrip.go.kr/"
    }
    
    # ---------------------------------------------------------
    # [네트워크 통신 골격] 추후 실제 API 엔드포인트 연동 시 사용할 구조
    # api_url = "https://www.foresttrip.go.kr/api/search..."
    # payload = {"searchDate": target_date, "regionCode": region}
    # try:
    #     response = requests.post(api_url, headers=headers, json=payload, timeout=5)
    #     response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     print(f"API 통신 에러: {e}")
    #     return [] # 통신 실패 시 빈 리스트 반환
    # ---------------------------------------------------------

    # 현재는 로직 검증을 위한 고도화된 마스터 데이터베이스 운영
    master_database = [
        {"id": "f01", "name": "국립 거제자연휴양림", "region": "gyeongnam", "room": "숲속의집 101호", "price": 72000, "status": "AVAILABLE"},
        {"id": "f02", "name": "국립 남해편백자연휴양림", "region": "gyeongnam", "room": "산림문화휴양관 302호", "price": 43000, "status": "AVAILABLE"},
        {"id": "f03", "name": "국립 대관령자연휴양림", "region": "gangwon", "room": "숲속의집 소나무", "price": 100000, "status": "AVAILABLE"},
        {"id": "f04", "name": "국립 유명산자연휴양림", "region": "seoul_gyeonggi", "room": "숲속의집 다람쥐", "price": 82000, "status": "SOLD_OUT"}
    ]

    filtered_results = []
    for item in master_database:
        if region == "all" or item["region"] == region:
            filtered_results.append({
                "forestName": item["name"],
                "roomName": item["room"],
                "price": f"{item['price']:,}원",
                "status": "예약가능" if item["status"] == "AVAILABLE" else "마감"
            })
            
    return filtered_results

@app.route('/api/vacancies', methods=['GET'])
def get_vacancies():
    """[컨트롤러] k-skill 명세에 따른 표준 흐름 제어"""
    target_date = request.args.get('date')
    region = request.args.get('region', 'all')

    # 1. 입력값 검증 (Validation)
    is_valid, err_msg = validate_inputs(target_date, region)
    if not is_valid:
        return jsonify({"error": True, "message": err_msg}), 400

    try:
        # 2. 데이터 수집 (Fetch)
        data = fetch_foresttrip_data(target_date, region)
        
        # 3. 표준화된 응답 포맷 (Standardized Output)
        return jsonify({
            "error": False,
            "count": len(data),
            "date": target_date,
            "region": region,
            "results": data
        }), 200

    except Exception as e:
        return jsonify({"error": True, "message": f"서버 내부 오류 발생: {str(e)}"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)