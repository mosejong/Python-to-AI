import streamlit as st
import chromadb
import torch
from transformers import ViTImageProcessor, ViTModel
from PIL import Image
import os
from pyngrok import ngrok

# --- [디자인 설정: 배경색 & 폰트] ---
st.set_page_config(page_title="Furniture Finder 🛋️", layout="wide")
st.markdown("""
    <div style='background-color: #1e293b; padding: 20px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #334155;'>
        <h1 style='text-align: center; color: #35c5f0; font-size: 2.5rem; margin-bottom: 0;'>
            🛋️ 가구 이미지 검색 엔진
        </h1>
        <p style='text-align: center; color: #94a3b8; font-size: 1.1rem; margin-top: 10px;'>
            가구 사진을 올리면 <b>DINO v2 AI</b>가 데이터베이스에서 가장 유사한 제품을 찾아냅니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- [ngrok 설정: 에러 방지용] ---
try:
    # 이미 열려있는 터널이 있는지 확인 ㅡㅡ
    tunnels = ngrok.get_tunnels()
    if not tunnels:
        public_url = ngrok.connect(8501)
        st.sidebar.success(f"🌍 외부 링크 활성화됨!")
        st.sidebar.code(public_url)
    else:
        st.sidebar.info(f"🌍 기존 링크 사용 중: {tunnels[0].public_url}")
except:
    pass

# --- [사이드바 디자인] ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/sofa.png")
    st.title("Furniture AI")
    st.write("DINO v2 가구 검색 엔진")
    num_results = st.slider("🔍 몇 개의 가구를 찾을까요?", 1, 5, 3)
    st.divider()
    st.caption("Produced by High School Developer ㅡㅡv")

# --- [모델 & DB 로드] ---
@st.cache_resource
def load_resources():
    processor = ViTImageProcessor.from_pretrained('facebook/dino-vits16')
    model = ViTModel.from_pretrained('facebook/dino-vits16').to("cpu")
    client = chromadb.PersistentClient(path="./persist_db")
    collection = client.get_collection(name="furniture")
    return processor, model, collection

processor, model, collection = load_resources()

# --- [메인 화면 UI] ---
st.title("🛋️ 어떤 가구인지 찾아드릴까요?")
st.write("---")

uploaded_file = st.file_uploader("📷 가구 사진을 여기에 올려주세요", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    query_img = Image.open(uploaded_file).convert("RGB")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📌 내가 업로드한 이미지")
        st.image(query_img, use_container_width=True)

    with col2:
        st.subheader("✨ AI가 추천하는 유사 가구")
        
        # 검색 로직
        inputs = processor(images=query_img, return_tensors="pt").to("cpu")
        with torch.no_grad():
            outputs = model(**inputs)
        query_embedding = outputs.pooler_output.squeeze().numpy().tolist()
        
        results = collection.query(query_embeddings=[query_embedding], n_results=num_results)

        # 결과 카드형 배치 ㅡㅡ
        res_cols = st.columns(num_results)
        for i, metadata in enumerate(results["metadatas"][0]):
            with res_cols[i]:
                # 경로 세탁
                raw_path = metadata['uri']
                clean_path = raw_path.replace("/content/furniture/", "furniture/img/")
                
                with st.container(border=True): # 카드 테두리!
                    if os.path.exists(clean_path):
                        st.image(Image.open(clean_path), use_container_width=True)
                    else:
                        st.error("이미지 누락")
                    
                    st.markdown(f"<div style='color: #35c5f0; font-weight: bold;'>{metadata['name'].upper()}</div>", unsafe_allow_html=True)
                    st.caption(f"Similarity Distance: {results['distances'][0][i]:.2f}")