from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from jobs.models import (User, Company, JobSeeker, Area, EmploymentType, Job, JobApplication, Status,
                         Skill, Notification, UserNotification,
                         Career, Comment, Rating, Like)
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
import cloudinary
from django.urls import path
from jobs import dao
from django.shortcuts import render
from django.contrib.auth.models import Permission  # Phần chứng thực
from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken, IDToken
# from .models import User as CustomUser


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = '__all__'


class JobApplicationAdmin(admin.ModelAdmin):
    form = JobApplicationForm
    list_display = ['id', 'job', 'jobseeker', 'status', 'active', 'created_date']
    search_fields = ['id', 'created_date', 'status__role', 'job__title', 'jobseeker__user__username']
#   'status__role' => lấy trường role ở bảng Status thông qua khóa ngoại status của bảng hiện tại JobApplication
#   'applicant__user__username' => Tương tự như vậy nhưng đi qua thêm 1 bảng trung gian nữa (User)


# Thiết kế lại form cho model User
class UserForm(forms.ModelForm):
    # def clean(self):
    #     cleaned_data = super().clean()
    #     is_superuser = cleaned_data.get('is_superuser')
    #     is_staff = cleaned_data.get('is_staff')
    #     is_employer = cleaned_data.get('is_employer')
    #     is_applicant = cleaned_data.get('is_applicant')
    #
    #     # If the user is not a superuser or staff, ensure they select one of the roles
    #     if not is_superuser and not is_staff:
    #         if is_employer and is_applicant:
    #             raise forms.ValidationError("Can only be selected as employer or applicant.")
    #         if not is_employer and not is_applicant:
    #             raise forms.ValidationError("Must choose whether to be the employer or the applicant.")
    #
    #     return cleaned_data


    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile', 'gender', 'role', 'is_superuser', 'avatar')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'mobile', 'email', 'gender', 'is_superuser', 'role']
    search_fields = ['id', 'mobile']
    readonly_fields = ['is_superuser']  # Trường is_superuser chỉ cho đọc không cho chỉnh
    form = UserForm  # Ghi đè lại form mặc định (form mình tự tạo ghi đè lên)
    # Thiết kế để khi lick vào link url của ảnh thì có thể truy cập vào ảnh
    def avatar(self, user):
        if user.avatar:
            if type(user.image) is cloudinary.CloudinaryResource:
                return mark_safe(
                    "<img src='{img_url}' alt='{alt}' width=120px/>".format(img_url=user.avatar.url, alt='AvatarUser'))
            return mark_safe("<img src='/static/{img_url}' alt='{alt}' width=120px/>".format(img_url=user.avatar.name,
                                                                                             alt='AvatarUser'))



class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        skills = cleaned_data.get('skills')
        areas = cleaned_data.get('areas')

        if skills and skills.count() > 5:
            raise forms.ValidationError("You can select a maximum of 5 skills.")

        if areas and areas.count() > 3:
            raise forms.ValidationError("You can select a maximum of 3 areas.")

        return cleaned_data

# Tạo inlineModel (Từ model Applicant có thể thêm luôn JobApplication)


class JobApplicationInline(admin.StackedInline):
    model = JobApplication
    pk_name = 'jobseeker'

class JobSeekerAdmin(admin.ModelAdmin):
    form = JobSeekerForm
    list_display = ['id', 'position', 'career', 'user_username', 'user_mobile', 'user_email', 'user_gender',
                    'salary_expectation', 'cv']
    search_fields = ['id', 'position', 'career__name', 'user__username', 'user__mobile', 'user__email', ]
    list_filter_horizontal = ['salary_expectation', ]
    inlines = (JobApplicationInline,)
    # Để cho list_display lấy thông tin
    def career(self, obj):
        return obj.career.name

    # Để cho list_display lấy thông tin
    def user_username(self, obj):
        return obj.user.username

    # Để cho list_display lấy thông tin
    def user_mobile(self, obj):
        return obj.user.mobile

    # Để cho list_display lấy thông tin
    def user_email(self, obj):
        return obj.user.email

    # Để cho list_display lấy thông tin
    def user_gender(self, obj):
        return obj.user.gender



# Tạo inlineModel (Từ model Employer có thể thêm luôn RecruitmentPost)
class CompanyInline(admin.StackedInline):
    model = Job
    pk_name = 'company'


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'position', 'companyName', 'company_type', 'user_username', 'user_mobile', 'user_email',
                    'user_gender', ]
    search_fields = ['id', 'position', 'companyName', 'user__username', 'user__mobile', 'user__email', ]
    # Thêm vào để có thể tạo inlineModel
    inlines = (CompanyInline,)

    def user_username(self, obj):
        return obj.user.username

    def user_mobile(self, obj):
        return obj.user.mobile

    def user_email(self, obj):
        return obj.user.email

    def user_gender(self, obj):
        return obj.user.gender

    # Để cho list_display lấy thông tin
    def company_type(self, obj):
        return dict(Company.STATUS_CHOICES)[obj.status]


