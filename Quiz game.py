import tkinter as tk
from tkinter import messagebox
import mysql.connector

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("3250x1830")
        self.root.configure(bg='blue')  # Background color

        self.question_label = tk.Label(root, text="", font=("arial black", 30), bg='yellow')
        self.question_label.pack(pady=50)

        self.var = tk.StringVar()
        self.options = []
        for i in range(4):
            option = tk.Radiobutton(root, text="", variable=self.var,font=("arial black", 20), value=i+1, bg='#C0C0C0', activebackground='#A0A0A0')
            option.pack(pady=40)
            
            
            option.pack(pady=5)
            self.options.append(option)

        self.next_button = tk.Button(root, text="Next", command=self.next_question, bg='#4CAF50', fg='white')
        self.next_button.pack(pady=10)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi@232006",
            database="school"
        )

        self.cursor = self.conn.cursor()
        self.questions = []
        self.current_question_index = 0
        self.load_questions()

    def load_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        self.questions = self.cursor.fetchall()
        self.display_question()

    def display_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.question_label.config(text=current_question[1])

            for i in range(4):
                self.options[i].config(text=current_question[i + 2])

        else:
            self.question_label.config(text="Quiz Completed")

    def next_question(self):
        selected_option = self.var.get()
        print("selected_option",selected_option)
        if selected_option == "":
            messagebox.showinfo("Error", "Please select an option!")
            return

        current_question = self.questions[self.current_question_index]
        correct_option = current_question[6]
        
        selected_option_intvalue = int(selected_option)
        
        selected_option_str = current_question[selected_option_intvalue+1]
        print("selected_option_str ",selected_option_str)
        print("correct_option ",correct_option)
        
        if selected_option_str == correct_option:
            messagebox.showinfo("Correct", "Your answer is correct!", icon='info')
        else:
            messagebox.showinfo("Wrong", "Your answer is wrong!", icon='warning')
            self.root.destroy()

        self.current_question_index += 1
        self.display_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
