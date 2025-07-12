# IMAPsync Migrator para Webmin/Virtualmin

Um módulo simples e eficaz para Webmin/Virtualmin que migra contas de e-mail entre servidores IMAP usando o poder do `imapsync`. Ele fornece uma interface limpa dentro do Webmin e um visualizador de log em tempo real para monitorar o processo de migração.

## ✨ Funcionalidades

- **🖥️ Interface Amigável:** Formulário limpo e intuitivo para configurar detalhes dos servidores de origem e destino
- **📊 Monitoramento em Tempo Real:** Visualizador de log ao vivo que atualiza automaticamente a cada 2 segundos, mostrando a saída do `imapsync` em tempo real
- **🔒 Tratamento Seguro de Senhas:** Senhas são armazenadas em arquivos temporários com permissões seguras e automaticamente deletadas após a migração
- **🎛️ Opções Avançadas:** Suporte para conexões SSL/TLS, filtros de pastas, restrições de tamanho/idade e relatórios por e-mail
- **🐛 Modo Debug:** Ferramentas de depuração integradas para solucionar problemas de migração
- **🌐 Suporte Multi-idioma:** Disponível em Inglês e Português
- **⚡ Autocontido:** Robusto e independente de configurações específicas de tema do Webmin

## 📋 Pré-requisitos

Antes de instalar este módulo, você **deve** ter o `imapsync` instalado no seu servidor.

### Instalando o imapsync

**Para Debian/Ubuntu:**

```bash
sudo apt-get update && sudo apt-get install imapsync
```

**Para Red Hat/CentOS:**

```bash
sudo yum install epel-release && sudo yum install imapsync
```

**Para outras distribuições:**
Verifique seu gerenciador de pacotes ou instale a partir do [código fonte](https://github.com/imapsync/imapsync).

## 🚀 Instalação

### Instalação Rápida (Recomendado)

1. Vá para a [página de Releases](https://github.com/wmolinjr/imap-migrator/releases) deste repositório
2. Baixe o arquivo `imap-migrator.wbm.gz` mais recente
3. No Webmin, navegue para **Webmin → Configuração do Webmin → Módulos do Webmin**
4. Selecione **De arquivo local** ou **De arquivo enviado**
5. Escolha o arquivo `imap-migrator.wbm.gz` que você baixou
6. Clique em **Instalar Módulo**

O módulo estará disponível na categoria **Ferramentas** no menu lateral.

### Instalação Manual

1. Baixe os arquivos do módulo
2. Extraia para `/usr/share/webmin/imap-migrator/`
3. Configure as permissões adequadas: `chmod 755 /usr/share/webmin/imap-migrator/`
4. Reinicie o Webmin

## 🛠️ Uso

### Migração Básica

1. Navegue para **Ferramentas → IMAP Migrator** no Webmin
2. Preencha os detalhes do servidor de origem:
   - **Servidor IMAP:** Endereço do seu servidor de origem
   - **Usuário:** Nome de usuário da conta de e-mail
   - **Senha:** Senha da conta de e-mail
   - **Segurança:** Escolha SSL/TLS se necessário
3. Preencha os detalhes do servidor de destino (mesmos campos)
4. Clique em **Iniciar Migração**
5. Monitore o log em tempo real para acompanhar o progresso

### Opções Avançadas

O módulo inclui várias funcionalidades avançadas acessíveis através de abas:

- **Credenciais:** Configuração básica do servidor
- **Avançado:** Limites de tamanho, filtros de idade, inclusão/exclusão de pastas, relatórios por e-mail
- **Depurar:** Opções de depuração e ferramentas de teste em tempo real

## 🔧 Para Desenvolvedores

### Compilando a partir do Código Fonte

Se você quiser modificar o módulo ou compilar o pacote a partir do código fonte:

1. Clone este repositório:

   ```bash
   git clone https://github.com/wmolinjr/imap-migrator.git
   cd imap-migrator
   ```

2. Execute o script de compilação:

   ```bash
   ./build.sh
   ```

3. O pacote `imap-migrator.wbm.gz` será criado no diretório raiz

### Configuração de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/wmolinjr/imap-migrator.git
cd imap-migrator

# Torne o script de compilação executável
chmod +x build.sh

# Compile o módulo
./build.sh
```

## 📁 Estrutura do Projeto

```
imap-migrator/
├── index.cgi              # Interface principal
├── migrate.cgi            # Execução da migração
├── status.cgi             # Status do log em tempo real
├── imap-migrator.js       # JavaScript frontend
├── imap-migrator-lib.pl   # Biblioteca backend
├── lang/                   # Arquivos de tradução
│   ├── en                 # Traduções em inglês
│   └── pt                 # Traduções em português
├── help/                   # Documentação de ajuda
└── build.sh               # Script de compilação
```

## 🐛 Solução de Problemas

### Problemas Comuns

**Módulo não aparece no Webmin:**

- Verifique as permissões adequadas dos arquivos
- Verifique os logs de erro do Webmin
- Confirme o caminho de instalação do módulo

**imapsync não encontrado:**

- Instale o pacote imapsync para sua distribuição
- Verifique se imapsync está no PATH: `which imapsync`

**Migração falha:**

- Verifique a conectividade do servidor
- Confirme as credenciais
- Revise os logs em tempo real para erros específicos
- Ative o modo debug para informações detalhadas

### Modo Debug

Ative o modo debug na aba **Depurar** para acessar:

- Ferramentas de teste em tempo real
- Logs detalhados do console
- Testes de conectividade do servidor
- Verificação de arquivos de log

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request. Para mudanças importantes, abra uma issue primeiro para discutir o que você gostaria de alterar.

### Como Contribuir

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Faça commit das suas mudanças (`git commit -m 'Adiciona alguma NovaFuncionalidade'`)
4. Faça push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💖 Apoie o Projeto

Se este projeto te ajudou, considere apoiar:

- 💸 [GitHub Sponsors](https://github.com/sponsors/wmolinjr)
- ☕ [Buy Me a Coffee](https://www.buymeacoffee.com/wmolinjr)
- 📢 Compartilhe com amigos e colegas!

Toda ajuda é bem-vinda para manter o projeto vivo 🚀

## 🙏 Agradecimentos

- [imapsync](https://github.com/imapsync/imapsync) - A ferramenta poderosa que torna tudo isso possível
- [Webmin](https://webmin.com/) - A excelente ferramenta de administração de sistema baseada na web
- Todos os contribuidores e usuários que ajudam a melhorar este módulo

---

**Feito com ❤️ para a comunidade Webmin**
