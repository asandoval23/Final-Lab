import os
import matplotlib.pyplot as plt
import numpy as np

class Student:
    def __init__(self, studentid, name):
        self.studentid=studentid
        self.name=name
        self.submissions={}
    def addsub(self, assignment_id, score, max_points):
        self.submissions[assignment_id]=(score, max_points)
    def findtotal(self):
        scoretotal=0
        total_max_points=0
        for assignment_id, (score, max_points) in self.submissions.items():
            points_earned=(score/100)*max_points
            scoretotal=scoretotal+points_earned
            total_max_points=total_max_points+max_points
        return scoretotal, total_max_points
    def percentage(self):
        total_score, total_max_points=self.findtotal()
        percentage=(total_score/total_max_points)*100
        return round(percentage)
class Assignment:
    def __init__(self, name, quiznumber, points):
        self.name= name
        self.quiznumber= quiznumber
        self.points= points
        self.submissions=[]
    def addsub(self, submission):
        self.submissions.append(submission)
    def get_statistics(self):
        if not self.submissions:
            print("Assignment not found")
        min_score= min(self.submissions, key=lambda x: x.score).score
        avg_score= sum([sub.score for sub in self.submissions]) / len(self.submissions)
        max_score= max(self.submissions, key=lambda x: x.score).score
        return {"min": min_score, "avg": avg_score, "max": max_score}
class Submission:
    def __init__(self, studentid, quiznumber, score):
        self.studentid=studentid
        self.quiznumber=quiznumber
        self.score=score

class completeInfo:
    def __init__(self):
        self.students={}
        self.assignments={}
        self.submissions=[]
        self.getstudents()
        self.getAssignments()
        self.getSubmissions()
    def getstudents(self):
        with open('data/students.txt', 'r') as file:
            for line in file:
                student_id=line[:3]
                name=line[3:].strip()
                self.students[student_id]=Student(student_id, name)
    def getAssignments(self):
        with open('data/assignments.txt', 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 3):
                name=lines[i].strip()
                assignment_id= lines[i+1].strip()
                points = int(lines[i+2].strip())
                assignment=Assignment(name, assignment_id, points)
                self.assignments[assignment_id]=assignment
    def getSubmissions(self):
        sublocation='data/submissions'
        for files in os.listdir(sublocation):
            if files.endswith('.txt'):
                with open(f'{sublocation}/{files}', 'r') as file:
                    for line in file:
                        student_id, assignment_id, score=line.strip().split('|')
                        score=int(score)
                        submission=Submission(student_id, assignment_id, score)
                        self.submissions.append(submission)
                        if student_id in self.students and assignment_id in self.assignments:
                            student=self.students[student_id]
                            assignment=self.assignments[assignment_id]
                            assignment.addsub(submission)
                            student.addsub(assignment_id, score, assignment.points)

    def getgrade(self, student_name):
        for student in self.students.values():
            if student.name==student_name:
                return student.percentage()
        return "Student not found"
    def getstats(self, assignment_name):
        for assignment in self.assignments.values():
            if assignment.name==assignment_name:
                stats= assignment.get_statistics()
                if stats["min"] is None:
                    return "Assignment not found"
                return f"Min: {stats['min']}%\nAvg: {int(stats['avg'])}%\nMax: {stats['max']}%"
        return "Assignment not found"

def menu():
    completedinfo=completeInfo()
    while True:
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        choice = input("\nEnter your selection: ")
        if choice=='1':
            student_name=input("What is the student's name: ")
            grade=completedinfo.getgrade(student_name)
            print(f"{grade}%")
        elif choice=='2':
            assignment_name=input("What is the assignment name: ")
            stats=completedinfo.getstats(assignment_name)
            print(stats)
        elif choice=='3':
            assignment_name=input("What is the assignment name: ")
            found_assignment=None
            for assignment in completedinfo.assignments.values():
                if assignment.name==assignment_name:
                    found_assignment=assignment
                    break
            if not found_assignment:
                print("Assignment not found")
            else:
                scores=[sub.score for sub in found_assignment.submissions]
                plt.hist(scores, bins=7)
                plt.xticks(np.arange(50, 110, 10))
                plt.yticks(np.arange(0,10,2))
                plt.show()
                #when I used the given bins it just made 2 orange bars :/

if __name__=="__main__":
    menu()
