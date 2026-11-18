# Laboratório local de SQL Injection

Aplicação didática com dois endpoints de login:
- `/login-vulnerable`: consulta SQL montada por concatenação, intencionalmente vulnerável.
- `/login-secure`: consulta parametrizada, usada como exemplo de correção.

**Uso exclusivamente local e educacional.** Não publique esta aplicação na internet, não use credenciais reais e não reutilize o padrão vulnerável em sistemas reais.

## Executar

Na raiz do projeto:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

python lab/app.py
```

Abra `http://127.0.0.1:5000`. O servidor vincula somente ao loopback local.

Credencial fictícia:
- usuário: `aluno`
- senha: `dio123`

## Demonstração manual

No formulário da página inicial, selecione o endpoint vulnerável e teste as credenciais fictícias acima. Em seguida, no endpoint vulnerável, use como usuário a entrada abaixo e deixe a senha vazia:

```text
' OR '1'='1' --
```

Compare com o endpoint seguro usando a mesma entrada. O endpoint seguro deve rejeitar a autenticação.

A entrada é uma prova de conceito simples para este laboratório SQLite específico. Não a use contra qualquer sistema externo.

## Testes automatizados

Na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam login válido, rejeição de senha incorreta e diferença entre os endpoints para a entrada de demonstração.
