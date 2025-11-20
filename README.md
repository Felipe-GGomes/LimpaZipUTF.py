# 🧹 LimpaZipUTF - Organização, Limpeza e Automação de Arquivos Acadêmicos

## 🚀 Sobre o Projeto

**LimpaZipUTF** é uma ferramenta automatizada feita em Python com foco em estudantes e profissionais da UTFPR, resolvendo um problema comum: o acúmulo de arquivos didáticos, códigos, documentos e compactados misturados e desorganizados.

**Objetivo principal:**  
- Organizar rapidamente grandes diretórios de disciplinas acadêmicas
- Separar arquivos úteis por tipo e excluir lixo digital
- Descompactar arquivos automaticamente sem misturar projetos

---

## 🏗️ Funcionalidades do Projeto

- **Extração automática:** Move tudo útil das subpastas para a raiz
- **Descompactação inteligente:** Suporta `.zip`, `.rar`, `.7z`, mantendo tudo que foi extraído dentro da pasta especial `ZIPS`
- **Organização por tipos:** Cria pastas: `Documentos/`, `Código/`, `Texto/`, `Imagens/`, `ZIPS/`
- **Lixeira invisível:** Remove arquivos inúteis, cachês e arquivos do sistema automaticamente
- **Interação com usuário:** Pergunta antes de executar partes destrutivas
- **Modo simulação:** Preview total antes de executar mudanças reais

---

## 📝 Como Funciona

1. O usuário coloca o script na pasta principal.
2. Executa um comando único no PowerShell/CMD.
3. Segue prompts simples (`y/n`) para descompactação e organização.
4. O resultado: tudo organizado por tipo, cada ZIP descompactado fica separado em ZIPS – **sem misturar com o resto!**

---

## 💡 Ideias de Melhoria (TODO)

- [ ] **Integração com Google Drive/OneDrive:** Sincronizar pastas organizadas direto na nuvem
- [ ] **Interface gráfica (GUI):** Com botões para rodar organização/extração; exibir estatísticas visuais
- [ ] **Customização de extensões/pastas:** Usuário pode adicionar novas regras por um arquivo `.config`
- [ ] **Relatório pós-processamento:** Gerar PDF/HTML com estatísticas da limpeza/organização
- [ ] **Backup automático:** Antes de remover arquivos, criar backup ZIP rápido
- [ ] **Suporte a outros sistemas (Linux/Mac):** Adaptação automática para diferentes finais de linha e permissões
- [ ] **Logs detalhados:** Salvar tudo que foi movido/removido em um arquivo de histórico
- [ ] **Testes automatizados:** Scripts de teste garantindo que nenhum arquivo útil seja perdido

---

## 👨‍💻 Autor

**Felipe Gabriel Gomes**  
Estudante UTFPR Pato Branco  
Desenvolvido para ajudar colegas de Engenharia/ADS e profissionais da área

---

## 🤝 Como Contribuir

1. Dê uma estrela ⭐ no repositório!
2. Faça fork, crie seu branch: `git checkout -b minha-feature`
3. Commit suas melhorias e envie um pull request
4. Use a seção TODO para sugerir novas ideias/improvements

---

## 📜 Licença

MIT - Livre para uso e adaptação acadêmica ou profissional

---

## 🗣️ Contato & Suporte

- Issue Tracker no GitHub
- Email: felipeggomes80@gmail.com

---

**Última atualização: Novembro 2025**
