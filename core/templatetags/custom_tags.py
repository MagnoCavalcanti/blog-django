from django import template
from django.urls import reverse, resolve, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def is_feed_url(context, css_class, exact=True):
    
    request = context.get('request')
    if not request:
        return "" # Retorna vazio se não tiver objeto request

    # 1. Tenta obter o caminho (path) da URL fornecida (url_name)
    try:
        # Usa reverse() para obter o path da URL a partir do seu nome
        url_path = reverse("feed")
    except NoReverseMatch:
        return ""

    # 2. Compara o path da requisição com o path da URL
    current_path = request.path

    if exact:
        # Correspondência EXATA
        if current_path != url_path:
            return css_class

    return ""