from fastapi import APIRouter

router = APIRouter(prefix="/report", tags=["Reports"])

@router.get("/")
def get_items():
    return [{"id": 1, "Report": "Minha rua tem um buraco"}]