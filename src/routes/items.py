from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
def get_items():
    return [{"id": 1, "name": "Item de Teste Zelus"}]