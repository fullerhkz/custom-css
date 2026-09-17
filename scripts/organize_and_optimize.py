#!/usr/bin/env python3
"""Organize, optimize, document and format BJ-Share CSS themes."""
import os
import re
from pathlib import Path
import tinycss2 as css

ROOT = Path(__file__).resolve().parents[1]
ORGANIZED_DIR = ROOT / 'BJ-organized'

THEMES_META = {
    'BJ-Black': {
        'name': 'BJ-Black',
        'desc': 'Tema escuro clássico em tons de preto e grafite profundo, com alto contraste e elegância.',
        'palette': 'Fundo: #303030 / Texto: #ccc / Realces: #555, #777'
    },
    'BJ-Blue': {
        'name': 'BJ-Blue',
        'desc': 'Tema claro moderno com detalhes em azul clássico, links dinâmicos e leitura suave.',
        'palette': 'Fundo claro / Texto escuro / Bordas e Sombras: #2255aa, #3a70cc'
    },
    'BJ-Clean': {
        'name': 'BJ-Clean',
        'desc': 'Tema claro e minimalista com foco total no conteúdo, tipografia límpida e tons neutros.',
        'palette': 'Fundo branco/neutro / Texto: #333 / Realces: #bbb, #c0c0d0'
    },
    'BJ-Darkness': {
        'name': 'BJ-Darkness',
        'desc': 'Tema ultra-escuro (deep dark) para ambientes com pouca luz e economia visual.',
        'palette': 'Fundo: #1a1a1a / Texto: #fff, #ccc / Realces: #444, #555'
    },
    'BJ-Grey': {
        'name': 'BJ-Grey',
        'desc': 'Tema balanceado em escala de cinzas refinada, neutro, discreto e sem fadiga visual.',
        'palette': 'Fundo cinza suave / Texto neutro / Realces: #777, #aaa, #c0c0d0'
    },
    'BJ-Midnight': {
        'name': 'BJ-Midnight',
        'desc': 'Tema escuro premium em tons noturnos azulados/índigo, com realces em azul royal e dourado.',
        'palette': 'Fundo: rgb(21, 21, 24) / Texto: #C6C7CF / Realces: #3463a7, #4281da, #e0e0e8'
    },
    'BJ-NewBlack': {
        'name': 'BJ-NewBlack',
        'desc': 'Evolução moderna do BJ-Black com realces em tons ciano/azul profundo e banner translúcido.',
        'palette': 'Fundo: #111, #323131 / Texto: #fff / Realces: #2a5a7a, #4d7c9a'
    },
    'BJ-Pink': {
        'name': 'BJ-Pink',
        'desc': 'Tema vibrante com paleta em tons de rosa, magenta suave e fundos acolhedores.',
        'palette': 'Fundo: #eab3e1 / Texto: #333 / Realces: #802855, #b03080'
    },
    'BJ-Red': {
        'name': 'BJ-Red',
        'desc': 'Tema de alto impacto com destaques e bordas em vermelho escarlate e fundo escuro refinado.',
        'palette': 'Fundo: #303030 / Texto: #fff / Realces: #8c1c1c, #c0392b'
    }
}

