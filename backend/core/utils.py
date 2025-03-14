from django.http import JsonResponse
from rest_framework import status
import uuid
from django.db import transaction, IntegrityError

def generate_unique_id(prefix="USR", model=None, field="id"):
    """
    Generate a unique ID with a prefix.
    """
    max_attempts = 5
    for _ in range(max_attempts):
        unique_id = f"{prefix}-{uuid.uuid4().hex[:8]}"  # Shortened for readability
        if model and hasattr(model, 'objects') and not model.objects.filter(**{field: unique_id}).exists():
            return unique_id
        elif not model:
            return unique_id
    raise IntegrityError(f"Failed to generate unique ID with prefix {prefix} after {max_attempts} attempts")

def api_response(data=None, message="Success", status_code=status.HTTP_200_OK, errors=None):
    """
    Standardize API responses across the project.
    """
    response = {
        "status": "success" if status_code < 400 else "error",
        "message": message,
        "data": data if data is not None else {},
    }
    if errors:
        response["errors"] = errors
    return JsonResponse(response, status=status_code)

def paginate_queryset(queryset, request, page_size=10):
    """
    Paginate a queryset based on request parameters.
    """
    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    return {
        "results": page,
        "count": paginator.page.paginator.count,
        "next": paginator.get_next_link(),
        "previous": paginator.get_previous_link(),
    }