# Infraestrutura

## Visão geral

```mermaid
flowchart LR
    U[Navegador<br/>alunos e professores] -- HTTPS 443 --> SL
    subgraph OCI["Oracle Cloud · sa-saopaulo-1"]
      SL[Security List da VCN<br/>entrada: 22, 80, 443] --> VM
      subgraph VM["VM Rocky Linux 9.6 · instance-20260822-2224"]
        C[Caddy 2.11<br/>:80 → redireciona<br/>:443 TLS Let's Encrypt] -- proxy --> A[uvicorn + FastAPI<br/>127.0.0.1:8000<br/>systemd: lisa-worksheets]
        A --> D[(SQLite<br/>/opt/lisa-worksheets/data)]
      end
    end
    A -. SMTP 587 .-> G[Gmail<br/>lexway.english@gmail.com]
    LE[Let's Encrypt] -. desafio ACME .-> C
```

| Item | Valor |
|---|---|
| Provedor | Oracle Cloud Infrastructure (OCI), região **São Paulo** (`sa-saopaulo-1`) |
| Instância | `instance-20260822-2224` (hostname `vniclisa`) |
| IP público | `64.181.168.113` |
| Endereço da aplicação | <https://64-181-168-113.sslip.io> |
| Sistema operacional | Rocky Linux 9.6 (Blue Onyx), kernel 5.14, x86_64, SELinux **enforcing** |
| Recursos | 2 vCPU, ~764 MB de RAM + 4 GB de swap, disco de 46 GB |
| Acesso SSH | usuário `rocky`, chave `ssh-key-2026-08-23.key` (alias local `oracle-lisa`) |

### Por que essa arquitetura
- A VM tem pouca memória (764 MB). Um único processo Python com SQLite usa ~60–80 MB e não exige um
  servidor de banco de dados separado nem Docker.
- O Caddy emite e renova o certificado HTTPS sozinho e é um único binário.
- O volume esperado (uma escola, dezenas/centenas de alunos) cabe com folga no SQLite em modo WAL.

## Rede e domínio

