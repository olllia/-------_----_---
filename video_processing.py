import cv2
import logging
import torch
from torch import nn
from torchvision import transforms
from moviepy.editor import VideoFileClip
from config import MAX_VIDEO_DURATION, mtcnn, device
from torchvision import models

model = models.resnet18(pretrained=True)

# Заморозка весов всех слоев, кроме последнего
for param in model.parameters():
    param.requires_grad = False

model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 1),
    nn.Sigmoid()
)

model = model.to(device)

model_weights_path = 'gender_classification.pth'

try:
    model.load_state_dict(torch.load(model_weights_path))
except RuntimeError as e:
    print(f"Ошибка загрузки модели: {e}")

model.eval()

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomRotation(degrees=15),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def process_video_with_faces(video_path, output_path):
    gender_list = []  # Список для хранения предсказанных полов
    processed_faces = {}  # Словарь для отслеживания уже обработанных лиц и их пола

    try:
        # Открываем видео с помощью MoviePy
        clip = VideoFileClip(video_path)

        # Если длина видео превышает лимит, обрезаем его до MAX_VIDEO_DURATION
        if clip.duration > MAX_VIDEO_DURATION:
            logging.info(f"Видео слишком длинное ({clip.duration:.2f} сек). Обрезаем до {MAX_VIDEO_DURATION} сек.")
            clip = clip.subclip(0, MAX_VIDEO_DURATION)

        def process_frame(frame):
            # Обработка кадров
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame_pil = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes, _ = mtcnn.detect(frame_pil)

            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = [int(b) for b in box]

                    # Уникальный идентификатор для текущего лица
                    face_id = (x1, y1, x2, y2)

                    # Если лицо уже обработано, используем сохраненное значение
                    if face_id in processed_faces:
                        gender = processed_faces[face_id]
                    else:
                        # Извлечение области лица для предсказания
                        face = frame[y1:y2, x1:x2]
                        if face.size != 0:  # Проверка, что лицо найдено
                            # Рисуем прямоугольник вокруг лица
                            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), 4)

                            face_tensor = transform(cv2.cvtColor(face, cv2.COLOR_BGR2RGB)).unsqueeze(
                                0)  # Добавляем размерность для батча

                            with torch.no_grad():  # Отключение градиентов
                                output = model(face_tensor)
                                predicted = (output > 0.5).int()  # Получаем предсказанный класс

                                # Определяем текст для отображения
                                gender = 'Male' if predicted.item() == 0 else 'Female'
                                processed_faces[face_id] = gender  # Сохраняем пол для этого лица

                            cv2.putText(image, gender, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)
                            gender_list.append(gender)  # Добавляем пол в список

                    # Если лицо уже было классифицировано, отображаем сохраненный пол
                    if face_id in processed_faces:
                        cv2.putText(image, processed_faces[face_id], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                    (255, 255, 255), 3)

            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Обработка видео
        processed_clip = clip.fl_image(process_frame)
        processed_clip.write_videofile(output_path, codec="libx264")

    except Exception as e:
        logging.error(f"Ошибка при обработке видео: {e}")
        raise

    return list(processed_faces.values())  # Возвращаем список полов




