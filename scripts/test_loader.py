from torch.utils.data import DataLoader
from dataset import DeepfakeDataset

dataset = DeepfakeDataset("data/train")
loader = DataLoader(dataset, batch_size=8, shuffle=True)

images, labels = next(iter(loader))

print("Images shape:", images.shape)
print("Labels:", labels)
