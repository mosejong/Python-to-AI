from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import chromadb
import torch
from transformers import ViTImageProcessor, ViTModel
from PIL import Image
import io
import os

app = FastAPI()

# --- [정적 파일 설정] ---
# 스트림릿에서 썼던 이미지 폴더를 연결해 ㅡㅡv
app.mount("/furniture", StaticFiles(directory="furniture"), name="furniture")

# --- [리소스 로드] ---
# @st.cache_resource 대신 전역 변수로 로드 (서버 켜질 때 1회)
processor = ViTImageProcessor.from_pretrained('facebook/dino-vits16')
model = ViTModel.from_pretrained('facebook/dino-vits16').to("cpu")
client = chromadb.PersistentClient(path="./persist_db")
collection = client.get_collection(name="furniture")

@app.get("/", response_class=HTMLResponse)
async def main():
    # 프론트엔드 HTML 호출
    return open("index.html", encoding="utf-8").read()

@app.post("/search")
async def search(file: UploadFile = File(...), num_results: int = 3):
    # 1. 이미지 읽기
    img_data = await file.read()
    query_img = Image.open(io.BytesIO(img_data)).convert("RGB")
    
    # 2. 벡터화 (클로드가 말한 세밀한 버전 vs 정석 버전 선택 가능)
    inputs = processor(images=query_img, return_tensors="pt").to("cpu")
    
    with torch.no_grad():
        outputs = model(**inputs)
        
        # [방법 A] 정석 (pooler_output)
        # query_embedding = outputs.pooler_output.squeeze().numpy().tolist()
        
        # [방법 B] 클로드 추천 (last_hidden_state의 CLS 토큰) - 주석 해제해서 써봐!
        query_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy().tolist()

    # 3. DB 검색
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=num_results
    )

    # 4. 결과 가공 (스트림릿의 '경로 세탁' 로직 포함)
    matches = []
    for i, metadata in enumerate(results["metadatas"][0]):
        # 스트림릿에서 하던 경로 세탁을 여기서 미리 해서 보냄 ㅡㅡv
        raw_path = metadata['uri']
        clean_path = raw_path.replace("/content/furniture/", "furniture/img/")
        
        matches.append({
            "name": metadata['name'].upper(),
            "distance": round(results['distances'][0][i], 4),
            "image_url": f"/{clean_path}" # 프론트에서 바로 쓸 주소
        })
    
    return {"matches": matches}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)