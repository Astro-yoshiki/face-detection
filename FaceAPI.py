import os
import cognitive_face as cf
from PIL import Image, ImageDraw, ImageFont


class FaceAPI:
    def __init__(self, img_src, SUBSCRIPTION_KEY=None, BASE_URL=None):
        if SUBSCRIPTION_KEY is not None:
            self.SUBSCRIPTION_KEY = SUBSCRIPTION_KEY
        else:
            self.SUBSCRIPTION_KEY = os.environ.get("SUBSCRIPTION_KEY")
        if BASE_URL is not None:
            self.BASE_URL = BASE_URL
        else:
            self.BASE_URL = "https://forlearning.cognitiveservices.azure.com/face/v1.0"

        cf.Key.set(self.SUBSCRIPTION_KEY)
        cf.BaseUrl.set(self.BASE_URL)

        img_url = img_src
        attributes = "age, gender, emotion"
        self.response = cf.face.detect(img_url, attributes=attributes)

        # イメージオブジェクト生成
        self.img = Image.open(img_url)
        self.drawing = ImageDraw.Draw(self.img)

    @staticmethod
    # 顔と認識された箇所に四角を描く関数
    def draw_rectangle(draw, coordinates, color, width=1):
        for i in range(width):
            rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
            rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
            draw.rectangle((rect_start, rect_end), outline=color)

    @staticmethod
    # 顔と認識された箇所に性別を描く関数
    def draw_info(draw, coordinates, gender, align, font, fill):
        draw.text(coordinates, gender, align=align, font=font, fill=fill)

    def face_detect(self):
        for index in range(len(self.response)):
            # 取得した顔情報
            image_top = self.response[index]["faceRectangle"]["top"]
            image_left = self.response[index]["faceRectangle"]["left"]
            image_height = self.response[index]["faceRectangle"]["height"]
            image_width = self.response[index]["faceRectangle"]["width"]
            image_gender = self.response[index]["faceAttributes"]["gender"]
            image_age = int(self.response[index]["faceAttributes"]["age"])
            image_emotion = max(self.response[index]["faceAttributes"]["emotion"],
                                key=self.response[index]["faceAttributes"]["emotion"].get)

            # 関数呼び出し(四角)
            face_top_left = (image_left, image_top)
            face_bottom_right = (image_left + image_width, image_top + image_height)
            outline_width = 10
            outline_color = "Yellow"
            self.draw_rectangle(self.drawing, (face_top_left, face_bottom_right),
                                color=outline_color, width=outline_width)

            # 関数呼び出し(性別)
            gender_top_left = (image_left, image_top - 310)
            font = ImageFont.truetype("Helvetica.ttc", 100)
            align = "Left"
            fill = "Yellow"
            self.draw_info(self.drawing, gender_top_left, image_gender, align, font, fill)

            # 関数呼び出し(年齢)
            age_top_left = (image_left, image_top - 220)
            font = ImageFont.truetype("Helvetica.ttc", 100)
            align = "Left"
            fill = "Yellow"
            self.draw_info(self.drawing, age_top_left, str(image_age), align, font, fill)

            # 関数呼び出し(感情)
            emotion_top_left = (image_left, image_top - 130)
            font = ImageFont.truetype("Helvetica.ttc", 100)
            align = "Left"
            fill = "Yellow"
            self.draw_info(self.drawing, emotion_top_left, image_emotion, align, font, fill)

        return self.img


if __name__ == "__main__":
    _img_src = "sample.jpg"
    api = FaceAPI(img_src=_img_src)
    img = api.face_detect()
    img.show()