- **Domínio**: ainda não há domínio próprio. Usamos o [sslip.io](https://sslip.io), um DNS público que
  resolve `64-181-168-113.sslip.io` para `64.181.168.113`. Isso permite ter certificado válido do
  Let's Encrypt sem comprar domínio.
- **Firewall da OCI** (Security List da sub‑rede): regras de entrada TCP de `0.0.0.0/0` nas portas
  **22** (SSH), **80** (HTTP, necessário para o desafio ACME e o redirecionamento) e **443** (HTTPS).
- **Firewall da VM**: `firewalld` não está ativo; o controle é feito na Security List.
- A aplicação escuta **somente em 127.0.0.1:8000**; nada além do Caddy fica exposto.

### Trocar para um domínio próprio (ex.: `atividades.lexwayenglish.com`)
1. No DNS do domínio, crie um registro **A** `atividades` → `64.181.168.113`.
2. No servidor, edite `/etc/caddy/Caddyfile` trocando `64-181-168-113.sslip.io` pelo novo nome (e o destino do
   redirecionamento) e rode `sudo systemctl reload caddy`.
3. Atualize `WS_BASE_URL` em `/etc/lisa-worksheets.env` e `sudo systemctl restart lisa-worksheets`
   (é o endereço usado nos links de redefinição de senha).

## Serviços

### Caddy (proxy reverso + HTTPS)
- Instalado pelo repositório COPR oficial `@caddy/caddy` (`dnf install caddy`), serviço `caddy.service`.
- Configuração: [`deploy/Caddyfile`](../deploy/Caddyfile) → `/etc/caddy/Caddyfile`.
- Certificados e conta ACME em `/var/lib/caddy/.local/share/caddy/` (renovação automática).
- SELinux: `setsebool -P httpd_can_network_connect 1` para permitir o proxy até a porta 8000.
- Se o certificado falhar (ex.: porta 80/443 fechada), o Caddy tenta de novo com espera crescente.
  Depois de corrigir a rede: `sudo systemctl restart caddy`.

### Aplicação (`lisa-worksheets.service`)
- Código em `/opt/lisa-worksheets`, dono: usuário de sistema **`worksheets`** (sem shell).
- Python **3.11** (pacote `python3.11` do AppStream) em virtualenv `/opt/lisa-worksheets/.venv`.
- Unidade systemd: [`deploy/lisa-worksheets.service`](../deploy/lisa-worksheets.service), com hardening
  (`ProtectSystem=strict`, `ProtectHome`, `NoNewPrivileges`, `PrivateTmp`, escrita só em `data/`) e
  `MemoryMax=300M`. Reinicia sozinha em caso de falha.
- Variáveis de ambiente em **`/etc/lisa-worksheets.env`** (permissão 600, fora do repositório; valores com espaço entre aspas). Modelo em
  [`.env.example`](../.env.example).

| Variável | Uso |
|---|---|
| `WS_SECRET_KEY` | assina o cookie de sessão (gerada aleatoriamente na instalação) |
| `WS_HTTPS` | `1` = cookie só via HTTPS |
| `WS_DB_PATH` | caminho do banco SQLite |
| `WS_TZ` | fuso para exibir datas (`America/Sao_Paulo`) |
| `WS_BASE_URL` | URL pública usada nos e-mails |
| `WS_SCHOOL_EMAIL` | e-mail de contato exibido no rodapé |
| `WS_SMTP_HOST/PORT/USER/PASSWORD/FROM` | envio de e-mail (recuperação de senha) |

### E-mail (SMTP)
A recuperação de senha envia e-mails pela conta **lexway.english@gmail.com**. O Gmail não aceita a senha
normal da conta via SMTP; é preciso uma **senha de app**:

1. Na conta Google, ative a **Verificação em duas etapas**.
2. Acesse <https://myaccount.google.com/apppasswords>, crie uma senha de app (ex.: "LexWay Worksheets").
3. No servidor, preencha em `/etc/lisa-worksheets.env`:
   ```
   WS_SMTP_HOST=smtp.gmail.com
   WS_SMTP_PORT=587
   WS_SMTP_USER=lexway.english@gmail.com
   WS_SMTP_PASSWORD=<senha de app de 16 letras>
   WS_SMTP_FROM="LexWay English <lexway.english@gmail.com>"
   ```
4. `sudo systemctl restart lisa-worksheets` e teste:
   `sudo /opt/lisa-worksheets/deploy/manage.sh test-email --to seu@email.com`

Enquanto o SMTP não estiver configurado, o sistema continua funcionando: o professor/admin gera o link de
redefinição pelo painel (botão 🔑) e envia por WhatsApp.

## Banco de dados e backup
- Arquivo: `/opt/lisa-worksheets/data/worksheets.db` (SQLite 3.34, modo WAL). As migrações rodam
  automaticamente na inicialização (`app/db.py`).
- **Backup diário** às 03:15 via `/etc/cron.d/lisa-worksheets-backup` → [`deploy/backup.sh`](../deploy/backup.sh),
  usando a API de backup online do SQLite (cópia consistente com o app rodando). Mantém 14 dias em
  `/opt/lisa-worksheets/data/backups/`. O deploy também faz um backup antes de atualizar.
- Os backups ficam no mesmo disco. Para proteção contra perda da VM, copie periodicamente para fora, ex.:
  `scp oracle-lisa:/opt/lisa-worksheets/data/backups/worksheets-AAAAMMDD-HHMM.db .`
- Restaurar: `sudo systemctl stop lisa-worksheets`, copiar o backup sobre `worksheets.db` (dono `worksheets`),
  remover `worksheets.db-wal`/`-shm` e `sudo systemctl start lisa-worksheets`.

## Deploy

A partir de uma máquina com acesso SSH (`oracle-lisa` no `~/.ssh/config`):

```bash
./deploy/deploy.sh            # empacota app/, envia, faz backup, instala dependências e reinicia
```

### Instalação do zero (referência)
```bash
sudo dnf -y install python3.11 python3.11-pip tar 'dnf-command(copr)'
sudo dnf -y copr enable @caddy/caddy && sudo dnf -y install caddy
sudo useradd --system --home-dir /opt/lisa-worksheets --shell /sbin/nologin worksheets
sudo mkdir -p /opt/lisa-worksheets/data && sudo tar xzf app.tgz -C /opt/lisa-worksheets
sudo python3.11 -m venv /opt/lisa-worksheets/.venv
sudo /opt/lisa-worksheets/.venv/bin/pip install -r /opt/lisa-worksheets/requirements.txt
sudo chown -R worksheets:worksheets /opt/lisa-worksheets
sudo cp .env.example /etc/lisa-worksheets.env && sudo chmod 600 /etc/lisa-worksheets.env   # editar valores
sudo cp deploy/lisa-worksheets.service /etc/systemd/system/ && sudo systemctl enable --now lisa-worksheets
sudo cp deploy/Caddyfile /etc/caddy/Caddyfile && sudo setsebool -P httpd_can_network_connect 1
sudo systemctl enable --now caddy
echo '15 3 * * * worksheets /opt/lisa-worksheets/deploy/backup.sh' | sudo tee /etc/cron.d/lisa-worksheets-backup
# criar o administrador (pede a senha):
sudo /opt/lisa-worksheets/deploy/manage.sh create-admin --username lexwayenglish --name "LexWay English" --email lexway.english@gmail.com
```

## Operação

| Tarefa | Comando |
|---|---|
| Status | `systemctl status lisa-worksheets caddy` |
| Logs da aplicação (inclui envio de e-mail) | `sudo journalctl -u lisa-worksheets -f` |
| Logs do Caddy / certificado | `sudo journalctl -u caddy -f` |
| Reiniciar app | `sudo systemctl restart lisa-worksheets` |
| Recarregar Caddy | `sudo systemctl reload caddy` |
| Trocar senha de alguém pelo terminal | `sudo /opt/lisa-worksheets/deploy/manage.sh set-password --username X` |
| Uso de memória | `systemctl status lisa-worksheets \| grep Memory` |

## Segurança
- HTTPS obrigatório (HSTS) e cookie de sessão `Secure`, `HttpOnly`, `SameSite=Lax`, assinado.
- Proteção CSRF por verificação de `Origin`/`Referer` em requisições que alteram dados.
- Senhas com PBKDF2‑SHA256 (150 mil iterações, salt individual). Trocar/redefinir a senha encerra as
  outras sessões.
- Limite de tentativas de login (10 a cada 10 min por IP) e de pedidos de recuperação (5 a cada 15 min).
- Tokens de redefinição aleatórios, guardados apenas como hash SHA‑256, uso único e com validade.
- O gabarito nunca é enviado ao navegador do aluno; a correção acontece no servidor.
- Cabeçalhos `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`.
- Segredos (`/etc/lisa-worksheets.env`, banco, senhas) ficam fora do Git.
