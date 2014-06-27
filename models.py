from django.db import models

from django.contrib.auth.models import User

class Journal(models.Model):
    """Unified journal"""
    timestamp = models.DateTimeField(auto_now_add=True)
    address = models.IPAddressField()
    agent = models.CharField(max_length=255)
    #referer = models.CharField(max_length=255)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    @property
    def location(self):
        from django.contrib.gis.geoip import GeoIP
        geoip = GeoIP()
        return geoip.country(self.address)
    @property
    def agent_property(self):
        from user_agents import parse
        # TODO: clean this pile of dirt which is here because parse() gives os.family="Windows 7"/"Windows Vista"... for Windows, not just "Windows" as we want
        result = parse(self.agent)
        return {'os': {'family': result.os.family if result.os.family.split(' ', 0)!='Windows' else 'Windows'}, 'browser': {'family': result.browser.family}, 'is_pc': result.is_pc, 'is_mobile': result.is_mobile, 'is_tablet': result.is_tablet, 'is_bot': result.is_bot}
    class Meta:
        abstract = True
