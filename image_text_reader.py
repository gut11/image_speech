import pytesseract
import language_tool_python as languagetool
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
import cv2
import gtts


def text_to_speech(text):
    return gtts.gTTS(text=text, lang="pt", slow=False)


def get_image_text(img_path):
    return pytesseract.image_to_string(img_path, lang="por")


def correct_text(text):
    tool = languagetool.LanguageTool("pt-BR")
    corrected_text = tool.correct(text)
    return corrected_text


def img_has_text(image):
    text = pytesseract.image_to_string(image)
    return len(text.strip()) > 0


def play_audio(audio):
    fp = BytesIO()
    audio.write_to_fp(fp)
    fp.seek(0)
    audio_data = fp.read()
    audio_segment = AudioSegment.from_file(BytesIO(audio_data))
    play(audio_segment)


def get_img_from_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        capture_success, frame = cap.read()
        if capture_success:
            if img_has_text(frame):
                play_audio_from_img(frame)
            cv2.imshow("webcam", frame)  # press escape to exit
            if cv2.waitKey(30) == 27:
                break
    cap.release()
    cv2.destroyAllWindows()


def play_audio_from_img(img):
    text = get_image_text(img)
    print(text)
    speech = text_to_speech(text)
    play_audio(speech)


get_img_from_webcam()
