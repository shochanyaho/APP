from django.db import models
import numpy as np

class FaceFeature(models.Model):
    id = models.AutoField(primary_key=True)  # ID（自動増加）
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    features = models.BinaryField()  # 顔特徴量（バイナリデータとして保存）

    def set_features(self, feature_array):
        """ NumPy 配列をバイナリデータに変換して保存 """
        self.features = np.array(feature_array).tobytes()

    def get_features(self):
        """ バイナリデータを NumPy 配列に復元 """
        return np.frombuffer(self.features, dtype=np.float64).reshape(-1, 2)
