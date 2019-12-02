from django.db import models


class UploadImage(models.Model):
    """
    上传图片
    """
    name = models.CharField(default="", max_length=60, null=True, blank=True, verbose_name="图片名称")
    # code = models.CharField(default="", max_length=60, nul=True, blank=True, verbose_name="图片编码")
    image = models.ImageField(upload_to="avatar/%Y%m%d/", null=True, blank=True, verbose_name="图片")
    creator = models.CharField(default="", max_length=60, null=True, blank=True, verbose_name="用户名")

    class Meta:
        verbose_name_plural = verbose_name = "图片列表"

    def __str__(self):
        return self.name
