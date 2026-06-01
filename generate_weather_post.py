#!/usr/bin/env python3
"""
Gerador automático de post diário de clima.

- Lê a chave da API OpenWeather do .env (variável OPENWEATHER_API_KEY)
- Usa a cidade definida na variável de ambiente CITY (padrão: São Paulo)
- Cria um arquivo Markdown em ./posts/<YYYY-MM-DD>-weather.md
- Formato pronto para ser consumido por Jekyll/Hugo (front‑matter + conteúdo)
"""

import os
import datetime
import pathlib
import requests

# -------------------------------------------------------------
# Configurações (variáveis de ambiente)
# -------------------------------------------------------------
API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITY    = os.getenv('CITY', 'Sao Paulo')
if not API_KEY:
    raise RuntimeError('OPENWEATHER_API_KEY não está definido no .env')

# -------------------------------------------------------------
# Função para buscar o clima
# -------------------------------------------------------------
def fetch_weather():
    url = (
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
    )
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()

# -------------------------------------------------------------
# Formata o markdown do post
# -------------------------------------------------------------
def format_post(data):
    temp      = data['main']['temp']
    desc      = data['weather'][0]['description'].capitalize()
    humidity  = data['main']['humidity']
    wind      = data['wind']['speed']
    date_str  = datetime.datetime.now().strftime('%Y-%m-%d')
    title     = f'Previsão do Tempo – {CITY} ({date_str})'

    front_matter = f'''---\ntitle: "{title}"\ndate: {date_str}\n---\n\n'''
    body = f'''## 🌤️ Clima de hoje em {CITY}\n\n'''
    body += f'''- **Temperatura:** {temp}\u00b0C\n'''
    body += f'''- **Condição:** {desc}\n'''
    body += f'''- **Umidade:** {humidity}%\n'''
    body += f'''- **Vento:** {wind} m/s\n\n'''
    body += '''### 🛒 Ofertas do Mercado Livre relacionadas ao clima\n\n'''
    body += '''- **Ventiladores portáteis** – [ver no Mercado Livre](https://www.mercadolivre.com.br/ventilador)\n'''
    body += '''- **Roupas leves** – [ver no Mercado Livre](https://www.mercadolivre.com.br/roupas+leve)\n'''
    body += '''- **Protetor solar** – [ver no Mercado Livre](https://www.mercadolivre.com.br/protetor+solar)\n'''

    return front_matter + body

# -------------------------------------------------------------
# Salva o arquivo markdown
# -------------------------------------------------------------
def save_post(md_content):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    out_path = pathlib.Path('posts') / f'{today}-weather.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_content, encoding='utf-8')
    print(f'✅ Post salvo em {out_path}')

# -------------------------------------------------------------
# Execução principal
# -------------------------------------------------------------
if __name__ == '__main__':
    weather_data = fetch_weather()
    markdown = format_post(weather_data)
    save_post(markdown)
