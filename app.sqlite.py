#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Gerenciamento de Notas de Alunos - Versão SQLite
Aplicação Python para gerenciar notas sem necessidade de PostgreSQL
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
import os


class SistemaNotas:
    """Classe principal para gerenciar o sistema de notas com SQLite"""
    
    def __init__(self, db_file='sistema_notas.db'):
        """
        Inicializa a conexão com o banco de dados SQLite
        
        Args:
            db_file: Nome do arquivo do banco de dados
        """
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            self._criar_tabelas()
            print(f"✓ Conexão com banco de dados '{db_file}' estabelecida com sucesso!")
        except Exception as e:
            print(f"✗ Erro ao conectar ao banco de dados: {e}")
            raise
    
    def _criar_tabelas(self):
        """Cria as tabelas se não existirem"""
        # Tabela de Alunos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de Disciplinas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                carga_horaria INTEGER NOT NULL
            )
        """)
        
        # Tabela de Notas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER NOT NULL,
                disciplina_id INTEGER NOT NULL,
                nota1 REAL CHECK (nota1 >= 0 AND nota1 <= 10),
                nota2 REAL CHECK (nota2 >= 0 AND nota2 <= 10),
                nota3 REAL CHECK (nota3 >= 0 AND nota3 <= 10),
                semestre TEXT NOT NULL,
                FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE,
                UNIQUE(aluno_id, disciplina_id, semestre)
            )
        """)
        
        self.conn.commit()
    
    def __del__(self):
        """Fecha a conexão ao destruir o objeto"""
        if hasattr(self, 'conn'):
            self.conn.close()
    
    # ==================== ALUNOS ====================
    
    def adicionar_aluno(self, matricula: str, nome: str) -> bool:
        """Adiciona um novo aluno"""
        try:
            self.cursor.execute(
                "INSERT INTO alunos (matricula, nome) VALUES (?, ?)",
                (matricula, nome)
            )
            self.conn.commit()
            print(f"✓ Aluno {nome} (matrícula {matricula}) adicionado com sucesso!")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Erro: Matrícula {matricula} já existe!")
            return False
        except Exception as e:
            print(f"✗ Erro ao adicionar aluno: {e}")
            return False
    
    def listar_alunos(self) -> List[Dict]:
        """Lista todos os alunos cadastrados"""
        try:
            self.cursor.execute(
                "SELECT id, matricula, nome, data_cadastro FROM alunos ORDER BY nome"
            )
            alunos = []
            for row in self.cursor.fetchall():
                alunos.append({
                    'id': row[0],
                    'matricula': row[1],
                    'nome': row[2],
                    'data_cadastro': row[3]
                })
            return alunos
        except Exception as e:
            print(f"✗ Erro ao listar alunos: {e}")
            return []
    
    def buscar_aluno(self, matricula: str) -> Optional[Dict]:
        """Busca um aluno pela matrícula"""
        try:
            self.cursor.execute(
                "SELECT id, matricula, nome, data_cadastro FROM alunos WHERE matricula = ?",
                (matricula,)
            )
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'matricula': row[1],
                    'nome': row[2],
                    'data_cadastro': row[3]
                }
            return None
        except Exception as e:
            print(f"✗ Erro ao buscar aluno: {e}")
            return None
    
    # ==================== DISCIPLINAS ====================
    
    def adicionar_disciplina(self, codigo: str, nome: str, carga_horaria: int) -> bool:
        """Adiciona uma nova disciplina"""
        try:
            self.cursor.execute(
                "INSERT INTO disciplinas (codigo, nome, carga_horaria) VALUES (?, ?, ?)",
                (codigo, nome, carga_horaria)
            )
            self.conn.commit()
            print(f"✓ Disciplina {nome} ({codigo}) adicionada com sucesso!")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Erro: Código {codigo} já existe!")
            return False
        except Exception as e:
            print(f"✗ Erro ao adicionar disciplina: {e}")
            return False
    
    def listar_disciplinas(self) -> List[Dict]:
        """Lista todas as disciplinas cadastradas"""
        try:
            self.cursor.execute(
                "SELECT id, codigo, nome, carga_horaria FROM disciplinas ORDER BY nome"
            )
            disciplinas = []
            for row in self.cursor.fetchall():
                disciplinas.append({
                    'id': row[0],
                    'codigo': row[1],
                    'nome': row[2],
                    'carga_horaria': row[3]
                })
            return disciplinas
        except Exception as e:
            print(f"✗ Erro ao listar disciplinas: {e}")
            return []
    
    # ==================== NOTAS ====================
    
    def adicionar_notas(self, matricula: str, codigo_disciplina: str, 
                       nota1: float, nota2: float, nota3: float, semestre: str) -> bool:
        """Adiciona notas para um aluno em uma disciplina"""
        try:
            # Buscar IDs
            self.cursor.execute("SELECT id FROM alunos WHERE matricula = ?", (matricula,))
            aluno = self.cursor.fetchone()
            if not aluno:
                print(f"✗ Aluno com matrícula {matricula} não encontrado!")
                return False
            
            self.cursor.execute("SELECT id FROM disciplinas WHERE codigo = ?", (codigo_disciplina,))
            disciplina = self.cursor.fetchone()
            if not disciplina:
                print(f"✗ Disciplina com código {codigo_disciplina} não encontrada!")
                return False
            
            # Inserir notas
            self.cursor.execute(
                """INSERT INTO notas (aluno_id, disciplina_id, nota1, nota2, nota3, semestre) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (aluno[0], disciplina[0], nota1, nota2, nota3, semestre)
            )
            self.conn.commit()
            
            media = (nota1 + nota2 + nota3) / 3
            situacao = "APROVADO" if media >= 7.0 else "REPROVADO"
            print(f"✓ Notas adicionadas! Média: {media:.2f} - Situação: {situacao}")
            return True
        except sqlite3.IntegrityError:
            print(f"✗ Erro: Notas já existem para este aluno/disciplina/semestre!")
            return False
        except Exception as e:
            print(f"✗ Erro ao adicionar notas: {e}")
            return False
    
    def atualizar_notas(self, matricula: str, codigo_disciplina: str,
                       nota1: float, nota2: float, nota3: float, semestre: str) -> bool:
        """Atualiza notas de um aluno em uma disciplina"""
        try:
            self.cursor.execute(
                """UPDATE notas 
                   SET nota1 = ?, nota2 = ?, nota3 = ?
                   WHERE aluno_id = (SELECT id FROM alunos WHERE matricula = ?)
                   AND disciplina_id = (SELECT id FROM disciplinas WHERE codigo = ?)
                   AND semestre = ?""",
                (nota1, nota2, nota3, matricula, codigo_disciplina, semestre)
            )
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                media = (nota1 + nota2 + nota3) / 3
                situacao = "APROVADO" if media >= 7.0 else "REPROVADO"
                print(f"✓ Notas atualizadas! Nova média: {media:.2f} - Situação: {situacao}")
                return True
            else:
                print("✗ Nenhuma nota encontrada para atualizar!")
                return False
        except Exception as e:
            print(f"✗ Erro ao atualizar notas: {e}")
            return False
    
    # ==================== CONSULTAS ====================
    
    def ver_situacao_aluno(self, matricula: str) -> List[Dict]:
        """Consulta a situação de um aluno específico"""
        try:
            self.cursor.execute("""
                SELECT 
                    a.matricula,
                    a.nome AS aluno,
                    d.codigo AS cod_disciplina,
                    d.nome AS disciplina,
                    n.nota1,
                    n.nota2,
                    n.nota3,
                    (n.nota1 + n.nota2 + n.nota3) / 3 AS media,
                    CASE 
                        WHEN (n.nota1 + n.nota2 + n.nota3) / 3 >= 7.0 THEN 'APROVADO'
                        ELSE 'REPROVADO'
                    END AS situacao,
                    n.semestre
                FROM notas n
                INNER JOIN alunos a ON n.aluno_id = a.id
                INNER JOIN disciplinas d ON n.disciplina_id = d.id
                WHERE a.matricula = ?
                ORDER BY d.nome
            """, (matricula,))
            
            resultado = []
            for row in self.cursor.fetchall():
                resultado.append({
                    'matricula': row[0],
                    'aluno': row[1],
                    'cod_disciplina': row[2],
                    'disciplina': row[3],
                    'nota1': row[4],
                    'nota2': row[5],
                    'nota3': row[6],
                    'media': row[7],
                    'situacao': row[8],
                    'semestre': row[9]
                })
            return resultado
        except Exception as e:
            print(f"✗ Erro ao consultar situação do aluno: {e}")
            return []
    
    def ver_todas_situacoes(self) -> List[Dict]:
        """Consulta a situação de todos os alunos"""
        try:
            self.cursor.execute("""
                SELECT 
                    a.matricula,
                    a.nome AS aluno,
                    d.codigo AS cod_disciplina,
                    d.nome AS disciplina,
                    n.nota1,
                    n.nota2,
                    n.nota3,
                    (n.nota1 + n.nota2 + n.nota3) / 3 AS media,
                    CASE 
                        WHEN (n.nota1 + n.nota2 + n.nota3) / 3 >= 7.0 THEN 'APROVADO'
                        ELSE 'REPROVADO'
                    END AS situacao,
                    n.semestre
                FROM notas n
                INNER JOIN alunos a ON n.aluno_id = a.id
                INNER JOIN disciplinas d ON n.disciplina_id = d.id
                ORDER BY a.nome, d.nome
            """)
            
            resultado = []
            for row in self.cursor.fetchall():
                resultado.append({
                    'matricula': row[0],
                    'aluno': row[1],
                    'cod_disciplina': row[2],
                    'disciplina': row[3],
                    'nota1': row[4],
                    'nota2': row[5],
                    'nota3': row[6],
                    'media': row[7],
                    'situacao': row[8],
                    'semestre': row[9]
                })
            return resultado
        except Exception as e:
            print(f"✗ Erro ao consultar situações: {e}")
            return []
    
    def ver_resumo_aluno(self, matricula: str = None) -> List[Dict]:
        """Consulta o resumo de um aluno ou de todos os alunos"""
        try:
            if matricula:
                query = """
                    SELECT 
                        a.matricula,
                        a.nome,
                        n.semestre,
                        COUNT(*) AS total_disciplinas,
                        SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 >= 7.0 THEN 1 ELSE 0 END) AS aprovado,
                        SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 < 7.0 THEN 1 ELSE 0 END) AS reprovado,
                        ROUND(AVG((n.nota1 + n.nota2 + n.nota3) / 3), 2) AS media_geral
                    FROM alunos a
                    INNER JOIN notas n ON a.id = n.aluno_id
                    WHERE a.matricula = ?
                    GROUP BY a.matricula, a.nome, n.semestre
                    ORDER BY a.nome
                """
                self.cursor.execute(query, (matricula,))
            else:
                query = """
                    SELECT 
                        a.matricula,
                        a.nome,
                        n.semestre,
                        COUNT(*) AS total_disciplinas,
                        SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 >= 7.0 THEN 1 ELSE 0 END) AS aprovado,
                        SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 < 7.0 THEN 1 ELSE 0 END) AS reprovado,
                        ROUND(AVG((n.nota1 + n.nota2 + n.nota3) / 3), 2) AS media_geral
                    FROM alunos a
                    INNER JOIN notas n ON a.id = n.aluno_id
                    GROUP BY a.matricula, a.nome, n.semestre
                    ORDER BY a.nome
                """
                self.cursor.execute(query)
            
            resultado = []
            for row in self.cursor.fetchall():
                resultado.append({
                    'matricula': row[0],
                    'nome': row[1],
                    'semestre': row[2],
                    'total_disciplinas': row[3],
                    'aprovado': row[4],
                    'reprovado': row[5],
                    'media_geral': row[6]
                })
            return resultado
        except Exception as e:
            print(f"✗ Erro ao consultar resumo: {e}")
            return []
    
    def listar_aprovados(self) -> List[Dict]:
        """Lista alunos aprovados em todas as disciplinas"""
        try:
            self.cursor.execute("""
                SELECT 
                    a.matricula,
                    a.nome,
                    n.semestre,
                    COUNT(*) AS total_disciplinas,
                    ROUND(AVG((n.nota1 + n.nota2 + n.nota3) / 3), 2) AS media_geral
                FROM alunos a
                INNER JOIN notas n ON a.id = n.aluno_id
                GROUP BY a.matricula, a.nome, n.semestre
                HAVING SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 < 7.0 THEN 1 ELSE 0 END) = 0
                ORDER BY media_geral DESC
            """)
            
            resultado = []
            for row in self.cursor.fetchall():
                resultado.append({
                    'matricula': row[0],
                    'nome': row[1],
                    'semestre': row[2],
                    'total_disciplinas': row[3],
                    'media_geral': row[4]
                })
            return resultado
        except Exception as e:
            print(f"✗ Erro ao listar aprovados: {e}")
            return []
    
    def listar_reprovados(self) -> List[Dict]:
        """Lista alunos com alguma reprovação"""
        try:
            self.cursor.execute("""
                SELECT 
                    a.matricula,
                    a.nome,
                    n.semestre,
                    SUM(CASE WHEN (n.nota1 + n.nota2 + n.nota3) / 3 < 7.0 THEN 1 ELSE 0 END) AS disciplinas_reprovadas,
                    ROUND(AVG((n.nota1 + n.nota2 + n.nota3) / 3), 2) AS media_geral
                FROM alunos a
                INNER JOIN notas n ON a.id = n.aluno_id
                GROUP BY a.matricula, a.nome, n.semestre
                HAVING disciplinas_reprovadas > 0
                ORDER BY disciplinas_reprovadas DESC, media_geral ASC
            """)
            
            resultado = []
            for row in self.cursor.fetchall():
                resultado.append({
                    'matricula': row[0],
                    'nome': row[1],
                    'semestre': row[2],
                    'disciplinas_reprovadas': row[3],
                    'media_geral': row[4]
                })
            return resultado
        except Exception as e:
            print(f"✗ Erro ao listar reprovados: {e}")
            return []
    
    def estatisticas_semestre(self, semestre: str) -> Optional[Dict]:
        """Consulta estatísticas gerais de um semestre"""
        try:
            self.cursor.execute("""
                SELECT 
                    ? AS semestre,
                    COUNT(DISTINCT aluno_id) AS total_alunos,
                    COUNT(*) AS total_matriculas,
                    SUM(CASE WHEN (nota1 + nota2 + nota3) / 3 >= 7.0 THEN 1 ELSE 0 END) AS total_aprovacoes,
                    SUM(CASE WHEN (nota1 + nota2 + nota3) / 3 < 7.0 THEN 1 ELSE 0 END) AS total_reprovacoes,
                    ROUND(AVG((nota1 + nota2 + nota3) / 3), 2) AS media_geral,
                    ROUND(100.0 * SUM(CASE WHEN (nota1 + nota2 + nota3) / 3 >= 7.0 THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_aprovacao
                FROM notas
                WHERE semestre = ?
            """, (semestre, semestre))
            
            row = self.cursor.fetchone()
            if row and row[1] > 0:  # Se há alunos
                return {
                    'semestre': row[0],
                    'total_alunos': row[1],
                    'total_matriculas': row[2],
                    'total_aprovacoes': row[3],
                    'total_reprovacoes': row[4],
                    'media_geral': row[5],
                    'taxa_aprovacao': row[6]
                }
            return None
        except Exception as e:
            print(f"✗ Erro ao consultar estatísticas: {e}")
            return None
    
    def inserir_dados_exemplo(self):
        """Insere dados de exemplo no banco"""
        print("\n--- INSERINDO DADOS DE EXEMPLO ---")
        
        # Alunos
        alunos = [
            ('2024001', 'João Silva'),
            ('2024002', 'Maria Santos'),
            ('2024003', 'Pedro Oliveira'),
            ('2024004', 'Ana Costa'),
            ('2024005', 'Carlos Souza')
        ]
        
        for matricula, nome in alunos:
            self.adicionar_aluno(matricula, nome)
        
        # Disciplinas
        disciplinas = [
            ('MAT101', 'Matemática I', 60),
            ('FIS101', 'Física I', 60),
            ('POR101', 'Português', 40),
            ('HIS101', 'História', 40),
            ('QUI101', 'Química I', 60)
        ]
        
        for codigo, nome, carga in disciplinas:
            self.adicionar_disciplina(codigo, nome, carga)
        
        # Notas
        notas = [
            ('2024001', 'MAT101', 8.5, 7.0, 9.0, '2024.1'),
            ('2024001', 'FIS101', 7.5, 8.0, 7.0, '2024.1'),
            ('2024001', 'POR101', 9.0, 8.5, 9.5, '2024.1'),
            ('2024001', 'HIS101', 7.0, 7.5, 8.0, '2024.1'),
            ('2024001', 'QUI101', 6.0, 7.5, 8.0, '2024.1'),
            
            ('2024002', 'MAT101', 9.0, 9.5, 10.0, '2024.1'),
            ('2024002', 'FIS101', 8.5, 9.0, 8.0, '2024.1'),
            ('2024002', 'POR101', 10.0, 9.5, 9.0, '2024.1'),
            ('2024002', 'HIS101', 8.0, 8.5, 9.0, '2024.1'),
            ('2024002', 'QUI101', 9.0, 8.5, 9.5, '2024.1'),
            
            ('2024003', 'MAT101', 5.0, 6.0, 6.5, '2024.1'),
            ('2024003', 'FIS101', 7.0, 7.5, 8.0, '2024.1'),
            ('2024003', 'POR101', 6.0, 5.5, 6.0, '2024.1'),
            ('2024003', 'HIS101', 8.0, 7.5, 7.0, '2024.1'),
            ('2024003', 'QUI101', 9.0, 8.0, 8.5, '2024.1'),
        ]
        
        for matricula, codigo, n1, n2, n3, sem in notas:
            self.adicionar_notas(matricula, codigo, n1, n2, n3, sem)
        
        print("\n✓ Dados de exemplo inseridos com sucesso!")


# ==================== FUNÇÕES DE IMPRESSÃO ====================

def imprimir_linha(tamanho=80):
    """Imprime uma linha separadora"""
    print("=" * tamanho)


def imprimir_alunos(alunos: List[Dict]):
    """Imprime lista de alunos formatada"""
    if not alunos:
        print("Nenhum aluno encontrado.")
        return
    
    imprimir_linha()
    print(f"{'Matrícula':<15} {'Nome':<40} {'Data Cadastro':<20}")
    imprimir_linha()
    for aluno in alunos:
        print(f"{aluno['matricula']:<15} {aluno['nome']:<40} {aluno['data_cadastro']}")
    imprimir_linha()
    print(f"Total: {len(alunos)} aluno(s)")


def imprimir_disciplinas(disciplinas: List[Dict]):
    """Imprime lista de disciplinas formatada"""
    if not disciplinas:
        print("Nenhuma disciplina encontrada.")
        return
    
    imprimir_linha()
    print(f"{'Código':<10} {'Nome':<40} {'Carga Horária':<15}")
    imprimir_linha()
    for disc in disciplinas:
        print(f"{disc['codigo']:<10} {disc['nome']:<40} {disc['carga_horaria']:<15}h")
    imprimir_linha()
    print(f"Total: {len(disciplinas)} disciplina(s)")


def imprimir_situacao(situacoes: List[Dict]):
    """Imprime situação dos alunos formatada"""
    if not situacoes:
        print("Nenhuma informação encontrada.")
        return
    
    imprimir_linha(100)
    print(f"{'Matrícula':<12} {'Aluno':<20} {'Disciplina':<20} {'N1':<6} {'N2':<6} {'N3':<6} {'Média':<7} {'Situação':<12}")
    imprimir_linha(100)
    for s in situacoes:
        print(f"{s['matricula']:<12} {s['aluno']:<20} {s['disciplina']:<20} "
              f"{s['nota1']:<6.2f} {s['nota2']:<6.2f} {s['nota3']:<6.2f} "
              f"{s['media']:<7.2f} {s['situacao']:<12}")
    imprimir_linha(100)


def imprimir_resumo(resumos: List[Dict]):
    """Imprime resumo dos alunos formatado"""
    if not resumos:
        print("Nenhuma informação encontrada.")
        return
    
    imprimir_linha(90)
    print(f"{'Matrícula':<12} {'Nome':<25} {'Semestre':<10} {'Total':<8} {'Aprov.':<8} {'Reprov.':<8} {'Média':<8}")
    imprimir_linha(90)
    for r in resumos:
        print(f"{r['matricula']:<12} {r['nome']:<25} {r['semestre']:<10} "
              f"{r['total_disciplinas']:<8} {r['aprovado']:<8} {r['reprovado']:<8} {r['media_geral']:<8.2f}")
    imprimir_linha(90)


# ==================== MENU INTERATIVO ====================

def menu_principal():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("   SISTEMA DE GERENCIAMENTO DE NOTAS")
    print("="*50)
    print("1.  Adicionar Aluno")
    print("2.  Listar Alunos")
    print("3.  Adicionar Disciplina")
    print("4.  Listar Disciplinas")
    print("5.  Adicionar Notas")
    print("6.  Atualizar Notas")
    print("7.  Ver Situação de um Aluno")
    print("8.  Ver Situação de Todos os Alunos")
    print("9.  Ver Resumo de um Aluno")
    print("10. Ver Resumo de Todos os Alunos")
    print("11. Listar Alunos Aprovados")
    print("12. Listar Alunos Reprovados")
    print("13. Estatísticas do Semestre")
    print("14. Inserir Dados de Exemplo")
    print("0.  Sair")
    print("="*50)


def executar_menu():
    """Executa o menu interativo"""
    print("\n=== SISTEMA DE NOTAS - SQLite ===")
    print("Banco de dados: sistema_notas.db")
    
    try:
        sistema = SistemaNotas('sistema_notas.db')
    except:
        print("\n✗ Não foi possível inicializar o banco de dados. Encerrando...")
        return
    
    while True:
        menu_principal()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n--- ADICIONAR ALUNO ---")
            matricula = input("Matrícula: ").strip()
            nome = input("Nome completo: ").strip()
            sistema.adicionar_aluno(matricula, nome)
        
        elif opcao == "2":
            print("\n--- LISTA DE ALUNOS ---")
            alunos = sistema.listar_alunos()
            imprimir_alunos(alunos)
        
        elif opcao == "3":
            print("\n--- ADICIONAR DISCIPLINA ---")
            codigo = input("Código: ").strip()
            nome = input("Nome: ").strip()
            carga = int(input("Carga horária: ").strip())
            sistema.adicionar_disciplina(codigo, nome, carga)
        
        elif opcao == "4":
            print("\n--- LISTA DE DISCIPLINAS ---")
            disciplinas = sistema.listar_disciplinas()
            imprimir_disciplinas(disciplinas)
        
        elif opcao == "5":
            print("\n--- ADICIONAR NOTAS ---")
            matricula = input("Matrícula do aluno: ").strip()
            codigo = input("Código da disciplina: ").strip()
            nota1 = float(input("Nota 1 (0-10): ").strip())
            nota2 = float(input("Nota 2 (0-10): ").strip())
            nota3 = float(input("Nota 3 (0-10): ").strip())
            semestre = input("Semestre (ex: 2024.1): ").strip()
            sistema.adicionar_notas(matricula, codigo, nota1, nota2, nota3, semestre)
        
        elif opcao == "6":
            print("\n--- ATUALIZAR NOTAS ---")
            matricula = input("Matrícula do aluno: ").strip()
            codigo = input("Código da disciplina: ").strip()
            semestre = input("Semestre (ex: 2024.1): ").strip()
            nota1 = float(input("Nova Nota 1 (0-10): ").strip())
            nota2 = float(input("Nova Nota 2 (0-10): ").strip())
            nota3 = float(input("Nova Nota 3 (0-10): ").strip())
            sistema.atualizar_notas(matricula, codigo, nota1, nota2, nota3, semestre)
        
        elif opcao == "7":
            print("\n--- SITUAÇÃO DO ALUNO ---")
            matricula = input("Matrícula: ").strip()
            situacoes = sistema.ver_situacao_aluno(matricula)
            imprimir_situacao(situacoes)
        
        elif opcao == "8":
            print("\n--- SITUAÇÃO DE TODOS OS ALUNOS ---")
            situacoes = sistema.ver_todas_situacoes()
            imprimir_situacao(situacoes)
        
        elif opcao == "9":
            print("\n--- RESUMO DO ALUNO ---")
            matricula = input("Matrícula: ").strip()
            resumos = sistema.ver_resumo_aluno(matricula)
            imprimir_resumo(resumos)
        
        elif opcao == "10":
            print("\n--- RESUMO DE TODOS OS ALUNOS ---")
            resumos = sistema.ver_resumo_aluno()
            imprimir_resumo(resumos)
        
        elif opcao == "11":
            print("\n--- ALUNOS APROVADOS ---")
            aprovados = sistema.listar_aprovados()
            imprimir_resumo(aprovados)
        
        elif opcao == "12":
            print("\n--- ALUNOS REPROVADOS ---")
            reprovados = sistema.listar_reprovados()
            if reprovados:
                imprimir_linha(80)
                print(f"{'Matrícula':<12} {'Nome':<25} {'Semestre':<10} {'Reprov.':<10} {'Média':<8}")
                imprimir_linha(80)
                for r in reprovados:
                    print(f"{r['matricula']:<12} {r['nome']:<25} {r['semestre']:<10} "
                          f"{r['disciplinas_reprovadas']:<10} {r['media_geral']:<8.2f}")
                imprimir_linha(80)
        
        elif opcao == "13":
            print("\n--- ESTATÍSTICAS DO SEMESTRE ---")
            semestre = input("Semestre (ex: 2024.1): ").strip()
            stats = sistema.estatisticas_semestre(semestre)
            if stats:
                imprimir_linha()
                print(f"Semestre: {stats['semestre']}")
                print(f"Total de alunos: {stats['total_alunos']}")
                print(f"Total de matrículas: {stats['total_matriculas']}")
                print(f"Aprovações: {stats['total_aprovacoes']}")
                print(f"Reprovações: {stats['total_reprovacoes']}")
                print(f"Média geral: {stats['media_geral']:.2f}")
                print(f"Taxa de aprovação: {stats['taxa_aprovacao']:.2f}%")
                imprimir_linha()
            else:
                print("✗ Nenhum dado encontrado para este semestre.")
        
        elif opcao == "14":
            confirmacao = input("Deseja inserir dados de exemplo? (s/n): ").strip().lower()
            if confirmacao == 's':
                sistema.inserir_dados_exemplo()
        
        elif opcao == "0":
            print("\nEncerrando sistema...")
            break
        
        else:
            print("\n✗ Opção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    executar_menu()