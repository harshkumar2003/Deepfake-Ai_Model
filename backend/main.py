# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import shutil, os, traceback

# app = FastAPI()

# # 🔴 TEMP DEBUG CORS (allow all)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_DIR = "uploaded_videos"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload")
# async def upload_video(video: UploadFile = File(...)):
#     try:
#         from scripts.inference import predict_video

#         video_path = os.path.join(UPLOAD_DIR, video.filename)
#         with open(video_path, "wb") as buffer:
#             shutil.copyfileobj(video.file, buffer)

#         result = predict_video(video_path)
#         return result

#     except Exception as e:
#         print("🔥 BACKEND CRASH 🔥")
#         traceback.print_exc()
#         return {"error": str(e)}


# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# import shutil, os, uuid, traceback

# from scripts.inference import predict_video_ensemble  # ✅ use final function

# app = FastAPI()

# # 🔴 TEMP DEBUG CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=False,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_DIR = "uploaded_videos"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload")
# async def upload_video(video: UploadFile = File(...)):
#     file_path = None

#     try:
#         # 🔥 unique filename (VERY IMPORTANT)
#         filename = f"{uuid.uuid4().hex}.mp4"
#         file_path = os.path.join(UPLOAD_DIR, filename)

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(video.file, buffer)

#         # 🔥 prediction
#         result = predict_video_ensemble(file_path)

#         return result

#     except Exception as e:
#         print("🔥 BACKEND CRASH 🔥")
#         traceback.print_exc()
#         return {"error": str(e)}

#     finally:
#         # 🔥 cleanup (VERY IMPORTANT)
#         if file_path and os.path.exists(file_path):
#             os.remove(file_path)


import os
import shutil
import uuid
import traceback

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ── import from the new inference script ──────────────────────────────────────
from scripts.inference import load_all_models, predict_video

# ══════════════════════════════════════════════
#  APP SETUP
# ══════════════════════════════════════════════
app = FastAPI(title="Deepfake Detection API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten this in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv"}
MAX_FILE_MB = 500

# ══════════════════════════════════════════════
#  LOAD MODELS ONCE AT STARTUP  ← key fix
#  Your original code had no startup loading,
#  so models reloaded on every single request.
# ══════════════════════════════════════════════
@app.on_event("startup")
async def startup_event():
    global MODELS
    print("Loading models at startup...")
    MODELS = load_all_models()
    print("Models ready.")

MODELS = {}   # filled at startup


# ══════════════════════════════════════════════
#  HEALTH CHECK
# ══════════════════════════════════════════════
@app.get("/health")
def health():
    return {
        "status": "ok",
        "models_loaded": list(MODELS.keys()),
    }


# ══════════════════════════════════════════════
#  UPLOAD + PREDICT
# ══════════════════════════════════════════════
@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    file_path = None

    try:
        # ── 1. validate file extension ─────────────────────────────────────
        original_name = video.filename or "upload"
        ext = os.path.splitext(original_name)[-1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type '{ext}'. "
                       f"Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # ── 2. validate file size ──────────────────────────────────────────
        video.file.seek(0, 2)           # seek to end
        size_mb = video.file.tell() / (1024 * 1024)
        video.file.seek(0)              # rewind

        if size_mb > MAX_FILE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"File too large ({size_mb:.1f} MB). Max allowed: {MAX_FILE_MB} MB"
            )

        # ── 3. save to disk with unique name ──────────────────────────────
        filename  = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # ── 4. run inference ───────────────────────────────────────────────
        if not MODELS:
            raise HTTPException(
                status_code=503,
                detail="Models not loaded yet. Try again in a moment."
            )

        result = predict_video(file_path, MODELS)

        # ── 5. clean response ──────────────────────────────────────────────
        if result.get("prediction") == "ERROR":
            return JSONResponse(
                status_code=422,
                content={
                    "error":   result.get("error", "Inference failed"),
                    "video":   original_name,
                }
            )

        return {
            "video":            original_name,
            "prediction":       result["prediction"],          # "REAL" / "FAKE" / "UNCERTAIN"
            "authenticity":     result["authenticity"],        # 0–100, higher = more real
            "ensemble_prob":    result["ensemble_prob"],       # raw fake probability
            "frames_used":      result["frames_used"],
            "model_scores": {
                name: score
                for name, score in result["model_scores"].items()
            },
        }

    except HTTPException:
        raise   # let FastAPI handle these normally

    except Exception as e:
        print("═" * 50)
        print("BACKEND CRASH")
        traceback.print_exc()
        print("═" * 50)
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "video": getattr(video, "filename", "unknown")}
        )

    finally:
        # always clean up the uploaded file
        if file_path and os.path.exists(file_path):
            os.remove(file_path)