class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']


class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    search_fields = ['id', 'type']


class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'deadline', 'quantity', 'career_name', 'position', 'companyName', 'employmenttype',
                    'gender', 'location', 'salary', 'reported']
    search_fields = ['id', 'title', 'career__name', 'position', 'company__companyName', 'employmenttype__type',
                     'location', 'gender']
    list_filter_horizontal = ['quantity', 'salary']  # Lọc theo chiều ngang => Không hiện thanh kéo

    def career_name(self, obj):
        return obj.career.name

    def companyName(self, obj):
        return obj.company.companyName

    # Custom function để hiển thị trạng thái reported
    def reported(self, obj):
        if obj.reported:
            return format_html(
                '<span style="color:red;">Yes</span>')  # Nếu bài đăng bị báo cáo, hiển thị "Yes" với màu đỏ
        else:
            return format_html(
                '<span style="color:green;">No</span>')  # Nếu bài đăng không bị báo cáo, hiển thị "No" với màu xanh lá cây

    reported.short_description = 'Reported'  # Đặt tên cho cột "Reported" trong trang quản trị
    reported.admin_order_field = 'reported'  # Cho phép sắp xếp bài đăng theo trạng thái reported

    # Phần tìm kiếm lương lớn hơn hoặc bằng
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Nếu có mức lương được nhập vào trong thanh tìm kiếm
        if search_term.isdigit():
            salary = int(search_term)
            queryset |= self.model.objects.filter(salary__gte=salary)

        return queryset, use_distinct


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'role']


class SkillAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CareerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class CommentInline(admin.StackedInline):
    model = Comment  # Chỉ định rằng InlineAdmin này sẽ hiển thị các comment con của một comment cha.
    fk_name = 'parent'  # Chỉ định khóa ngoại liên kết các comment con với comment cha là parent.
    extra = 0  # Không hiển thị trường để thêm comment con mới khi chưa có comment cha.
    # Chỉ định các trường sẽ hiển thị trong InlineAdmin.
    fields = ['content', 'jobseeker', 'company', 'job']
    # Đánh dấu các trường applicant, employer, recruitment chỉ để đọc, không cho phép chỉnh sửa trong InlineAdmin.
    readonly_fields = ['job']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'jobseeker_username', "interaction__job__title"]
    search_fields = ['id', 'jobseeker__user__username', 'company__user__username']
    # 'applicant__user__username', 'employer__user__username' : search_fields lấy thông tin thông qua kế thừa model -> khóa ngoại -> Nơi cần lấy thông tin
    inlines = [CommentInline]

    # Để cho list_display lấy thông tin: Thông qua kế thừa model -> Khóa ngoại -> Nơi cần lấy thông tin
    def jobseeker_username(self, obj):
        if obj.jobseeker:
            return obj.jobseeker.user.username
        return None

    # Vì lấy chung thông tin tới User nên phải viết thêm 1 hàm def
    # Để cho list_display lấy thông tin: Thông qua kế thừa model -> Khóa ngoại -> Nơi cần lấy thông tin
    def company_username(self, obj):
        if obj.company:
            return obj.company.user.username
        return None

    # Để cho list_display lấy thông tin: Thông qua kế thừa model -> Khóa ngoại -> Nơi lấy thông tin
    def interaction__job__title(self, obj):
        return obj.job.title


class InteractionAdmin(admin.ModelAdmin):
    def jobseeker_username(self, obj):
        if obj.jobseeker:
            return obj.jobseeker.user.username
        return None

    def company_username(self, obj):
        if obj.company:
            return obj.company.user.username
        return None

    def get_username(self, obj):
        if obj.company:
            return obj.company.user.username
        if obj.jobseeker:
            return obj.jobseeker.user.username
        return None

class RatingAdmin(InteractionAdmin):
    list_display = ['id', 'rating', 'get_username', 'interaction__job__title']
    search_fields = ['id', 'rating', 'jobseeker__user__username', 'company__user__username']

    def get_list_display(self, request):
        # Kiểm tra loại người tạo rating và quyết định các trường hiển thị
        if self.model.objects.filter(company__isnull=False).exists():
            # Nếu có ít nhất một rating liên quan đến company
            return ['id', 'rating', 'company_username', 'interaction__job__title']
        else:
            # Nếu tất cả các rating đều liên quan đến jobseeker
            return ['id', 'rating', 'jobseeker_username', 'interaction__job__title']

    def interaction__job__title(self, obj):
        if obj.job:
            return obj.job.title
        return None

