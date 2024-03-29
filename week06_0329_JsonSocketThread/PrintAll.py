class PrintAll:
    def __init__(self,input_dict):
        self.stu_dict = input_dict

    def execute(self):
        print ("\n==== student list ====")
        for _ , info in self.stu_dict.items():
            for key , value in info.items():
                if key == 'name':
                    print(f"\nName: {value}")
                elif key == 'scores':
                    for subject , score in value.items():
                        print(f"  subject: {subject},score: {score}")
        print ("\n======================")
        return self.stu_dict