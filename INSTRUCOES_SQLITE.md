# Sistema de Notas - Versão SQLite (SIMPLIFICADA)

## 🎯 SOLUÇÃO PARA O ERRO DE CONEXÃO

Se você recebeu o erro "✗ Não foi possível conectar ao banco de dados", use esta versão simplificada que **NÃO PRECISA** de PostgreSQL instalado!

## ✨ Vantagens desta versão

- ✅ **Não precisa instalar PostgreSQL**
- ✅ **Não precisa configurar usuário/senha**
- ✅ **Banco de dados em arquivo** (sistema_notas.db)
- ✅ **Funciona imediatamente**
- ✅ **Todas as funcionalidades do sistema original**

## 🚀 Como Usar

### 1. Executar o programa:
```bash
python app_sqlite.py
```

**É só isso!** O programa vai:
- Criar automaticamente o arquivo `sistema_notas.db`
- Criar todas as tabelas necessárias
- Estar pronto para uso

### 2. Inserir dados de exemplo (opcional):
No menu, escolha a opção **14** para inserir dados de exemplo automaticamente.

## 📱 Funcionalidades

Todas as 14 funcionalidades do sistema original:

1. **Adicionar Aluno** - Cadastra novo aluno
2. **Listar Alunos** - Mostra todos os alunos
3. **Adicionar Disciplina** - Cadastra disciplina
4. **Listar Disciplinas** - Mostra todas as disciplinas
5. **Adicionar Notas** - Registra 3 notas
6. **Atualizar Notas** - Modifica notas existentes
7. **Ver Situação de um Aluno** - Notas e situação individual
8. **Ver Situação de Todos** - Notas e situação geral
9. **Ver Resumo de um Aluno** - Estatísticas individuais
10. **Ver Resumo de Todos** - Estatísticas gerais
11. **Listar Aprovados** - Alunos aprovados
12. **Listar Reprovados** - Alunos reprovados
13. **Estatísticas do Semestre** - Dados gerais
14. **Inserir Dados de Exemplo** - Popula o banco automaticamente
0. **Sair** - Encerra o programa

## 💡 Exemplo de Uso Rápido

```bash
# 1. Execute o programa
python app_sqlite.py

# 2. No menu, digite 14 e pressione ENTER
# Isso vai inserir dados de exemplo

# 3. Depois digite 8 e pressione ENTER
# Isso vai mostrar a situação de todos os alunos

# 4. Digite 13 e pressione ENTER
# Digite: 2024.1
# Isso vai mostrar as estatísticas do semestre
```

## 📊 Dados de Exemplo

Ao escolher a opção 14, o sistema insere:

**5 Alunos:**
- João Silva (2024001)
- Maria Santos (2024002)
- Pedro Oliveira (2024003)
- Ana Costa (2024004)
- Carlos Souza (2024005)

**5 Disciplinas:**
- Matemática I (MAT101)
- Física I (FIS101)
- Português (POR101)
- História (HIS101)
- Química I (QUI101)

**Notas variadas** para demonstrar aprovações e reprovações

## 🔧 Diferenças do PostgreSQL

| Característica | PostgreSQL | SQLite |
|---------------|------------|--------|
| Instalação | Necessária | Não necessária |
| Configuração | Usuário/senha | Nenhuma |
| Arquivo | Servidor | Arquivo .db |
| Complexidade | Alta | Baixa |
| Ideal para | Produção | Desenvolvimento/Estudo |

## 📝 Arquivo do Banco de Dados

O arquivo `sistema_notas.db` será criado automaticamente na mesma pasta do programa. Você pode:

- **Copiar** o arquivo para backup
- **Deletar** o arquivo para começar do zero
- **Compartilhar** o arquivo com outras pessoas

## ⚠️ Observações

- Todas as notas devem estar entre 0 e 10
- Média de aprovação: 7.0
- Cálculo: (nota1 + nota2 + nota3) / 3
- Matrícula e código de disciplina devem ser únicos

## 🆚 Quando usar cada versão?

**Use app_sqlite.py (esta versão) se:**
- Você está aprendendo/testando
- Não quer instalar PostgreSQL
- Quer algo simples e rápido
- É para uso pessoal ou pequeno

**Use app.py (PostgreSQL) se:**
- É para produção/empresa
- Precisa de múltiplos usuários simultâneos
- Precisa de recursos avançados
- Tem PostgreSQL instalado

## 🎓 Conclusão

Esta versão SQLite é **perfeita para aprender e testar** o sistema de notas sem complicações de instalação e configuração!

**Basta executar:**
```bash
python app_sqlite.py
```

E começar a usar! 🚀