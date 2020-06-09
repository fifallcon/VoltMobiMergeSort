class SmartLine:
    my_file = ""
    current_line = ""

    def __init__(self, filename):
        self.my_file = open(filename, "r")
        self.current_line = self.my_file.readline()

    def data(self):
        return self.current_line.strip()

    def key(self):
        return self.current_line.split(' - ')[0].strip()

    def value(self):
        return self.current_line.split(' - ')[1].strip()

    def next(self):
        self.current_line = self.my_file.readline()

    def end_read(self):
        self.my_file.close()
