import tkinter as tk
from tkinter import messagebox
import random
questions=[{
            "question": "What is the capital of India?",
            "options": ["Mumbai", "Delhi", "Hyderabad", "Chennai"],
            "answer": "Delhi"
        },
        {
            "question": "Which language is mainly used for Data Science?",
            "options": ["Python", "Java", "C++", "HTML"],
            "answer": "Python"
        },
        {
            "question": "Who developed the theory of relativity?",
            "options": ["Newton", "Einstein", "Tesla", "Galileo"],
            "answer": "Einstein"
}]
class Quizapp:
    def __init__(self,master):
        self.master=master
        self.master.title("Quiz app")
        self.master.geometry("600x400")
        self.score=0
        self.q_index=0
        self.time_left=10
        self.quiz_questions=questions.copy()
        random.shuffle(self.quiz_questions)
        self.question_label=tk.Label(master,text="",wraplength=600,font=("Arial",14))
        self.question_label.pack(pady=20)
        self.buttons=[]
        for i in range(4):
            btn=tk.Button(master,text="",width=20,command=lambda idx=i:self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)
        self.timer_label=tk.Label(master,text=f"Time left: {self.time_left}s",font=("Arial",12))
        self.timer_label.pack(pady=10)
        self.score_label=tk.Label(master,text=f"Score: {self.score}",font=("Arial",12))
        self.score_label.pack(pady=5)
        self.restart_btn=tk.Button(master,text="Restart Quiz",command=self.restart_quiz)
        self.restart_btn.pack(pady=10)

        self.show_question()
        self.update_timer()
    
    def show_question(self):
        if self.q_index<len(self.quiz_questions):
            q=self.quiz_questions[self.q_index]
            self.question_label.config(text=q["question"])
            for i,option in enumerate(q["options"]):
                self.buttons[i].config(text=option)
            self.time_left=10
        else:
            messagebox.showinfo("quiz completed",f"Your score:{self.score}/{len(self.quiz_questions)}")
            self.master.destroy()
    def check_answer(self,idx):
        selected=self.buttons[idx].cget("text")
        correct=self.quiz_questions[self.q_index]["answer"]
        if selected==correct:
            self.score+=1
            self.score_label.config(text=f"Score: {self.score}")
        self.q_index+=1
        self.show_question()
    def update_timer(self):
        if self.q_index<len(self.quiz_questions):
            if self.time_left>0:
                self.timer_label.config(text=f"time left: {self.time_left}s")
                self.time_left-=1
                self.master.after(1000,self.update_timer)
            else:
                self.q_index+=1
                self.show_question()
                self.update_timer()

    def restart_quiz(self):
        self.score=0
        self.q_index=0
        self.score_label.config(text=f"Score :{self.score}")
        random.shuffle(self.quiz_questions)
        self.show_question()
        self.update_timer()
root=tk.Tk()
app=Quizapp(root)
root.mainloop()