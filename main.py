from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image, ImageOps
import io

app = FastAPI()

def apply_negative_filter(image: Image.Image) -> Image.Image:
    # Aplica um filtro negativo na imagem
    return ImageOps.invert(image)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        # Abre a imagem usando PIL
        image = Image.open(file.file).convert("RGB")  # Converte para RGB se não estiver nesse modo
        
        # Aplica o filtro negativo à imagem
        filtered_image = apply_negative_filter(image)
        
        # Cria um objeto BytesIO para armazenar a imagem processada em memória
        img_io = io.BytesIO()
        
        # Salva a imagem processada no objeto BytesIO
        filtered_image.save(img_io, 'JPEG')
        
        # Retorna o ponteiro do objeto BytesIO para o início
        img_io.seek(0)
        
        # Retorna a imagem processada como uma resposta HTTP com o tipo de mídia 'image/jpeg'
        return StreamingResponse(
            content=img_io,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"attachment; filename=filtered_{file.filename}"}
        )
    except Exception as e:
        # Em caso de erro, retorna um erro 500 com a mensagem do erro
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Serve o arquivo HTML
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
