from typing import Any, Dict, Optional


async def find_many_with_page_info(
    model,
    where: Optional[Dict[str, Any]] = None,
    page: int = 1,
    limit: int = 10,
    order: Optional[Dict[str, Any]] = None,
):
    where = where or {}
    order = order or {}

    skip = (page - 1) * limit
    data = await model.find_many(where=where, skip=skip, take=limit, order=order)
    count = await model.count(where=where)
    last_page = (count // limit) + (1 if count % limit else 0) if limit else 1

    return {
        "data": data,
        "pagination": {
            "count": count,
            "lastPage": last_page,
            "page": page,
            "perPage": limit,
        },
    }


async def update_parcial_data(model, where: dict, data: Dict[str, Any]):
    parcial_data = {k: v for k, v in data.items() if v is not None}

    if not parcial_data:
        return None

    return await model.update(where=where, data=parcial_data)
