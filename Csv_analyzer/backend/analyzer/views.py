from django.http import JsonResponse
from django.http import HttpResponse
import pandas as pd
import os
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

def home(request):
    return HttpResponse("Welcome to CSV Analyzer!")

@ensure_csrf_cookie
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        
        try:
            # CSVをDataFrameとして読み込む
            df = pd.read_csv(csv_file)
            
            # 数値データのみを対象に相関係数を計算
            correlation_matrix = df.corr().to_dict()
            
            return JsonResponse({"message": "CSVを正常に処理しました", "correlation": correlation_matrix})
        
        except Exception as e:
            return JsonResponse({"error": f"CSVの読み込みに失敗: {str(e)}"}, status=400)
    
    return JsonResponse({"error": "ファイルが送信されていません"}, status=400)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})
