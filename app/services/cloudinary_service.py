import cloudinary
import cloudinary.uploader
from app.core.config import settings

class CloudinaryService:
    def __init__(self):
        # Configurar Cloudinary com as credenciais
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
    
    async def upload_image(self, file_content: bytes, folder: str) -> str:
        """
        Faz upload de uma imagem para o Cloudinary
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            folder: Pasta onde salvar (ex: "empresas/123/logo")
        
        Returns:
            URL pública da imagem
        """
        try:
            result = cloudinary.uploader.upload(
                file_content,
                folder=f"agendei/{folder}",
                transformation=[
                    {'width': 1200, 'height': 800, 'crop': 'limit'},
                    {'quality': 'auto'}
                ]
            )
            return result['secure_url']
        except Exception as e:
            raise Exception(f"Erro no upload para Cloudinary: {str(e)}")