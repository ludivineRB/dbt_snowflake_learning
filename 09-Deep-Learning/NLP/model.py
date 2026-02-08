import torch
import torch.nn as nn
from transformers import CamembertModel, CamembertTokenizer
from typing import List, Dict, Optional

class CapitalClassifier(nn.Module):
    """
    Modèle de classification pour prédire les capitales basé sur CamemBERT.
    """
    def __init__(self, num_capitals: int, model_name: str = "camembert-base"):
        super(CapitalClassifier, self).__init__()
        self.bert = CamembertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_capitals)
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        output = self.dropout(pooled_output)
        logits = self.classifier(output)
        return logits

class CapitalPredictor:
    """
    Classe pour gérer les prédictions du modèle.
    """
    def __init__(self, model_path: Optional[str] = None):
        # Détection automatique du meilleur device disponible
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        
        self.tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        
        from data import get_all_capitals
        self.capitals = get_all_capitals()
        self.capital_to_idx = {capital: idx for idx, capital in enumerate(self.capitals)}
        self.idx_to_capital = {idx: capital for capital, idx in self.capital_to_idx.items()}
        
        self.model = CapitalClassifier(num_capitals=len(self.capitals))
        self.model.to(self.device)
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str):
        """Charge un modèle sauvegardé."""
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
    
    def predict(self, question: str) -> Dict[str, float]:
        """
        Prédit la capitale pour une question donnée.
        
        Args:
            question: La question sur la capitale
            
        Returns:
            Dict avec les top 5 prédictions et leurs probabilités
        """
        self.model.eval()
        
        encoding = self.tokenizer(
            question,
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors='pt'
        )
        
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask)
            probabilities = torch.nn.functional.softmax(outputs, dim=-1)
            
        top_probs, top_indices = torch.topk(probabilities[0], k=min(5, len(self.capitals)))
        
        predictions = {}
        for prob, idx in zip(top_probs.cpu().numpy(), top_indices.cpu().numpy()):
            capital = self.idx_to_capital[idx]
            predictions[capital] = float(prob)
        
        return predictions
    
    def get_capital_index(self, capital: str) -> int:
        """Retourne l'index d'une capitale."""
        return self.capital_to_idx.get(capital, -1)