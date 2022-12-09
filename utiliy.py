
# main.py

# Define grade-level based on the user's login_id
def grade_level(user,graduation_years):
    grade = ''
    if 'login_id' in user:
        grad_year = user['login_id'].split('@')[0][-2:]

        for g in graduation_years:
            if g['year'] == grad_year:
                grade = g['grade'] 

    return grade