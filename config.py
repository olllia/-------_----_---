import torch
from facenet_pytorch import MTCNN

# Токен бота
TOKEN = '7979311693:AAGr3YluwOuweEek3t6K20rvEsJmjbVfAD0'

# Настройка устройства для обработки
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)

# Максимальная длина видео в секундах
MAX_VIDEO_DURATION = 10
