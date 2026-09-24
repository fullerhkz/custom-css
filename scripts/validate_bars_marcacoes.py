#!/usr/bin/env python3
"""
Comprehensive validation script for BJ-Share theme bars, markings and Section 7 implementation.
"""
from pathlib import Path
import re
import tinycss2 as css

ROOT = Path(__file__).resolve().parents[1]
THEMES = ['Black', 'Blue', 'Clean', 'DarkBlue', 'Darkness', 'Grey', 'Midnight', 'NewBlack', 'Pink', 'Red']

def validate_css_syntax(path: Path):
    text = path.read_text()
    errors = []
    def visit(nodes):
        for n in nodes:
            if n.type == 'error':
                errors.append(f'{n.source_line}:{n.source_column}: {n.message}')
            elif n.type == 'qualified-rule':
                visit(css.parse_declaration_list(n.content, skip_comments=True, skip_whitespace=True))
            elif n.type == 'at-rule' and n.content is not None:
                visit(css.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))
    visit(css.parse_stylesheet(text, skip_comments=True, skip_whitespace=True))
    return errors

def validate_sections_and_markings(path: Path):
    text = path.read_text()
    issues = []
    
    # Check Section 7 structure
    for sec in ['7.1 Tokens', '7.2 Legibilidade', '7.3 Profundidade', '7.4 Campos e Foco',
                '7.5 Botões', '7.6 Menu', '7.7 Conforto']:
        if sec not in text:
            issues.append(f'Seção ausente: {sec}')
            
    # Check key markings and bars
    if 'inset 3px 0 0' not in text:
        issues.append('Marcação de barra inset 3px 0 0 ausente')
    if 'tr.torrent:hover > td:first-child' not in text:
        issues.append('Barra de torrent no hover ausente')
    if 'border-left: 3px solid' not in text:
        issues.append('Borda esquerda 3px em alerta/citação ausente')
    if 'current-menu-item' not in text:
        issues.append('Marcação de menu ativo ausente')
    if 'bjqs-markers' not in text:
        issues.append('Marcação de carrossel ausente')
    if 'scrollbar-color' not in text or '::-webkit-scrollbar' not in text:
        issues.append('Scrollbar customizada ausente')
    if '::selection' not in text:
        issues.append('Seleção customizada ausente')
    if ':focus-visible' not in text:
        issues.append('Foco acessível ausente')

    # A missing custom property invalidates the entire computed box-shadow.
    definitions = set(re.findall(r'(--[\w-]+)\s*:', text))
    for match in re.finditer(r'var\((--[\w-]+)\s*\)', text):
        if match.group(1) not in definitions:
            issues.append(f'Variável sem definição nem fallback: {match.group(1)}')

    if path.name.startswith('BJ-DarkBlue') and '7941f9941d487660d53683c66ac3a1b4.gif' not in text:
        issues.append('Banner original do DarkBlue ausente')
        
    return issues

def main():
    print("=" * 60)
    print("Iniciando validação dos 10 temas...")
    print("=" * 60)
    
    total_failures = 0
    
    for t in THEMES:
        root_path = ROOT / f"BJ-{t}.css"
        barras_path = ROOT / "css-barras-marcacoes" / f"BJ-{t}-new.css"
        org_path = ROOT / "BJ-organized" / f"BJ-{t}-organized.css"
        
        for name, p in [('Root (Pages)', root_path), ('css-barras-marcacoes', barras_path), ('BJ-organized', org_path)]:
            if not p.exists():
                print(f"❌ {t} [{name}]: Arquivo NÃO existe: {p}")
                total_failures += 1
                continue
                
            syntax_errs = validate_css_syntax(p)
            marking_issues = validate_sections_and_markings(p)
            
            if syntax_errs or marking_issues:
                print(f"❌ {t} [{name}]: {len(syntax_errs)} erros de sintaxe, {len(marking_issues)} falhas estruturais")
                for e in syntax_errs:
                    print(f"   Sintaxe: {e}")
                for i in marking_issues:
                    print(f"   Estrutura: {i}")
                total_failures += 1
            else:
                print(f"✓ {t:10} [{name:20}] — OK (Sintaxe e Marcações 100% válidas)")

        if root_path.exists() and barras_path.exists() and org_path.exists():
            if not (root_path.read_bytes() == barras_path.read_bytes() == org_path.read_bytes()):
                print(f'❌ {t}: cópias da raiz, fonte e BJ-organized divergem')
                total_failures += 1
                
    print("=" * 60)
    if total_failures == 0:
        print("SUCESSO: Todos os 10 temas foram validados sem erros!")
    else:
        print(f"FALHA: {total_failures} problemas encontrados.")
    print("=" * 60)
    assert total_failures == 0

if __name__ == '__main__':
    main()
