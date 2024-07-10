from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from scipy import stats
from .models import *
from .forms import *
import pandas as pd
import math
import os


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            admin = Admin.objects.get(email=email)
            print(admin)
            request.session['admin'] = email
            return redirect(admin_password)
        except Admin.DoesNotExist:
            pass
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            if email in data['Email'].values:
                request.session['user'] = email
                user_data = data[data['Email'] == email].iloc[0]
                name = user_data['Name']
                UserLoginActivity.objects.create(email=email, name=name)
                return redirect(user_self_analysis)
        messages.error(request, 'Email not found! Please try again.')
        return render(request, 'LOGIN.html')
    return render(request, 'LOGIN.html')


@login_required
def logout(request):
    if 'user' in request.session:
        del request.session['user']
    elif 'admin' in request.session:
        del request.session['admin']
    return redirect(login)


# < * * * * * * * * * * * * * * * * * * * * ADMIN * * * * * * * * * * * * * * * * * * * * >


@login_required
def admin_password(request):
    email = request.session.get('admin')
    if email:
        if request.method == 'POST':
            password = request.POST.get('password')
            email = request.session.get('admin')
            try:
                admin = Admin.objects.get(email=email)
                data = email
                print(data)
                if password == admin.password:
                    return redirect(admin_home)
                else:
                    messages.error(request, 'Incorrect Password')
            except Admin.DoesNotExist:
                messages.error(request, 'Admin with this email does not exist.')
        return render(request, 'Admin_PASSWORD.html')
    return redirect(login)


@login_required
def admin_home(request):
    email = request.session.get('admin')
    if email:
        uploaded_files = ExcelData.objects.all()
        if request.method == 'POST':
            form = ExcelDataForm(request.POST, request.FILES)
            if form.is_valid():
                ExcelData.objects.all().delete()
                form.save()
                messages.success(request, 'File Upload Successful')
                return redirect('admin_home')
            else:
                messages.error(request, 'File Upload Failed. Please try again.')
                return redirect('admin_home')
        else:
            form = ExcelDataForm()
        return render(request, 'Admin_HOME.html', {'form': form, 'uploaded_files': uploaded_files})
    return redirect(login)


@login_required
def delete_excel_data(request, excel_data_id):
    excel_data = get_object_or_404(ExcelData, pk=excel_data_id)
    if request.method == 'POST':
        excel_data.delete()
        return HttpResponseRedirect(reverse('admin_home'))
    return render(request, 'confirm_delete.html', {'excel_data': excel_data})


@login_required
def admin_profile(request):
    email = request.session.get('admin')
    if email:
        if request.method == 'POST':
            psw = request.POST.get('password')
            cnf = request.POST.get('confirm-password')
            if psw == cnf:
                Admin.objects.filter(email=request.session['admin']).update(password=psw)
                messages.success(request, 'Password Updated')
                return redirect('admin_profile')
            else:
                messages.error(request, 'Password Not Match!')
                return redirect('admin_profile')
        return render(request, 'Admin_PROFILE.html', {'email': email})
    return redirect(login)


@login_required
def student_activity(request):
    email = request.session.get('admin')
    if email:
        user_login_activity = UserLoginActivity.objects.all().order_by('-login_time')
        return render(request, 'Student_ACTIVITY.html', {'user_login_activity': user_login_activity})
    return redirect(login)


@login_required
def delete_user_login_activity(request):
    if request.method == 'POST':
        UserLoginActivity.objects.all().delete()
        return redirect('student_activity')
    else:
        return redirect('student_activity')


@login_required
def add_solution(request):
    email = request.session.get('admin')
    if email:
        uploaded_solutions = MockTestSolution.objects.all()
        if request.method == 'POST':
            form = MockTestSolutionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Solution Added')
                return redirect('add_solution')
            else:
                messages.error(request, 'Could Not Upload Solution')
                return redirect('add_solution')
        else:
            form = MockTestSolutionForm()
        return render(request, 'Admin_SOLUTIONS.html', {'form': form, 'uploaded_solutions': uploaded_solutions})
    return redirect(login)