PAINT_TRIGGERS = [
    ('2.1 Fundo Geral, Tipografia Base e Listas',
     lambda s: s in ['body', 'h2', 'ul.nobullet']),
    ('2.2 Links, Estados de Hover e Artistas Similares',
     lambda s: s.startswith('a') or 'similar_artist' in s),
    ('2.3 Formulários, Campos de Entrada e Barra BBCode',
     lambda s: any(s.startswith(k) for k in ['input', 'textarea', '.BBCodeToolbar'])),
    ('2.4 Imagens, Badges de Status e Indicadores de Ratio',
     lambda s: s.startswith('img') or s.startswith('.r0') or s.startswith('.r1') or s.startswith('.r2') or s.startswith('.r5') or s.startswith('.r9') or s.startswith('span.size')),
    ('2.5 Cabeçalho, Logotipo e Rodapé',
     lambda s: any(s.startswith(k) for k in ['#header', '#content', '#footer', '#logo'])),
    ('2.6 Menu Principal e Menus Dropdown',
     lambda s: s.startswith('#menu') or s.startswith('#menudrop')),
    ('2.7 Barra de Informações do Usuário e Estatísticas',
     lambda s: s.startswith('#userinfo') or s.startswith('#stats_')),
    ('2.8 Barras de Pesquisa e Notificações de Alerta',
     lambda s: s.startswith('#searchbars') or s.startswith('#alerts') or s.startswith('.alertbar')),
    ('2.9 Estrutura de Conteúdo, Caixas e Painéis',
     lambda s: any(s.startswith(k) for k in ['.box', '.box2', '.head', '.tags', '.noborder'])),
    ('2.10 Tabelas, Cabeçalhos e Linhas Alternadas',
     lambda s: s.startswith('table') or s.startswith('tr') or s.startswith('td') or s.startswith('.colhead') or s.startswith('.error_message') or s.startswith('.save_message') or s.startswith('.noty_') or s.startswith('.elem_error') or s.startswith('.show_torrents') or s.startswith('.hide_torrents') or s.startswith('.cat_list')),
    ('2.11 Listagem de Torrents, Detalhes e Tópicos',
     lambda s: any(k in s for k in ['torrent', 'last_read', 'unread', 'read', 'quoteheader', 'tbody'])),
    ('2.12 Citações (Blockquote), Mídia, Enquetes e Fórum',
     lambda s: s.startswith('blockquote') or any(k in s for k in ['iframe', 'unreadpm', '_poll', 'curtain', 'form tr', 'bookmark', 'linkbox', 'autocomplete', 'vote', 'forum_search', 'forum_unread', 'forum_post'])),
    ('2.13 Chat e Mensagens Rápidas (Shoutbox)',
     lambda s: 'chat' in s or 'shoutTable' in s or s in ['tr.row1', 'tr.row2']),
    ('2.14 Botões, Controles e Menus de Seleção',
     lambda s: any(s.startswith(k) for k in ['button', 'input[type=button]', 'input[type=submit]', 'input[type=\"button\"]', 'select', '.open', '.checkbox', '.multiselect', '.btn'])),
    ('2.15 Atalhos Fixos de Navegação (#irtopo, #irfinal)',
     lambda s: s.startswith('#irtopo') or s.startswith('#irfinal')),
    ('2.16 Tooltips Informativos e Caixas Flutuantes',
     lambda s: 'BJinfoBox' in s or 'data-tooltip' in s),
    ('2.17 Sliders e Carrossel de Destaques (BJQS)',
     lambda s: 'bjqs' in s),
    ('2.18 Badges Internos, Modais, Diálogos e Avisos',
     lambda s: any(k in s for k in ['internalbox', 'torrent_label', 'dialog', 'gorjeta', 'noteAlertMsg', 'browse_rating']))
]

