import json
import os
from pathlib import Path

def process_annotation_file(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Create a mapping of IDs to their text content and elements by ID
    id_to_text = {}
    id_to_element = {}
    for element in data['form']:
        id_to_text[element['id']] = element['text']
        id_to_element[element['id']] = element
    
    # Find which questions are linked to headers
    questions_in_headers = set()
    for element in data['form']:
        if element['label'] == 'header':
            for link in element.get('linking', []):
                if len(link) >= 2:
                    question_id = link[1]
                    if question_id in id_to_element and id_to_element[question_id]['label'] == 'question':
                        questions_in_headers.add(question_id)
    
    # Create question-answer pairs
    qa_pairs = {}
    
    # First pass: process regular questions that aren't part of headers
    for element in data['form']:
        if element['label'] == 'question' and element['id'] not in questions_in_headers:
            question_text = element['text']
            answers = []
            
            # Find all linked answers
            for link in element.get('linking', []):
                if len(link) >= 2:  # Ensure we have both source and target IDs
                    answer_id = link[1]
                    if answer_id in id_to_element and id_to_element[answer_id]['label'] == 'answer':
                        answers.append(id_to_text[answer_id])
            
            # Store as a single value if only one answer, otherwise as a list
            if len(answers) == 1:
                qa_pairs[question_text] = answers[0]
            elif len(answers) > 1:
                qa_pairs[question_text] = answers
            else:
                qa_pairs[question_text] = ""  # Empty string if no answers found
    
    # Second pass: process headers and their linked questions
    for element in data['form']:
        if element['label'] == 'header':
            header_text = element['text']
            header_questions = {}
            
            # Find all questions linked to this header
            for link in element.get('linking', []):
                if len(link) >= 2:
                    question_id = link[1]
                    # Find the question element
                    if question_id in id_to_element and id_to_element[question_id]['label'] == 'question':
                        q_element = id_to_element[question_id]
                        question_text = q_element['text']
                        
                        # Find all answers for this question
                        answers = []
                        for q_link in q_element.get('linking', []):
                            if len(q_link) >= 2:
                                answer_id = q_link[1]
                                if answer_id in id_to_element and id_to_element[answer_id]['label'] == 'answer':
                                    answers.append(id_to_text[answer_id])
                        
                        # Store as a single value if only one answer, otherwise as a list
                        if len(answers) == 1:
                            header_questions[question_text] = answers[0]
                        elif len(answers) > 1:
                            header_questions[question_text] = answers
                        else:
                            header_questions[question_text] = ""  # Empty string if no answers found
            
            if header_questions:  # Only add if there are linked questions
                qa_pairs[header_text] = header_questions
    
    return qa_pairs

def main():
    # Create output directory if it doesn't exist
    output_dir = Path('./dataset/processed/funsd/annotations')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all JSON files in the annotations folder
    annotations_dir = Path('./dataset/funsd/annotations')
    for input_file in annotations_dir.glob('*.json'):
        # try:
        qa_pairs = process_annotation_file(input_file)
        
        # Create output filename
        output_file = output_dir / f"{input_file.stem}_processed.json"
        
        # Save processed data
        with open(output_file, 'w') as f:
            json.dump(qa_pairs, f, indent=2)
        
        print(f"Processed {input_file.name} -> {output_file.name}")
            
        # except Exception as e:
        #     print(f"Error processing {input_file.name}: {str(e)}")

if __name__ == "__main__":
    main()