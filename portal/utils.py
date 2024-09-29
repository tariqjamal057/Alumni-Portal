def is_student(user):
    return user.groups.filter(name="student").exists()


def is_alumni(user):
    return user.groups.filter(name="alumni").exists()


def is_faculty(user):
    return user.groups.filter(name="faculty").exists()