LAYOUT_TRIGGERS = [
    ('3.1 Reset Global de Box Model e Fundo Base',
     lambda s: any(k in s for k in ['*::before', 'body, #userinfo, #alerts, a.BJinfoBox span'])),
    ('3.2 Tipografia e Elementos Básicos',
     lambda s: any(s == k for k in ['body', 'h1, h2, h3, h4', 'h2', 'h4', 'p', 'li', 'ul', 'ol', 'ul.nobullet', 'p.min_padding'])),
    ('3.3 Links e Estados de Texto',
     lambda s: any(k in s for k in ['a.similar_artist', '.similar_artist_header']) or s in ['a', 'a:hover']),
    ('3.4 Formulários, Campos e Mídia Básica',
     lambda s: any(k in s for k in ['.sceditor-container', '.BBCodeToolbar', 'img', '.dropzone', '.edit_changelog textarea']) or s in ['input', 'textarea'] or 'textarea:focus' in s),
    ('3.5 Chat, Formulários e Controles',
     lambda s: any(k in s for k in ['chat_mark_bg', 'shout_nick', 'form input.thin', 'span.grow', 'autocomplete-suggestions', 'tag_editor', 'placeholder'])),
    ('3.6 Indicadores de Ratio',
     lambda s: any(k in s for k in ['.r0', '.r1', '.r2', '.r5', '.r9', '.ratio_'])),
    ('3.7 Tamanhos BBCode',
     lambda s: 'span.size' in s),
    ('3.8 Estrutura Principal da Página',
     lambda s: any(k in s for k in ['#header', '#content', '.thin', '#footer', '#logo', '#wrapper'])),
    ('3.9 Menu Principal e Dropdowns',
     lambda s: '#menu' in s or '#menudrop' in s),
    ('3.10 Barra de Usuário e Estatísticas (#userinfo)',
     lambda s: '#userinfo' in s or '#stats_' in s or 'ul.stats li' in s),
    ('3.11 Busca, Alertas e Seletores (#searchbars, #alerts)',
     lambda s: any(k in s for k in ['#searchbars', '#alerts', '.alertbar'])),
    ('3.12 Utilitários de Visibilidade e Alinhamento',
     lambda s: any(k in s for k in ['.hide', '.hidden', '.center', '.left', '.right', '.clear', 'small_upvote', 'small_downvote', '.min_padding', '.nobr', '.number_column', '.spellcheck', '.two_columns', '.vertical_space', 'div.linkbox'])),
    ('3.13 Containers, Caixas, Sidebar e Imagens',
     lambda s: any(k in s for k in ['.head', '.box', '.box2', '.pad', '.sidebar', '.main_column', '.tags', '.noborder', 'ul.collage_images', '.body'])),
    ('3.14 Tabelas, Cabeçalhos e Mensagens',
     lambda s: any(k in s for k in ['table', 'th', 'td', 'tr.rowa', 'tr.rowb', '.colhead', '.colhead_dark', 'error_message', 'save_message', 'noty_', 'elem_error', 'show_torrents', 'hide_torrents', 'shoutTable', 'row1', 'row2', 'tr'])),
    ('3.15 Listagem e Filtros de Torrents',
     lambda s: any(k in s for k in ['torrent', 'torrent_table', 'group_torrent', 'filter_torrents'])),
    ('3.16 Citações e Mídia Embutida',
     lambda s: any(k in s for k in ['blockquote', 'iframe', 'code_container', 'quoteheader', 'post_return'])),
    ('3.17 Fórum, Leitura e Estados de Tópicos',
     lambda s: any(k in s for k in ['forum_post', 'last_read', 'unread', 'read', 'unreadpm', 'post_id', 'forum_search'])),
    ('3.18 Permissões, Enquetes e Overlays',
     lambda s: any(k in s for k in ['_poll', '.curtain', 'form tr', 'linkbox .brackets', 'top10_quantity_links', 'permission', 'submit_container', 'invitetree', 'user_options', 'lightbox', 'poll'])),
    ('3.19 Selects, Multiselect e Dropdowns',
     lambda s: any(k in s for k in ['button', 'input[type=button]', 'input[type=submit]', 'input[type=\"button\"]', 'select', 'dropdown-menu', 'checkbox', 'multiselect', '.btn'])),
    ('3.20 Atalhos Fixos de Navegação (#irtopo, #irfinal)',
     lambda s: any(k in s for k in ['#irtopo', '#irfinal'])),
    ('3.21 Tooltips BJinfoBox e Data-Tooltip',
     lambda s: any(k in s for k in ['BJinfoBox', 'data-tooltip'])),
    ('3.22 Info Boxes e Imagens de Destaque',
     lambda s: any(k in s for k in ['box_image', 'box_albumart', '.head + .pad'])),
    ('3.23 Slider BJQS e Carrossel',
     lambda s: any(k in s for k in ['bjqs', 'homesldframe', '#container', '#banner-fade', '#banner-slide'])),
    ('3.24 Marcadores Internos e Labels de Torrent',
     lambda s: any(k in s for k in ['internalbox', 'torrent_label'])),
    ('3.25 Diálogos e Modais',
     lambda s: 'dialog' in s),
    ('3.26 Animações nos Botões (Jelly Effect e Botões Destrutivos)',
     lambda s: any(k in s for k in ['jelly-effect', 'button:active', 'attn-cycle', 'gorjeta', 'Deletar', 'Delete', 'Remover'])),
    ('3.27 Acessibilidade: Respeita Redução de Movimento',
     lambda s: 'prefers-reduced-motion' in s),
    ('3.28 Alertas e Ajustes Finais',
     lambda s: any(k in s for k in ['noteAlertMsg', 'browse_rating', 'field_div']))
]

