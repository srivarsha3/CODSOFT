import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# ---------- Tokenizer ----------
class SimpleTokenizer:
    def __init__(self, vocab):
        self.word2idx = {word: idx for idx, word in enumerate(vocab)}
        self.idx2word = {idx: word for word, idx in self.word2idx.items()}
        self.vocab_size = len(vocab)

# Example vocabulary
vocab = ['<pad>', '<start>', '<end>', '<unk>', 'a', 'man', 'riding', 'horse']
tokenizer = SimpleTokenizer(vocab)

# ---------- Feature Extractor ----------
resnet = models.resnet50(pretrained=True)
resnet = nn.Sequential(*list(resnet.children())[:-1])
resnet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def extract_features(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        features = resnet(image_tensor).squeeze()
    return features

# ---------- Caption Generator ----------
class CaptionGenerator(nn.Module):
    def __init__(self, feature_dim, embed_dim, hidden_dim, vocab_size):
        super(CaptionGenerator, self).__init__()
        self.fc = nn.Linear(feature_dim, embed_dim)
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc_out = nn.Linear(hidden_dim, vocab_size)

    def forward(self, features, captions):
        features = self.fc(features).unsqueeze(1)
        embeddings = self.embed(captions)
        inputs = torch.cat((features, embeddings), dim=1)
        lstm_out, _ = self.lstm(inputs)
        outputs = self.fc_out(lstm_out)
        return outputs

# ---------- Generate Caption ----------
def generate_caption(model, features, tokenizer, max_len=20):
    caption = ['<start>']
    for _ in range(max_len):
        seq = torch.tensor([tokenizer.word2idx.get(w, tokenizer.word2idx['<unk>']) for w in caption]).unsqueeze(0)
        output = model(features, seq)
        pred_idx = output[0, -1].argmax().item()
        pred_word = tokenizer.idx2word[pred_idx]
        caption.append(pred_word)
        if pred_word == '<end>':
            break
    return ' '.join(caption[1:-1])

# ---------- Run ----------
image_path = "your_image.jpg"
features = extract_features(image_path)
model = CaptionGenerator(feature_dim=2048, embed_dim=256, hidden_dim=512, vocab_size=tokenizer.vocab_size)

# (Optional) Load pretrained weights here
# model.load_state_dict(torch.load("caption_model.pt"))

caption = generate_caption(model, features, tokenizer)
print("Generated Caption:", caption)