@login_required
def delete_solution(request, solution_id):
    solution = get_object_or_404(MockTestSolution, id=solution_id)
    if request.method == 'POST':
        solution.solution_file.delete()
        solution.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_study_plan(request):
    email = request.session.get('admin')
    if email:
        study_plan = StudyPlan.objects.all()
        if request.method == 'POST':
            form = StudyPlanForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Study Plan Added')
                return redirect('add_study_plan')
            else:
                messages.error(request, 'Could Not Upload Study Plan')
                return redirect('add_study_plan')
        else:
            form = StudyPlanForm()
        return render(request, 'Admin_STUDY_PLAN.html', {'form': form, 'study_plan': study_plan})
    return redirect(login)


@login_required
def delete_study_plan(request, plan_id):
    plan = get_object_or_404(StudyPlan, id=plan_id)
    if request.method == 'POST':
        plan.pdf_file.delete()
        plan.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_current_affairs(request):
    email = request.session.get('admin')
    if email:
        if request.method == 'POST':
            form = CurrentAffair(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('add_current_affairs')
        else:
            form = CurrentAffair()
        items = CurrentAffairs.objects.all().order_by('-created_at')
        return render(request, 'Admin_CURRENT_AFFAIRS.html', {'form': form, 'items': items})
    return redirect(login)


@login_required
def current_affairs_delete(request, item_id):
    item = get_object_or_404(CurrentAffairs, id=item_id)
    item.delete()
    return redirect('add_current_affairs')


@login_required
def admin_analysis(request):
    excel_data = ExcelData.objects.first()
    if excel_data:
        data = pd.read_excel(excel_data.excel_file.path, sheet_name='DB')
        mock_tests = data['MockTest'].unique()
        mock_test_details = []
        subjects = ['Current Affairs', 'Maths', 'English', 'Malayalam', 'Biology', 'History', 'Geography',
                    'Economics', 'Indian Constitution', 'Kerala Governance', 'Arts, Literature, Culture, Sports',
                    'Special Acts', 'Physics', 'Chemistry', 'IT']  # Add more subjects as needed
        for mock_test in mock_tests:
            test_data = data[data['MockTest'] == mock_test]
            total_students = len(test_data)
            avg_marks = round(test_data['Marks Obtained'].mean(), 2) if 'Marks Obtained' in test_data else 0.0
            max_marks = test_data['Maximum Marks'].iloc[0] if not test_data.empty else 0.0
            subject_details = {}
            for subject in subjects:
                subject_column = subject
                max_subject_column = f'Max_{subject.replace(" ", "_")}'
                if subject_column in test_data.columns and max_subject_column in test_data.columns:
                    subject_marks_sum = test_data[subject_column].sum()
                    max_subject_sum = test_data[max_subject_column].sum() if max_subject_column in test_data.columns else 0.0
                    subject_percentage = (subject_marks_sum / max_subject_sum) * 100 if max_subject_sum != 0 else 0.0
                    if subject_marks_sum > 0:
                        avg_subject_marks = subject_marks_sum / total_students if total_students != 0 else 0.0
                        subject_details[subject] = {
                            'subject_marks_sum': round(subject_marks_sum),
                            'max_subject_sum': round(max_subject_sum),
                            'subject_percentage': round(subject_percentage, 2),
                            'avg_subject_marks': round(avg_subject_marks, 2)
                        }
            if subject_details:
                mock_test_details.append({
                    'mock_test': mock_test,
                    'total_students': total_students,
                    'avg_marks': avg_marks,
                    'max_marks': max_marks,
                    'subject_details': subject_details,
                })
        mock_test_details.sort(key=lambda x: int(x['mock_test']), reverse=True)
        if mock_test_details:
            return render(request, 'Admin_ANALYSIS.html', {'mock_test_details': mock_test_details})
        else:
            messages.error(request, 'No mock tests with subject marks found.')
            return redirect('admin_home')
    else:
        messages.error(request, 'No Excel data found. Please upload the Excel file first.')
        return redirect('admin_home')


# < * * * * * * * * * * * * * * * * * * * * USER * * * * * * * * * * * * * * * * * * * * >


@login_required
def user_self_analysis(request):
    email = request.session.get('user')
    if email:
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            student_data = data[data['Email'] == email]
            attempted_mock_tests = student_data['MockTest'].values.tolist()
            test_display_data = {}
            for mock_test in attempted_mock_tests:
                correct = student_data.loc[student_data['MockTest'] == mock_test, 'Correct Questions'].values[0]
                incorrect = student_data.loc[student_data['MockTest'] == mock_test, 'Incorrect Questions'].values[0]
                skipped = student_data.loc[student_data['MockTest'] == mock_test, 'Skipped Questions'].values[0]
                total_marks = student_data.loc[student_data['MockTest'] == mock_test, 'Maximum Marks'].values[0]
                total_questions = correct + incorrect + skipped
                total_time = 60 if total_marks == 50 else 75
                test_display_data[mock_test] = {
                    'total_questions': total_questions,
                    'total_marks': total_marks,
                    'total_time': total_time
                }
            attempted_mock_tests.sort(reverse=True)
            sorted_test_display_data = {k: test_display_data[k] for k in sorted(test_display_data.keys(), reverse=True)}
            return render(request, 'USER_SELF_ANALYSIS.html', {
                'email': email,
                'mock_tests': attempted_mock_tests,
                'test_display_data': sorted_test_display_data
            })
    return redirect(login)


@login_required
def user_progress_report(request):
    email = request.session.get('user')
    if email:
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            student_data = data[data['Email'] == email]
            attempted_mock_tests = student_data['MockTest'].values.tolist()
            test_display_data = {}
            for mock_test in attempted_mock_tests:
                each_mock_data = data[data['MockTest'] == mock_test]
                each_mock_data = each_mock_data.copy()
                each_mock_data['percentile'] = each_mock_data['Marks Obtained'].apply(
                    lambda x: stats.percentileofscore(each_mock_data['Marks Obtained'], x))
                student_mock_data = each_mock_data.loc[each_mock_data['Email'] == email]
                percentile = round(student_mock_data['percentile'].values[0])
                rank = student_data.loc[student_data['MockTest'] == mock_test, 'Rank'].values[0]
                marks_obtained = round(student_data.loc[student_data['MockTest'] == mock_test, 'Marks Obtained'].values[0], 2)
                maximum_marks = round(student_data.loc[student_data['MockTest'] == mock_test, 'Maximum Marks'].values[0], 2)
                current_affairs = round(student_data.loc[student_data['MockTest'] == mock_test, 'Current Affairs'].values[0], 2)
                maths = round(student_data.loc[student_data['MockTest'] == mock_test, 'Maths'].values[0], 2)
                english = round(student_data.loc[student_data['MockTest'] == mock_test, 'English'].values[0], 2)
                malayalam = round(student_data.loc[student_data['MockTest'] == mock_test, 'Malayalam'].values[0], 2)
                biology = round(student_data.loc[student_data['MockTest'] == mock_test, 'Biology'].values[0], 2)
                history = round(student_data.loc[student_data['MockTest'] == mock_test, 'History'].values[0], 2)
                geography = round(student_data.loc[student_data['MockTest'] == mock_test, 'Geography'].values[0], 2)
                economics = round(student_data.loc[student_data['MockTest'] == mock_test, 'Economics'].values[0], 2)
                indian_constitution = round(student_data.loc[student_data['MockTest'] == mock_test, 'Indian Constitution'].values[0], 2)
                kerala_governance = round(student_data.loc[student_data['MockTest'] == mock_test, 'Kerala Governance'].values[0], 2)
                arts = round(student_data.loc[student_data['MockTest'] == mock_test, 'Arts, Literature, Culture, Sports'].values[0], 2)
                special_acts = round(student_data.loc[student_data['MockTest'] == mock_test, 'Special Acts'].values[0], 2)
                physics = round(student_data.loc[student_data['MockTest'] == mock_test, 'Physics'].values[0], 2)
                chemistry = round(student_data.loc[student_data['MockTest'] == mock_test, 'Chemistry'].values[0], 2)
                it = round(student_data.loc[student_data['MockTest'] == mock_test, 'IT'].values[0], 2)
                percentage = round((marks_obtained / maximum_marks) * 100, 2)
                test_display_data[mock_test] = {
                    'percentile': percentile,
                    'rank': rank,
                    'marks_obtained': marks_obtained,
                    'maximum_marks': maximum_marks,
                    'current_affairs': current_affairs,
                    'maths': maths,
                    'english': english,
                    'malayalam': malayalam,
                    'biology': biology,
                    'history': history,
                    'geography': geography,
                    'economics': economics,
                    'indian_constitution': indian_constitution,
                    'kerala_governance': kerala_governance,
                    'arts': arts,
                    'special_acts': special_acts,
                    'physics': physics,
                    'chemistry': chemistry,
                    'it': it,
                    'percentage': percentage
                }
            return render(request, 'USER_PROGRESS_REPORT.html', {'email': email, 'test_display_data': test_display_data})
    return redirect(login)


@login_required
def user_sectional_chart(request):
    email = request.session.get('user')
    if email:
        sections, selected_section, y, x = [], None, [], []
        if not email:
            return render(request, 'USER_SECTIONAL_CHART.html', {'error': 'User not logged in'})
        try:
            excel_data = ExcelData.objects.first()
            if not excel_data:
                return render(request, 'USER_SECTIONAL_CHART.html', {'error': 'Excel data not found'})
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
        except Exception as e:
            return render(request, 'USER_SECTIONAL_CHART.html', {'error': str(e)})
        student_data = data[data['Email'] == email].drop_duplicates(subset='MockTest')
        x = student_data['MockTest'].values.tolist()
        section_dict1 = {}
        for i in range(13, 28):
            n = data.columns[i].upper().replace('MARKS', '').replace('-', '')
            yyy = pd.to_numeric(student_data.iloc[:, i], errors='coerce').tolist()
            max_yyy = pd.to_numeric(student_data.iloc[:, i + 15], errors='coerce').tolist()
            z = [(ii * 100 / jj if jj != 0 else float('nan')) for ii, jj in zip(yyy, max_yyy)]
            if not all(math.isnan(k) for k in z):
                section_dict1[n] = z
        sections = list(section_dict1.keys())
        if request.method == 'POST':
            selected_section = request.POST.get('section')
            if selected_section:
                y = section_dict1.get(selected_section, [])
                filtered_x_y = [(x_value, y_value) for x_value, y_value in zip(x, y) if not math.isnan(y_value)]
                x, y = zip(*filtered_x_y) if filtered_x_y else ([], [])
        return render(request, 'USER_SECTIONAL_CHART.html', {
            'sections': sections,
            'selected_section': selected_section,
            'values': list(y),
            'x': list(x),
            'email': email
        })
    return redirect(login)


@login_required
def user_current_affairs(request):
    email = request.session.get('user')
    if email:
        items = CurrentAffairs.objects.all().order_by('-created_at')
        return render(request, 'USER_CURRENT_AFFAIRS.html', {'items': items})
    return redirect(login)


@login_required
def user_profile(request):
    email = request.session.get('user')
    if email:
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            user_data = data[data['Email'] == email].iloc[0]
            name = user_data['Name']
            phone = user_data['Phone']
            return render(request, 'USER_PROFILE.html', {'name': name, 'email': email, 'phone': phone})
    return redirect(login)


@login_required
def user_view_result(request, mock_test_id):
    email = request.session.get('user')
    if email:
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            student_data = data[data['Email'] == email]
            mock_test_data = student_data[student_data['MockTest'] == mock_test_id].iloc[0]
            correct = mock_test_data['Correct Questions']
            incorrect = mock_test_data['Incorrect Questions']
            skipped = mock_test_data['Skipped Questions']
            total_marks = mock_test_data['Maximum Marks']
            if total_marks == 50:
                total_time = 60
            else:
                total_time = 75
            total_questions = correct + incorrect + skipped
            marks_obtained = mock_test_data['Marks Obtained']
            date = mock_test_data['Date']
            rank = mock_test_data['Rank']
            total_students = max(data[data['MockTest'] == mock_test_id]['Rank'].values.tolist())
            time_taken = mock_test_data['Total Time(min)']
            accuracy = correct * 100 / total_questions
            each_mock_data = data[data['MockTest'] == mock_test_id]
            each_mock_data = each_mock_data.copy()
            each_mock_data['percentile'] = each_mock_data['Marks Obtained'].apply(
                lambda x: stats.percentileofscore(each_mock_data['Marks Obtained'], x))
            student_mock_data = each_mock_data.loc[each_mock_data['Email'] == email]
            percentile = student_mock_data['percentile'].values[0]
            return render(request, 'USER_VIEW_RESULT.html', {
                'mock_test_id': mock_test_id,
                'correct': correct,
                'incorrect': incorrect,
                'skipped': skipped,
                'total_marks': total_marks,
                'total_time': total_time,
                'total_questions': total_questions,
                'marks_obtained': marks_obtained,
                'date': date,
                'rank': rank,
                'total_students': total_students,
                'time_taken': time_taken,
                'percentile': percentile,
                'accuracy': accuracy
            })
    return redirect(login)


@login_required
def user_ai_analysis(request, mock_test_id):
    email = request.session.get('user')
    if email:
        excel_data = ExcelData.objects.first()
        if excel_data:
            excel_file_path = excel_data.excel_file.path
            data = pd.read_excel(excel_file_path, sheet_name='DB')
            student_data = data[data['Email'] == email]
            mock_test_data = student_data[student_data['MockTest'] == mock_test_id].iloc[0]
            subjects = ['Current Affairs', 'Maths', 'English', 'Malayalam', 'Biology', 'History', 'Geography',
                        'Economics', 'Indian Constitution', 'Kerala Governance', 'Arts, Literature, Culture, Sports',
                        'Special Acts', 'Physics', 'Chemistry', 'IT']
            subject_data = []
            for subject in subjects:
                obtained = mock_test_data[subject]
                max_obtained = mock_test_data[f'Max_{subject.replace(" ", "_")}']
                if pd.notna(obtained) and pd.notna(max_obtained):
                    percentage = (obtained / max_obtained) * 100 if max_obtained != 0 else 0
                    if percentage >= 75:
                        performance = 'Excellent'
                    elif 50 <= percentage < 75:
                        performance = 'Average'
                    else:
                        performance = 'Poor'
                    subject_data.append({
                        'subject': subject,
                        'obtained': obtained,
                        'max_obtained': max_obtained,
                        'percentage': percentage,
                        'performance': performance
                    })
            performance_order = {'Excellent': 0, 'Average': 1, 'Poor': 2}
            subject_data.sort(key=lambda x: performance_order[x['performance']])
            return render(request, 'USER_AI_ANALYSIS.html', {
                'mock_test_id': mock_test_id,
                'subject_data': subject_data,
            })
    return redirect(login)


@login_required
def download_mock_test_solution(request, mock_test_id):
    try:
        solution = MockTestSolution.objects.get(mock_test_number=mock_test_id)
    except MockTestSolution.DoesNotExist:
        return HttpResponse("No solution found for this mock test.", status=404)
    file_path = os.path.join(settings.MEDIA_ROOT, str(solution.solution_file))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse("Solution file not found.", status=404)


@login_required
def user_study_plan(request):
    email = request.session.get('user')
    if email:
        study_plan = StudyPlan.objects.all()
        return render(request, 'USER_STUDY_PLAN.html', {'study_plan': study_plan})
    return redirect(login)


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)






