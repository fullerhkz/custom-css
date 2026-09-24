#!/usr/bin/env python3
"""
Replicate Midnight's bars, markings and Section 7 overrides across all BJ-Share themes.
Respects the unique color palette, lightness/darkness, and style of each individual theme.
"""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / 'css-barras-marcacoes'
ORGANIZED_DIR = ROOT / 'BJ-organized'

THEMES = {
    'BJ-Black': {
        'name': 'BJ-Black',
        'desc': 'Tema escuro clássico em tons de preto e grafite profundo, com alto contraste e elegância.',
        'palette': 'Fundo: #1d1d1d / Texto: #fff, #ccc / Realces: #d4d4d8, #71717a',
        'is_dark': True,
        'accent': '#d4d4d8',          # titânio / platina prateada luminosa
        'accent_hover': '#ffffff',
        'accent_soft': 'rgba(255, 255, 255, 0.10)',
        'accent_ring': 'rgba(255, 255, 255, 0.28)',
        'secondary': '#71717a',       # grafite / zinco
        'secondary_soft': 'rgba(113, 113, 122, 0.15)',
        'gold_soft': 'rgba(245, 186, 73, 0.14)',
        'green_soft': 'rgba(74, 187, 98, 0.14)',
        'red_soft': 'rgba(235, 87, 87, 0.14)',
        'accent_border': '#3f3f46',
        'text_muted': '#a1a1aa',
        'edge': 'rgba(255, 255, 255, 0.07)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 6px 20px rgba(0, 0, 0, 0.50)',
        'head_bg': 'linear-gradient(180deg, #2c2c2e, #202022)',
        'head_color': '',
        'table_shadow': '0 2px 10px rgba(0, 0, 0, 0.40)',
        'menu_bg': 'linear-gradient(180deg, #262628, #1c1c1e)',
        'menu_border': '#3f3f46',
        'menu_shadow_op': '0.55',
        'dropdown_shadow_op': '0.55',
        'btn_bg': 'linear-gradient(180deg, #2d2d30, #222224)',
        'btn_border': 'var(--accent)',
        'btn_shadow_op': '0.4',
        'btn_hover_bg': 'linear-gradient(180deg, #38383c, #2a2a2e)',
        'btn_hover_border': 'rgba(255, 255, 255, 0.65)',
        'btn_hover_text': '#ffffff',
        'btn_hover_shadow_op': '0.45',
        'btn_active_bg': 'linear-gradient(180deg, #1c1c1e, #262628)',
        'submit_text': '#ffffff',
        'submit_active_bg': 'linear-gradient(180deg, #1c1c1e, #262628)',
        'input_hover_border': '#52525b',
        'focus_glow': 'rgba(255, 255, 255, 0.35)',
        'error_border': 'rgba(235, 87, 87, 0.45)',
        'error_text': '#fca5a5',
        'save_border': 'rgba(245, 186, 73, 0.45)',
        'save_text': '#fcd34d',
        'elem_error': '#ef4444',
        'quote_border_color': 'rgba(212, 212, 216, 0.65)',
        'quote_nested_color': 'rgba(113, 113, 122, 0.65)',
        'dialog_shadow_op': '0.6',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.70)',
        'carrossel_btn': '#333333',
        'carrossel_marker_text': '#111111',
        'scrollbar_thumb': '#4a4a50',
        'scrollbar_track': '#1a1a1c',
        'scrollbar_hover': '#606068',
        'selection_bg': 'rgba(255, 255, 255, 0.25)',
        'selection_text': '#ffffff',
        'current_menu_text': 'var(--text-primary)',
        'multiselect_text': 'var(--text-bright)',
        'bbcode_icon_fill': '#a1a1aa',
        'quoteheader_color': '#a1a1aa',
        'disabled_color': '#71717a',
    },
    'BJ-Blue': {
        'name': 'BJ-Blue',
        'desc': 'Tema claro moderno com detalhes em azul clássico, links dinâmicos e leitura suave.',
        'palette': 'Fundo claro / Texto escuro / Bordas e Sombras: #1d68cd, #0284c7',
        'is_dark': False,
        'accent': '#1d68cd',          # azul royal clássico e vivo
        'accent_hover': '#0e4a9e',
        'accent_soft': 'rgba(29, 104, 205, 0.10)',
        'accent_ring': 'rgba(29, 104, 205, 0.25)',
        'secondary': '#0284c7',       # azul celeste / sky
        'secondary_soft': 'rgba(2, 132, 199, 0.10)',
        'gold_soft': 'rgba(217, 130, 0, 0.12)',
        'green_soft': 'rgba(22, 142, 60, 0.12)',
        'red_soft': 'rgba(217, 48, 37, 0.12)',
        'accent_border': '#cbd5e1',
        'text_muted': '#64748b',
        'edge': 'rgba(255, 255, 255, 0.80)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 4px 16px rgba(0, 0, 0, 0.08)',
        'head_bg': 'linear-gradient(180deg, #f0f4fa, #e2eaf5)',
        'head_color': '    color: #0f2d59;\n',
        'table_shadow': '0 1px 6px rgba(0, 0, 0, 0.08)',
        'menu_bg': 'linear-gradient(180deg, #e8ecf4, #dbe2ee)',
        'menu_border': '#c4d0e2',
        'menu_shadow_op': '0.12',
        'dropdown_shadow_op': '0.15',
        'btn_bg': 'linear-gradient(180deg, #ffffff, #edf2f7)',
        'btn_border': '#c2cddb',
        'btn_shadow_op': '0.1',
        'btn_hover_bg': 'linear-gradient(180deg, #edf4fc, #dde8f7)',
        'btn_hover_border': 'rgba(29, 104, 205, 0.70)',
        'btn_hover_text': '#0e4a9e',
        'btn_hover_shadow_op': '0.15',
        'btn_active_bg': 'linear-gradient(180deg, #d8e4f2, #e8f0fa)',
        'submit_text': '#0e4a9e',
        'submit_active_bg': 'linear-gradient(180deg, #d0deee, #e2ecf7)',
        'input_hover_border': '#94a3b8',
        'focus_glow': 'rgba(29, 104, 205, 0.35)',
        'error_border': 'rgba(217, 48, 37, 0.45)',
        'error_text': '#b91c1c',
        'save_border': 'rgba(217, 130, 0, 0.45)',
        'save_text': '#b45309',
        'elem_error': '#dc2626',
        'quote_border_color': 'rgba(29, 104, 205, 0.55)',
        'quote_nested_color': 'rgba(2, 132, 199, 0.55)',
        'dialog_shadow_op': '0.2',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.45)',
        'carrossel_btn': '#dbe2ee',
        'carrossel_marker_text': '#ffffff',
        'scrollbar_thumb': '#a8b5c8',
        'scrollbar_track': '#eef2f7',
        'scrollbar_hover': '#8696ad',
        'selection_bg': 'rgba(29, 104, 205, 0.22)',
        'selection_text': '#000000',
        'current_menu_text': '#0e4a9e',
        'multiselect_text': 'var(--text-primary)',
        'bbcode_icon_fill': '#64748b',
        'quoteheader_color': '#475569',
        'disabled_color': '#94a3b8',
    },
    'BJ-Clean': {
        'name': 'BJ-Clean',
        'desc': 'Tema claro e minimalista com foco total no conteúdo, tipografia límpida e tons neutros.',
        'palette': 'Fundo branco/neutro / Texto: #1e293b / Realces: #246e82, #4b7b8a',
        'is_dark': False,
        'accent': '#246e82',          # petróleo / ardósia ciano
        'accent_hover': '#154c5b',
        'accent_soft': 'rgba(36, 110, 130, 0.10)',
        'accent_ring': 'rgba(36, 110, 130, 0.25)',
        'secondary': '#4b7b8a',       # ardósia suave
        'secondary_soft': 'rgba(75, 123, 138, 0.10)',
        'gold_soft': 'rgba(196, 124, 0, 0.12)',
        'green_soft': 'rgba(26, 138, 70, 0.12)',
        'red_soft': 'rgba(209, 44, 44, 0.12)',
        'accent_border': '#cbd5e1',
        'text_muted': '#64748b',
        'edge': 'rgba(255, 255, 255, 0.85)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 4px 14px rgba(0, 0, 0, 0.06)',
        'head_bg': 'linear-gradient(180deg, #eef4f6, #e0eaee)',
        'head_color': '    color: #1e4754;\n',
        'table_shadow': '0 1px 5px rgba(0, 0, 0, 0.06)',
        'menu_bg': 'linear-gradient(180deg, #e5e9ec, #d8dde1)',
        'menu_border': '#c5cbd2',
        'menu_shadow_op': '0.10',
        'dropdown_shadow_op': '0.12',
        'btn_bg': 'linear-gradient(180deg, #ffffff, #edf0f2)',
        'btn_border': '#c8ced4',
        'btn_shadow_op': '0.1',
        'btn_hover_bg': 'linear-gradient(180deg, #eef6f8, #dfedf1)',
        'btn_hover_border': 'rgba(36, 110, 130, 0.65)',
        'btn_hover_text': '#154c5b',
        'btn_hover_shadow_op': '0.12',
        'btn_active_bg': 'linear-gradient(180deg, #d8e3e7, #e8f0f3)',
        'submit_text': '#154c5b',
        'submit_active_bg': 'linear-gradient(180deg, #d0dce0, #e0ecf0)',
        'input_hover_border': '#94a3b8',
        'focus_glow': 'rgba(36, 110, 130, 0.30)',
        'error_border': 'rgba(209, 44, 44, 0.45)',
        'error_text': '#b91c1c',
        'save_border': 'rgba(196, 124, 0, 0.45)',
        'save_text': '#b45309',
        'elem_error': '#dc2626',
        'quote_border_color': 'rgba(36, 110, 130, 0.55)',
        'quote_nested_color': 'rgba(75, 123, 138, 0.55)',
        'dialog_shadow_op': '0.18',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.40)',
        'carrossel_btn': '#d8dde1',
        'carrossel_marker_text': '#ffffff',
        'scrollbar_thumb': '#b0bcc4',
        'scrollbar_track': '#eff3f5',
        'scrollbar_hover': '#8e9ca6',
        'selection_bg': 'rgba(36, 110, 130, 0.22)',
        'selection_text': '#000000',
        'current_menu_text': '#154c5b',
        'multiselect_text': 'var(--text-primary)',
        'bbcode_icon_fill': '#64748b',
        'quoteheader_color': '#475569',
        'disabled_color': '#94a3b8',
    },
    'BJ-DarkBlue': {
        'name': 'BJ-DarkBlue',
        'desc': 'Tema escuro clássico em tons de azul marinho profundo e ardósia, com realces em azul elétrico e gelo.',
        'palette': 'Fundo: #151518 / Texto: #C6C7CF / Realces: #5897f5, #38bdf8, #80b3ff',
        'is_dark': True,
        'accent': '#5897f5',          # azul oceânico / gelo elétrico
        'accent_hover': '#80b3ff',
        'accent_soft': 'rgba(88, 151, 245, 0.14)',
        'accent_ring': 'rgba(88, 151, 245, 0.35)',
        'secondary': '#38bdf8',       # ciano celeste
        'secondary_soft': 'rgba(56, 189, 248, 0.14)',
        'gold_soft': 'rgba(240, 192, 90, 0.13)',
        'green_soft': 'rgba(74, 206, 132, 0.13)',
        'red_soft': 'rgba(235, 95, 95, 0.13)',
        'accent_border': '#2b3040',
        'text_muted': '#9497a7',
        'edge': 'rgba(255, 255, 255, 0.06)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 6px 20px rgba(0, 0, 0, 0.40)',
        'head_bg': 'linear-gradient(180deg, #1c202d, #151824)',
        'head_color': '',
        'table_shadow': '0 2px 10px rgba(0, 0, 0, 0.35)',
        'menu_bg': 'linear-gradient(180deg, #171b26, #10131d)',
        'menu_border': '#2b3040',
        'menu_shadow_op': '0.55',
        'dropdown_shadow_op': '0.55',
        'btn_bg': 'linear-gradient(180deg, #222736, #191c28)',
        'btn_border': '#2f364a',
        'btn_shadow_op': '0.4',
        'btn_hover_bg': 'linear-gradient(180deg, #27344e, #1c263c)',
        'btn_hover_border': 'rgba(88, 151, 245, 0.70)',
        'btn_hover_text': '#ffffff',
        'btn_hover_shadow_op': '0.45',
        'btn_active_bg': 'linear-gradient(180deg, #151c2a, #202b40)',
        'submit_text': '#d6e4ff',
        'submit_active_bg': 'linear-gradient(180deg, #151c2a, #202b40)',
        'input_hover_border': '#3d4760',
        'focus_glow': 'rgba(88, 151, 245, 0.40)',
        'error_border': 'rgba(235, 95, 95, 0.45)',
        'error_text': '#fca5a5',
        'save_border': 'rgba(240, 192, 90, 0.45)',
        'save_text': '#fcd34d',
        'elem_error': '#ef4444',
        'quote_border_color': 'rgba(88, 151, 245, 0.55)',
        'quote_nested_color': 'rgba(56, 189, 248, 0.55)',
        'dialog_shadow_op': '0.6',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.70)',
        'carrossel_btn': '#1e2638',
        'carrossel_marker_text': '#0d1017',
        'scrollbar_thumb': '#353d52',
        'scrollbar_track': '#0f1218',
        'scrollbar_hover': '#495470',
        'selection_bg': 'rgba(88, 151, 245, 0.32)',
        'selection_text': '#ffffff',
        'current_menu_text': 'var(--text-bright)',
        'multiselect_text': 'var(--text-bright)',
        'bbcode_icon_fill': '#8b8f9e',
        'quoteheader_color': '#9499a8',
        'disabled_color': '#696c78',
    },
    'BJ-Darkness': {
        'name': 'BJ-Darkness',
        'desc': 'Tema ultra-escuro (deep dark) para ambientes com pouca luz e economia visual.',
        'palette': 'Fundo: #101010 / Texto: #fff, #ccc / Realces: #f0b548, #e67e22',
        'is_dark': True,
        'accent': '#f0b548',          # âmbar aquecido / dourado luminoso
        'accent_hover': '#ffd278',
        'accent_soft': 'rgba(240, 181, 72, 0.14)',
        'accent_ring': 'rgba(240, 181, 72, 0.35)',
        'secondary': '#e67e22',       # laranja crepúsculo
        'secondary_soft': 'rgba(230, 126, 34, 0.14)',
        'gold_soft': 'rgba(240, 181, 72, 0.14)',
        'green_soft': 'rgba(74, 187, 98, 0.14)',
        'red_soft': 'rgba(235, 87, 87, 0.14)',
        'accent_border': '#333333',
        'text_muted': '#a0a0a5',
        'edge': 'rgba(255, 255, 255, 0.05)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 6px 20px rgba(0, 0, 0, 0.60)',
        'head_bg': 'linear-gradient(180deg, #222222, #181818)',
        'head_color': '',
        'table_shadow': '0 2px 10px rgba(0, 0, 0, 0.50)',
        'menu_bg': 'linear-gradient(180deg, #1c1c1c, #121212)',
        'menu_border': '#333333',
        'menu_shadow_op': '0.60',
        'dropdown_shadow_op': '0.60',
        'btn_bg': 'linear-gradient(180deg, #262626, #1c1c1c)',
        'btn_border': '#383838',
        'btn_shadow_op': '0.4',
        'btn_hover_bg': 'linear-gradient(180deg, #332d20, #242017)',
        'btn_hover_border': 'rgba(240, 181, 72, 0.70)',
        'btn_hover_text': '#ffffff',
        'btn_hover_shadow_op': '0.45',
        'btn_active_bg': 'linear-gradient(180deg, #1a1712, #26221a)',
        'submit_text': '#ffe5a3',
        'submit_active_bg': 'linear-gradient(180deg, #1f1b13, #2e281b)',
        'input_hover_border': '#484848',
        'focus_glow': 'rgba(240, 181, 72, 0.35)',
        'error_border': 'rgba(235, 87, 87, 0.45)',
        'error_text': '#fca5a5',
        'save_border': 'rgba(240, 181, 72, 0.45)',
        'save_text': '#fcd34d',
        'elem_error': '#ef4444',
        'quote_border_color': 'rgba(240, 181, 72, 0.55)',
        'quote_nested_color': 'rgba(230, 126, 34, 0.55)',
        'dialog_shadow_op': '0.65',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.75)',
        'carrossel_btn': '#262626',
        'carrossel_marker_text': '#111111',
        'scrollbar_thumb': '#383838',
        'scrollbar_track': '#111111',
        'scrollbar_hover': '#505050',
        'selection_bg': 'rgba(240, 181, 72, 0.30)',
        'selection_text': '#ffffff',
        'current_menu_text': 'var(--text-bright)',
        'multiselect_text': 'var(--text-bright)',
        'bbcode_icon_fill': '#888888',
        'quoteheader_color': '#999999',
        'disabled_color': '#555555',
    },
    'BJ-Grey': {
        'name': 'BJ-Grey',
        'desc': 'Tema balanceado em escala de cinzas refinada, neutro, discreto e sem fadiga visual.',
        'palette': 'Fundo cinza suave / Texto neutro / Realces: #3f536e, #596f8c',
        'is_dark': False,
        'accent': '#3f536e',          # aço ardósia / steel-blue profundo
        'accent_hover': '#283648',
        'accent_soft': 'rgba(63, 83, 110, 0.12)',
        'accent_ring': 'rgba(63, 83, 110, 0.28)',
        'secondary': '#596f8c',       # azul ardósia clássico
        'secondary_soft': 'rgba(89, 111, 140, 0.12)',
        'gold_soft': 'rgba(189, 120, 0, 0.12)',
        'green_soft': 'rgba(28, 130, 65, 0.12)',
        'red_soft': 'rgba(199, 40, 40, 0.12)',
        'accent_border': '#9ca3af',
        'text_muted': '#555555',
        'edge': 'rgba(255, 255, 255, 0.60)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 4px 16px rgba(0, 0, 0, 0.12)',
        'head_bg': 'linear-gradient(180deg, #d6d6d6, #c6c6c6)',
        'head_color': '    color: #283648;\n',
        'table_shadow': '0 1px 6px rgba(0, 0, 0, 0.12)',
        'menu_bg': 'linear-gradient(180deg, #c4c4c4, #b4b4b4)',
        'menu_border': '#9aa0a6',
        'menu_shadow_op': '0.15',
        'dropdown_shadow_op': '0.20',
        'btn_bg': 'linear-gradient(180deg, #e4e4e4, #d0d0d0)',
        'btn_border': '#9ca3af',
        'btn_shadow_op': '0.15',
        'btn_hover_bg': 'linear-gradient(180deg, #dce2ea, #cbd4e0)',
        'btn_hover_border': 'rgba(63, 83, 110, 0.70)',
        'btn_hover_text': '#182332',
        'btn_hover_shadow_op': '0.18',
        'btn_active_bg': 'linear-gradient(180deg, #bfcad6, #cfd8e3)',
        'submit_text': '#182332',
        'submit_active_bg': 'linear-gradient(180deg, #b5c2d0, #c8d3e0)',
        'input_hover_border': '#6b7280',
        'focus_glow': 'rgba(63, 83, 110, 0.35)',
        'error_border': 'rgba(199, 40, 40, 0.45)',
        'error_text': '#991b1b',
        'save_border': 'rgba(189, 120, 0, 0.45)',
        'save_text': '#92400e',
        'elem_error': '#dc2626',
        'quote_border_color': 'rgba(63, 83, 110, 0.55)',
        'quote_nested_color': 'rgba(89, 111, 140, 0.55)',
        'dialog_shadow_op': '0.25',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.45)',
        'carrossel_btn': '#b8b8b8',
        'carrossel_marker_text': '#ffffff',
        'scrollbar_thumb': '#888888',
        'scrollbar_track': '#c8c8c8',
        'scrollbar_hover': '#666666',
        'selection_bg': 'rgba(63, 83, 110, 0.25)',
        'selection_text': '#000000',
        'current_menu_text': '#182332',
        'multiselect_text': 'var(--text-primary)',
        'bbcode_icon_fill': '#4b5563',
        'quoteheader_color': '#374151',
        'disabled_color': '#9ca3af',
    },
    'BJ-NewBlack': {
        'name': 'BJ-NewBlack',
        'desc': 'Evolução moderna do BJ-Black com realces em tons ciano/azul profundo e banner translúcido.',
        'palette': 'Fundo: #14171a, #1c1e22 / Texto: #fff / Realces: #4ba3d9, #2dd4bf',
        'is_dark': True,
        'accent': '#4ba3d9',          # azul ciano / cerúleo elétrico
        'accent_hover': '#78c1ef',
        'accent_soft': 'rgba(75, 163, 217, 0.14)',
        'accent_ring': 'rgba(75, 163, 217, 0.35)',
        'secondary': '#2dd4bf',       # verde-azulado / teal luminoso
        'secondary_soft': 'rgba(45, 212, 191, 0.14)',
        'gold_soft': 'rgba(230, 185, 90, 0.13)',
        'green_soft': 'rgba(65, 200, 130, 0.13)',
        'red_soft': 'rgba(225, 90, 90, 0.13)',
        'accent_border': '#273b4a',
        'text_muted': '#94a3b8',
        'edge': 'rgba(255, 255, 255, 0.06)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 6px 20px rgba(0, 0, 0, 0.45)',
        'head_bg': 'linear-gradient(180deg, #222b34, #182027)',
        'head_color': '',
        'table_shadow': '0 2px 10px rgba(0, 0, 0, 0.35)',
        'menu_bg': 'linear-gradient(180deg, #1c232a, #13181d)',
        'menu_border': '#273b4a',
        'menu_shadow_op': '0.55',
        'dropdown_shadow_op': '0.55',
        'btn_bg': 'linear-gradient(180deg, #242d36, #1a222a)',
        'btn_border': '#2a3c4c',
        'btn_shadow_op': '0.4',
        'btn_hover_bg': 'linear-gradient(180deg, #263e52, #1b2e3e)',
        'btn_hover_border': 'rgba(75, 163, 217, 0.70)',
        'btn_hover_text': '#ffffff',
        'btn_hover_shadow_op': '0.45',
        'btn_active_bg': 'linear-gradient(180deg, #15222d, #1f3343)',
        'submit_text': '#d2edfc',
        'submit_active_bg': 'linear-gradient(180deg, #142533, #1e3648)',
        'input_hover_border': '#3a5369',
        'focus_glow': 'rgba(75, 163, 217, 0.40)',
        'error_border': 'rgba(225, 90, 90, 0.45)',
        'error_text': '#fca5a5',
        'save_border': 'rgba(230, 185, 90, 0.45)',
        'save_text': '#fcd34d',
        'elem_error': '#ef4444',
        'quote_border_color': 'rgba(75, 163, 217, 0.55)',
        'quote_nested_color': 'rgba(45, 212, 191, 0.55)',
        'dialog_shadow_op': '0.6',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.70)',
        'carrossel_btn': '#1c2834',
        'carrossel_marker_text': '#0c1218',
        'scrollbar_thumb': '#2e4556',
        'scrollbar_track': '#11161b',
        'scrollbar_hover': '#3f5d74',
        'selection_bg': 'rgba(75, 163, 217, 0.32)',
        'selection_text': '#ffffff',
        'current_menu_text': 'var(--text-bright)',
        'multiselect_text': 'var(--text-bright)',
        'bbcode_icon_fill': '#8aa4b8',
        'quoteheader_color': '#94a3b8',
        'disabled_color': '#597082',
    },
    'BJ-Pink': {
        'name': 'BJ-Pink',
        'desc': 'Tema vibrante com paleta em tons de rosa, magenta suave e fundos acolhedores.',
        'palette': 'Fundo: #eab3e1, #faf0f8 / Texto: #333 / Realces: #b82e7e, #d9469e',
        'is_dark': False,
        'accent': '#b82e7e',          # magenta refinado / framboesa
        'accent_hover': '#8f1d5e',
        'accent_soft': 'rgba(184, 46, 126, 0.12)',
        'accent_ring': 'rgba(184, 46, 126, 0.28)',
        'secondary': '#d9469e',       # orquídea / rosa vivo
        'secondary_soft': 'rgba(217, 70, 158, 0.12)',
        'gold_soft': 'rgba(204, 126, 0, 0.12)',
        'green_soft': 'rgba(25, 140, 65, 0.12)',
        'red_soft': 'rgba(210, 40, 40, 0.12)',
        'accent_border': '#d4b2cc',
        'text_muted': '#6b7280',
        'edge': 'rgba(255, 255, 255, 0.85)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 4px 16px rgba(128, 40, 85, 0.08)',
        'head_bg': 'linear-gradient(180deg, #fcebf6, #f3d5ea)',
        'head_color': '    color: #691743;\n',
        'table_shadow': '0 1px 6px rgba(128, 40, 85, 0.08)',
        'menu_bg': 'linear-gradient(180deg, #ead0e4, #ddbfd6)',
        'menu_border': '#c9a7c3',
        'menu_shadow_op': '0.12',
        'dropdown_shadow_op': '0.15',
        'btn_bg': 'linear-gradient(180deg, #ffffff, #faedf6)',
        'btn_border': '#d4b5cd',
        'btn_shadow_op': '0.1',
        'btn_hover_bg': 'linear-gradient(180deg, #fcf0f8, #f4d8ed)',
        'btn_hover_border': 'rgba(184, 46, 126, 0.65)',
        'btn_hover_text': '#8f1d5e',
        'btn_hover_shadow_op': '0.14',
        'btn_active_bg': 'linear-gradient(180deg, #ebd1e4, #f8e5f2)',
        'submit_text': '#7a124e',
        'submit_active_bg': 'linear-gradient(180deg, #e4c4dc, #f2d8eb)',
        'input_hover_border': '#b892b0',
        'focus_glow': 'rgba(184, 46, 126, 0.35)',
        'error_border': 'rgba(210, 40, 40, 0.45)',
        'error_text': '#991b1b',
        'save_border': 'rgba(204, 126, 0, 0.45)',
        'save_text': '#92400e',
        'elem_error': '#dc2626',
        'quote_border_color': 'rgba(184, 46, 126, 0.55)',
        'quote_nested_color': 'rgba(217, 70, 158, 0.55)',
        'dialog_shadow_op': '0.2',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.45)',
        'carrossel_btn': '#dfc0d6',
        'carrossel_marker_text': '#ffffff',
        'scrollbar_thumb': '#c496ba',
        'scrollbar_track': '#f7e8f3',
        'scrollbar_hover': '#a37298',
        'selection_bg': 'rgba(184, 46, 126, 0.22)',
        'selection_text': '#000000',
        'current_menu_text': '#8f1d5e',
        'multiselect_text': 'var(--text-primary)',
        'bbcode_icon_fill': '#8d6884',
        'quoteheader_color': '#754b6d',
        'disabled_color': '#aa8aa3',
    },
    'BJ-Red': {
        'name': 'BJ-Red',
        'desc': 'Tema de alto impacto com destaques e bordas em vermelho escarlate e fundo escuro refinado.',
        'palette': 'Fundo: #181515, #221d1d / Texto: #fff / Realces: #e04343, #ff7675',
        'is_dark': True,
        'accent': '#e04343',          # vermelho escarlate / rubi vivo
        'accent_hover': '#f56e6e',
        'accent_soft': 'rgba(224, 67, 67, 0.14)',
        'accent_ring': 'rgba(224, 67, 67, 0.35)',
        'secondary': '#ff7675',       # coral carmesim
        'secondary_soft': 'rgba(255, 118, 117, 0.14)',
        'gold_soft': 'rgba(240, 185, 75, 0.13)',
        'green_soft': 'rgba(60, 195, 115, 0.13)',
        'red_soft': 'rgba(224, 67, 67, 0.15)',
        'accent_border': '#422828',
        'text_muted': '#a89f9f',
        'edge': 'rgba(255, 255, 255, 0.06)',
        'radius': '8px',
        'radius_sm': '6px',
        'lift': '0 6px 20px rgba(0, 0, 0, 0.45)',
        'head_bg': 'linear-gradient(180deg, #2c1f1f, #221616)',
        'head_color': '',
        'table_shadow': '0 2px 10px rgba(0, 0, 0, 0.40)',
        'menu_bg': 'linear-gradient(180deg, #241717, #180e0e)',
        'menu_border': '#422828',
        'menu_shadow_op': '0.55',
        'dropdown_shadow_op': '0.55',
        'btn_bg': 'linear-gradient(180deg, #2c2020, #201616)',
        'btn_border': '#482c2c',
        'btn_shadow_op': '0.4',
        'btn_hover_bg': 'linear-gradient(180deg, #422222, #301717)',
        'btn_hover_border': 'rgba(224, 67, 67, 0.70)',
        'btn_hover_text': '#ffffff',
        'btn_hover_shadow_op': '0.45',
        'btn_active_bg': 'linear-gradient(180deg, #1b0f0f, #2b1818)',
        'submit_text': '#ffd6d6',
        'submit_active_bg': 'linear-gradient(180deg, #221010, #331717)',
        'input_hover_border': '#5c3535',
        'focus_glow': 'rgba(224, 67, 67, 0.40)',
        'error_border': 'rgba(224, 67, 67, 0.45)',
        'error_text': '#fca5a5',
        'save_border': 'rgba(240, 185, 75, 0.45)',
        'save_text': '#fcd34d',
        'elem_error': '#ef4444',
        'quote_border_color': 'rgba(224, 67, 67, 0.55)',
        'quote_nested_color': 'rgba(255, 118, 117, 0.55)',
        'dialog_shadow_op': '0.6',
        'dialog_backdrop': 'rgba(0, 0, 0, 0.70)',
        'carrossel_btn': '#2c1818',
        'carrossel_marker_text': '#ffffff',
        'scrollbar_thumb': '#522d2d',
        'scrollbar_track': '#161010',
        'scrollbar_hover': '#703c3c',
        'selection_bg': 'rgba(224, 67, 67, 0.32)',
        'selection_text': '#ffffff',
        'current_menu_text': 'var(--text-bright)',
        'multiselect_text': 'var(--text-bright)',
        'bbcode_icon_fill': '#a38484',
        'quoteheader_color': '#a89595',
        'disabled_color': '#6e4f4f',
    }
}

