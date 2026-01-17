from flask import Flask, render_template, request
import random

app = Flask(__name__)

Final_Grade = 0
Improvement_Rate = 0

def calculate_grade(raw_file, extra_grade = ""):

    grades = []
    percentages = []

    if any(c.isalpha() for c in raw_file) and "\t" in raw_file:
        for line in raw_file.strip().split("\n"):
            if "/" not in line:
                continue
            startIndex = 0
            endIndex = 0
            for i in range(len(line)):
                if line[i] == "/" and (line[i+3] != "/" and line[i-3] != "/" and line[i-1].isdigit() and line[i+1].isdigit()):
                    for j in range(i-1, 0, -1):
                        if not line[j].isdigit() and line[j] != ".":
                            startIndex = j
                            break
                    for w in range(i+1, len(line), 1):
                        if not line[w].isdigit() and line[w] != ".":
                            endIndex = w
                            break

            grade = line[startIndex:endIndex]
            grade = grade.replace("\t", "")

            grades.append(grade)
    else:
        raw_file = "".join(c for c in raw_file if (c.isdigit() or c == "/" or c == "." or c == "\n"))
        for line in raw_file.strip().split("\n"):
            grades.append(line)

    extra_grade = extra_grade.strip()
    if extra_grade:
        grades.insert(0, extra_grade.strip())

    total_points = 0
    grade_points = 0

    extra_credit_points = 0

    for grade in grades:
        if "/" in grade:
            numerator, denominator = grade.split("/")

            num = float(numerator)
            den = float(denominator)

            total_points += den
            grade_points += num

            if den != 0:
                percentages.append(num / den * 100)
            else:
                extra_credit_points += num

    formatted_grades = "\n".join(grades)

    improvement_rate = "N/A"

    if len(percentages) >= 2:
        mid = len(percentages) // 2

        first_half = percentages[mid:]
        second_half = percentages[:mid]

        if first_half and second_half:
            avg_first = sum(first_half) / len(first_half)
            avg_second = sum(second_half) / len(second_half)

            improvement_rate = avg_second - avg_first

    if total_points != 0:
        final_grade = (grade_points / total_points) * 100
    else:
        final_grade = 100

    #Other stats
    num_scores = len(percentages)
    average_grade = sum(percentages) / len(percentages) if percentages else 0
    if total_points > 0:
        ec_help = (grade_points/total_points - (grade_points-extra_credit_points)/total_points) * 100

    global Final_Grade
    Final_Grade = final_grade
    global Improvement_Rate
    Improvement_Rate = improvement_rate

    stats = (
        f"Earned Points: {grade_points}<br>"
        f"Total Points: {total_points}<br>"
        f"Grade: {final_grade:.2f}%<br><br>"
        f"Other stats:<br>"
        f"# of Scores: {num_scores}<br>"
        f"Avg grade: {average_grade:.2f}<br>"
        f"Extra Credit % Increase: {ec_help:.2f}%<br>"
    )

    if improvement_rate != "N/A":
        stats += f"Improvement Rate: {improvement_rate:.2f}%"
    else:
        stats += "Improvement Rate: N/A"

    return formatted_grades, stats

