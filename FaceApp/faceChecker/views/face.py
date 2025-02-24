from django.shortcuts import render 
from django.http import HttpResponse
import cv2
from django.http import JsonResponse
import os
import time
from django.conf import settings
from scipy.spatial.distance import euclidean
import dlib
import numpy as np
from faceChecker.models.models import FaceFeature

# dlibのモデルのパス
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/shape_predictor_68_face_landmarks.dat")

# モデルを読み込む
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(MODEL_PATH) 

def hello_world(request):
    return HttpResponse("Hello, World!")

def camera_view(request):
    return render(request, "camera.html")

def normalize_features(features):
    """ 顔の特徴点を正規化する（顔の中央を原点にし、スケールを統一） """
    mean = np.mean(features, axis=0)  # 中心を求める
    norm_features = features - mean  # 平均を引いて中心化
    norm_features /= np.linalg.norm(norm_features)  # ノルム（長さ）で割ってスケール統一
    return norm_features

def is_already_registered(new_features, threshold=0.1):  # しきい値を調整
    """ 既存データと比較し、しきい値以下なら登録済みと判定（正規化後） """
    new_features = normalize_features(new_features)  # 🔹 新しいデータを正規化

    existing_features = FaceFeature.objects.all()

    for face in existing_features:
        stored_features = normalize_features(face.get_features())  # 🔹 既存データも正規化
        distance = euclidean(new_features.flatten(), stored_features.flatten())  
        print(f"Distance: {distance}")  
        if distance < threshold:
            return True  

    return False  

def capture_photo(request):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not camera.isOpened():
        print("Error: Camera not opened")  # 🔍 デバッグ用のログ出力
        return JsonResponse({"error": "Failed to open camera"}, status=500)

    time.sleep(2)

    ret, frame = camera.read()
    camera.release()

    if not ret or frame is None:
        print("Error: Failed to capture frame")  # 🔍 デバッグ用のログ出力
        return JsonResponse({"error": "Failed to capture photo"}, status=500)

    save_path = "media/captured_face.jpg"
    os.makedirs("media", exist_ok=True)
    cv2.imwrite(save_path, frame)

    features = extract_face_features(frame)
    if features is None:
        print("Error: No face detected")  # 🔍 デバッグ用のログ出力
        return JsonResponse({"error": "No face detected"}, status=400)

    if is_already_registered(features):
                return JsonResponse({"message": "既に登録されています"})

    # データベースに保存
    face_feature = FaceFeature()
    face_feature.set_features(features)
    face_feature.save()
    
    return JsonResponse({
        "message": "Photo captured and features saved",
        "image_url": "/media/captured_face.jpg"
    })


def extract_face_features(image):
    """ 顔の特徴量を抽出する関数 """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None

    for face in faces:
        landmarks = predictor(gray, face)
        features = np.array([(p.x, p.y) for p in landmarks.parts()], dtype=np.float64)
        return features  # 最初の顔の特徴量を返す

    return None

def get_face_features(request):
    """ データベースから最新の顔特徴量を取得する """
    latest_feature = FaceFeature.objects.last()
    
    if latest_feature:
        features = latest_feature.get_features().tolist()  # NumPy → Pythonリスト
        return JsonResponse({"features": features})
    else:
        return JsonResponse({"error": "No features found"}, status=404)