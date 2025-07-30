import re
import unicodedata

class FormatationService:
    """
    Service for formatting data keys.
    """
    def remover_acentos(self, texto: str) -> str:
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    
    def remover_espacos(self, texto: str) -> str:
        return re.sub("\s", "_", texto)

    def format_keys(self, data: dict) -> dict:
        data_formatado = {}
        
        for key, value in data.items():
            key_sem_acentos = self.remover_acentos(key)
            key_sem_espacos = self.remover_espacos(key_sem_acentos)
            key_formatada = re.sub(r"[^\w\s]", "", key_sem_espacos).lower().strip()
            data_formatado[key_formatada] = value

        return data_formatado