SECTION_7_TEMPLATE = """/* ====================================================================
 * SEÇÃO 7: PERSONALIZAÇÕES E OVERRIDES DO TEMA (APLICADOS POR ÚLTIMO)
 * {name} — Pacote de melhorias (v2.1). Estas regras sobrescrevem as
 * seções 2–6 (mesma especificidade + vir depois = vence), por isso ficam
 * juntas no final; cada bloco pode ser removido isoladamente.
 *   7.1 Tokens e Variáveis Adicionais
 *   7.2 Legibilidade e Links
 *   7.3 Profundidade (Caixas, Cabeçalhos e Tabelas)
 *   7.4 Campos e Foco
 *   7.5 Botões, Tabelas e Mensagens de Status
 *   7.6 Menu, Alertas, Citações, Modais e Carrossel
 *   7.7 Conforto (Ícones, Scrollbar, Seleção e Teclado)
 * ==================================================================== */
/* ----------------------------------------------------------------------
 * 7.1 Tokens e Variáveis Adicionais
 * ---------------------------------------------------------------------- */
:root {{
    /* Realce primário do tema */
    --theme-accent: {accent};
    --theme-hover: {accent_hover};
    --theme-soft: {accent_soft};
    --theme-ring: {accent_ring};

    /* Realce secundário */
    --theme-secondary: {secondary};
    --theme-secondary-soft: {secondary_soft};

    /* Versões "tinta" das cores semânticas (fundos de aviso combinam com o tema) */
    --gold-soft: {gold_soft};
    --green-soft: {green_soft};
    --red-soft: {red_soft};

    /* Bordas e contraste */
    --accent: {accent_border};
    --text-muted: {text_muted};

    /* Novos auxiliares */
    --edge: {edge}; /* brilho de 1px no topo */
    --radius: {radius};
    --radius-sm: {radius_sm};
    --lift: {lift};
}}

/* ----------------------------------------------------------------------
 * 7.2 Legibilidade e Links
 * ---------------------------------------------------------------------- */
a:hover {{
    color: var(--theme-hover);
}}

/* Links dentro de texto corrido ganham cor — sublinhado só aparece no hover */
td.body a,
blockquote a,
.torrent_description a,
.wiki_body a {{
    color: var(--theme-accent);
    text-decoration: none;
}}

td.body a:hover,
blockquote a:hover,
.torrent_description a:hover,
.wiki_body a:hover {{
    color: var(--theme-hover);
    text-decoration: underline;
}}

/* Ícones e contraste */
.BBCodeToolbar-icon {{
    fill: {bbcode_icon_fill};
}}

strong.quoteheader {{
    color: {quoteheader_color};
}}

button:disabled,
input[type="button"]:disabled,
input[type="submit"]:disabled {{
    color: {disabled_color};
}}

.multiselect-container > li > a > label.radio,
.multiselect-container > li > a > label.checkbox {{
    color: {multiselect_text};
}}

/* ----------------------------------------------------------------------
 * 7.3 Profundidade (Caixas, Cabeçalhos e Tabelas)
 * ---------------------------------------------------------------------- */
.box,
.box2 {{
    border-radius: var(--radius);
    box-shadow: inset 0 1px 0 var(--edge), var(--lift);
}}

/* Cabeçalho de caixa: leve degradê + barra colorida lateral como "assinatura" */
.head {{
    background: {head_bg};
{head_color}    box-shadow: inset 3px 0 0 var(--theme-accent), inset 0 1px 0 var(--edge);
    padding: 4px 8px;
}}

.box > .head:first-child,
.box2 > .head:first-child {{
    border-radius: calc(var(--radius) - 1px) calc(var(--radius) - 1px) 0 0;
}}

table {{
    box-shadow: {table_shadow};
}}

/* Sem sombra de texto em fundos onde borra a leitura */
tr.torrent,
tr.group,
tr.group_torrent,
tr.season_header,
td.season_header,
tr.resolution_header,
button,
input[type="button"],
input[type="submit"],
.bjqs-controls a,
span.size1,
span.size2,
span.size3,
span.size4,
span.size5,
span.size6,
span.size7,
span.size8,
span.size9,
span.size10 {{
    text-shadow: none;
}}

/* ----------------------------------------------------------------------
 * 7.4 Campos e Foco
 * ---------------------------------------------------------------------- */
/* border-radius / caret em campos de texto (não mexe em botões) */
input:not([type="button"], [type="submit"], [type="reset"], [type="checkbox"], [type="radio"], [type="image"], [type="file"]),
textarea,
select {{
    border-radius: var(--radius-sm);
    caret-color: var(--theme-accent);
}}

input:not([type="button"], [type="submit"], [type="reset"], [type="checkbox"], [type="radio"], [type="image"], [type="file"]),
textarea {{
    padding: 3px 6px;
}}

input:not([type="button"], [type="submit"], [type="reset"], [type="checkbox"], [type="radio"], [type="image"], [type="file"]):hover:not(:focus),
textarea:hover:not(:focus),
select:hover:not(:focus) {{
    border-color: {input_hover_border};
}}

/* Glow de 15px — TODOS os campos de escrita, sem exceção */
input:focus,
form input:focus,
form textarea:focus,
textarea:focus,
textarea:focus-visible,
form button:focus,
select:focus,
.sceditor-container iframe,
.sceditor-container textarea,
.sceditor-container textarea:focus,
[contenteditable="true"]:focus,
[contenteditable="true"]:focus-visible,
#searchbars input:focus,
.edit_changelog textarea:focus {{
    border-color: var(--theme-accent) !important;
    box-shadow: inset 1px 2px 4px var(--shadow-deep), 0 0 15px {focus_glow} !important;
    outline: none !important;
}}

.sceditor-container:focus-within {{
    border: 1px solid var(--theme-accent) !important;
    box-shadow: 0 0 15px {focus_glow} !important;
    outline: none !important;
    border-width: 1px !important;
    border-style: solid !important;
    border-radius: var(--radius-sm);
}}

/* ----------------------------------------------------------------------
 * 7.5 Botões, Tabelas e Mensagens de Status
 * ---------------------------------------------------------------------- */
button,
input[type="button"],
input[type="submit"] {{
    background: {btn_bg};
    border: 1px solid {btn_border};
    border-radius: var(--radius-sm);
    box-shadow: inset 0 1px 0 var(--edge), 0 1px 3px rgba(0, 0, 0, {btn_shadow_op});
    transition: background 0.18s, border-color 0.18s, transform 0.12s ease, box-shadow 0.18s, color 0.18s;
}}

/* Hover: lift + gradiente + borda temática (some ao sair) */
button:hover,
input[type="button"]:hover,
input[type="submit"]:hover,
.btn:hover,
.btn:focus,
.btn-default:hover,
button[onclick="atualizarLancamentos()"]:hover {{
    background: {btn_hover_bg} !important;
    border-color: {btn_hover_border} !important;
    color: {btn_hover_text} !important;
    transform: translateY(-1px);
    box-shadow: inset 0 1px 0 var(--edge), 0 4px 12px rgba(0, 0, 0, {btn_hover_shadow_op}) !important;
}}

/* Pressionado: afunda */
button:active,
input[type="button"]:active,
input[type="submit"]:active {{
    background: {btn_active_bg};
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
    transform: translateY(1px);
}}

/* Submit normal */
input[type="submit"] {{
    color: {submit_text};
}}

input[type="submit"]:active {{
    background: {submit_active_bg};
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.5);
}}

/* Linha de torrent: barra colorida à esquerda no hover ajuda a seguir a linha */
tr.torrent:hover > td:first-child,
tr.group:hover > td:first-child,
tr.group_torrent:hover > td:first-child {{
    box-shadow: inset 3px 0 0 var(--theme-accent);
}}

/* Mensagens: tinta translúcida em vez de blocos saturados */
.error_message {{
    background: var(--red-soft);
    border: 1px solid {error_border};
    color: {error_text};
    border-radius: var(--radius-sm);
    padding: 4px 10px;
}}

.save_message {{
    background: var(--gold-soft);
    border: 1px solid {save_border};
    color: {save_text};
    border-radius: var(--radius-sm);
    padding: 4px 10px;
}}

.elem_error {{
    border: 2px solid {elem_error};
    border-radius: var(--radius-sm);
}}

/* PM não lida */
tr.unreadpm {{
    background-color: var(--theme-soft);
}}

/* ----------------------------------------------------------------------
 * 7.6 Menu, Alertas, Citações, Modais e Carrossel
 * ---------------------------------------------------------------------- */
#menu {{
    background-image: {menu_bg};
    border-bottom: 1px solid {menu_border};
    box-shadow: 0 6px 20px rgba(0, 0, 0, {menu_shadow_op});
}}

#menudrop ul li.current-menu-item {{
    background: var(--theme-soft);
    border-bottom-color: var(--theme-accent);
}}

#menudrop ul li.current-menu-item > a {{
    color: {current_menu_text};
}}

#menudrop ul ul {{
    border: 1px solid {menu_border};
    border-radius: 0 0 var(--radius-sm) var(--radius-sm);
    box-shadow: 0 14px 30px rgba(0, 0, 0, {dropdown_shadow_op});
}}

.alertbar {{
    border-radius: var(--radius-sm);
    border-left: 3px solid var(--theme-accent);
}}

.alertbar a,
table.shoutTable a {{
    color: var(--theme-accent);
}}

.alertbar a:hover {{
    color: var(--theme-hover);
}}

/* Citações: barra colorida; níveis aninhados alternam acento primário/secundário */
blockquote {{
    border-left: 3px solid {quote_border_color};
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}}

blockquote blockquote {{
    border-left-color: {quote_nested_color};
}}

blockquote blockquote blockquote {{
    border-left-color: {quote_border_color};
}}

dialog {{
    border-radius: 12px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, {dialog_shadow_op}), inset 0 1px 0 var(--edge);
}}

dialog::backdrop {{
    background: {dialog_backdrop};
    backdrop-filter: blur(4px);
}}

.curtain {{
    backdrop-filter: blur(3px);
}}

/* Botões do carrossel */
ul.bjqs-controls.v-centered li a {{
    background: {carrossel_btn};
}}

ul.bjqs-controls.v-centered li a:hover {{
    background: var(--theme-soft);
}}

ol.bjqs-markers li.active-marker a,
ol.bjqs-markers li a:hover {{
    background: var(--theme-accent);
    color: {carrossel_marker_text};
}}

/* ----------------------------------------------------------------------
 * 7.7 Conforto (Ícones, Scrollbar, Seleção e Teclado)
 * ---------------------------------------------------------------------- */
/* Ícones Font Awesome (.fad / .fal / .far): lift + press (como os botões).
 * Dentro de <button> o botão já sobe/afunda — o ícone só ganha brilho. */
.fad,
.fal,
.far {{
    display: inline-block;
    transition: transform 0.12s ease, filter 0.18s ease;
}}

a:hover .fad,
a:hover .fal,
a:hover .far,
.fad:hover,
.fal:hover,
.far:hover {{
    transform: translateY(-1px);
}}

a:active .fad,
a:active .fal,
a:active .far,
.fad:active,
.fal:active,
.far:active {{
    transform: translateY(1px);
}}

button:hover .fad,
button:hover .fal,
button:hover .far,
button:active .fad,
button:active .fal,
button:active .far {{
    transform: none;
    filter: brightness(1.12);
}}

html {{
    accent-color: var(--theme-accent); /* checkbox/radio/range */
    scrollbar-width: thin;
    scrollbar-color: {scrollbar_thumb} {scrollbar_track};
}}

::-webkit-scrollbar {{
    width: 10px;
    height: 10px;
}}

::-webkit-scrollbar-track {{
    background: {scrollbar_track};
}}

::-webkit-scrollbar-thumb {{
    background: {scrollbar_thumb};
    border-radius: 6px;
    border: 2px solid {scrollbar_track};
}}

::-webkit-scrollbar-thumb:hover {{
    background: {scrollbar_hover};
}}

::selection {{
    background: var(--theme-ring);
    color: {selection_text};
}}

/* Navegação por teclado: só aparece com Tab, não no clique do mouse */
a:focus-visible,
button:focus-visible,
select:focus-visible,
[tabindex]:focus-visible {{
    outline: 2px solid var(--theme-accent);
    outline-offset: 2px;
    border-radius: 3px;
}}
"""

