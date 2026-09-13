# LexWay Worksheets

Plataforma de **atividades interativas de inglês** da LexWay English, inspirada no LiveWorksheets.
Professores montam atividades por **turma e nível (CEFR A1–C2)**, os alunos resolvem online e recebem
**correção automática**, com **retakes** e **quadro de notas**.

🌐 Produção: <https://64-181-168-113.sslip.io>

---

## Funcionalidades

### Tipos de atividade
| Tipo | Como o aluno responde | Correção |
|---|---|---|
| Preencher lacunas | digita nas lacunas do texto | automática (aceita respostas alternativas; ignora maiúsculas e ponto final) |
| Dropdown | escolhe a opção em cada lacuna | automática |
| Múltipla escolha | marca uma alternativa | automática |
| Verdadeiro ou falso | True / False por afirmação | automática |
| Colocar na ordem | clica/arrasta blocos para montar a frase | automática (aceita ordens alternativas) |
| Ligar colunas | liga os itens com linhas coloridas | automática |
| Classificar em grupos | coloca palavras nas colunas certas | automática |
| Texto livre | escreve um texto | nota provisória por palavras‑chave + **revisão do professor** |

### Para o aluno
- Lista de atividades da sua turma (a fazer / já feitas), filtro por matéria.
- Resolução no navegador (desktop e celular), barra de progresso e aviso de questões em branco.
- Correção imediata com ✓/✗ por item; respostas certas mostradas conforme a regra da atividade.
- **Retakes** até o limite definido; nota final pela melhor, última ou média das tentativas.
- Página "Minhas notas" com média geral.

### Para professores e administração
- Editor visual de atividades (8 tipos), com pontuação, imagem, instruções, prazo, publicação e "Testar como aluno".
- Resultados por atividade, **liberar tentativa extra** para um aluno, corrigir texto livre com comentário.
- Quadro de notas por turma (0–10) com exportação **CSV**.
- Cadastro de alunos, turmas e professores (conforme o perfil — veja abaixo).
- **Recuperação de senha** por e‑mail e link de redefinição gerado pelo professor/admin.

## Perfis e permissões

| | Administrador | Professor(a) | Aluno(a) |
|---|:---:|:---:|:---:|
| Cadastrar/editar **turmas** | ✅ | — | — |
| Cadastrar **professores** e dar acesso às turmas | ✅ | — | — |
| Criar/editar **atividades** | ✅ todas | ✅ das suas turmas | — |
| Cadastrar/editar **alunos** | ✅ todos | ✅ das suas turmas | — |
| Ver resultados, corrigir, liberar retakes, notas | ✅ todas | ✅ das suas turmas | — |
| Gerar link de redefinição de senha | ✅ qualquer usuário | ✅ seus alunos | — |
| **Resolver atividades** e ver as próprias notas | — | — | ✅ |

Regras de escopo:
- Um professor só enxerga turmas às quais o administrador o vinculou (`class_teachers`).
- Atividade de professor precisa estar atribuída a pelo menos uma turma dele. Ao editar, vínculos com turmas
  de outros professores são preservados.
- Atividade **sem turma** (só o admin pode criar) fica disponível para todas as turmas do mesmo nível.

Usuários iniciais: `lexwayenglish` (administrador, lexway.english@gmail.com), `lisa` (professora da turma
"A1 — Turma da Lisa") e `felipe` (aluno dessa turma). As senhas **não** ficam no repositório.

## Recuperação de senha
1. Em **Entrar → Esqueci minha senha**, a pessoa informa usuário ou e‑mail.
2. Se a conta tiver e‑mail, recebe um link de uso único válido por **1 hora** (a resposta da tela é sempre a
   mesma, para não revelar quais contas existem; limite de 5 pedidos a cada 15 min por IP).
3. Alunos sem e‑mail: o professor clica em 🔑 na lista de alunos e envia o link gerado (válido por 72 h).
4. Ao redefinir ou trocar a senha, todas as outras sessões daquele usuário são encerradas.

O envio usa SMTP configurado por variáveis `WS_SMTP_*` (ver [.env.example](.env.example) e
[docs/infraestrutura.md](docs/infraestrutura.md#e-mail-smtp)).

## Rodando localmente

Requisitos: Python 3.10+.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

export WS_DB_PATH=./data/dev.db
.venv/bin/python -m app.seed --teacher-password lisa-dev-123 --student-password felipe-dev-123
.venv/bin/python -m app.manage create-admin --username admin --name "Admin" --password admin-dev-123
.venv/bin/uvicorn app.main:app --reload --port 8000
```

Abra <http://127.0.0.1:8000>. Sem `WS_SMTP_*`, os e‑mails não são enviados (fica registrado no log) —
use o link de redefinição gerado pelo painel.

### Comandos de administração (`app/manage.py`)
No servidor, use `sudo /opt/lisa-worksheets/deploy/manage.sh <comando>`.
```bash
python -m app.manage create-admin --username X --name "Nome" --email a@b.com   # pede a senha
python -m app.manage set-password --username X
python -m app.manage link-teacher --username lisa --class-name "A1 — Turma da Lisa"
python -m app.manage test-email --to alguem@exemplo.com
```

## Estrutura do projeto
```
app/
  main.py          rotas (login, recuperação de senha, admin, professor, aluno) e regras de acesso
  grading.py       tipos de questão: validação, visão do aluno (sem gabarito) e correção
  db.py            SQLite: esquema e migrações
  auth.py          hash de senha (PBKDF2-SHA256)
  mailer.py        envio de e-mail via SMTP
  manage.py        CLI de administração
  seed.py          dados de exemplo (turma A1, Lisa, Felipe, atividades "Verb To Be" e "Countries")
  templates/       páginas Jinja2 (admin/, teacher/, student/)
  static/          style.css (identidade LexWay), player.js (resolver), builder.js (editor), img/
deploy/
  deploy.sh        publica a versão local no servidor
  manage.sh        roda app.manage no servidor com as variáveis de produção
  backup.sh        backup diário do banco
  lisa-worksheets.service, Caddyfile
docs/
  infraestrutura.md   servidor, rede, HTTPS, serviços, deploy, backup, e-mail
  aplicacoes.md       stack, arquitetura, modelo de dados e formato das atividades
```

## Documentação
- [Infraestrutura](docs/infraestrutura.md)
- [Aplicações e arquitetura](docs/aplicacoes.md)
