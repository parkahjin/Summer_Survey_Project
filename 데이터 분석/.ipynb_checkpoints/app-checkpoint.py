from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask 애플리케이션 생성
app = Flask(__name__)

# MySQL 데이터베이스 설정 변경
# 'mysql+mysqlconnector://사용자이름:비밀번호@호스트주소:포트번호/데이터베이스이름' 형식
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/survey_db'
db = SQLAlchemy(app)

# User 테이블 모델 (기존 코드와 동일)
class User(db.Model):
    __tablename__ = 'users' # MySQL에서는 테이블 이름을 명시하는 것이 좋습니다
    id = db.Column(db.Integer, primary_key=True) # 아이디
    username = db.Column(db.String(80), unique=True, nullable=False) # 이름
    password = db.Column(db.String(120), nullable=False) # 비밀번호

    def __repr__(self):
        return f'<User {self.username}>'

# Survey 테이블 모델 (기존 코드와 동일)
 class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 어떤 사용자가 응답했는지 연결
    age_group = db.Column(db.String(50), nullable=False) # 1. 연령대
    gender = db.Column(db.String(50), nullable=False) # 2. 성별      
    activity = db.Column(db.String(100), nullable=False) # 3. 활동
    location_type = db.Column(db.String(50), nullable=False) # 4. 장소 (국내/해외)
    location_detail = db.Column(db.String(100), nullable=True) # 4. 장소 세부 정보
    transportation = db.Column(db.String(100), nullable=False) # 5. 교통수단
    duration = db.Column(db.String(50), nullable=False) # 6. 휴가 기간
    companions = db.Column(db.String(100), nullable=False) # 7. 함께한 사람
    expenditure = db.Column(db.String(100), nullable=False) # 8. 총 비용
    satisfaction = db.Column(db.String(50), nullable=False) # 9. 만족도
    next_experience = db.Column(db.String(100), nullable=False) # 10. 다음 휴가 경험
# 데이터베이스 테이블 생성
with app.app_context():
    db.create_all()

# 회원가입 API
@app.route('/register', methods=['POST'])
def register():
    # 1. 사용자가 보낸 JSON 데이터 받기
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 2. 필수 정보가 누락되었는지 확인
    if not username or not password:
        return jsonify({'error': '아이디 또는 비밀번호가 누락되었습니다.'}), 400

    # 3. 이미 존재하는 사용자인지 확인
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': '이미 존재하는 사용자 이름입니다.'}), 409

    # 4. 새로운 User 객체 생성 및 데이터베이스에 추가
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    # 5. 성공 메시지 반환
    return jsonify({'message': '회원가입이 성공적으로 완료되었습니다.'}), 201

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True, port=5001)