def generate_dark_blue_base():
    """Build BJ-DarkBlue-new.css based on Midnight base, adjusted to DarkBlue palette."""
    midnight_src = (SRC_DIR / 'BJ-Midnight-new.css').read_text()
    
    # We take up to line 2812 of Midnight
    m_split = midnight_src.find('/* ====================================================================\n * SEÇÃO 7:')
    assert m_split != -1
    base_midnight = midnight_src[:m_split]
    
    # Replace metadata and descriptions
    base_db = base_midnight.replace('Tema: BJ-Midnight', 'Tema: BJ-DarkBlue')
    base_db = re.sub(
        r'Descrição: Tema escuro premium noturno.*?\*/',
        'Descrição: Tema escuro clássico em tons de azul marinho profundo e ardósia,\n *            com realces em azul elétrico e gelo.\n * Paleta principal: Fundo: #151518 / Texto: #C6C7CF / Realces: #5897f5, #38bdf8, #80b3ff\n * \n * ÍNDICE DAS SEÇÕES:\n *   0. VARIÁVEIS DE COR (:root) — preâmbulo, antes da Seção 1\n *   1. DEFAULTS AUXILIARES (@layer bj-defaults)\n *   2. PALETA DE CORES E APARÊNCIA ESPECÍFICA DO TEMA\n *      2.1  Fundo Geral, Tipografia Base e Listas\n *      2.2  Links, Estados de Hover e Artistas Similares\n *      2.3  Formulários, Campos de Entrada e Barra BBCode\n *      2.4  Imagens, Badges de Status e Indicadores de Ratio\n *      2.5  Cabeçalho, Logotipo e Rodapé\n *      2.6  Menu Principal e Menus Dropdown\n *      2.7  Barra de Informações do Usuário e Estatísticas\n *      2.8  Barras de Pesquisa e Notificações de Alerta\n *      2.9  Estrutura de Conteúdo, Caixas e Painéis\n *      2.10 Tabelas, Cabeçalhos e Linhas Alternadas\n *      2.11 Listagem de Torrents, Detalhes e Tópicos\n *      2.12 Citações (Blockquote), Mídia, Enquetes e Fórum\n *      2.13 Chat e Mensagens Rápidas (Shoutbox)\n *      2.14 Botões, Controles e Menus de Seleção\n *      2.15 Atalhos Fixos de Navegação (#irtopo, #irfinal)\n *      2.16 Tooltips Informativos e Caixas Flutuantes\n *      2.17 Sliders e Carrossel de Destaques (BJQS)\n *      2.18 Badges Internos, Modais, Diálogos e Avisos\n *   3. ESTRUTURA GLOBAL E LAYOUT RESPONSIVO (BASE COMUM)\n *      3.1  Reset Global de Box Model e Fundo Base\n *      3.2  Tipografia e Elementos Básicos\n *      3.3  Links e Estados de Texto\n *      3.4  Formulários, Campos e Mídia Básica\n *      3.5  Chat, Formulários e Controles\n *      3.6  Indicadores de Ratio\n *      3.7  Tamanhos BBCode\n *      3.8  Estrutura Principal da Página\n *      3.9  Menu Principal e Dropdowns\n *      3.10 Barra de Usuário e Estatísticas (#userinfo)\n *      3.11 Busca, Alertas e Seletores (#searchbars, #alerts)\n *      3.12 Utilitários de Visibilidade e Alinhamento\n *      3.13 Containers, Caixas, Sidebar e Imagens\n *      3.14 Tabelas, Cabeçalhos e Mensagens\n *      3.15 Listagem e Filtros de Torrents\n *      3.16 Citações e Mídia Embutida\n *      3.17 Fórum, Leitura e Estados de Tópicos\n *      3.18 Permissões, Enquetes e Overlays\n *      3.19 Selects, Multiselect e Dropdowns\n *      3.20 Atalhos Fixos de Navegação (#irtopo, #irfinal)\n *      3.21 Tooltips BJinfoBox e Data-Tooltip\n *      3.22 Info Boxes e Imagens de Destaque\n *      3.23 Slider BJQS e Carrossel\n *      3.24 Marcadores Internos e Labels de Torrent\n *      3.25 Diálogos e Modais\n *      3.26 Animações nos Botões (Lift + Press e Botões Destrutivos)\n *      3.27 Acessibilidade: Respeita Redução de Movimento\n *      3.28 Alertas e Ajustes Finais\n *   4. CONTROLE DO MENU FIXO (STICKY NAVIGATION)\n *      Controlado por classe no <body> (.bj-sticky-menu) — ver Seção 4 e o script de toggle.\n *   5. MEDIA QUERIES E RESPONSIVIDADE (MOBILE / TABLET / 4K)\n *   6. AJUSTES FINAIS DE LAYOUT E COMPATIBILIDADE MOBILE\n *   7. PERSONALIZAÇÕES E OVERRIDES DO TEMA (aplicados por último)\n *\n * ==================================================================== */',
        base_db,
        flags=re.DOTALL
    )

    # Adjust Section 0 :root
    db_root = """:root {
    /* Texto — família azul-acinzentada clássica */
    --text-primary: #C6C7CF;
    --text-bright: #e8ecf4;
    --text-muted: #8b8f9e;
    --text-secondary: #bfc4d2;
    --text-5: #C6C7CF;
    --text-6: #9499a8;
    --text-7: #d2d6e4;

    /* Sombras */
    --shadow: rgba(0, 0, 0, 0.50);
    --shadow-soft: #000;
    --shadow-strong: rgba(0, 0, 0, 0.40);
    --shadow-deep: rgba(0, 0, 0, 0.30);
    --shadow-5: #5897f5;
    --shadow-6: rgba(0, 0, 0, 0.50);
    --shadow-7: rgba(0, 0, 0, 0.70);

    /* Superfícies — escada azul-marinho ardósia */
    --accent-4: #151518; /* body */
    --accent-5: #181b24; /* menu / input / footer */
    --accent-alt: #1c202d; /* boxes / painéis */
    --accent-6: #202434; /* headers / colhead */
    --accent-7: #252b3d; /* rows / torrents / secondary */
    --accent-3: #2d344a; /* hover / elevated */
    --accent: #333c54; /* bordas */
    --accent-8: #5897f5; /* focus / active blue */

    /* Realces semânticos */
    --gold: #fcd34d;
    --green: #4ade80;
    --red: #f87171;
    color-scheme: dark;
}"""
    base_db = re.sub(r':root\s*\{[^}]+\}', db_root, base_db, count=1)
    return base_db

