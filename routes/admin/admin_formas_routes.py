from fastapi import APIRouter, Form
from fastapi.templating import Jinja2Templates

from data import forma_pagamento_repo


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/admin/formas_pagamento")
async def get_formas_pagamento():
    formas_pagamento = forma_pagamento_repo.obter_todas()
    response = templates.TemplateResponse("formas_pagamento.html", {"request": {}, "formas_pagamento": formas_pagamento})
    return response