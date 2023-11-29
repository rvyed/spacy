import pandas as pd
import spacy
import json
import os
import time

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def sanitize_filename(name):
    # Replace any non-alphanumeric characters with underscores
    return "".join([c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in name])

def process_biography(df, biography_name, output_folder):
    # Sanitize the biography name to be used in the filename
    biography_name_sanitized = sanitize_filename(biography_name)
    biography_df = df[df['page_title'] == biography_name]
    json_output = []

    # Process each sentence in the biography column
    for index, row in biography_df.iterrows():
        sentence = str(row['biography'])  # Convert to string in case of non-string types
        doc = nlp(sentence)
        entities = []

        for ent in doc.ents:
            entities.append((ent.label_, ent.text))

        # Construct the JSON structure
        sentence_data = {
            "sentence": sentence,
            "sentence_id": f"{biography_name_sanitized}_{index+1}",
            "NER": entities
        }
        json_output.append(sentence_data)

    # Output file name
    output_file = f"{biography_name_sanitized}_NER.json"
    output_path = os.path.join(output_folder, output_file)  # Save to the new folder on Desktop
    with open(output_path, 'w') as file:
        json.dump(json_output, file, indent=4)

    print(f"Processed and saved: {output_file} in {output_folder}")

# Start the timer
start_time = time.time()

# Directory where the CSV files are stored
input_directory = "/Users/raed/Desktop/workjsonfiles"  # Update this path to the location of your CSV files
output_directory = os.path.join(os.path.expanduser('~'), 'Desktop', 'Processed_JSON_Files')

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Process each CSV file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path)
        unique_biographies = df['page_title'].unique()

        # Process each unique biography in the CSV
        for biography_name in unique_biographies:
            process_biography(df, biography_name, output_directory)

# End the timer and print the total time taken
end_time = time.time()
print(f"All biographies have been processed. Total time taken: {end_time - start_time:.2f} seconds.")
