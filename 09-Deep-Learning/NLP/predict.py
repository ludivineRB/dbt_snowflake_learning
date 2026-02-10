import argparse
from model import CapitalPredictor
import os

def main():
    parser = argparse.ArgumentParser(description="Prédire la capitale d'un pays")
    parser.add_argument("--model", type=str, default="capital_model.pth", help="Chemin vers le modèle entraîné")
    parser.add_argument("--question", type=str, help="Question à poser (ex: 'Quelle est la capitale de France ?')")
    parser.add_argument("--interactive", action="store_true", help="Mode interactif")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Erreur: Le modèle '{args.model}' n'existe pas.")
        print("Veuillez d'abord entraîner le modèle avec: python train.py")
        return
    
    print("Chargement du modèle...")
    predictor = CapitalPredictor(model_path=args.model)
    
    if args.interactive:
        print("\nMode interactif activé. Tapez 'quit' pour quitter.\n")
        while True:
            question = input("Entrez votre question: ")
            if question.lower() == 'quit':
                break
            
            predictions = predictor.predict(question)
            
            print("\nPrédictions:")
            for capital, prob in predictions.items():
                print(f"  {capital}: {prob:.2%}")
            print()
    
    elif args.question:
        predictions = predictor.predict(args.question)
        
        print(f"\nQuestion: {args.question}")
        print("\nPrédictions:")
        for capital, prob in predictions.items():
            print(f"  {capital}: {prob:.2%}")
    
    else:
        print("Veuillez spécifier une question avec --question ou utiliser --interactive")

if __name__ == "__main__":
    main()