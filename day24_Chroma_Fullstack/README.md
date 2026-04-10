# 🛋️ Furniture Awards AI

DINOv2와 ChromaDB를 활용해 가구 이미지의 임베딩을 추출하고,  
유사한 가구를 검색한 뒤 **시상식 형태의 UI**로 결과를 보여주는 이미지 검색 프로젝트입니다.

Streamlit으로 빠르게 프로토타입을 만들고,  
이후 FastAPI + HTML/CSS/JavaScript 구조로 확장해 서비스형 흐름으로 구현했습니다.

---

## ✨ 주요 기능

- **DINOv2 기반 이미지 임베딩 추출**
  - 업로드한 가구 이미지를 벡터(embedding)로 변환
- **ChromaDB 기반 유사도 검색**
  - 벡터 유사도를 기준으로 가장 비슷한 가구 검색
- **Streamlit 버전**
  - 빠른 프로토타이핑 및 검색 결과 확인용
- **FastAPI 버전**
  - 백엔드 API + 프론트엔드 분리 구조
- **Award System**
  - TOP 3 결과를 3위 → 2위 → 1위 순으로 공개하는 시상식 UI
- **History System**
  - 최근 5회 검색 기록 저장(LocalStorage)

---

## 🛠 Tech Stack

- Python
- Streamlit
- FastAPI
- ChromaDB
- Torch
- Transformers
- Pillow
- HTML / CSS / JavaScript
- LocalStorage

---

## 📂 Project Structure

```text
day24_Chroma_Fullstack/
├── app.py          # Streamlit 프로토타입 버전
├── server.py       # FastAPI 서버
├── index.html      # FastAPI용 프론트엔드 UI
├── requirements.txt
└── persist_db/     # ChromaDB 저장소
```

---

## 🚀 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. FastAPI 버전 실행

```bash
uvicorn server:app --host 0.0.0.0 --port 8501
```

실행 후 브라우저에서 접속:

```text
http://127.0.0.1:8501
```

같은 네트워크 환경에서는 모바일에서도 접속 가능합니다.

### 3. Streamlit 버전 실행

```bash
streamlit run app.py
```

---

## 🔍 구현 포인트

- DINOv2를 사용해 이미지 특징 벡터를 추출
- ChromaDB에 저장된 벡터와 비교해 유사한 가구 검색
- FastAPI에서 이미지 업로드 → 검색 → JSON 응답 흐름 구성
- 프론트엔드에서 결과를 시상식 UI로 렌더링
- LocalStorage를 활용해 최근 검색 기록 저장

---

## 📌 느낀 점

이 프로젝트를 통해  
**벡터 검색 + API 서버 + 프론트엔드 UI**를 하나의 흐름으로 연결하는 경험을 할 수 있었습니다.

단순 검색 기능 구현을 넘어서,  
결과를 어떻게 보여줄지까지 고민하면서 UX의 중요성도 함께 느꼈습니다.

---

## 🧩 개선 예정

- 검색 정확도 향상을 위한 전처리 개선
- 임베딩 추출 방식 비교
- UI 애니메이션 고도화
- 코드 구조 분리 및 리팩토링