def format_decls(content_nodes, indent=3):
    decls = css.parse_declaration_list(content_nodes, skip_whitespace=True, skip_comments=False)
    lines = []
    prefix = ' ' * indent
    for d in decls:
        if d.type == 'declaration':
            val = css.serialize(d.value).strip()
            val = re.sub(r'/\*\*/', '', val)
            imp = ' !important' if d.important else ''
            lines.append(f'{prefix}{d.name}: {val}{imp};')
    return '\n'.join(lines)

def format_rule(node, indent=3):
    sel = css.serialize(node.prelude).strip()
    sel = re.sub(r'/\*\*/', '', sel)
    # If selector has comma-separated list, clean spacing
    parts = [p.strip() for p in sel.split(',')]
    sel_clean = ',\n'.join(parts)
    decls = format_decls(node.content, indent=indent)
    return f'{sel_clean} {{\n{decls}\n}}\n'

def format_at_rule(node, outer_indent=0):
    keyword = node.lower_at_keyword
    prelude = css.serialize(node.prelude).strip()
    out_pref = ' ' * outer_indent
    if node.content is None:
        return f'{out_pref}@{keyword} {prelude};\n'
    
    nested = css.parse_rule_list(node.content, skip_whitespace=True, skip_comments=False)
    inner_parts = []
    for r in nested:
        if r.type == 'qualified-rule':
            r_sel = css.serialize(r.prelude).strip()
            r_parts = [p.strip() for p in r_sel.split(',')]
            r_sel_clean = ',\n'.join(' ' * (outer_indent + 3) + p for p in r_parts)
            r_decls = format_decls(r.content, indent=outer_indent + 6)
            inner_parts.append(f'{r_sel_clean} {{\n{r_decls}\n{out_pref}   }}')
        elif r.type == 'at-rule':
            inner_parts.append(format_at_rule(r, outer_indent=outer_indent + 3).rstrip())
    body = '\n\n'.join(inner_parts)
    return f'{out_pref}@{keyword} {prelude} {{\n{body}\n{out_pref}}}\n'

