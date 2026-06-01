import os, json, datetime, requests

API_KEY='2f08cc...18'
CITY = os.getenv('CITY', 'Sao Paulo')

def fetch_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def format_post(data):
    temp = data['main']['temp']
    desc = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    title = f'Previsão do Tempo – {CITY} ({date_str})'
    md = f"---\ntitle: \"{title}\"\ndate: {date_str}\n---\n\n"
    md += f"## \ud83c\udf24\ufe0f Clima de hoje\n\n"
    md += f"- **Temperatura:** {temp}\u202f\u00b0C\n"
    md += f"- **Condição:** {desc}\n"
    md += f"- **Umidade:** {humidity}%\n"
    md += f"- **Vento:** {wind} m/s\n\n"
    md += "### \ud83d\udce6 Ofertas do Mercado Livre relacionadas ao clima\n\n"
    md += "- **Ventiladores portáteis** – [ver no Mercado Livre](https://www.mercadolivre.com.br/ventilador)\n"
    md += "- **Roupas leves** – [ver no Mercado Livre](https://www.mercadolivre.com.br/roupas+leve)\n"
    md += "- **Protetor solar** – [ver no Mercado Livre](https://www.mercadolivre.com.br/protetor+solar)\n"
    return md

def save_post(md):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'news_site/posts/{today}-weather.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f'Post saved to {filename}')

if __name__ == '__main__':
    data = fetch_weather()
    md = format_post(data)
    save_post(md)