class LikeAdmin(InteractionAdmin):
    list_display = ['id', 'active', 'get_username', 'interaction__job__title']
    search_fields = ['id', 'jobseeker__user__username', 'company__user__username']

    def get_list_display(self, request):
        # Kiểm tra loại người tạo rating và quyết định các trường hiển thị
        if self.model.objects.filter(company__isnull=False).exists():
            # Nếu có ít nhất một rating liên quan đến company
            return ['id', 'active', 'company_username', 'interaction__job__title']
        else:
            # Nếu tất cả các rating đều liên quan đến jobseeker
            return ['id', 'active', 'jobseeker_username', 'interaction__job__title']
    def interaction__job__title(self, obj):
        return obj.job.title


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_date']
    search_fields = ['content']


class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'notification__content')


# Tạo trang admin theo cách của mình -> Ghi đè lại cái đã có
class MyAdminSite(admin.AdminSite):
    site_header = 'JOB MANAGEMENT SYSTEM'
    index_title = 'Welcome to the management system'
    site_title = 'Custom by DTT'
    site_url = "/"

    # Ghi đè lại url đã có
    def get_urls(self):
        return [
            path('stats/', self.stats_view),   # => myadmin/stats, myadmin là cái tạo phía dưới
            path('search/', self.search_by_salary),  # => myadmin/search, myadmin là cái tạo phía dưới
        ] + super().get_urls()

    # Cái này dẫn tới folder templates/
    def stats_view(self, request):
        return TemplateResponse(request, 'admin/jobStats.html', {
            'queryset': dao.count_job_application_quarter_career(),

            'femaleApply': dao.recruitment_posts_with_female_applicants(),
        })

    # Cái này dẫn tới folder templates/
    def search_by_salary(self, request):
        if request.method == 'GET':
            salary = request.GET.get('salary')
            if salary:
                # Lọc các bài đăng có mức lương lớn hơn hoặc bằng mức lương nhập vào
                recruitment_posts = dao.search_salary_recruiment_post(salary)
                return render(request, 'admin/search_salary.html',
                              {'recruitment_posts': recruitment_posts, 'salary': salary,
                               })
        return render(request, 'admin/search_salary.html', {})


class GrantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'application', 'expires', 'redirect_uri')


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'application', 'expires', 'scope')


class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'application', 'access_token')


class IDTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'user')


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'user', 'authorization_grant_type', 'client_type')


# Tạo đối tượng
my_admin_site = MyAdminSite(name='myadmin')  # tạo đường dẫn myadmin thay thế cho admin hiện tại

my_admin_site.register(User, UserAdmin),
my_admin_site.register(Company, CompanyAdmin),
my_admin_site.register(JobSeeker, JobSeekerAdmin),
my_admin_site.register(Area, AreaAdmin),
my_admin_site.register(EmploymentType, EmploymentTypeAdmin),
my_admin_site.register(Job, JobAdmin),
my_admin_site.register(JobApplication, JobApplicationAdmin),
my_admin_site.register(Status, StatusAdmin),
my_admin_site.register(Skill, SkillAdmin),
my_admin_site.register(Career, CareerAdmin),
my_admin_site.register(Comment, CommentAdmin),
my_admin_site.register(Rating, RatingAdmin),
my_admin_site.register(Permission),
my_admin_site.register(Like, LikeAdmin),
my_admin_site.register(Notification, NotificationAdmin)
my_admin_site.register(AccessToken, AccessTokenAdmin),
my_admin_site.register(Application, ApplicationAdmin),
my_admin_site.register(IDToken, IDTokenAdmin),
my_admin_site.register(Grant, GrantAdmin)
my_admin_site.register(RefreshToken, RefreshTokenAdmin)
my_admin_site.register(UserNotification, UserNotificationAdmin)




# # Register your models here.
# admin.site.register(User, UserAdmin),
# admin.site.register(Company, EmployerAdmin),
# admin.site.register(Applicant, ApplicantAdmin),
# admin.site.register(Area, AreaAdmin),
# admin.site.register(EmploymentType, EmploymentTypeAdmin),
# admin.site.register(RecruitmentPost, RecruitmentPostAdmin),
# admin.site.register(JobApplication, JobApplicationAdmin),
# admin.site.register(Status, StatusAdmin),
# admin.site.register(Skill, SkillAdmin),
# admin.site.register(Career, CareerAdmin),
# admin.site.register(Comment, CommentAdmin),
# admin.site.register(Rating, RatingAdmin),
# admin.site.register(Permission),
# admin.site.register(Like, LikeAdmin),
