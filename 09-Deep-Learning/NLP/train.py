import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import CamembertTokenizer
from tqdm import tqdm
import json
import os
from typing import Dict, List
from model import CapitalClassifier, CapitalPredictor
from data import get_all_capitals

class CapitalDataset(Dataset):
    """Dataset pour l'entraînement du modèle de capitales."""
    
    def __init__(self, data_path: str, tokenizer, capital_to_idx: Dict[str, int]):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.tokenizer = tokenizer
        self.capital_to_idx = capital_to_idx
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        text = item['text']
        label = self.capital_to_idx[item['label']]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=128,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

def train_model(
    train_data_path: str = 'train_data.json',
    test_data_path: str = 'test_data.json',
    num_epochs: int = 50,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    model_save_path: str = 'capital_model.pth',
    patience: int = 5,
    save_every: int = 10
):
    """
    Entraîne le modèle de classification des capitales.
    """
    # Détection automatique du meilleur device disponible
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Utilisation du GPU CUDA: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Utilisation du GPU Apple Silicon (MPS)")
    else:
        device = torch.device("cpu")
        print("Utilisation du CPU")
    
    print(f"Device sélectionné: {device}")
    
    tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
    
    capitals = get_all_capitals()
    capital_to_idx = {capital: idx for idx, capital in enumerate(capitals)}
    
    train_dataset = CapitalDataset(train_data_path, tokenizer, capital_to_idx)
    test_dataset = CapitalDataset(test_data_path, tokenizer, capital_to_idx)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    model = CapitalClassifier(num_capitals=len(capitals))
    model.to(device)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=3)
    criterion = nn.CrossEntropyLoss()
    
    best_accuracy = 0
    epochs_without_improvement = 0
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
        
        for batch in progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)
            
            optimizer.zero_grad()
            
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            accuracy = 100 * correct / total
            progress_bar.set_postfix({'loss': f'{loss.item():.4f}', 'acc': f'{accuracy:.2f}%'})
        
        avg_train_loss = total_loss / len(train_loader)
        train_accuracy = 100 * correct / total
        
        model.eval()
        test_correct = 0
        test_total = 0
        test_loss = 0
        
        with torch.no_grad():
            for batch in test_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['label'].to(device)
                
                outputs = model(input_ids, attention_mask)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
                
                _, predicted = torch.max(outputs, 1)
                test_total += labels.size(0)
                test_correct += (predicted == labels).sum().item()
        
        test_accuracy = 100 * test_correct / test_total
        avg_test_loss = test_loss / len(test_loader)
        
        print(f"\nEpoch {epoch+1}/{num_epochs}")
        print(f"Train Loss: {avg_train_loss:.4f}, Train Acc: {train_accuracy:.2f}%")
        print(f"Test Loss: {avg_test_loss:.4f}, Test Acc: {test_accuracy:.2f}%")
        print(f"Learning Rate: {scheduler.get_last_lr()[0]:.2e}")
        
        # Early stopping et sauvegarde
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            epochs_without_improvement = 0
            torch.save(model.state_dict(), model_save_path)
            print(f"Nouveau meilleur modèle sauvegardé avec une précision de {test_accuracy:.2f}%")
        else:
            epochs_without_improvement += 1
            
        # Sauvegarde périodique
        if (epoch + 1) % save_every == 0:
            checkpoint_path = f"checkpoint_epoch_{epoch+1}.pth"
            torch.save(model.state_dict(), checkpoint_path)
            print(f"Checkpoint sauvegardé: {checkpoint_path}")
            
        # Early stopping
        if epochs_without_improvement >= patience:
            print(f"Arrêt anticipé après {patience} époques sans amélioration")
            break
            
        scheduler.step(test_accuracy)
        
        # Sauvegarder à la fin même si pas d'amélioration
        if epoch == num_epochs - 1:
            torch.save(model.state_dict(), model_save_path)
            print(f"Modèle final sauvegardé")
    
    print(f"\nEntraînement terminé. Meilleure précision: {best_accuracy:.2f}%")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Entraîner le modèle de classification des capitales')
    parser.add_argument('--num_epochs', type=int, default=50, help='Nombre d\'époques')
    parser.add_argument('--batch_size', type=int, default=16, help='Taille du batch')
    parser.add_argument('--learning_rate', type=float, default=2e-5, help='Taux d\'apprentissage')
    parser.add_argument('--model_save_path', type=str, default='capital_model.pth', help='Chemin de sauvegarde du modèle')
    parser.add_argument('--patience', type=int, default=5, help='Patience pour l\'early stopping')
    parser.add_argument('--save_every', type=int, default=10, help='Fréquence de sauvegarde des checkpoints')
    
    args = parser.parse_args()
    
    if not os.path.exists('train_data.json'):
        print("Création des données d'entraînement...")
        os.system("python data.py")
    
    train_model(
        num_epochs=args.num_epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        model_save_path=args.model_save_path,
        patience=args.patience,
        save_every=args.save_every
    )