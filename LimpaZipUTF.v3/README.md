# 🧹 LimpaZipUTF - Organizador de Arquivos UTFPR

Um script Python que **extrai, descompacta e organiza** automaticamente arquivos de disciplinas da UTFPR, separando por tipo e limpando lixo digital.

## 📋 O Que o Script Faz

### 1️⃣ **Extrai Arquivos de Subpastas**
- Move arquivos úteis de pastas profundas para Sa raiz
- Remove arquivos inúteis (cache, logs, configurações do sistema)
- Deleta pastas vazias automaticamente

### 2️⃣ **Descompacta Arquivos Compactados**
- Suporta: `.zip`, `.rar`, `.7z`
- Cria pasta **ZIPS** separada para não bagunçar projetos
- Cada arquivo descompactado fica em `ZIPS/arquivo_quak/`

### 3️⃣ **Organiza por Tipo**
- 📁 **Documentos/** → PDFs, DOCs, PPTs, XLSs
- 💻 **Código/** → Java, Python, C++, JS, SQL, etc
- 📝 **Texto/** → TXTs, MDs, CSVs
- 🖼️ **Imagens/** → PNGs, JPGs, SVGs, GIFs
- 📦 **ZIPS/** → Arquivos compactados + descompactados

---

## 🚀 Como Usar

### **Pré-Requisitos**

1. **Python 3.7+** instalado
2. Para descompactar `.RAR` e `.7Z`, instale:
   - **7-Zip** (recomendado, grátis): https://www.7-zip.org/
   - Ou **WinRAR**: https://www.winrar.com/

### **Instalação**

1. Baixe o arquivo `LimpaZipUTF.py`
2. Coloque na **mesma pasta** que você quer organizar
3. Abra **PowerShell** ou **CMD** nessa pasta

### **Passo a Passo**

#### **1. Simulação (Ver o Que Vai Acontecer)**

```bash
python LimpaZipUTF.py "C:\Caminho\Da\Pasta"
```

Isso mostra tudo que SERIA feito, sem modificar nada.

#### **2. Executar de Verdade**

```bash
python LimpaZipUTF.py "C:\Caminho\Da\Pasta" --executar
```

O script vai:
- ✅ Extrair e limpar
- ❓ Pergunta: `[y/n] Descompactar todos?`
  - Digite `y` (yes) para descompactar
  - Digite `n` (no) para pular
- ❓ Pergunta: `[y/n] Organizar arquivos por extensão?`
  - Digite `y` para organizar em pastas
  - Digite `n` para deixar na raiz

#### **3. Exemplo Real (Seu Comando)**

```bash
python LimpaZipUTF.py "C:\Users\Felipe\Desktop\OO42S_1763606059\Curso_Fundamentos_de_Orientao..._.985224" --executar
```

Pronto! O script vai rodar.

---

## 📊 Exemplo de Resultado

**Antes:**
```
📁 Pasta Disciplina
├── 📂 Aula 1
│   ├── Slide.pptx
│   └── Código.java
├── 📂 Aula 2
│   ├── aula.pdf
│   └── projeto.zip
└── 📂 Cache
    └── thumbs.db
```

**Depois:**
```
📁 Pasta Disciplina
├── 📁 Documentos/
│   ├── Slide.pptx
│   └── aula.pdf
├── 📁 Código/
│   └── Código.java
├── 📁 ZIPS/
│   ├── projeto.zip
│   └── 📁 projeto_quak/
│       └── (conteúdo descompactado)
└── LimpaZipUTF.py
```

---

## 🎯 Todos os Comandos

| Comando | O Que Faz |
|---------|----------|
| `python LimpaZipUTF.py "caminho"` | Modo **simulação** (preview) |
| `python LimpaZipUTF.py "caminho" --executar` | **Executa** as mudanças |
| `python LimpaZipUTF.py "caminho" --silencioso` | Menos detalhes na tela |
| `python LimpaZipUTF.py "caminho" --extensoes` | Lista extensões permitidas |

### **Combinações**
```bash
# Simulação com poucos detalhes
python LimpaZipUTF.py "caminho" --silencioso

# Executa sem muita informação
python LimpaZipUTF.py "caminho" --executar --silencioso

# Ver apenas as extensões suportadas
python LimpaZipUTF.py "caminho" --extensoes
```

---

## 📝 O Que É Mantido e Removido

### ✅ Extensões Mantidas

**Documentos:** `.pdf`, `.doc`, `.docx`, `.ppt`, `.pptx`, `.xls`, `.xlsx`

**Código:** `.java`, `.py`, `.c`, `.cpp`, `.h`, `.hpp`, `.js`, `.html`, `.css`, `.sql`, `.class`, `.jar`

**Texto:** `.txt`, `.md`, `.csv`

**Imagens:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`

**Compactados:** `.zip`, `.rar`, `.7z`

### ❌ Arquivos Removidos (Lixo)

- `index.html`, `index.htm`, `index.php`
- `thumbs.db` (cache Windows)
- `.ds_store` (cache macOS)
- `desktop.ini` (config Windows)
- `comet_html_doc.xml` (lixo de sites)

---

## ⚙️ Explicação Detalhada dos Passos

### **PASSO 1: Extração e Limpeza**
```
[EXECUÇÃO] Processando: C:\Users\Felipe\Desktop\...
📤 MOVENDO: Aula 1/Slide.pptx → Slide.pptx
📤 MOVENDO: Aula 2/Código.java → Código.java
🗑️  REMOVENDO: Cache/thumbs.db (0.15 MB)
📁 PASTA VAZIA REMOVIDA: Aula 1
```

### **PASSO 2: Descompactação**
```
📦 Encontrados 1 arquivo(s) compactado(s):
  • projeto.zip

[y/n] Descompactar todos? y

📦 Descompactando: projeto.zip
📁 Criando pasta: ZIPS/projeto_quak/
✅ ZIP descompactado com sucesso!
📦 Arquivo compactado movido para: ZIPS/projeto.zip

✅ Descompactados: 1
📦 Compactados movidos para ZIPS: 1
```

### **PASSO 3: Organização por Extensão**
```
[y/n] Organizar arquivos por extensão? y

📊 PREVIEW - Arquivos por categoria:
  📁 Documentos: 2 arquivo(s)
  📁 Código: 1 arquivo(s)

📂 MOVENDO: Slide.pptx → Documentos/
📂 MOVENDO: aula.pdf → Documentos/
📂 MOVENDO: Código.java → Código/

✅ Arquivos organizados: 3
📁 Pastas criadas: 2
```

---

## 🆘 Troubleshooting

### **Problema: "Arquivo não encontrado"**
- ❌ Verifique se o caminho está correto
- ✅ Use aspas: `"C:\Caminho Com Espaços"`

### **Problema: Não descompacta .RAR**
- ❌ Você não tem 7-Zip ou WinRAR instalado
- ✅ Instale: https://www.7-zip.org/ (grátis)

### **Problema: "Permission denied"**
- ❌ Pasta ou arquivo em uso por outro programa
- ✅ Feche programas usando os arquivos e tente novamente

### **Problema: Script não roda**
- ❌ Python não está no PATH
- ✅ Use caminho completo: `C:\Python312\python.exe LimpaZipUTF.py ...`

---

## 💡 Dicas Práticas

1. **Sempre comece com simulação:**
   ```bash
   python LimpaZipUTF.py "caminho"
   ```
   Veja o que vai mudar antes de clicar em `y`.

2. **Responda `n` na primeira vez:**
   ```
   [y/n] Descompactar todos? n
   [y/n] Organizar por extensão? n
   ```
   Assim você vê se limpou bem antes de reorganizar.

3. **Organize uma disciplina por vez:**
   Não tente com a pasta INTEIRA do semestre, faça por disciplina.

4. **Backup é sempre bom:**
   Faça uma cópia antes de executar pela primeira vez.

---

## 📦 Estrutura do ZIPS

Cada arquivo descompactado fica separado:

```
📁 ZIPS/
├── projeto.zip          ← Original
├── 📁 projeto_quak/     ← Conteúdo descompactado
│   ├── src/
│   ├── bin/
│   └── README.md
├── aula.rar            ← Original
└── 📁 aula_quak/       ← Conteúdo descompactado
    ├── slides.pptx
    └── exercicios.pdf
```

Assim seus projetos Java não se misturam com o resto! 🎯

---

## 🐛 Relatório de Erros

Se algo der errado, o script mostra:

```
⚠️  Erros encontrados:
  • arquivo.zip: Falha na descompactação
  • pasta/documento.pdf: Permission denied
```

Copie a mensagem de erro e tente resolver.

---

## 👨‍💻 Autor

**Felipe Gabriel Gomes**
- Estudante ADS - UTFPR Pato Branco
- Engenharia de Software - Uni Guairaca
- Estagiário SAG Software Agroindustriais

---

## 📜 Licença

Use livremente! ⭐ Se gostou, dá uma estrelinha no repositório!

---

## 📞 Suporte

Se tiver dúvidas:
1. Leia este README
2. Rode em modo **simulação** primeiro
3. Verifique o exemplo na seção "Todos os Comandos"
4. Se ainda não funcionar, procure por erros na seção "Troubleshooting"

---

**Última atualização:** Novembro 2025
**Versão:** 1.0
**Python:** 3.7+
