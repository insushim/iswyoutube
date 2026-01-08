"""
Firebase Client Module
======================
Firebase 연동을 위한 클라이언트
"""

import os
from typing import Dict, Optional
from pathlib import Path


class FirebaseClient:
    """Firebase 클라이언트"""

    def __init__(self):
        self.db = None
        self.storage = None
        self.initialized = False
        self._load_config()

    def _load_config(self):
        """환경변수에서 Firebase 설정 로드"""
        from dotenv import load_dotenv
        load_dotenv('config/api_keys.env')

        self.config = {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
        }

    def initialize(self):
        """Firebase Admin SDK 초기화"""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore, storage

            if self.initialized:
                return True

            service_account_path = "config/firebase-service-account.json"
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred, {
                    'storageBucket': self.config.get('storageBucket')
                })
            else:
                try:
                    firebase_admin.get_app()
                except ValueError:
                    firebase_admin.initialize_app(options={
                        'storageBucket': self.config.get('storageBucket')
                    })

            self.db = firestore.client()
            self.storage = storage.bucket()
            self.initialized = True
            print("✓ Firebase initialized successfully")
            return True

        except Exception as e:
            print(f"Firebase initialization error: {e}")
            return False

    def save_project(self, project_id: str, data: Dict) -> bool:
        """프로젝트 데이터 저장"""
        if not self.initialized:
            self.initialize()

        if not self.db:
            return False

        try:
            self.db.collection('projects').document(project_id).set(data)
            return True
        except Exception as e:
            print(f"Save project error: {e}")
            return False

    def get_project(self, project_id: str) -> Optional[Dict]:
        """프로젝트 데이터 조회"""
        if not self.initialized:
            self.initialize()

        if not self.db:
            return None

        try:
            doc = self.db.collection('projects').document(project_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Get project error: {e}")
            return None

    def upload_file(self, local_path: str, remote_path: str) -> Optional[str]:
        """파일 업로드 및 URL 반환"""
        if not self.initialized:
            self.initialize()

        if not self.storage:
            return None

        try:
            blob = self.storage.blob(remote_path)
            blob.upload_from_filename(local_path)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"Upload file error: {e}")
            return None

    def download_file(self, remote_path: str, local_path: str) -> bool:
        """파일 다운로드"""
        if not self.initialized:
            self.initialize()

        if not self.storage:
            return False

        try:
            blob = self.storage.blob(remote_path)
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(local_path)
            return True
        except Exception as e:
            print(f"Download file error: {e}")
            return False


# 싱글톤 인스턴스
firebase_client = FirebaseClient()
