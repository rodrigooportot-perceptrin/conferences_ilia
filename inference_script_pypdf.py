import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os
from pypdf import PdfReader  # Switched from fitz to pypdf
import pandas as pd
from tqdm import tqdm
import gc

# --- 1. Setup ---
os.environ["HF_HOME"] = "/home/roportot/archive/huggingface_cache"
os.environ["HSA_OVERRIDE_GFX_VERSION"] = "9.0.10" 
os.environ["HF_TOKEN"] = "my_secret_token" 

model_id = "mistralai/Mistral-Small-Instruct-2409"
pdf_folder = "/mnt-homes/dccnas/cenia/roportot/archive/conferencias_2025/downloaded_papers/icml_2025"
output_csv = "/mnt-homes/dccnas/cenia/roportot/archive/conferencias_2025/classification_results/icml_2025_workshops_classification_results.csv"

# --- 2. Load Model & Tokenizer ---
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    low_cpu_mem_usage=True
)

system_prompt = (
    "Eres capaz de detectar autores e instituciones provenientes de Latinoamérica y el Caribe "
    "al analizar el texto de la primera página de un artículo científico de ciencias de la computación. "
    "Puedes observar el dominio de los correos electrónicos de autores, por ejemplo '.cl' o '.br', así como los nombres "
    "de instituciones o sus direcciones, en caso de estar presentes. Considera que podrían estar en español o portugués. \n\n"
    "Los siguientes dominios de países son aquellos que debes detectar: .ar .bo .br .cl .co .cr .cu .do .ec .hn .gt .jm .mx .pa .pe .py .sv .uy .ve \n\n"
    "Ten en cuenta que pueden haber dominios compuestos que también incluyen el código "
    "del país, algunos ejemplos son 'usp.br' o 'edu.mx'. Presta especial atención en estos casos, "
    "siempre teniendo en cuenta que esté presente alguno de los códigos indicados. \n\n"
    "Responde 1 si detectas algo relacionado y 0 en caso contrario."
)

# --- 3. Processing Loop ---
results = []
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]

#pdf_files = pdf_files[0:300] # test

index = 0

for filename in tqdm(pdf_files, desc="Processing PDFs"):
    filepath = os.path.join(pdf_folder, filename)
    text_pages = ""
    
    try:
        # pypdf is much more "forgiving" with broken PDF metadata
        reader = PdfReader(filepath)
        
        # Extract text from first page
        # IF CONFERENCE == KDD/SIGIR GET SECOND PAGE OF PAPER INSTEAD OF THE FIRST ONE

        # IF PAPER FROM IEEE REMOVE THE FOLLOWING TEXT
        # Authorized licensed use limited to: Pontificia Universidad Catolica de Chile
        for i in range(min(1, len(reader.pages))):
            text_pages += reader.pages[i].extract_text() + "\n"

            # ieee_download_text = "Authorized licensed use limited to: Pontificia Universidad Catolica de Chile"
            # text_pages = text_pages.replace(ieee_download_text, "")

        if not text_pages.strip():
            # Fallback: some PDFs need a slightly more aggressive extraction
            results.append({"filename": filename, "latam_detected": "Empty"}) # or "Empty"
            continue

        print("our_text ", text_pages[0:100])

        # Prepare Chat
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"[PAPER]\n{text_pages} [INSTRUCCIÓN FINAL]: Basado en el texto anterior, ¿proviene este paper de LatAm/Caribe? Responde solo 1 (sí) o 0 (no)"} # Cap text to avoid context blowup
        ]

        inputs = tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, 
            return_tensors="pt", return_dict=True
        ).to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=10, do_sample=False, 
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
        #final_answer = "1" if "1" in response else "0"
        
        res_dict = {"filename": filename, "latam_detected": response}
        print("rest_dict ", res_dict)

        results.append(res_dict)

        # 4. SAFE MEMORY RELEASE
        del inputs, outputs  # Remove references to heavy tensors
        if index % 10 == 0:
            gc.collect()     # Clear Python garbage without touching GPU cache directly
        index += 1

    except Exception as e:
        print(f"Failed to parse {filename}: {e}")
        results.append({"filename": filename, "latam_detected": "Error"})

        if 'inputs' in locals(): del inputs
        if 'outputs' in locals(): del outputs
        gc.collect()

# --- 4. Save ---
df = pd.DataFrame(results)
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df.to_csv(output_csv, index=False)
print(f"Classification finished. Results saved to {output_csv}")