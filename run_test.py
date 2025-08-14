import json
import nbformat
import sys

# Define the correct answers
CORRECT_ANSWERS = {
    1: 'C', 2: 'D', 3: 'C', 4: 'C', 5: 'B',
    6: 'C', 7: 'C', 8: 'B', 9: 'B', 10: 'B'
}

def extract_student_answers(notebook_path):
    """
    Extracts answers from the student's Jupyter Notebook file.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        # If the file doesn't exist, return an error message for the output
        return {}, f"Error: The file '{notebook_path}' was not found."
    except Exception as e:
        return {}, f"An error occurred while reading the notebook: {e}"

    student_answers = {}
    question_number = 1
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            source_text = cell.source
            if f"{question_number}." in source_text and "Correct Answer:" in source_text:
                for line in source_text.split('\n'):
                    if "Correct Answer:" in line:
                        answer = line.split("Correct Answer:")[1].strip().upper()
                        if answer:
                            student_answers[question_number] = answer[0]
                        break
                question_number += 1
    
    if not student_answers:
        return {}, "Could not extract any answers from the notebook. Please ensure answers are filled in."
        
    return student_answers, "Answers extracted successfully."

def grade_answers(student_answers):
    """
    Compares student answers to the correct answers and calculates the score.
    """
    score = 0
    total_questions = len(CORRECT_ANSWERS)
    
    for q_num, correct_ans in CORRECT_ANSWERS.items():
        student_ans = student_answers.get(q_num)
        if student_ans and student_ans == correct_ans:
            score += 1
            
    return score, total_questions

def main():
    """
    Main function to run the grading and output results as JSON.
    """
    notebook_path = 'L1_EA_Quiz.ipynb'
    student_answers, message = extract_student_answers(notebook_path)
    
    score = 0
    total_questions = len(CORRECT_ANSWERS)
    
    if student_answers:
        score, total_questions = grade_answers(student_answers)
        output_message = f"Grading complete.\nStudent answered {score} out of {total_questions} questions correctly."
    else:
        # If no answers were extracted, the score is 0 and we use the error message
        output_message = message

    # The autograding action expects a JSON output to assign points.
    # We create a JSON object that describes the test run.
    test_result = {
        'tests': [
            {
                'name': 'Quiz Autograding',
                'score': score,
                'max_score': total_questions,
                'output': output_message,
            }
        ]
    }
    
    # Print the JSON to standard output
    print(json.dumps(test_result))

if __name__ == "__main__":
    main()
