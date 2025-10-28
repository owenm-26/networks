
class Node:
    def __init__(self,student_status: int, gender:int, major: int, vertex_degree:int):
        self.student_status = student_status
        self.gender = gender
        self.major = major
        self.vertex_degree = vertex_degree
    def __repr__(self):
        return f"Node(status={self.student_status}, gender={self.gender}, major={self.major}, degree={self.vertex_degree})"
    