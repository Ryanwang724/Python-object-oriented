def main(student_dict):
    print ("\n==== student list ====")
    for stu, info in student_dict.items():
        print(f"\nName: {stu}")
        for subject, score in info.items():
            print(f"  subject: {subject}, score: {score}")
    print ("\n======================")