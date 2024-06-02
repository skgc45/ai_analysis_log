import logging
import os
import random
from typing import Union
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from dotenv import load_dotenv

# 環境変数の取得
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_host = os.getenv("DB_HOST")

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my_app")
file_handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# データベース設定
DATABASE_URL = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# データベースモデル
class AnalysisLog(Base):
    __tablename__ = "ai_analysis_log"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, index=True)
    success = Column(Boolean)
    message = Column(String)
    class_ = Column("class", Integer)
    confidence = Column(Float)
    request_timestamp = Column(DateTime)
    response_timestamp = Column(DateTime)


app = FastAPI()


# APIリクエスト用のモデル
class ImagePathReqest(BaseModel):
    image_path: str


class ImagePathResponse(BaseModel):
    success: bool
    message: str
    estimated_data: object  # {"class": int, "confidence": float}


def addAnalysisLog(
    request: ImagePathReqest, response: ImagePathResponse, request_timestamp: datetime
):
    # データベースに結果を保存
    db = None
    try:
        db = SessionLocal()
        log = AnalysisLog(
            image_path=request.image_path,
            success=response["success"],
            message=response["message"],
            class_=response["estimated_data"].get("class"),
            confidence=response["estimated_data"].get("confidence"),
            request_timestamp=request_timestamp,
            response_timestamp=datetime.now(),
        )
        db.add(log)
        db.commit()
    except Exception as e:
        logger.error(
            f"Fail insert DB. request={request}, request_time={request_timestamp}"
        )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if db is not None:
            db.close()


def mock_classify_image(image_data):
    # Imageの解析
    # analys_result = await analys_Image(image_data)
    pass
    # 解析結果の返却
    success = True if random.randint(1, 10) <= 8 else False
    class_ = random.randint(1, 10)
    confidence = round(random.uniform(0, 1), 4)
    errMsg = "" if success else "Error:E50012"
    return success, class_, confidence, errMsg


def check_authorization(authorization_value: Union[str, None]):
    try:
        type_, token = authorization_value.split(" ")
    except:
        logger.error(f"Fail authorization. authorization_header={authorization_value}")
        raise HTTPException(status_code=403)

    # API認可の確認
    if type_ == "Bearer" and token == "dummy_token":
        return
    else:
        logger.error(f"Fail authorization. authorization_header={authorization_value}")
        raise HTTPException(status_code=403)


# APIエンドポイント
@app.post("/analyze-image")
async def analyze_image(
    request: ImagePathReqest, authorization: Union[str, None] = Header(default=None)
):
    request_timestamp = datetime.now()

    # API認可のチェック
    check_authorization(authorization_value=authorization)
    # リクエストのバリデーション
    if len(request.image_path) > 255:
        raise HTTPException(
            status_code=400, detail="length of 'image_path' is greater than 255"
        )
    # Imageのダウンロード
    # image_data =  download_image(request.image_path)
    image_data = None

    # 画像解析
    sucess, class_, confidence, errMsg = mock_classify_image(image_data)

    response: ImagePathResponse
    if sucess:
        response = {
            "success": True,
            "message": "success",
            "estimated_data": {"class": class_, "confidence": confidence},
        }
    else:
        response = {
            "success": False,
            "message": errMsg,
            "estimated_data": {},
        }
    # 解析結果をDB保存
    addAnalysisLog(
        request=request, response=response, request_timestamp=request_timestamp
    )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
