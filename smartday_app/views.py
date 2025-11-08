import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Item
from django.views.decorators.http import require_GET, require_POST


def task(request):
    categories = list(Category.objects.all().values('id', 'name', 'type'))
    return JsonResponse({'categories': categories})

# --- CATEGORY CREATION ---
@csrf_exempt
def add_category(request):
    """Create a new Task or Routine category (e.g., Task 2, Routine 1)."""
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        cat_type = data.get('type')

        category = Category.objects.create(name=name, type=cat_type)

        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'type': category.type
        })

# --- ITEM CREATION ---
@csrf_exempt
def add_item(request):
    """Add a new item to a specific category."""
    if request.method == 'POST':
        data = json.loads(request.body)
        category_id = data.get('category_id')
        title = data.get('title')
        time = data.get('time')

        category = Category.objects.get(id=category_id)
        item = Item.objects.create(
            category=category,
            title=title,
            time=time if category.type == 'routine' else None
        )

        return JsonResponse({
            'id': item.id,
            'title': item.title,
            'status': item.status,
            'time': str(item.time) if item.time else None
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

# --- TOGGLE ITEM STATUS ---
@csrf_exempt
def toggle_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item = Item.objects.get(id=item_id)
            item.status = 'completed' if item.status == 'active' else 'active'
            item.save()
            return JsonResponse({'status': 'ok', 'id': item.id, 'new_status': item.status})
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
@csrf_exempt
def delete_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            item = Item.objects.get(id=item_id)
            item.delete()
            return JsonResponse({'status': 'ok', 'id': item_id})
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# --- LOAD ITEMS BY CATEGORY ---
def get_items(request, category_id):
    """Get all items for a specific category."""
    items = Item.objects.filter(category_id=category_id).values("id", "title", "status", "time")
    return JsonResponse({"items": list(items)})

@require_GET
def get_categories(request):
    """
    Returns JSON:
    { "categories": [
        {"id":1,"name":"Task 1","type":"task","items":[{"id":11,"title":"foo","status":"active"}, ...]},
        ...
      ]
    }
    """
    # choose filter: for now return categories with no user (your test setup)
    # If you want all categories regardless of user, use Category.objects.all()
    categories_qs = Category.objects.filter(user__isnull=True).prefetch_related('items').order_by('created_at')

    categories = []
    for cat in categories_qs:
        items = list(cat.items.all().values('id', 'title', 'status', 'time'))
        categories.append({
            'id': cat.id,
            'name': cat.name,
            'type': cat.type,
            'items': items
        })
    return JsonResponse({'categories': categories})