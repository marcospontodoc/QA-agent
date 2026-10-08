import os

from dotenv import load_dotenv
from openai import OpenAI


def read_documentation(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

documentation = read_documentation("docs/login.md")

response = client.chat.completions.create(
    model="apodex/apodex-1.1-mini:free",
    messages=[
        {
            "role": "user",
            "content": f"""
Você é um analista de QA especializado em levantamento de cenários de teste.

Analise a documentação abaixo e identifique os cenários de teste que devem ser considerados.

Para cada cenário, informe:
- ID
- Título
- Tipo (Positivo ou Negativo)
- Prioridade
- Pré-condições
- Passos
- Resultado esperado

Também identifique possíveis lacunas ou informações que não estão definidas na documentação.

IMPORTANTE:
- Não invente regras de negócio que não estejam na documentação.
- Diferencie claramente o que está documentado do que é uma sugestão de teste.
- Busque cenários positivos e negativos.
- Considere casos de fronteira quando houver informações suficientes.

DOCUMENTAÇÃO:

{documentation}
"""
        }
    ]
)

print(response.choices[0].message.content)