def make_header_banner(theme_key):
    info = THEMES_META[theme_key]
    return f"""/* ====================================================================
 * BJ-Share Custom CSS — Tema: {info['name']}
 * Versão: 2.0 (Otimizado, Modular e Reorganizado)
 * Descrição: {info['desc']}
 * Paleta principal: {info['palette']}
 *
 * ÍNDICE DAS SEÇÕES:
 *   1. DEFAULTS AUXILIARES (@layer bj-defaults)
 *   2. PALETA DE CORES E APARÊNCIA ESPECÍFICA DO TEMA
 *      2.1  Fundo Geral, Tipografia Base e Listas
 *      2.2  Links, Estados de Hover e Artistas Similares
 *      2.3  Formulários, Campos de Entrada e Barra BBCode
 *      2.4  Imagens, Badges de Status e Indicadores de Ratio
 *      2.5  Cabeçalho, Logotipo e Rodapé
 *      2.6  Menu Principal e Menus Dropdown
 *      2.7  Barra de Informações do Usuário e Estatísticas
 *      2.8  Barras de Pesquisa e Notificações de Alerta
 *      2.9  Estrutura de Conteúdo, Caixas e Painéis
 *      2.10 Tabelas, Cabeçalhos e Linhas Alternadas
 *      2.11 Listagem de Torrents, Detalhes e Tópicos
 *      2.12 Citações (Blockquote), Mídia, Enquetes e Fórum
 *      2.13 Chat e Mensagens Rápidas (Shoutbox)
 *      2.14 Botões, Controles e Menus de Seleção
 *      2.15 Atalhos Fixos de Navegação (#irtopo, #irfinal)
 *      2.16 Tooltips Informativos e Caixas Flutuantes
 *      2.17 Sliders e Carrossel de Destaques (BJQS)
 *      2.18 Badges Internos, Modais, Diálogos e Avisos
 *   3. ESTRUTURA GLOBAL E LAYOUT RESPONSIVO (BASE COMUM)
 *      3.1  Reset Global de Box Model e Fundo Base
 *      3.2  Tipografia e Elementos Básicos
 *      3.3  Links e Estados de Texto
 *      3.4  Formulários, Campos e Mídia Básica
 *      3.5  Chat, Formulários e Controles
 *      3.6  Indicadores de Ratio
 *      3.7  Tamanhos BBCode
 *      3.8  Estrutura Principal da Página
 *      3.9  Menu Principal e Dropdowns
 *      3.10 Barra de Usuário e Estatísticas (#userinfo)
 *      3.11 Busca, Alertas e Seletores (#searchbars, #alerts)
 *      3.12 Utilitários de Visibilidade e Alinhamento
 *      3.13 Containers, Caixas, Sidebar e Imagens
 *      3.14 Tabelas, Cabeçalhos e Mensagens
 *      3.15 Listagem e Filtros de Torrents
 *      3.16 Citações e Mídia Embutida
 *      3.17 Fórum, Leitura e Estados de Tópicos
 *      3.18 Permissões, Enquetes e Overlays
 *      3.19 Selects, Multiselect e Dropdowns
 *      3.20 Atalhos Fixos de Navegação (#irtopo, #irfinal)
 *      3.21 Tooltips BJinfoBox e Data-Tooltip
 *      3.22 Info Boxes e Imagens de Destaque
 *      3.23 Slider BJQS e Carrossel
 *      3.24 Marcadores Internos e Labels de Torrent
 *      3.25 Diálogos e Modais
 *      3.26 Animações nos Botões (Jelly Effect e Botões Destrutivos)
 *      3.27 Acessibilidade: Respeita Redução de Movimento
 *      3.28 Alertas e Ajustes Finais
 *   4. CONTROLE DO MENU FIXO (STICKY NAVIGATION)
 *      Troque '@media all' por '@media not all' na Seção 4 para desligar o menu fixo.
 *   5. MEDIA QUERIES E RESPONSIVIDADE (MOBILE / TABLET / 4K)
 *   6. AJUSTES FINAIS DE LAYOUT E COMPATIBILIDADE MOBILE
 * ==================================================================== */\n\n"""

