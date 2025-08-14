import json
import nbformat
import os

# 定义正确答案
# 注意：这里的答案是根据您提供的 ipynb 文件提取的。
# 键是问题编号 (从1开始)，值是正确选项 ('A', 'B', 'C', or 'D')。
CORRECT_ANSWERS = {
    1: 'C',
    2: 'D',
    3: 'C',
    4: 'C',
    5: 'B',
    6: 'C',
    7: 'C',
    8: 'B',
    9: 'B',
    10: 'B'
}

def extract_student_answers(notebook_path):
    """
    从学生的 Jupyter Notebook 文件中提取答案。
    假设学生在每个问题对应的 Markdown 单元格的'Correct Answer:'后填写答案。
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"错误：找不到文件 {notebook_path}。请确保学生提交的文件名正确。")
        return {}
    except Exception as e:
        print(f"读取或解析 Notebook 时出错: {e}")
        return {}

    student_answers = {}
    question_number = 1

    # 遍历 notebook 中的所有单元格
    for cell in nb.cells:
        # 我们只关心 Markdown 单元格
        if cell.cell_type == 'markdown':
            # 检查单元格内容是否包含问题的标识
            if f"{question_number}." in cell.source and "Correct Answer:" in cell.source:
                lines = cell.source.split('\n')
                for line in lines:
                    # 寻找包含答案的行
                    if "Correct Answer:" in line:
                        # 提取冒号后面的字符，并去除首尾空格，转换为大写
                        answer = line.split("Correct Answer:")[1].strip().upper()
                        # 只取第一个字符作为答案
                        if answer:
                            student_answers[question_number] = answer[0]
                        break # 找到答案后跳出内层循环
                question_number += 1
    return student_answers

def main():
    """
    主函数，用于比较学生答案和正确答案，并计算分数。
    """
    notebook_path = 'L1_EA_Quiz.ipynb' # 学生作业文件的路径
    student_answers = extract_student_answers(notebook_path)
    
    score = 0
    total_questions = len(CORRECT_ANSWERS)

    if not student_answers:
        print("未能从学生提交的文件中提取任何答案。得分为 0。")
        # 即使没有答案，我们也要显式地输出测试失败，以便 Classroom 捕捉
        print("[FAIL] No answers found.")
        return

    # 对比答案
    for q_num, correct_ans in CORRECT_ANSWERS.items():
        student_ans = student_answers.get(q_num)
        if student_ans and student_ans == correct_ans:
            score += 1
    
    print(f"学生共答对了 {score} / {total_questions} 题。")

    # GitHub Classroom 通过标准输出来判断测试是否通过。
    # 如果所有题目都正确，我们输出一个成功的消息。
    # 否则，输出失败的消息。Classroom 将会标记此测试为失败，但仍然会记录分数。
    # 这里的关键是让 Classroom 知道测试已运行。
    if score == total_questions:
        print("\n[PASS] 所有题目回答正确！")
    else:
        # 即使部分正确，我们也输出一个明确的失败信号，
        # 因为学生没有拿到满分。分数仍会被记录。
        print(f"\n[FAIL] {total_questions - score} a/{total_questions} 题回答错误。")

if __name__ == "__main__":
    main()
