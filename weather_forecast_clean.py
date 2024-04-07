import requests
import os
import json

# Função para buscar dados de previsão do tempo da API:
def fetch_weather_data(city, api_key, units='metric'):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    try:
        response = requests.get(url)
        response.raise_for_status() # Levanta uma exceção se a resposta indicar um erro HTTP

        #Cache de resultados
        cache_filename = f'{city}_{units}.json'
        if os.path.exists(cache_filename):
            with open(cache_filename, 'r') as cache_file:
                return json.load(cache_file)
        else:
            data = response.json()
            with open(cache_filename, 'w') as cache_file:
                json.dump(data, cache_file)
            return data
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Verifique sua chave API do OPenWeatherMap. Parece ser inválida")
        else:
            print(f'Erro HTTP: `{http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Erro ao buscar os dados da previsão do tempo: {req_err}')
    except Exception as e:
        print(f'Erro inesperado: {e}')
    return None 

# Função para exibir a previsão de tempo
def display_weather_forecast(data):
    if data and data.get("cod") != 404:
        descricao  = data["weather"][0]["description"]
        temperatura = data["main"]["temp"]
        umidade= data["main"]["humidity"]
        vento = data["wind"]["speed"]
        pais = data["sys"]["country"]
        cidade = data["name"]
        print(f"Previsão do tempo em {cidade}, {pais}: ")
        print(f"Descriçãao: {descricao}: ")
        print(f"Temperatura: {temperatura} °C: ")
        print(f"Umidade: {umidade}%: ")
        print(f"Velocidade do Vento: {vento} m/s """)
    else:
        print("City not found")

# Função para carregar configurações do arquivo externo 

def loading_config(filename='config.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    else:
        print("Arquivo de configuração não encontrado")
        return {}

# Função principal
def main():
    # Carrega configurações
    config = loading_config()
    api_key = config.get("api_key")
    units = config.get("units", "metric")

    # Se a chave da API não estiver definida no arquivo de configuração
    if not api_key:
        print("Chave da API do OpenWeatherMap não encontrada no arquivo de configuração.")
        api_key = input("Digite sua chave da API do OpenWeatherMap: ")

    city = input("Digite o nome da cidade: ")
    
    weather_data = fetch_weather_data(city, api_key, units)
    if weather_data:
        display_weather_forecast(weather_data)

if __name__ == "__main__":
    main()