def organize_theme(file_path):
    theme_stem = file_path.stem.replace('-organized', '')
    raw = file_path.read_text()
    
    # 1. Clean syntax errors and comments
    raw = re.sub(r'^\s*/\s*background-image:[^\n]+\n', '', raw, flags=re.MULTILINE)
    raw = raw.replace('/**/', '')
    
    tree = css.parse_stylesheet(raw, skip_comments=True, skip_whitespace=True)
    
    # Split nodes into sections
    layer_defaults_node = None
    paint_nodes = []
    layout_nodes = []
    fixed_menu_node = None
    media_nodes = []
    layout_fixes_nodes = []
    
    found_layout = False
    in_fixed_menu = False
    in_layout_fixes = False
    
    for n in tree:
        if n.type == 'at-rule' and n.lower_at_keyword == 'layer' and 'bj-defaults' in css.serialize(n.prelude):
            layer_defaults_node = n
            continue
        
        if n.type == 'qualified-rule' and '*, *::before, *::after' in css.serialize(n.prelude).replace('\n', ' '):
            found_layout = True
        
        if not found_layout:
            paint_nodes.append(n)
        else:
            if n.type == 'at-rule' and n.lower_at_keyword == 'media':
                prelude_str = css.serialize(n.prelude).strip()
                if prelude_str == 'all':
                    fixed_menu_node = n
                    continue
                elif '901px' in prelude_str or ('900px' in prelude_str and len(media_nodes) >= 6):
                    layout_fixes_nodes.append(n)
                    continue
                elif fixed_menu_node is not None:
                    media_nodes.append(n)
                    continue
            layout_nodes.append(n)
            
    # Assemble output
    out = []
    out.append(make_header_banner(theme_stem))
    
    # Section 1: Defaults
    out.append("""/* ====================================================================
 * SEÇÃO 1: DEFAULTS AUXILIARES (COMPONENTES MODERNOS)
 * Aplicação em camada (@layer bj-defaults) para garantir baixa especificidade
 * e fácil sobrescrita por regras nativas do tema.
 * ==================================================================== */\n""")
    if layer_defaults_node:
        out.append(format_at_rule(layer_defaults_node, outer_indent=0))
        out.append('\n')
        
    # Section 2: Paint (Theme specific)
    out.append("""/* ====================================================================
 * SEÇÃO 2: PALETA DE CORES E APARÊNCIA ESPECÍFICA DO TEMA
 * Cores de fundo, texto, bordas, sombras e imagens exclusivas deste tema.
 * ==================================================================== */\n""")
    
    current_paint_sub = None
    for n in paint_nodes:
        if n.type == 'qualified-rule':
            sel = css.serialize(n.prelude).strip()
            sel_norm = ' '.join(sel.split())
            sub_title = None
            for title, pred in PAINT_TRIGGERS:
                if pred(sel_norm):
                    sub_title = title
                    break
            if sub_title is None:
                sub_title = '2.18 Badges Internos, Modais, Diálogos e Avisos'
            
            if sub_title != current_paint_sub:
                current_paint_sub = sub_title
                out.append(f"""/* ----------------------------------------------------------------------
 * {current_paint_sub}
 * ---------------------------------------------------------------------- */\n""")
            out.append(format_rule(n, indent=3))
            out.append('\n')
        elif n.type == 'at-rule':
            out.append(format_at_rule(n, outer_indent=0))
            out.append('\n')

    # Section 3: Layout (Common structure)
    out.append("""/* ====================================================================
 * SEÇÃO 3: ESTRUTURA GLOBAL E LAYOUT RESPONSIVO (BASE COMUM)
 * Dimensionamento, flex/grid, alinhamentos, posições e tipografia estrutural.
 * ==================================================================== */\n""")
    
    current_layout_sub = None
    for n in layout_nodes:
        if n.type == 'qualified-rule':
            sel = css.serialize(n.prelude).strip()
            sel_norm = ' '.join(sel.split())
            sub_title = None
            for title, pred in LAYOUT_TRIGGERS:
                if pred(sel_norm):
                    sub_title = title
                    break
            if sub_title is None:
                sub_title = '3.28 Alertas e Ajustes Finais'
            
            if sub_title != current_layout_sub:
                current_layout_sub = sub_title
                out.append(f"""/* ----------------------------------------------------------------------
 * {current_layout_sub}
 * ---------------------------------------------------------------------- */\n""")
            out.append(format_rule(n, indent=3))
            out.append('\n')
        elif n.type == 'at-rule':
            sel = '@' + n.lower_at_keyword + ' ' + css.serialize(n.prelude).strip()
            sel_norm = ' '.join(sel.split())
            sub_title = None
            for title, pred in LAYOUT_TRIGGERS:
                if pred(sel_norm):
                    sub_title = title
                    break
            if sub_title is None:
                sub_title = '3.26 Animações nos Botões (Jelly Effect e Botões Destrutivos)'
                
            if sub_title != current_layout_sub:
                current_layout_sub = sub_title
                out.append(f"""/* ----------------------------------------------------------------------
 * {current_layout_sub}
 * ---------------------------------------------------------------------- */\n""")
            out.append(format_at_rule(n, outer_indent=0))
            out.append('\n')

    # Section 4: Fixed menu
    out.append("""/* ====================================================================
 * SEÇÃO 4: CONTROLE DO MENU FIXO (STICKY NAVIGATION)
 *
 * INSTRUÇÕES:
 *   - Para MANTER o menu fixo: use '@media all {'
 *   - Para DESATIVAR o menu fixo (menu estático no topo): troque para '@media not all {'
 *   Em resoluções mobile (<= 900px), o menu sempre rola naturalmente.
 * ==================================================================== */\n""")
    if fixed_menu_node:
        out.append(format_at_rule(fixed_menu_node, outer_indent=0))
        out.append('\n')

    # Section 5: Media Queries
    out.append("""/* ====================================================================
 * SEÇÃO 5: MEDIA QUERIES E RESPONSIVIDADE (MOBILE / TABLET / 4K)
 * Adaptação de larguras, colunas, menus e caixas para diferentes resoluções.
 * ==================================================================== */\n""")
    for n in media_nodes:
        prelude_str = css.serialize(n.prelude).strip()
        desc = ""
        if '1921px' in prelude_str:
            desc = "Monitores Ultrawide e 1440p (2K)"
        elif '3840px' in prelude_str:
            desc = "Monitores 4K UHD"
        elif '1024px' in prelude_str:
            desc = "Notebooks compactos e tablets em modo paisagem"
        elif '768px' in prelude_str:
            desc = "Tablets em modo retrato e telas intermediárias"
        elif '550px' in prelude_str:
            desc = "Smartphones grandes / telas menores que 550px"
        elif '420px' in prelude_str:
            desc = "Smartphones comuns (<= 420px)"
        elif '300px' in prelude_str:
            desc = "Dispositivos ultra-compactos (<= 300px)"
        elif '900px' in prelude_str:
            desc = "Transição mobile / desktop (<= 900px)"
            
        out.append(f"""/* ----------------------------------------------------------------------
 * Breakpoint: @media {prelude_str} — {desc}
 * ---------------------------------------------------------------------- */\n""")
        out.append(format_at_rule(n, outer_indent=0))
        out.append('\n')

    # Section 6: Layout fixes
    out.append("""/* ====================================================================
 * SEÇÃO 6: AJUSTES FINAIS DE LAYOUT E COMPATIBILIDADE MOBILE
 * Ajustes de contenção de largura de alertas, empilhamento de perfil e alinhamento.
 * ==================================================================== */\n""")
    for n in layout_fixes_nodes:
        prelude_str = css.serialize(n.prelude).strip()
        if '901px' in prelude_str:
            out.append("/* O left global de ul ganha de right quando ambos têm largura fixa (desktop). */\n")
        elif '900px' in prelude_str:
            out.append("/* position: static não empilha um ul que ainda tem display: inline (mobile). */\n")
        out.append(format_at_rule(n, outer_indent=0))
        out.append('\n')
        
    final_css = ''.join(out)
    # Final whitespace cleanup
    final_css = re.sub(r'\n{3,}', '\n\n', final_css)
    return final_css

def main():
    css_files = sorted(ORGANIZED_DIR.glob('*.css'))
    print(f"Encontrados {len(css_files)} arquivos em BJ-organized.")
    
    for path in css_files:
        theme = path.stem.replace('-organized', '')
        print(f"Processando {path.name}...")
        organized_content = organize_theme(path)
        path.write_text(organized_content)
        
        # Verify syntax
        tree = css.parse_stylesheet(organized_content, skip_comments=True, skip_whitespace=True)
        errors = []
        def check(nodes):
            for n in nodes:
                if n.type == 'error':
                    errors.append(f"{n.source_line}: {n.message}")
                elif n.type == 'qualified-rule':
                    check(css.parse_declaration_list(n.content, skip_comments=True, skip_whitespace=True))
                elif n.type == 'at-rule' and n.content is not None:
                    check(css.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))
        check(tree)
        assert len(errors) == 0, f"Erro de sintaxe em {theme}: {errors}"
        print(f" -> {path.name}: {len(organized_content)} bytes, 0 erros de sintaxe.")

if __name__ == '__main__':
    main()
