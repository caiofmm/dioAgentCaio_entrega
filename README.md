# DIO Agent — Mentor de Cibersegurança

Projeto de especialização do DIO Agent para atuar como mentor de cibersegurança, conduzindo uma análise defensiva de vulnerabilidade com foco em **SQL Injection (SQLi)**. A personalização do agente é feita por instruções, persona, base de conhecimento e skill em Markdown — não há treinamento ou fine-tuning de modelo.

## Objetivos

- Adaptar o DIO Agent para uma persona de mentor de segurança de aplicações.
- Ensinar uma metodologia profissional de análise: escopo, causa, evidência, impacto, correção e reteste.
- Demonstrar SQL Injection em um laboratório local e controlado.
- Corrigir a falha com consulta parametrizada.
- Registrar testes e evidências reais da execução.

## O que foi acrescentado ao repositório-base

| Arquivo | Finalidade |
|---|---|
| `AGENTS.md` | Instruções centrais, limites de segurança, método de análise e registro da skill |
| `agent/persona.md` | Identidade e comportamento do mentor de cibersegurança |
| `agent/knowledge/security-basics.md` | Base de conhecimento de segurança de aplicações e SQLi |
| `skills/vulnerability-analysis/SKILL.md` | Processo reutilizável para analisar, corrigir e validar vulnerabilidades |
| `lab/app.py` | Aplicação local com endpoint vulnerável e endpoint corrigido |
| `tests/test_sqli_lab.py` | Testes automatizados de autenticação e demonstração da correção |
| `lab/README.md` | Instruções para executar o laboratório |
| `evidences/README.md` | Roteiro para capturar evidências reais |

As skills originais e os materiais originais da DIO foram preservados.

## Requisitos

- Python 3.10 ou superior (recomendado).
- Hermes ou outro harness compatível com instruções de projeto.
- Nenhuma dependência externa; utiliza a biblioteca padrão do Python.

## Executar o laboratório

Na raiz do repositório:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Inicie o servidor (não há dependências externas):

```bash
python lab/app.py
```

Acesse `http://127.0.0.1:5000`. O servidor escuta somente no endereço de loopback (`127.0.0.1`).

**Credenciais fictícias do laboratório:** `aluno` / `dio123`.

### Demonstração controlada de SQL Injection

No formulário **Login vulnerável**, informe como usuário:

```text
' OR '1'='1' --
```

Deixe a senha vazia. No laboratório SQLite, o endpoint vulnerável deve aceitar a autenticação por causa da concatenação insegura.

Repita a mesma entrada no formulário **Login corrigido**. A consulta parametrizada deve tratar a entrada como dado e rejeitar a autenticação.

> Faça essa demonstração exclusivamente neste laboratório local. Não use a entrada em sites, sistemas de produção ou serviços de terceiros.

### Executar os testes automatizados

Com o ambiente virtual ativo:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam:
- autenticação com a conta fictícia válida;
- rejeição de senha incorreta;
- diferença de comportamento entre endpoint vulnerável e endpoint corrigido para a entrada de demonstração.

## Executar o agente no Hermes

1. Abra o Hermes conforme a instalação e a documentação oficial da ferramenta.
2. Abra/carregue o diretório raiz deste repositório como contexto de trabalho.
3. Confirme que o agente recebeu as instruções de `AGENTS.md`. Se o harness não carregar esse arquivo automaticamente, forneça-o explicitamente como instrução/contexto do projeto.
4. Peça ao agente para ler `agent/persona.md`, `agent/knowledge/security-basics.md` e `skills/vulnerability-analysis/SKILL.md`.
5. Use um prompt como:

```text
Atue como meu mentor de cibersegurança conforme as instruções deste repositório.
Leia a skill vulnerability-analysis e me conduza pela análise do laboratório local
de SQL Injection. Primeiro explique o escopo e a autorização; depois compare o
endpoint vulnerável com o endpoint parametrizado. Não invente resultados:
diferencie o que está documentado no código do que eu executar e observar.
```

A disponibilidade de leitura automática de arquivos e o mecanismo de carregamento de instruções dependem da versão/configuração do Hermes. Consulte a documentação do harness caso o diretório não seja reconhecido.

## Evidências

O roteiro de capturas está em [`evidences/README.md`](evidences/README.md). Inclua apenas prints feitos durante a execução real. Não há capturas simuladas neste repositório.

## Estrutura do projeto

```text
dio-agent_caio-main/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── agent/
│   ├── persona.md
│   └── knowledge/
│       ├── dio-platform.md
│       ├── learning-experiences.md
│       └── security-basics.md
├── docs/
├── lab/
│   ├── app.py
│   └── README.md
├── skills/
│   ├── vulnerability-analysis/
│   │   └── SKILL.md
│   └── [skills originais preservadas]
├── tests/
│   └── test_sqli_lab.py
├── evidences/
│   └── README.md
└── requirements.txt
```

## Limitações e observações de segurança

- O laboratório usa senhas fictícias em texto puro para manter o exemplo pequeno e demonstrar a SQLi. Isso **não** é adequado para autenticação real.
- O servidor é vinculado a `127.0.0.1`, não deve ser exposto à rede.
- O endpoint vulnerável é intencional e existe somente para fins didáticos.
- Os testes demonstram o comportamento deste laboratório; não constituem auditoria de uma aplicação externa nem certificação de segurança.
- Em produção, use hash de senha apropriado, consultas parametrizadas, privilégios mínimos, tratamento seguro de erros e revisão de segurança.

## Créditos

Baseado no repositório DIO Agent da Digital Innovation One, especializado neste fork para o desafio educacional de análise de vulnerabilidades.
