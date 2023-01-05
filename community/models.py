from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('THe Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model"""
    username = models.CharField(max_length=20, blank=True)
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    code = models.CharField(max_length=5, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                                max_length=10, blank=True)
    nickname = models.CharField(max_length=20, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=64, unique=True)
    address = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to='profile/%Y%m%d/', default='user_profile_image.png')
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_sdp = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class TimeStampedModel(models.Model):
    """Time stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #admin에서 안보이게

def get_upload_path(instance, filename):
    return 'community/img/{}'.format(filename)    
class BoardPhoto(TimeStampedModel):
    image = models.ImageField(
        upload_to=get_upload_path, default='board_image.png'
    )

class BoardComment(TimeStampedModel):
    board = models.ForeignKey(
        'FreeBoard', related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    # isParent: true일 경우 parent 댓글, false일 경우 child 댓글
    isParent = models.BooleanField(null=False, blank=False, default=True)
        # parent 댓글이 삭제되어도, child 댓글은 유지, parent를 null 설정
    parent = models.ForeignKey(
        'BoardComment', related_name='childs', on_delete=models.SET_NULL, null=True, blank=True)
    # 댓글 writer가 회원 탈퇴해도, 댓글은 유지, writer를 null 설정
    writer = models.ForeignKey(
        'User', related_name='comments', on_delete=models.SET_NULL, null=True, blank=False)
    # 멘션된 사용자가 회원 탈퇴하더라도, 댓글은 유지, mention을 null 설정
    mention = models.ForeignKey(
        'User', related_name='mentionedComments', on_delete=models.SET_NULL, null=True, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.board.title, str(self.id))


class Report(models.Model):
    """Report Category Definition"""
    REPORT1 = "게시판 성격에 부적절함"
    REPORT2 = "음란물/불건전한 만남 및 대화"
    REPORT3 = "사칭/사기성 게시글"
    REPORT4 = "욕설/비하"
    REPORT5 = "낚시/도배성 게시글"
    REPORT6 = "상업적 광고 및 판매"
    REPORT_CHOICES = (
        (REPORT1, "게시판 성격에 부적절함"),
        (REPORT2, "음란물/불건전한 만남 및 대화"),
        (REPORT3, "사칭/사기성 게시글"),
        (REPORT4, "욕설/비하"),
        (REPORT5, "낚시/도배성 게시글"),
        (REPORT6, "상업적 광고 및 판매"),
    )

    report_reason = models.CharField(choices=REPORT_CHOICES, max_length=30)    

    class Meta:
        abstract = True

# class Hashtag(models.Model):


class Board(TimeStampedModel):
    title = models.CharField(max_length=100)
    writer_name = models.ForeignKey("User", on_delete=models.CASCADE)  #게시글다는 사람 이름
    content = models.TextField(max_length=2000)
    board_like_cnt = models.PositiveIntegerField(default=0, verbose_name='좋아요 수')

class FreeBoard(Board, BoardPhoto, BoardComment, Report, TimeStampedModel):
    
    def __str__(self):
        return self.title


class PlaceRecommendBoard(Board, BoardPhoto, BoardComment, Report, TimeStampedModel):
    relation = models.TextField(max_length=1000)
    html_content = models.TextField(max_length=50000)

    def __str__(self):
        return self.title

class PromotionBoard(Board, BoardPhoto, BoardComment, Report, TimeStampedModel):
    def __str__(self):
        return self.title

class MeetingBoard(Board, BoardPhoto, BoardComment, Report, TimeStampedModel):

    def __str__(self):
        return self.title
