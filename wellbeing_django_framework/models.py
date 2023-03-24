from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django_cryptography.fields import encrypt

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = encrypt(models.DateTimeField(auto_now_add=True))
    title = encrypt(models.CharField(max_length=100, blank=True, default=''))
    code = encrypt(models.TextField())
    linenos = encrypt(models.BooleanField(default=False))
    language = encrypt(models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100))
    style = encrypt(models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100))
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = encrypt(models.TextField())

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['created']