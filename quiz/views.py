import requests
import json
from django.shortcuts import render, redirect
#from django.views.decorators.csrf import csrf_exempt

GROQ_API_KEY = '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'

def home(request):
    return render(request, 'quiz/home.html')

def quiz_view(request):
    if request.method == 'POST':
        subject = request.POST.get("subject")
        topic = request.POST.get("topic")
        num_questions = int(request.POST.get("num_questions", 5))
        difficulty = request.POST.get("difficulty")
        time_limit = int(request.POST.get("time_limit", 120))

        prompt = (
            f"Generate {num_questions} multiple-choice questions (MCQs) on the topic '{topic}' "
            f"under the subject '{subject}' with difficulty '{difficulty}'. "
            "Each question should have 4 options labeled A to D and specify the correct answer.\n\n"
            "Format like this:\n\n"
            "Q. What is the capital of France?\n"
            "A. Berlin\nB. Madrid\nC. Paris\nD. Rome\nAnswer: C\n\n"
        )

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            data = response.json()
        except Exception as e:
            return render(request, 'quiz/home.html', {"error": "API error. Please try again."})

        if "choices" not in data:
            return render(request, 'quiz/home.html', {"error": "Failed to get quiz from Groq."})

        content = data["choices"][0]["message"]["content"]

        questions = []
        blocks = content.strip().split("Q.")
        for block in blocks[1:]:
            lines = block.strip().split("\n")
            q_text = lines[0].strip()
            options = {}
            answer = ""

            for line in lines[1:]:
                if line.startswith("A."):
                    options["A"] = line[2:].strip()
                elif line.startswith("B."):
                    options["B"] = line[2:].strip()
                elif line.startswith("C."):
                    options["C"] = line[2:].strip()
                elif line.startswith("D."):
                    options["D"] = line[2:].strip()
                elif line.startswith("Answer:"):
                    answer = line.split(":")[1].strip()

            if q_text and options and answer:
                questions.append({
                    "question": q_text,
                    "options": options,
                    "answer": answer
                })

        if not questions:
            return render(request, 'quiz/home.html', {"error": "Could not parse quiz questions."})

        request.session["questions"] = questions
        request.session["time_limit"] = time_limit

        return render(request, 'quiz/quiz.html', {
            "questions": questions,
            "time_limit": time_limit
        })

    return redirect('home')

def submit_quiz(request):
    if request.method == 'POST':
        questions = request.session.get("questions", [])
        score = 0
        total = len(questions)

        for i, q in enumerate(questions):
            user_ans = request.POST.get(f"q{i}", "").strip()
            correct = q["answer"].strip()
            if user_ans == correct:
                score += 1

        return render(request, 'quiz/result.html', {
            "score": score,
            "total": total
        })

    return redirect('home')
