# Para iniciar a API:
```cmd
    python -m uvicorn API:app --reload
```
# Passos para funcionamento:
1. Executar uma requição *POST* no URL "http://127.0.0.1:8000/update/CODIGO_DE_ALGUM_VIDEO" , código exemplo: *sbc461eSyrk*
2. Esperar até o video estar baixado (status pode ser encontrado no console)
3. Para atualizar os metadados:
    1. Fazer requisição *PUT* NO URL "http://127.0.0.1:8000/update/CODIGO/metadata" com um corpo json de:
    ```JSON
    {
        "title": "TITULO",
        "channel": "ARTISTA",
        "album": "ALBUM"
    }
    ```
4. Executar uma requisição *POST* no URL "http://127.0.0.1:8000/downloadMP3/CODIGO" para converter o MP4 em MP3 e adicionar os metadados

# Obs:
Caso tente baixar o mesmo vídeo 2x seguidas, o yt_dlp irá reclamar que o arquivo já existe.
Caso o mesmo ocorra, um erro *irá* acontecer.
Para evitar tal erro, apague o arquivo após o baixar quando for fazer uma atualização no programa.

