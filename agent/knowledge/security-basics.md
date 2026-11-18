# Fundamentos de segurança de aplicações

## Princípios

- **Confidencialidade:** somente pessoas e processos autorizados acessam a informação.
- **Integridade:** dados não são alterados indevidamente.
- **Disponibilidade:** sistemas e dados permanecem acessíveis quando necessários.
- **Menor privilégio:** cada componente recebe apenas as permissões necessárias.
- **Defesa em profundidade:** controles complementares reduzem dependência de uma única barreira.

## SQL Injection (SQLi)

SQL Injection ocorre quando dados controlados pelo usuário são concatenados/interpolados diretamente em uma instrução SQL, permitindo que a entrada altere a estrutura ou a lógica da consulta.

### Exemplo vulnerável (conceitual)

```python
query = "SELECT id FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
cursor.execute(query)
```

A entrada passa a ser interpretada como parte da linguagem SQL, e não apenas como dado.

### Correção preferencial: consulta parametrizada

```python
cursor.execute(
    "SELECT id FROM users WHERE username = ? AND password = ?",
    (username, password)
)
```

O driver envia os valores separadamente da estrutura SQL. O marcador varia conforme o driver (`?`, `%s`, `:name` etc.). Nunca misture marcadores de drivers diferentes.

**Importante:** em aplicações reais, não armazene senhas em texto puro. Use hash de senha apropriado (por exemplo, Argon2id, scrypt ou bcrypt) com parâmetros adequados. O laboratório simplificado usa credenciais fictícias apenas para demonstrar SQLi; não é um modelo de autenticação para produção.

## Outras medidas relevantes

- Validar entradas conforme regras de negócio, sem tratar validação como substituta de parametrização.
- Usar contas de banco com privilégios mínimos.
- Não retornar mensagens de erro SQL detalhadas ao usuário final.
- Registrar eventos de segurança sem gravar senhas, tokens ou dados sensíveis.
- Gerenciar segredos fora do código-fonte.
- Manter dependências atualizadas e testar alterações.

## Como avaliar uma evidência

Registre: ambiente, versão/configuração, pré-condições, entrada usada, resultado observado, resultado esperado, horário e limitações. Uma demonstração em laboratório comprova o comportamento daquele laboratório, não a presença da mesma falha em outros sistemas.

## Reteste mínimo para SQLi

1. Confirmar que a conta fictícia válida autentica.
2. Confirmar que credenciais inválidas são rejeitadas.
3. Usar a entrada de teste documentada somente no endpoint vulnerável local e observar o comportamento.
4. Repetir a mesma entrada no endpoint corrigido e confirmar rejeição.
5. Executar testes automatizados e verificar que o endpoint seguro não aceita a condição de bypass.
