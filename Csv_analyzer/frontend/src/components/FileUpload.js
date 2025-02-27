import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState(null);  // ファイルを保存するためのstate
  const [message, setMessage] = useState('');
  const [correlation, setCorrelation] = useState(null);  // 相関関係のstate

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);  // ドロップしたファイルをsetFileで保存
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  // CSRFトークンをcookieから取得する関数
  const getCsrfToken = async () => {
    try {
      const response = await axios.get('http://localhost:8000/csrf/', { withCredentials: true });
      document.cookie = `csrftoken=${response.data.csrfToken}; path=/`;
      console.log("取得したCSRFトークン:", response.data.csrfToken);
      return response.data.csrfToken;
    } catch (error) {
      console.error("CSRFトークンの取得に失敗しました:", error);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('ファイルを選択してください');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const csrfToken = await getCsrfToken();  // CSRFトークンを取得
    console.log(csrfToken);
    try {
      const response = await axios.post('http://localhost:8000/upload_csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      });
      setMessage(response.data.message);
      
      // 相関関係を取得してセット
      setCorrelation(response.data.correlation);
    } catch (error) {
      if (error.response) {
        setMessage('アップロード失敗: ' + error.response.data.error);
      } else if (error.request) {
        setMessage('サーバーに接続できませんでした');
      } else {
        setMessage('エラーが発生しました: ' + error.message);
      }
    }    
  };

  return (
    <div>
      <div {...getRootProps()} style={{ border: '2px dashed #aaa', padding: '20px', textAlign: 'center' }}>
        <input {...getInputProps()} />
        <p>{file ? file.name : 'ここにCSVファイルをドラッグ＆ドロップ、またはクリックして選択'}</p>
      </div>
      <button onClick={handleUpload} style={{ marginTop: '10px' }}>アップロード</button>
      {message && <p>{message}</p>}
      
      {/* 相関関係の結果を表示 */}
      {correlation && (
        <div>
          <h3>相関関係の結果</h3>
          <pre>{JSON.stringify(correlation, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
