import os

def split_text_into_batches(input_file, output_dir="batches", max_chars=15000):
    """
    Splits a large text file into smaller batches, respecting paragraph boundaries.
    max_chars=15000 is roughly 2500-3000 words, the "sweet spot" for LLM attention.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split by paragraphs (double newlines) to avoid cutting sentences in half
    paragraphs = content.split('\n\n')
    
    current_batch = []
    current_length = 0
    batch_number = 1

    print(f"📦 Starting batch generation for {input_file}...")

    for para in paragraphs:
        para_length = len(para)
        
        # If adding this paragraph exceeds the limit, save the current batch
        if current_length + para_length > max_chars and current_batch:
            save_batch(current_batch, output_dir, batch_number)
            batch_number += 1
            current_batch = [para]
            current_length = para_length
        else:
            current_batch.append(para)
            current_length += para_length

    # Save the final batch if anything is left
    if current_batch:
        save_batch(current_batch, output_dir, batch_number)

    print(f"✅ Success! Generated {batch_number} batches in the '{output_dir}' folder.")

def save_batch(batch_data, output_dir, batch_number):
    filename = os.path.join(output_dir, f"rtl_batch_{batch_number:02d}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(batch_data))
    print(f"   Saved {filename}")

if __name__ == "__main__":
    # Ensure your text file is named exactly this, or change the name below
    INPUT_FILE = r"C:\Users\kagas\Pictures\ALIN1_final_repository_local\ALIN1_Repositary\backup of github alin1\backend\source_documents\rtl\full RTL context.txt" 
    
    if os.path.exists(INPUT_FILE):
        split_text_into_batches(INPUT_FILE)
    else:
        print(f"❌ Error: Could not find '{INPUT_FILE}'. Please check the file name.")