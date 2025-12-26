import os
import sys
import warnings
import webbrowser
from dotenv import load_dotenv
from googleapiclient.discovery import build
import auth

# Google API의 Python 버전 경고 메시지 숨기기
warnings.filterwarnings('ignore', category=FutureWarning, module='google.api_core._python_version_support')

# API 키 디렉토리 경로
API_KEY_DIR = "/Users/a1/github/api_key"
ENV_PATH = os.path.join(API_KEY_DIR, ".env")

def ensure_env_loaded():
    """지정된 .env를 로드한다. auth.py가 참조할 수 있게 선 로드"""
    load_dotenv(dotenv_path=ENV_PATH, override=False)

def fetch_first_five_rows(spreadsheet_id, sheet_name):
    """스프레드시트에서 첫 5행을 가져옵니다"""
    ensure_env_loaded()
    
    creds = auth.get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    
    # 시트 이름에 특수문자나 한글이 있으면 작은따옴표로 감싸야 함
    range_a1 = f"'{sheet_name}'!A1:Z5"
    
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_a1,
        majorDimension="ROWS"
    ).execute()
    
    values = result.get('values', [])
    return values

def main():
    """메인 함수"""
    spreadsheet_id = "1YWiFGyJjNDbOC8eFTbS1HEhmxfZAC-hLvI8KdA1Gku8"
    sheet_name = "테스트"
    
    # 구글 시트 URL 생성 및 브라우저에서 열기
    sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    print(f"구글 시트 열기: {sheet_url}")
    webbrowser.open(sheet_url)
    
    try:
        rows = fetch_first_five_rows(spreadsheet_id, sheet_name)
        
        if not rows or len(rows) == 0:
            print("데이터가 없습니다.")
            return
        
        for idx, row in enumerate(rows):
            row_str = "\t".join(str(cell) for cell in row)
            print(f"[{idx}]\t{row_str}")
    except Exception as e:
        print(f"Google Sheets API 호출 실패: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

