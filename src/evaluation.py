import pandas as pd
import mlflow
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, answer_correctness
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.rag import LegalRAG
from src import config
import json
import os
import argparse

# Test veri seti yolu
EVAL_DATA_PATH = os.path.join(config.DATA_DIR, "eval_data (3).json")

def run_evaluation(data_path=None, experiment_name="ragas_evaluation_multimodel"):
    # MODELLER (Kullanıcı isteği üzerine sadece gpt-4o)
    MODELS = ["gpt-4o"]
    
    # Veri setini yükle
    target_path = data_path if data_path else EVAL_DATA_PATH
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
        print(f"{len(test_data)} adet test sorusu yüklendi ({target_path}).")
    except FileNotFoundError:
        print(f"HATA: {target_path} bulunamadı!")
        return

    # Evaluator LLM (Değerlendirmeyi yapan hakem model - Sabit ve güçlü olmalı)
    eval_llm = ChatOpenAI(model="gpt-4o", api_key=config.OPENAI_API_KEY)
    eval_embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL, api_key=config.OPENAI_API_KEY)

    for model_name in MODELS:
        print(f"\n==========================================")
        print(f"MODEL DEĞERLENDİRİLİYOR: {model_name}")
        print(f"==========================================\n")
        
        try:
            rag = LegalRAG(model_name=model_name)
            
            results = {
                "question": [],
                "answer": [],
                "contexts": [],
                "ground_truth": []
            }

            # 1. Soruları RAG Sistemine Sor
            for item in test_data:
                try:
                    # Cevap ve Kaynakları Al
                    answer, sources, context_texts = rag.generate_answer(item['question'])
                    
                    results["question"].append(item['question'])
                    results["answer"].append(answer)
                    # RAGAS için tam metin içeriği kullanıyoruz
                    results["contexts"].append(context_texts)
                    results["ground_truth"].append(item.get('ground_truth_answer', ''))
                except Exception as e:
                    print(f"HATA ({model_name} - {item['question']}): {e}")
                    results["question"].append(item['question'])
                    results["answer"].append(f"HATA: {str(e)}")
                    results["contexts"].append([])
                    results["ground_truth"].append(item.get('ground_truth_answer', ''))

            # 2. Dataset Oluştur
            dataset = Dataset.from_dict(results)

            # 3. RAGAS ile Değerlendir
            print(f"[{model_name}] RAGAS Metrikleri Hesaplanıyor...")
            
            scores = evaluate(
                dataset=dataset,
                metrics=[faithfulness, answer_relevancy, answer_correctness],
                llm=eval_llm,
                embeddings=eval_embeddings
            )
            
            print(f"[{model_name}] Sonuçlar: {scores}")

            # 4. MLflow'a Kaydet
            mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
            mlflow.set_experiment(experiment_name)
            
            run_name = f"eval_{model_name}"
            with mlflow.start_run(run_name=run_name):
                # Parametreleri kaydet
                mlflow.log_param("model_name", model_name)
                
                # RAGAS skorlarını sözlüğe çevir
                scores_dict = scores.to_pandas().mean(numeric_only=True).to_dict()
                mlflow.log_metrics(scores_dict)
                
                # Detaylı sonuçları CSV olarak kaydet
                filename = f"evaluation_results_{model_name}_{experiment_name}.csv"
                df_result = scores.to_pandas()
                df_result.to_csv(filename, index=False)
                mlflow.log_artifact(filename)
            
            print(f"[{model_name}] Değerlendirme tamamlandı ve MLflow'a kaydedildi.")

        except Exception as e:
            print(f"MODEL HATASI ({model_name}): {e}")
            print(f"{model_name} için değerlendirme atlanıyor.")

    print("\nTüm modeller için süreç tamamlandı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG evaluation")
    parser.add_argument("--data_path", type=str, help="Path to evaluation dataset JSON")
    parser.add_argument("--experiment_name", type=str, default="ragas_evaluation_multimodel", help="MLflow experiment name")
    args = parser.parse_args()
    
    run_evaluation(data_path=args.data_path, experiment_name=args.experiment_name)