def main():
    print("Iniciando geração das marcações e barras para os temas...")
    
    # 1. First, create BJ-DarkBlue-new.css base if not present
    db_base = generate_dark_blue_base()
    (SRC_DIR / 'BJ-DarkBlue-new.css').write_text(db_base + "\n/* Placeholder */\n")
    
    # 2. Process each theme
    all_theme_files = {}
    
    for theme_key, cfg in THEMES.items():
        src_file = SRC_DIR / f"{theme_key}-new.css"
        assert src_file.exists(), f"Arquivo não encontrado: {src_file}"
        content = src_file.read_text()
        
        # Cut cleanly at the exact end of Section 6 (the alertbar mobile media query)
        sec6_marker = '.alertbar {\n        max-width: 100%;\n    }\n}'
        cut_point = content.find(sec6_marker)
        assert cut_point != -1, f"Ponto de corte da Seção 6 não encontrado em {theme_key}"
        base_content = content[:cut_point + len(sec6_marker)].rstrip()
        
        # Format Section 7
        sec7 = SECTION_7_TEMPLATE.format(**cfg)
        
        # Combine
        full_content = base_content + "\n\n" + sec7
        
        # Save to css-barras-marcacoes
        src_file.write_text(full_content)
        print(f"✓ Atualizado: {src_file.name} ({len(full_content.splitlines())} linhas)")
        all_theme_files[theme_key] = full_content

    # Midnight is preserved as the model (already has Section 7)
    midnight_file = SRC_DIR / 'BJ-Midnight-new.css'
    all_theme_files['BJ-Midnight'] = midnight_file.read_text()
    print(f"✓ Mantido como referência: {midnight_file.name}")
    
    # 3. Copy all 10 files to root with Pages naming: BJ-<Name>.css
    for theme_name, content in all_theme_files.items():
        root_dest = ROOT / f"{theme_name}.css"
        root_dest.write_text(content)
        print(f"✓ Copiado para a raiz: {root_dest.name}")
        
        # Also sync BJ-organized
        org_dest = ORGANIZED_DIR / f"{theme_name}-organized.css"
        org_dest.write_text(content)

    print("\nTodos os 10 arquivos foram gerados e copiados para a raiz!")

if __name__ == '__main__':
    main()
