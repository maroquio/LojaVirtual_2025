from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from repo import forma_pagamento_repo


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/formas_pagamento")
async def get_formas_pagamento():
    formas_pagamento = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse("admin/formas_pagamento.html", {"request": {}, "formas_pagamento": formas_pagamento})
    return response