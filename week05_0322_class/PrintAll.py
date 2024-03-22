class PrintAll:
    def __init__(self,input_dict):
        self.stu_dict = input_dict
    def execute(self):
        print ("\n==== student list ====")
        for stu, info in self.stu_dict.items():
            print(f"\nName: {stu}")
            for subject, score in info.items():
                print(f"  subject: {subject}, score: {score}")
        print ("\n======================")
        return self.stu_dict