def get_wisdom(final_grade, improvement_rate):
    response = ""

    if final_grade >= 95:
        response = random.choice([
            "You did well, and it is okay to be grateful for that. Still, remember that your worth was never earned by effort, it was given by God long before this grade existed. Give thanks, stay humble, and do not forget to live, love, and serve beyond the classroom.",
            "Excellence feels good, but it is not the goal of life. Even Scripture reminds us that wisdom without love is empty. Enjoy your success, but do not build your identity on achievement, build it on who you are becoming.",
            "You're at the top right now, but don't let it make you forget life exists outside of school. Hang out with friends, explore hobbies, and make memories while you can.",
            "It's easy to get caught up in perfection, but the best moments come from curiosity and adventure, not just grades. Celebrate this win, then go live a little."
        ])

    elif final_grade >= 90:
        response = random.choice([
            "This reflects discipline and responsibility, gifts that matter far beyond school. Life will not ask how perfect you were—it will ask how faithful you were. Rest sometimes, laugh often, and remember you are more than what you produce.",
            "You're clearly capable, and that's something to be proud of. Just don't let chasing perfection stop you from enjoying the bigger picture.",
            "You're doing well, but grades don't make life fun. Make sure to spend time with friends, explore your passions, and have moments just for yourself.",
            "Strong work now is good, but don't forget that high school is temporary. Balance studying with activities that actually make you happy."
        ])

    elif final_grade >= 85:
        response = random.choice([
            "This shows growth, not completion. Life is less about reaching a score and more about walking a path. Keep learning, but do not rush past the moments that shape your heart.",
            "You're doing well, even if it does not feel extraordinary. Quiet progress still matters. Invest in people and character as much as results.",
            "You're getting there, but don't let school take up your whole life. Try new clubs, sports, or hobbies—you'll be grateful later.",
            "Grades are only one part of the story. Build friendships, learn skills, and enjoy the experiences that grades can't measure."
        ])

    elif final_grade >= 80:
        response = random.choice([
            "This is a moment, not a message about your future. A single number cannot explain a whole life. Focus on balance, work honestly, rest intentionally, and trust the process.",
            "You're somewhere in the middle, and that's okay. Most of life is lived there. Stay consistent, stay kind to yourself, and keep perspective.",
            "It's a decent grade, but don't stress too much. Go outside, hang with friends, or do something creative—life is more than scores.",
            "You're doing okay, and that's enough to build on. Take time for yourself too, whether that's sports, music, or just relaxing."
        ])

    elif final_grade >= 75:
        response = random.choice([
            "It's okay to feel disappointed, but don't confuse struggle with failure. Even Scripture is full of imperfect people still called for purpose. Learn what you can, then place the rest in God's hands.",
            "This grade doesn't close doors—it just slows you down for reflection. Adjust your habits, ask for help, and keep moving forward without shame.",
            "You're not failing at life—just facing a challenge. Use it to learn, but don't let it consume your happiness or social life.",
            "It's a wake-up call, not a punishment. Try new strategies, get help if you need it, and remember to enjoy the little things outside school."
        ])

    elif final_grade >= 70:
        response = random.choice([
            "This might sting, but it says nothing about your value. God never loved you more when you succeeded or less when you struggled. Be patient with yourself and take the next right step.",
            "You're not falling behind in life—just being reminded you're human. Pause, reflect, and trust that growth often comes quietly.",
            "It's not great, but it's fixable. Ask for help, make a plan, and don't forget to take breaks and have fun with friends.",
            "One low grade isn't the end. Focus on what you can control, like effort and habits, and still make time to enjoy yourself."
        ])

    else:
        response = random.choice([
            "This hurts, and that's okay. But your purpose was never hidden in a report card. God's plans do not fail because of a bad grade. Breathe, regroup, and trust that this moment is not the end of your story.",
            "Years from now, this number will fade—but who you became through adversity will remain. Seek wisdom, ask for guidance, and do not let temporary failure steal eternal perspective.",
            "It's a rough grade, but it doesn't define you. Take a deep breath, ask for help, and remember there's more to life than school.",
            "A bad grade is just feedback, not failure. Learn from it, adjust your approach, and still make time for the things that make you happy."
        ])

    return response

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    raw_file = ""
    extra_grade = ""
    wisdom = ""

    if request.method == "POST":
        raw_file = request.form.get("raw_file", "")
        extra_grade = request.form.get("extra_grade", "")

        if raw_file != "":
            formatted, result = calculate_grade(raw_file, extra_grade)
            wisdom = get_wisdom(Final_Grade, Improvement_Rate)

            raw_file = formatted

    return render_template(
        "index.html",
        result=result,
        raw_file=raw_file,
        extra_grade=extra_grade,
        wisdom=wisdom
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
