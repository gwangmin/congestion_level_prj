from django.db import models

# Create your models here.
class Facility(models.Model):
    '''
    시설
    '''
    name = models.CharField(max_length=200, verbose_name='시설명')
    intro = models.TextField(null=True, blank=True, verbose_name='시설 소개')
    addr = models.CharField(max_length=200, verbose_name='주소')
    web_addr = models.CharField(max_length=200, verbose_name='홈페이지 주소')
    phone_num = models.CharField(max_length=30, verbose_name='전화번호')

    def __str__(self) -> str:
        return self.name

class Building(models.Model):
    '''
    관
    '''
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='관 이름')
    intro = models.TextField(null=True, blank=True, verbose_name='관 소개')
    congest_lv = models.CharField(max_length=30, null=True, blank=True, verbose_name='혼잡도') # float

    def __str__(self) -> str:
        return self.name
    
class CCTV(models.Model):
    '''
    CCTV
    '''
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    coverage = models.CharField(max_length=200, verbose_name='촬영 범위')
    computed_congest_lv = models.CharField(max_length=30, null=True, blank=True, verbose_name='계산된 혼잡도')

    def __str__(self) -> str:
        return f'{self.building.name} - {self.id}'
    
class Statistics(models.Model):
    '''
    관별 통계
    '''
    building = models.ForeignKey(Building, null=True, blank=True, on_delete=models.CASCADE)
    time = models.DateTimeField()
    congest_lv = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'[{self.building.name}] {self.time} - {self.congest_lv}'
