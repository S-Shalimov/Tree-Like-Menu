from django import template
from django.urls import resolve
from ..models import MenuPoint

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = resolve(request.path_info).url_name
    menu_items = MenuPoint.objects.filter(name=menu_name).prefetch_related('children')
    return render_menu(menu_items, current_url)


def get_parents(current_item):
    parents = []
    while True:
        parents.insert(0, current_item)
        if current_item.parent:
            current_item = current_item.parent
        else:
            break
    return parents


def render_menu(menu_items, current_url, depth=1, parent_tree=True):
    html = '<ul>'

    if menu_items.first().parent and parent_tree:
        for parent in get_parents(menu_items.first().parent):
            html += f'<li><a href="{parent.url}">{parent.name}</a></li><ul>'

    for item in menu_items:
        active = item.url == current_url
        html += f'<li class={"active" if active else ""}>'
        html += f'<a href="{item.url}">{item.name}</a>'
        if item.children.exists() and depth > 0:
            html += render_menu(item.children.all(), current_url, depth=depth - 1, parent_tree=False)
        html += '</li>'

    if menu_items.first().parent and parent_tree:
        for parent in get_parents(menu_items.first().parent):
            html += '</ul>'

    html += '</ul>'

    return html
