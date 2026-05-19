import speech_recognition as sr            #speech_recognition 라이브러리를 불러온다   
import requests     # HTTP 요청을 보내기 위한 라이브러리를 불러옴
import os            # 운영체제 명령어 실행을 위한 라이브러리를 불러옴 
import time         # 시관관련 기능을 사용하는 라이브러리를 불러옴 

API_KEY = "Enter your API key here"   #본인의 API키를 입력 
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"  # 기상청 날씨 데이터 주소를 저장 

def speak(option, msg):  # 음성을 출력하기 위한 speak라는 함수를 만듦  
    os.system("espeak {} '{}'".format(option, msg))   # espeak 명령어로 option 설정과 msg를 음성으로 출력 

try:
    while True:  #무한반복 
        r = sr.Recognizer()  #음성인식 객체를 생성 
        
        with sr.Microphone() as source:  #마이크를 사용 source에 마이크 입력을 저장 
            print("Say something!")   # 말하라고 안내 
            audio = r.listen(source)   #마이크로 들어온 음성을 녹음 후 audio에 저장 
            
        try:
            text = r.recognize_google(audio, language='ko-KR')  # 데이터를 한국어로 변환 
            print("You said: " + text)    # 사용자가 말한 내용을 출력 
            if text in "날씨":  # 날씨라고 말했으면 
                print("날씨 음성을 인식하였습니다.")    # 날씨 음성을 인식하였습니다. 출력 
                response = requests.get(url)   # 기상청 사이트에 접속하여 데이터를 가져옴   
                data = response.json()          # 데이터를 json형식으로 변환 
                temp = data["main"]["temp"]     # 기온 정보를 추출 
                humi = data["main"]["humidity"]  # 습도 정보를 추출 
                
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'    # 출력할 문장을 만듦 
                
                option = '-s 180 -p 50 -a 200 -v ko+f5'   #음성 출력 설정 
                speak(option, msg)      #날씨 정보를 음성으로 읽음 
            
        except sr.UnknownValueError:    #음성을 알아듣지 못 하였을 때 
            print("Google Speech Recognition could not understand audio")    # 실패 메세지 출력 
        except sr.RequestError as e:    #인터넷 문제나 음성 서비스 문제일 때 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))    #오류 내용을 출력 

except KeyboardInterrupt:    #ctrl c로 강제종료
    pass    #강제종
