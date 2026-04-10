# Day24 - Streamlit to FastAPI Fullstack

## Overview
오늘은 가구 이미지 유사도 검색 서비스를 만들면서  
**Streamlit 기반 프로토타입**과 **FastAPI + HTML/JS 기반 풀스택 구조**를 모두 경험했다.

처음에는 Streamlit으로 빠르게 검색 기능을 구현했고,  
이후 FastAPI와 프론트엔드를 직접 연결하면서 서비스 구조를 더 확장해봤다.

## Tech Stack
- Python
- Streamlit
- FastAPI
- ChromaDB
- PyTorch
- Transformers
- HTML / CSS / JavaScript
- LocalStorage

## What I Implemented

### 1. Streamlit Prototype
- Streamlit을 사용해 가구 이미지 검색 기능을 빠르게 프로토타이핑했다.
- DINOv2 기반 임베딩 추출과 ChromaDB 검색 결과를 카드 형태로 바로 확인할 수 있게 구성했다.
- 슬라이더로 검색 개수를 조절하고, 업로드한 이미지와 유사 결과를 한 화면에서 비교할 수 있도록 만들었다.

### 2. Image Embedding Extraction
- DINOv2 기반 모델을 사용해 가구 이미지의 특징 벡터(embedding)를 추출했다.
- 이미지 분류가 아니라 벡터 유사도 비교를 위한 표현 추출 흐름을 이해했다.
- 임베딩 추출 방식으로 `pooler_output`과 `CLS token(last_hidden_state[:, 0, :])` 활용 가능성을 확인했다.

### 3. Vector Search with ChromaDB
- 추출한 임베딩을 ChromaDB에 연결해 유사한 가구 이미지를 검색했다.
- 검색 결과를 distance 기준으로 정렬하고, 가장 유사한 이미지를 반환하도록 구성했다.
- 키워드 검색이 아닌 벡터 유사도 기반 검색 흐름을 직접 구현했다.

### 4. FastAPI Backend
- 이미지 업로드를 처리하는 `POST /search` API를 구현했다.
- 업로드 이미지 → 임베딩 추출 → DB 검색 → JSON 응답까지 하나의 흐름으로 연결했다.
- StaticFiles 설정을 통해 결과 이미지를 프론트엔드에서 바로 표시할 수 있도록 구성했다.
- `0.0.0.0` 호스트 설정으로 모바일 기기에서도 테스트 가능한 환경을 만들었다.

### 5. Frontend UI / UX
- HTML / CSS / JavaScript로 검색 결과를 직접 렌더링하는 프론트엔드를 구성했다.
- 단순 검색 결과 리스트 대신 **시상식 컨셉의 TOP 3 발표 UI**를 구현했다.
- 3위 → 2위 → 1위 순서로 결과를 공개하는 unveiling 로직을 적용했다.
- 버튼 활성화/비활성화 상태를 순차적으로 제어해 발표 흐름을 만들었다.

### 6. Search History System
- LocalStorage를 사용해 최근 5회 검색 기록을 저장하는 기능을 추가했다.
- 업로드 이미지, 결과, 시간을 함께 저장해 간단한 히스토리 시스템을 구현했다.

## Streamlit vs FastAPI

### Streamlit에서 느낀 점
- 빠르게 기능을 확인하고 프로토타입을 만들기에 좋았다.
- Python만으로 화면까지 바로 구성할 수 있어서 구현 속도가 빨랐다.

### FastAPI에서 느낀 점
- 백엔드와 프론트엔드를 분리해서 더 서비스다운 구조를 만들 수 있었다.
- API 응답, 정적 파일 처리, 프론트 UI 제어까지 직접 다루면서 구조를 더 깊게 이해할 수 있었다.

## Issues and Fixes

### Issue 1. Mobile access was not available
- `127.0.0.1` 환경에서는 모바일 기기에서 서버에 접속할 수 없었다.
- 서버 호스트를 `0.0.0.0`으로 변경해 같은 네트워크 환경에서 접속 가능하도록 수정했다.

### Issue 2. Search results were functional but visually flat
- 결과를 단순 카드 형태로만 보여주면 임팩트가 약했다.
- 시상식 컨셉 UI와 순차 공개 방식을 적용해 결과 확인 과정 자체를 더 흥미롭게 바꿨다.

### Issue 3. Code complexity increased as features grew
- 검색, UI 제어, 히스토리 저장 기능이 추가되면서 코드가 점점 복잡해졌다.
- 반복되는 로직을 줄이고 구조를 정리하면서 가독성을 높이려고 했다.

## What I Learned
- Streamlit은 빠른 프로토타입에 강하고, FastAPI는 구조화된 서비스 구현에 더 적합하다는 점을 체감했다.
- 벡터 검색은 단순 분류와 다른 방식의 문제 해결 흐름이라는 점을 이해했다.
- 기능 구현뿐 아니라 UI/UX 설계가 결과물의 완성도를 크게 바꾼다는 점을 느꼈다.

## Next Step
- `day24_Chroma_Fullstack` 프로젝트 폴더 GitHub 업로드 및 README 정리
- 프로젝트 README 작성
- 전처리 및 임베딩 추출 방식 비교
- 검색 정확도 개선 방향 실험
- 프론트엔드/백엔드 코드 구조 정리