from typing import Optional, List

from ..app_instance import app, db
from ..schemas import *
from ..models import *

@app.post("/process")
async def transform_text(request: TextRequest):
    original_text = request.text
    transformed_text = db.search(original_text)

    return {"original": original_text, "transformed": transformed_text}