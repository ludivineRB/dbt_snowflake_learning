#!/usr/bin/env python3
"""Generate all diagrams for the DataWarehouse course modules."""
import os
import graphviz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

# ── Couleurs ──
BLUE = "#3B82F6"
DARK_BLUE = "#1E3A5F"
LIGHT_BLUE = "#DBEAFE"
GREEN = "#10B981"
LIGHT_GREEN = "#D1FAE5"
ORANGE = "#F59E0B"
LIGHT_ORANGE = "#FEF3C7"
RED = "#EF4444"
GRAY = "#6B7280"
LIGHT_GRAY = "#F3F4F6"
GOLD = "#F59E0B"
SILVER = "#9CA3AF"
BRONZE = "#CD7F32"


def save_graphviz(g, path):
    """Render graphviz and save to path (without .png extension in path arg)."""
    g.render(path, format='png', cleanup=True)
    print(f"  ✓ {os.path.basename(path)}.png")


# ═══════════════════════════════════════════════
# MODULE 01 - Introduction
# ═══════════════════════════════════════════════
def gen_01():
    print("Module 01...")
    out = os.path.join(IMG, "01")

    # 1. Silos de données
    g = graphviz.Digraph('silos', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Le problème des silos de données',
        'labelloc': 't', 'fontsize': '20', 'fontname': 'Helvetica-Bold',
        'pad': '0.5', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '12', 'style': 'filled'},
       edge_attr={'color': '#999999'})

    g.node('erp', 'ERP\n(Oracle)', fillcolor='#BFDBFE', shape='box', width='2')
    g.node('crm', 'CRM\n(Salesforce)', fillcolor='#D1FAE5', shape='box', width='2')
    g.node('ecom', 'E-commerce\n(Shopify)', fillcolor='#FEF3C7', shape='box', width='2')
    g.node('f1', 'Formats\ndifférents', shape='ellipse', fillcolor='#FEE2E2')
    g.node('f2', 'Formats\ndifférents', shape='ellipse', fillcolor='#FEE2E2')
    g.node('f3', 'Formats\ndifférents', shape='ellipse', fillcolor='#FEE2E2')

    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('erp')
        s.node('crm')
        s.node('ecom')

    g.edge('erp', 'f1')
    g.edge('crm', 'f2')
    g.edge('ecom', 'f3')

    g.node('prob', 'Données dispersées\net incohérentes', shape='box',
           fillcolor='#FCA5A5', fontcolor='white', style='filled,bold')
    g.edge('f1', 'prob', style='dashed')
    g.edge('f2', 'prob', style='dashed')
    g.edge('f3', 'prob', style='dashed')

    save_graphviz(g, os.path.join(out, 'silos-donnees'))

    # 2. Centralisation DW
    g = graphviz.Digraph('central', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'La solution : centralisation',
        'labelloc': 't', 'fontsize': '20', 'fontname': 'Helvetica-Bold',
        'pad': '0.5', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '12', 'style': 'filled'},
       edge_attr={'color': '#4B5563'})

    for n, lbl, col in [('erp', 'ERP', '#BFDBFE'), ('crm', 'CRM', '#D1FAE5'), ('ecom', 'E-commerce', '#FEF3C7')]:
        g.node(n, lbl, fillcolor=col, shape='box', width='1.8')

    g.node('etl', 'ETL / ELT', fillcolor='#FDE68A', shape='box', width='2.5',
           fontsize='14', style='filled,bold')
    g.node('dw', 'DATA WAREHOUSE\n(Vue unifiée)', fillcolor='#1E3A5F', fontcolor='white',
           shape='box', width='4', height='1', fontsize='16', style='filled,bold')

    for n, lbl, col in [('bi', 'BI\nDashboards', '#DBEAFE'), ('rep', 'Reports', '#DBEAFE'), ('ml', 'Machine\nLearning', '#DBEAFE')]:
        g.node(n, lbl, fillcolor=col, shape='box', width='1.8')

    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('erp'); s.node('crm'); s.node('ecom')
    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('bi'); s.node('rep'); s.node('ml')

    for n in ['erp', 'crm', 'ecom']:
        g.edge(n, 'etl')
    g.edge('etl', 'dw')
    for n in ['bi', 'rep', 'ml']:
        g.edge('dw', n)

    save_graphviz(g, os.path.join(out, 'centralisation-dw'))

    # 3. DW vs Data Lake vs Lakehouse
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.axis('off')

    cols = [('#1E3A5F', 'Data Warehouse'), ('#065F46', 'Data Lake'), ('#7C3AED', 'Lakehouse')]
    props = [
        ['Données structurées', 'Toutes données (brutes)', 'Toutes données'],
        ['Schema-on-write', 'Schema-on-read', 'Schema flexible'],
        ['SQL', 'SQL, Python, Spark', 'SQL + Python + ML'],
        ['Coût élevé', 'Coût bas', 'Coût optimisé'],
        ['Qualité haute', 'Qualité variable', 'Qualité + ACID'],
    ]
    labels = ['Structure', 'Schema', 'Traitement', 'Coût', 'Qualité']

    for i, (color, title) in enumerate(cols):
        x = 0.05 + i * 0.32
        ax.add_patch(FancyBboxPatch((x, 0.78), 0.28, 0.15, boxstyle="round,pad=0.02",
                                     facecolor=color, edgecolor='none'))
        ax.text(x + 0.14, 0.855, title, ha='center', va='center', fontsize=16,
                fontweight='bold', color='white')

    for j, (label, row) in enumerate(zip(labels, props)):
        y = 0.62 - j * 0.14
        ax.text(0.02, y + 0.04, label, ha='left', va='center', fontsize=11,
                fontweight='bold', color='#374151')
        for i, val in enumerate(row):
            x = 0.05 + i * 0.32
            bg = ['#EBF5FF', '#ECFDF5', '#F5F3FF'][i]
            ax.add_patch(FancyBboxPatch((x, y - 0.01), 0.28, 0.1, boxstyle="round,pad=0.01",
                                         facecolor=bg, edgecolor='#D1D5DB'))
            ax.text(x + 0.14, y + 0.04, val, ha='center', va='center', fontsize=10, color='#1F2937')

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.1, 1)
    fig.suptitle('Data Warehouse vs Data Lake vs Lakehouse', fontsize=18, fontweight='bold', y=0.98)
    fig.savefig(os.path.join(out, 'dw-vs-datalake.png'), dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print("  ✓ dw-vs-datalake.png")


# ═══════════════════════════════════════════════
# MODULE 02 - OLTP vs OLAP
# ═══════════════════════════════════════════════
def gen_02():
    print("Module 02...")
    out = os.path.join(IMG, "02")

    # 1. OLTP vs OLAP
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for ax, title, color, bg, items in [
        (ax1, 'SYSTÈME OLTP', BLUE, '#EBF5FF', [
            'Objectif : Opérations quotidiennes',
            'Transactions courtes et fréquentes',
            'CRUD (Create, Read, Update, Delete)',
            'Accès à quelques lignes à la fois',
            'Haute disponibilité (99.99%)',
            'Temps de réponse < 1 seconde',
            'Modélisation normalisée (3NF)',
            'Exemples : PostgreSQL, MySQL, Oracle'
        ]),
        (ax2, 'SYSTÈME OLAP', ORANGE, '#FEF9E7', [
            'Objectif : Analyser pour décider',
            'Requêtes complexes sur gros volumes',
            'Agrégations, calculs, comparaisons',
            'Accès à millions de lignes',
            'Lecture intensive (peu d\'écriture)',
            'Temps de réponse : sec. à min.',
            'Modélisation dénormalisée (Star)',
            'Exemples : BigQuery, Snowflake'
        ])
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.03",
                                     facecolor=bg, edgecolor=color, linewidth=3))
        ax.text(0.5, 0.9, title, ha='center', va='center', fontsize=18,
                fontweight='bold', color=color)
        ax.plot([0.1, 0.9], [0.83, 0.83], color=color, linewidth=2)
        for i, item in enumerate(items):
            marker = '●' if i == 0 else '○'
            weight = 'bold' if i == 0 else 'normal'
            ax.text(0.1, 0.75 - i * 0.09, f'{marker}  {item}', ha='left', va='center',
                    fontsize=11, color='#1F2937', fontweight=weight)

    fig.suptitle('OLTP vs OLAP', fontsize=22, fontweight='bold', y=0.98)
    fig.savefig(os.path.join(out, 'oltp-vs-olap.png'), dpi=150, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  ✓ oltp-vs-olap.png")

    # 2. Star Schema
    g = graphviz.Digraph('star', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Star Schema (Schéma en étoile)',
        'labelloc': 't', 'fontsize': '20', 'fontname': 'Helvetica-Bold',
        'dpi': '150', 'pad': '0.5', 'nodesep': '1', 'ranksep': '1.2'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'shape': 'record', 'style': 'filled'})

    g.node('fact', '{FACT_SALES|product_key (FK)|customer_key (FK)|date_key (FK)|store_key (FK)|quantity|amount}',
           fillcolor='#FDE68A', color='#F59E0B')
    g.node('date', '{DIM_DATE|date_key (PK)|date|year|quarter|month|is_holiday}',
           fillcolor='#DBEAFE', color='#3B82F6')
    g.node('prod', '{DIM_PRODUCT|product_key (PK)|name|category|brand|price}',
           fillcolor='#DBEAFE', color='#3B82F6')
    g.node('cust', '{DIM_CUSTOMER|customer_key (PK)|name|email|segment|region}',
           fillcolor='#DBEAFE', color='#3B82F6')
    g.node('store', '{DIM_STORE|store_key (PK)|store_name|city|country}',
           fillcolor='#DBEAFE', color='#3B82F6')

    g.edge('fact', 'date', label='FK', color='#3B82F6', dir='forward')
    g.edge('fact', 'prod', label='FK', color='#3B82F6', dir='forward')
    g.edge('fact', 'cust', label='FK', color='#3B82F6', dir='forward')
    g.edge('fact', 'store', label='FK', color='#3B82F6', dir='forward')

    save_graphviz(g, os.path.join(out, 'star-schema'))

    # 3. Row vs Column storage
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    data = [
        ['1', 'Alice', 'Paris', '100'],
        ['2', 'Bob', 'Lyon', '200'],
        ['3', 'Carol', 'Paris', '150'],
        ['4', 'David', 'Lyon', '300'],
    ]
    cols_h = ['id', 'nom', 'region', 'amount']

    # Row-based
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1); ax1.axis('off')
    ax1.set_title('Row-based (OLTP)', fontsize=16, fontweight='bold', color=BLUE, pad=15)
    for i, row in enumerate(data):
        y = 0.8 - i * 0.18
        for j, val in enumerate(row):
            x = 0.05 + j * 0.23
            color = '#FEE2E2' if j in [2, 3] else '#F3F4F6'
            ax1.add_patch(FancyBboxPatch((x, y), 0.2, 0.12, boxstyle="round,pad=0.01",
                                          facecolor=color, edgecolor='#D1D5DB'))
            ax1.text(x + 0.1, y + 0.06, val, ha='center', va='center', fontsize=10)
    for j, col in enumerate(cols_h):
        ax1.text(0.05 + j * 0.23 + 0.1, 0.96, col, ha='center', va='center',
                 fontsize=10, fontweight='bold', color='#374151')
    ax1.text(0.5, 0.05, 'Lit TOUTES les colonnes → I/O inutile', ha='center',
             fontsize=11, color=RED, fontweight='bold')

    # Column-based
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')
    ax2.set_title('Column-based (OLAP)', fontsize=16, fontweight='bold', color=ORANGE, pad=15)
    for j, col in enumerate(cols_h):
        x = 0.05 + j * 0.23
        is_used = col in ['region', 'amount']
        for i, row in enumerate(data):
            y = 0.65 - i * 0.14
            color = '#D1FAE5' if is_used else '#F3F4F6'
            border = '#10B981' if is_used else '#D1D5DB'
            ax2.add_patch(FancyBboxPatch((x, y), 0.2, 0.1, boxstyle="round,pad=0.01",
                                          facecolor=color, edgecolor=border, linewidth=1.5 if is_used else 1))
            ax2.text(x + 0.1, y + 0.05, row[j], ha='center', va='center', fontsize=10)
        ax2.text(x + 0.1, 0.85, col, ha='center', va='center', fontsize=10, fontweight='bold',
                 color=GREEN if is_used else '#374151')
    ax2.text(0.5, 0.05, 'Lit SEULEMENT region + amount → I/O minimal', ha='center',
             fontsize=11, color=GREEN, fontweight='bold')

    fig.suptitle('Stockage Row-based vs Column-based', fontsize=18, fontweight='bold', y=1.02)
    fig.savefig(os.path.join(out, 'row-vs-column.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ row-vs-column.png")


# ═══════════════════════════════════════════════
# MODULE 03 - Modélisation
# ═══════════════════════════════════════════════
def gen_03():
    print("Module 03...")
    out = os.path.join(IMG, "03")

    # 1. Snowflake schema
    g = graphviz.Digraph('snowflake', graph_attr={
        'rankdir': 'LR', 'bgcolor': 'white', 'label': 'Snowflake Schema (Schéma en flocon)',
        'labelloc': 't', 'fontsize': '20', 'fontname': 'Helvetica-Bold',
        'dpi': '150', 'pad': '0.5'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '10', 'shape': 'record', 'style': 'filled'})

    g.node('fact', '{FACT_SALES|product_key (FK)|amount|quantity}',
           fillcolor='#FDE68A', color='#F59E0B')
    g.node('prod', '{DIM_PRODUCT|product_key (PK)|product_name|category_key (FK)|brand_key (FK)}',
           fillcolor='#DBEAFE', color='#3B82F6')
    g.node('cat', '{DIM_CATEGORY|category_key (PK)|category_name|department}',
           fillcolor='#D1FAE5', color='#10B981')
    g.node('brand', '{DIM_BRAND|brand_key (PK)|brand_name|origin_country}',
           fillcolor='#D1FAE5', color='#10B981')

    g.edge('fact', 'prod', label='FK', color='#3B82F6')
    g.edge('prod', 'cat', label='FK', color='#10B981')
    g.edge('prod', 'brand', label='FK', color='#10B981')

    save_graphviz(g, os.path.join(out, 'snowflake-schema'))

    # 2. SCD Type 2
    fig, ax = plt.subplots(1, 1, figsize=(14, 5))
    ax.axis('off')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.suptitle('SCD Type 2 — Historisation complète', fontsize=18, fontweight='bold')

    headers = ['customer_key', 'customer_id', 'segment', 'valid_from', 'valid_to', 'is_current']
    row1 = ['1', 'C12345', 'Silver', '2020-01-01', '2024-03-15', 'false']
    row2 = ['2', 'C12345', 'Gold', '2024-03-15', '9999-12-31', 'true']
    widths = [0.14, 0.13, 0.1, 0.14, 0.14, 0.12]

    for j, (h, w) in enumerate(zip(headers, widths)):
        x = 0.07 + sum(widths[:j])
        ax.add_patch(FancyBboxPatch((x, 0.68), w - 0.01, 0.1, boxstyle="round,pad=0.005",
                                     facecolor='#1E3A5F', edgecolor='none'))
        ax.text(x + w / 2 - 0.005, 0.73, h, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white')

    for j, (v, w) in enumerate(zip(row1, widths)):
        x = 0.07 + sum(widths[:j])
        ax.add_patch(FancyBboxPatch((x, 0.54), w - 0.01, 0.1, boxstyle="round,pad=0.005",
                                     facecolor='#FEE2E2', edgecolor='#E5E7EB'))
        ax.text(x + w / 2 - 0.005, 0.59, v, ha='center', va='center', fontsize=9, color='#6B7280')

    for j, (v, w) in enumerate(zip(row2, widths)):
        x = 0.07 + sum(widths[:j])
        ax.add_patch(FancyBboxPatch((x, 0.40), w - 0.01, 0.1, boxstyle="round,pad=0.005",
                                     facecolor='#D1FAE5', edgecolor='#10B981'))
        ax.text(x + w / 2 - 0.005, 0.45, v, ha='center', va='center', fontsize=9,
                fontweight='bold', color='#065F46')

    ax.annotate('Changement\nde segment', xy=(0.45, 0.54), xytext=(0.45, 0.30),
                fontsize=11, color=RED, fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color=RED, lw=2))

    ax.text(0.5, 0.18, 'Ancien enregistrement clôturé (is_current = false)\n'
            'Nouvel enregistrement créé (is_current = true)',
            ha='center', fontsize=10, color='#4B5563', style='italic')

    fig.savefig(os.path.join(out, 'scd-type2.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ scd-type2.png")

    # 3. Fact vs Dimension
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))
    ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    ax.add_patch(FancyBboxPatch((0.02, 0.1), 0.4, 0.8, boxstyle="round,pad=0.03",
                                 facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=2))
    ax.text(0.22, 0.82, 'TABLE DE FAITS', ha='center', fontsize=16, fontweight='bold', color='#92400E')
    ax.text(0.22, 0.70, 'Mesures quantitatives', ha='center', fontsize=12, color='#78350F')
    for i, txt in enumerate(['Montants (SUM)', 'Quantités (COUNT)', 'Ratios (AVG)', 'Métriques business']):
        ax.text(0.12, 0.55 - i * 0.1, f'●  {txt}', fontsize=11, color='#451A03')

    ax.add_patch(FancyBboxPatch((0.58, 0.1), 0.4, 0.8, boxstyle="round,pad=0.03",
                                 facecolor='#DBEAFE', edgecolor='#3B82F6', linewidth=2))
    ax.text(0.78, 0.82, 'TABLE DE DIMENSIONS', ha='center', fontsize=16, fontweight='bold', color='#1E40AF')
    ax.text(0.78, 0.70, 'Contexte descriptif', ha='center', fontsize=12, color='#1E3A8A')
    for i, txt in enumerate(['Qui ? (Client)', 'Quoi ? (Produit)', 'Quand ? (Date)', 'Où ? (Lieu)']):
        ax.text(0.68, 0.55 - i * 0.1, f'●  {txt}', fontsize=11, color='#1E3A5F')

    ax.annotate('', xy=(0.58, 0.5), xytext=(0.42, 0.5),
                arrowprops=dict(arrowstyle='<->', color='#6B7280', lw=2.5))
    ax.text(0.50, 0.53, 'FK', ha='center', fontsize=12, fontweight='bold', color='#6B7280')

    fig.suptitle('Tables de Faits vs Dimensions', fontsize=18, fontweight='bold')
    fig.savefig(os.path.join(out, 'fact-vs-dimension.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ fact-vs-dimension.png")


# ═══════════════════════════════════════════════
# MODULE 04 - Architectures
# ═══════════════════════════════════════════════
def gen_04():
    print("Module 04...")
    out = os.path.join(IMG, "04")

    # 1. Inmon Top-Down
    g = graphviz.Digraph('inmon', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Bill Inmon — Top-Down (Enterprise DW)',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled', 'shape': 'box'})

    for s in ['ERP', 'CRM', 'Files']:
        g.node(f's_{s}', s, fillcolor=LIGHT_GRAY, color=GRAY)
    g.node('etl', 'ETL', fillcolor='#FDE68A', color=ORANGE, width='3', fontsize='14')
    g.node('dw', 'Enterprise Data Warehouse\n(Normalisé 3NF)\nSource unique de vérité',
           fillcolor=DARK_BLUE, fontcolor='white', width='5', fontsize='13')
    for m in ['Finance', 'Ventes', 'Marketing']:
        g.node(f'm_{m}', f'Data Mart\n{m}', fillcolor=LIGHT_BLUE, color=BLUE)

    with g.subgraph() as s:
        s.attr(rank='same')
        for n in ['ERP', 'CRM', 'Files']:
            s.node(f's_{n}')
    with g.subgraph() as s:
        s.attr(rank='same')
        for n in ['Finance', 'Ventes', 'Marketing']:
            s.node(f'm_{n}')

    for n in ['ERP', 'CRM', 'Files']:
        g.edge(f's_{n}', 'etl')
    g.edge('etl', 'dw')
    for n in ['Finance', 'Ventes', 'Marketing']:
        g.edge('dw', f'm_{n}')

    save_graphviz(g, os.path.join(out, 'inmon-top-down'))

    # 2. Kimball Bottom-Up
    g = graphviz.Digraph('kimball', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Ralph Kimball — Bottom-Up (Dimensional)',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled', 'shape': 'box'})

    for s in ['ERP', 'CRM', 'Files']:
        g.node(f's_{s}', s, fillcolor=LIGHT_GRAY, color=GRAY)
    for i, m in enumerate(['Ventes', 'Finance', 'Marketing']):
        g.node(f'etl_{i}', 'ETL', fillcolor='#FDE68A', color=ORANGE)
        g.node(f'm_{m}', f'Data Mart {m}\n(Star Schema)', fillcolor=LIGHT_BLUE, color=BLUE)

    g.node('dw', 'DATA WAREHOUSE\n(Conformed Dimensions)', fillcolor=DARK_BLUE,
           fontcolor='white', width='5', fontsize='13')

    for i, (s, m) in enumerate(zip(['ERP', 'CRM', 'Files'], ['Ventes', 'Finance', 'Marketing'])):
        g.edge(f's_{s}', f'etl_{i}')
        g.edge(f'etl_{i}', f'm_{m}')
        g.edge(f'm_{m}', 'dw')

    save_graphviz(g, os.path.join(out, 'kimball-bottom-up'))

    # 3. Lakehouse
    g = graphviz.Digraph('lakehouse', graph_attr={
        'rankdir': 'BT', 'bgcolor': 'white', 'label': 'Architecture Lakehouse',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150',
        'compound': 'true'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled', 'shape': 'box'})

    g.node('storage', 'Object Storage (S3, GCS, ADLS)\nParquet, ORC, Delta',
           fillcolor=LIGHT_GRAY, color=GRAY, width='8')
    g.node('delta', 'Delta Lake / Apache Iceberg\nACID Transactions • Time Travel • Schema Evolution',
           fillcolor='#DBEAFE', color=BLUE, width='8')

    with g.subgraph() as s:
        s.attr(rank='same')
        s.node('sql', 'SQL\nEngine', fillcolor='#D1FAE5', color=GREEN, width='2')
        s.node('spark', 'Python\nSpark', fillcolor='#D1FAE5', color=GREEN, width='2')
        s.node('ml', 'ML\nTraining', fillcolor='#D1FAE5', color=GREEN, width='2')

    g.node('meta', 'Unified Metadata Layer\n(Unity Catalog / Iceberg / Hive Metastore)',
           fillcolor=DARK_BLUE, fontcolor='white', width='8')

    g.edge('storage', 'delta')
    for n in ['sql', 'spark', 'ml']:
        g.edge('delta', n)
        g.edge(n, 'meta')

    save_graphviz(g, os.path.join(out, 'lakehouse'))

    # 4. Lambda vs Kappa
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    for ax, title, color, layers in [
        (ax1, 'Architecture Lambda', BLUE, [
            ('Sources', 0.9, '#F3F4F6'),
            ('Speed Layer\n(Streaming: Kafka/Flink)', 0.65, '#DBEAFE'),
            ('Batch Layer\n(ETL: Spark/Airflow)', 0.65, '#BFDBFE'),
            ('Serving Layer\n(Combined)', 0.40, '#93C5FD'),
            ('Queries', 0.18, '#1E3A5F'),
        ]),
        (ax2, 'Architecture Kappa', GREEN, [
            ('Sources', 0.9, '#F3F4F6'),
            ('Event Stream\n(Kafka)', 0.72, '#D1FAE5'),
            ('Stream Processing\n(Real-time + Micro-batch + ML)', 0.52, '#A7F3D0'),
            ('Serving Layer', 0.32, '#6EE7B7'),
            ('Queries', 0.15, '#065F46'),
        ])
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=color, pad=10)
        for label, y, bg in layers:
            fc = 'white' if bg in ['#1E3A5F', '#065F46'] else '#1F2937'
            ax.add_patch(FancyBboxPatch((0.08, y - 0.07), 0.84, 0.12,
                                         boxstyle="round,pad=0.02", facecolor=bg, edgecolor=color))
            ax.text(0.5, y - 0.01, label, ha='center', va='center', fontsize=11,
                    color=fc, fontweight='bold')

    # Lambda special: split speed/batch
    ax1.add_patch(FancyBboxPatch((0.08, 0.58), 0.38, 0.12,
                                  boxstyle="round,pad=0.02", facecolor='#DBEAFE', edgecolor=BLUE))
    ax1.text(0.27, 0.64, 'Speed Layer\n(Streaming)', ha='center', fontsize=10, fontweight='bold')
    ax1.add_patch(FancyBboxPatch((0.54, 0.58), 0.38, 0.12,
                                  boxstyle="round,pad=0.02", facecolor='#BFDBFE', edgecolor=BLUE))
    ax1.text(0.73, 0.64, 'Batch Layer\n(ETL daily)', ha='center', fontsize=10, fontweight='bold')
    # Cover the original combined layer
    ax1.add_patch(FancyBboxPatch((0.08, 0.58), 0.84, 0.12,
                                  boxstyle="round,pad=0.02", facecolor='white', edgecolor='white'))
    ax1.add_patch(FancyBboxPatch((0.08, 0.58), 0.38, 0.12,
                                  boxstyle="round,pad=0.02", facecolor='#DBEAFE', edgecolor=BLUE))
    ax1.text(0.27, 0.64, 'Speed Layer\n(Streaming)', ha='center', fontsize=10, fontweight='bold')
    ax1.add_patch(FancyBboxPatch((0.54, 0.58), 0.38, 0.12,
                                  boxstyle="round,pad=0.02", facecolor='#BFDBFE', edgecolor=BLUE))
    ax1.text(0.73, 0.64, 'Batch Layer\n(ETL daily)', ha='center', fontsize=10, fontweight='bold')

    fig.suptitle('Lambda vs Kappa', fontsize=20, fontweight='bold', y=1.01)
    fig.savefig(os.path.join(out, 'lambda-kappa.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ lambda-kappa.png")


# ═══════════════════════════════════════════════
# MODULE 05 - Opérations OLAP
# ═══════════════════════════════════════════════
def gen_05():
    print("Module 05...")
    out = os.path.join(IMG, "05")

    # 1. ROLAP / MOLAP / HOLAP
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    configs = [
        ('ROLAP', '#3B82F6', '#EBF5FF', [
            ('Base relationnelle\n(PostgreSQL, BigQuery)', 0.25, '#DBEAFE'),
            ('Couche OLAP\n(SQL à la volée)', 0.65, '#93C5FD'),
        ], 'Dominant\naujourd\'hui (Cloud)'),
        ('MOLAP', '#F59E0B', '#FEF9E7', [
            ('Cube multidimensionnel\n(pré-calculé)', 0.45, '#FDE68A'),
        ], 'En déclin\n(cubes SSAS)'),
        ('HOLAP', '#10B981', '#ECFDF5', [
            ('Base ROLAP\n(données détail)', 0.25, '#A7F3D0'),
            ('Cube MOLAP\n(agrégations)', 0.65, '#6EE7B7'),
        ], 'Hybride\n(niche)'),
    ]
    for ax, (title, color, bg, layers, trend) in zip(axes, configs):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.03",
                                     facecolor=bg, edgecolor=color, linewidth=2))
        ax.text(0.5, 0.92, title, ha='center', fontsize=18, fontweight='bold', color=color)
        for label, y, lc in layers:
            ax.add_patch(FancyBboxPatch((0.1, y - 0.08), 0.8, 0.18,
                                         boxstyle="round,pad=0.02", facecolor=lc, edgecolor=color))
            ax.text(0.5, y + 0.01, label, ha='center', fontsize=10, fontweight='bold')
        ax.text(0.5, 0.08, trend, ha='center', fontsize=9, color=GRAY, style='italic')

    fig.suptitle('Approches OLAP : ROLAP vs MOLAP vs HOLAP', fontsize=18, fontweight='bold', y=1.01)
    fig.savefig(os.path.join(out, 'rolap-molap-holap.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ rolap-molap-holap.png")

    # 2. Slice vs Dice
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    for ax, title, desc, color in [
        (ax1, 'SLICE (Trancher)', 'Fixer UNE dimension\nWHERE catégorie = \'Électro\'', BLUE),
        (ax2, 'DICE (Découper)', 'Filtrer PLUSIEURS dimensions\nWHERE cat IN (...)\nAND trim IN (...)\nAND region = ...', ORANGE),
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=color, pad=15)

        # Simplified cube representation
        cube_pts = np.array([[0.2, 0.2], [0.7, 0.2], [0.7, 0.7], [0.2, 0.7]])
        back_pts = cube_pts + np.array([0.15, 0.15])
        # Back face
        ax.fill([p[0] for p in back_pts], [p[1] for p in back_pts], color='#E5E7EB', alpha=0.5)
        ax.plot([p[0] for p in list(back_pts) + [back_pts[0]]],
                [p[1] for p in list(back_pts) + [back_pts[0]]], color='#9CA3AF')
        # Connecting lines
        for f, b in zip(cube_pts, back_pts):
            ax.plot([f[0], b[0]], [f[1], b[1]], color='#9CA3AF', linestyle='--')
        # Front face
        ax.fill([p[0] for p in cube_pts], [p[1] for p in cube_pts], color='#F3F4F6', alpha=0.8)
        ax.plot([p[0] for p in list(cube_pts) + [cube_pts[0]]],
                [p[1] for p in list(cube_pts) + [cube_pts[0]]], color='#6B7280', linewidth=2)

    # Slice highlight
    ax1.fill([0.2, 0.7, 0.7, 0.2], [0.35, 0.35, 0.55, 0.55], color=BLUE, alpha=0.3)
    ax1.plot([0.2, 0.7], [0.35, 0.35], color=BLUE, linewidth=2)
    ax1.plot([0.2, 0.7], [0.55, 0.55], color=BLUE, linewidth=2)
    ax1.text(0.5, 0.08, 'Fixer UNE dimension\nWHERE catégorie = \'Électro\'',
             ha='center', fontsize=10, color='#4B5563')

    # Dice highlight
    ax2.fill([0.3, 0.55, 0.55, 0.3], [0.3, 0.3, 0.55, 0.55], color=ORANGE, alpha=0.4)
    ax2.add_patch(FancyBboxPatch((0.3, 0.3), 0.25, 0.25, boxstyle="round,pad=0.01",
                                  facecolor=ORANGE, alpha=0.3, edgecolor=ORANGE, linewidth=2))
    ax2.text(0.5, 0.08, 'Filtrer PLUSIEURS dimensions\n= sous-cube',
             ha='center', fontsize=10, color='#4B5563')

    fig.suptitle('Slice vs Dice', fontsize=20, fontweight='bold', y=1.01)
    fig.savefig(os.path.join(out, 'slice-dice.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ slice-dice.png")

    # 3. Roll-Up vs Drill-Down
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    for ax, title, color, direction in [
        (ax1, 'ROLL-UP (Agréger)', BLUE, 'up'),
        (ax2, 'DRILL-DOWN (Détailler)', ORANGE, 'down'),
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=color, pad=15)

        levels = [
            ('France : 275K', 0.82, 0.3),
            ('IDF : 200K        Rhône : 75K', 0.55, 0.2),
            ('Paris : 200K     Lyon : 75K', 0.28, 0.15),
        ]
        if direction == 'down':
            levels = levels[::-1]

        for i, (label, y, _) in enumerate(levels):
            alpha = [1.0, 0.7, 0.5][i] if direction == 'up' else [0.5, 0.7, 1.0][i]
            w = [0.5, 0.7, 0.86][i]
            x = (1 - w) / 2
            ax.add_patch(FancyBboxPatch((x, y - 0.06), w, 0.14,
                                         boxstyle="round,pad=0.02", facecolor=color,
                                         alpha=alpha * 0.3, edgecolor=color))
            ax.text(0.5, y + 0.01, label, ha='center', fontsize=11, fontweight='bold', color='#1F2937')

        # Arrows
        arrow = '↑' if direction == 'up' else '↓'
        ax.text(0.5, 0.45, arrow, ha='center', fontsize=30, color=color)
        ax.text(0.5, 0.69, arrow, ha='center', fontsize=30, color=color)

    fig.suptitle('Roll-Up vs Drill-Down', fontsize=20, fontweight='bold', y=1.01)
    fig.savefig(os.path.join(out, 'rollup-drilldown.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ rollup-drilldown.png")


# ═══════════════════════════════════════════════
# MODULE 06 - Technologies Cloud
# ═══════════════════════════════════════════════
def gen_06():
    print("Module 06...")
    out = os.path.join(IMG, "06")

    # 1. Snowflake Architecture
    g = graphviz.Digraph('snowflake_arch', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Architecture Snowflake',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled', 'shape': 'box'})

    g.node('cloud', 'Cloud Services\nAuthentification • Metadata • Optimiseur • Sécurité',
           fillcolor=DARK_BLUE, fontcolor='white', width='8')
    for size in ['XS', 'M', 'XL']:
        g.node(f'wh_{size}', f'Warehouse {size}\n(Compute)', fillcolor='#D1FAE5', color=GREEN, width='2.2')
    g.node('storage', 'Storage (S3 / Azure / GCS)\nSéparé & Mutualisé',
           fillcolor=LIGHT_GRAY, color=GRAY, width='8')

    with g.subgraph() as s:
        s.attr(rank='same')
        for size in ['XS', 'M', 'XL']:
            s.node(f'wh_{size}')

    g.edge('cloud', 'wh_XS'); g.edge('cloud', 'wh_M'); g.edge('cloud', 'wh_XL')
    g.edge('wh_XS', 'storage'); g.edge('wh_M', 'storage'); g.edge('wh_XL', 'storage')

    save_graphviz(g, os.path.join(out, 'snowflake-arch'))

    # 2. BigQuery Architecture
    g = graphviz.Digraph('bq_arch', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Architecture BigQuery (Serverless)',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled', 'shape': 'box'})

    g.node('dremel', 'DREMEL (Query Engine)\nExécution distribuée • SQL massif',
           fillcolor='#DBEAFE', color=BLUE, width='8')
    g.node('jupiter', 'JUPITER NETWORK\n1 Petabit/s bandwidth',
           fillcolor='#FDE68A', color=ORANGE, width='8')
    g.node('colossus', 'COLOSSUS (Distributed Storage)\nFormat Capacitor (colonnes optimisé)',
           fillcolor=LIGHT_GRAY, color=GRAY, width='8')
    g.node('label', 'Serverless : Aucune infrastructure à gérer',
           shape='none', fontsize='12', fontcolor=BLUE)

    g.edge('dremel', 'jupiter')
    g.edge('jupiter', 'colossus')
    g.edge('colossus', 'label', style='invis')

    save_graphviz(g, os.path.join(out, 'bigquery-arch'))

    # 3. Comparison table
    fig, ax = plt.subplots(1, 1, figsize=(14, 7))
    ax.axis('off')

    providers = ['Snowflake', 'BigQuery', 'Redshift', 'Synapse']
    criteria = ['Serverless', 'Multi-cloud', 'Pricing', 'ML intégré', 'Streaming', 'Écosystème']
    data = [
        ['Partiel', 'Natif', 'Option', 'Partiel'],
        ['Oui', 'Non', 'Non', 'Non'],
        ['Credits', 'TB scanné', 'Noeud/h', 'DWU'],
        ['Snowpark', 'BQ ML', 'SageMaker', 'Azure ML'],
        ['Snowpipe', 'Natif', 'Kinesis', 'Event Hub'],
        ['Indépendant', 'Google', 'AWS', 'Microsoft'],
    ]
    highlights = [
        [0, 1, 0, 0],  # serverless: BQ best
        [1, 0, 0, 0],  # multi-cloud: Snowflake
        [0, 0, 0, 0],
        [0, 1, 0, 0],  # ML: BQ
        [0, 1, 0, 0],  # streaming: BQ
        [1, 0, 0, 0],  # ecosystem: Snowflake (independent)
    ]
    colors_p = ['#29B5E8', '#4285F4', '#FF9900', '#0078D4']

    # Headers
    for j, (prov, col) in enumerate(zip(providers, colors_p)):
        x = 0.25 + j * 0.18
        ax.add_patch(FancyBboxPatch((x, 0.87), 0.16, 0.08, boxstyle="round,pad=0.01",
                                     facecolor=col, edgecolor='none'))
        ax.text(x + 0.08, 0.91, prov, ha='center', va='center', fontsize=12,
                fontweight='bold', color='white')

    for i, (crit, row, hi) in enumerate(zip(criteria, data, highlights)):
        y = 0.77 - i * 0.12
        ax.text(0.05, y + 0.03, crit, fontsize=11, fontweight='bold', color='#374151')
        for j, (val, h) in enumerate(zip(row, hi)):
            x = 0.25 + j * 0.18
            bg = '#D1FAE5' if h else '#F9FAFB'
            border = '#10B981' if h else '#E5E7EB'
            ax.add_patch(FancyBboxPatch((x, y), 0.16, 0.08, boxstyle="round,pad=0.01",
                                         facecolor=bg, edgecolor=border))
            ax.text(x + 0.08, y + 0.04, val, ha='center', va='center', fontsize=10)

    fig.suptitle('Comparaison Cloud Data Warehouses', fontsize=18, fontweight='bold')
    fig.savefig(os.path.join(out, 'comparaison-cloud-dw.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ comparaison-cloud-dw.png")


# ═══════════════════════════════════════════════
# MODULE 07 - PostgreSQL vs BigQuery
# ═══════════════════════════════════════════════
def gen_07():
    print("Module 07...")
    out = os.path.join(IMG, "07")

    # 1. PG vs BQ Architecture
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    for ax, title, color, bg, layers in [
        (ax1, 'PostgreSQL', '#336791', '#EBF5FF', [
            ('Postmaster\n(Gestion connexions, WAL writer)', 0.78, '#BFDBFE'),
            ('Shared Memory\n(Shared buffers, Lock tables)', 0.55, '#93C5FD'),
            ('Stockage disque local\n(Row-based, B-tree indexes)', 0.32, '#60A5FA'),
        ]),
        (ax2, 'BigQuery', '#4285F4', '#EFF6FF', [
            ('Dremel (Query Engine)\n(Milliers de workers distribués)', 0.78, '#BFDBFE'),
            ('Jupiter Network\n(1 Petabit/s)', 0.55, '#FDE68A'),
            ('Colossus Storage\n(Column-based, distribué)', 0.32, '#E5E7EB'),
        ])
    ]:
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
        ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.03",
                                     facecolor=bg, edgecolor=color, linewidth=3))
        ax.text(0.5, 0.93, title, ha='center', fontsize=20, fontweight='bold', color=color)
        for label, y, lc in layers:
            ax.add_patch(FancyBboxPatch((0.08, y - 0.08), 0.84, 0.18,
                                         boxstyle="round,pad=0.02", facecolor=lc, edgecolor=color))
            ax.text(0.5, y + 0.01, label, ha='center', fontsize=10, fontweight='bold')
            if y < 0.78:
                ax.annotate('', xy=(0.5, y + 0.10), xytext=(0.5, y + 0.17),
                            arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

    ax1.text(0.5, 0.12, 'Scaling vertical\nUn seul serveur', ha='center',
             fontsize=11, color='#336791', style='italic')
    ax2.text(0.5, 0.12, 'Scaling horizontal\nServerless & automatique', ha='center',
             fontsize=11, color='#4285F4', style='italic')

    fig.suptitle('PostgreSQL vs BigQuery — Architectures', fontsize=20, fontweight='bold', y=1.01)
    fig.savefig(os.path.join(out, 'pg-vs-bq-arch.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ pg-vs-bq-arch.png")

    # 2. Decision tree
    g = graphviz.Digraph('decision', graph_attr={
        'rankdir': 'TB', 'bgcolor': 'white', 'label': 'Arbre de décision : PostgreSQL vs BigQuery',
        'labelloc': 't', 'fontsize': '18', 'fontname': 'Helvetica-Bold', 'dpi': '150'
    }, node_attr={'fontname': 'Helvetica', 'fontsize': '11', 'style': 'filled'})

    g.node('q1', 'Volume > 100 GB ?', shape='diamond', fillcolor='#FDE68A', color=ORANGE, width='2.5', height='1')
    g.node('q2', 'Besoin\nserverless ?', shape='diamond', fillcolor='#FDE68A', color=ORANGE, width='2', height='0.9')
    g.node('q3', 'Besoin\nOLTP aussi ?', shape='diamond', fillcolor='#FDE68A', color=ORANGE, width='2', height='0.9')

    g.node('bq', 'BIGQUERY', shape='box', fillcolor='#4285F4', fontcolor='white',
           fontsize='14', style='filled,bold', width='2')
    g.node('other', 'Snowflake\nRedshift', shape='box', fillcolor=LIGHT_BLUE, color=BLUE, width='2')
    g.node('pg', 'POSTGRESQL', shape='box', fillcolor='#336791', fontcolor='white',
           fontsize='14', style='filled,bold', width='2')
    g.node('both', 'PostgreSQL\nou BigQuery', shape='box', fillcolor=LIGHT_GRAY, color=GRAY, width='2')

    g.edge('q1', 'q2', label='  OUI', fontsize='10', color='#10B981')
    g.edge('q1', 'q3', label='  NON', fontsize='10', color='#EF4444')
    g.edge('q2', 'bq', label='  OUI', fontsize='10', color='#10B981')
    g.edge('q2', 'other', label='  NON', fontsize='10', color='#EF4444')
    g.edge('q3', 'pg', label='  OUI', fontsize='10', color='#10B981')
    g.edge('q3', 'both', label='  NON', fontsize='10', color='#EF4444')

    save_graphviz(g, os.path.join(out, 'decision-tree'))


# ═══════════════════════════════════════════════
# MODULE 08 - Medallion
# ═══════════════════════════════════════════════
def gen_08():
    print("Module 08...")
    out = os.path.join(IMG, "08")

    # 1. Medallion layers
    fig, ax = plt.subplots(1, 1, figsize=(12, 14))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    layers = [
        (0.04, '#8B6914', '#FDF6E3', 'BRONZE — Raw Data',
         ['Données brutes (as-is)', 'Append-only, immutable', 'Rétention longue (années)',
          'Format : Parquet, JSON']),
        (0.30, '#6B7280', '#F9FAFB', 'SILVER — Cleaned & Conformed',
         ['Dédoublonnées et validées', 'Types castés (STRING → DATE)',
          'Valeurs normalisées', 'Qualité contrôlée']),
        (0.56, '#B8860B', '#FFFBEB', 'GOLD — Business Ready',
         ['Agrégations pré-calculées', 'Métriques KPIs', 'Star Schema dénormalisé',
          'Optimisé BI / ML / Reporting']),
    ]
    borders = ['#CD7F32', '#9CA3AF', '#DAA520']

    for (y, border, bg, title, items), b in zip(layers, borders):
        ax.add_patch(FancyBboxPatch((0.05, y), 0.9, 0.22, boxstyle="round,pad=0.02",
                                     facecolor=bg, edgecolor=b, linewidth=3))
        ax.text(0.5, y + 0.185, title, ha='center', fontsize=15, fontweight='bold', color=border)
        for i, item in enumerate(items):
            ax.text(0.15, y + 0.13 - i * 0.035, f'●  {item}', fontsize=10, color='#374151')

    # Sources
    ax.add_patch(FancyBboxPatch((0.2, -0.05), 0.6, 0.06, boxstyle="round,pad=0.01",
                                 facecolor=LIGHT_GRAY, edgecolor=GRAY))
    ax.text(0.5, -0.02, 'Data Sources (ERP, CRM, APIs, Files)', ha='center',
            fontsize=10, color=GRAY, fontweight='bold')

    # Consumers
    for i, lbl in enumerate(['BI / Dashboards', 'Data Science / ML', 'Reporting']):
        x = 0.12 + i * 0.3
        ax.add_patch(FancyBboxPatch((x, 0.83), 0.22, 0.05, boxstyle="round,pad=0.01",
                                     facecolor='#DBEAFE', edgecolor=BLUE))
        ax.text(x + 0.11, 0.855, lbl, ha='center', fontsize=9, fontweight='bold', color=DARK_BLUE)

    # Arrows
    for y1, y2 in [(0.01, 0.04), (0.26, 0.30), (0.52, 0.56), (0.78, 0.83)]:
        ax.annotate('', xy=(0.5, y2), xytext=(0.5, y1),
                    arrowprops=dict(arrowstyle='->', color='#6B7280', lw=2))

    fig.suptitle('Architecture Medallion (Bronze / Silver / Gold)', fontsize=20, fontweight='bold', y=0.95)
    fig.savefig(os.path.join(out, 'medallion-layers.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ medallion-layers.png")

    # 2. Transformations
    fig, ax = plt.subplots(1, 1, figsize=(16, 6))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    boxes = [
        (0.02, '#CD7F32', '#FDF6E3', 'BRONZE', [
            'order_id_raw: "12345"',
            'date_raw: "20240115"',
            'amount_raw: "-5"',
            'email_raw: "  ALICE@GMAIL  "',
        ]),
        (0.36, '#9CA3AF', '#F9FAFB', 'SILVER', [
            'order_id: 12345 (INT)',
            'order_date: 2024-01-15',
            'amount: filtré (invalide)',
            'email: "alice@gmail.com"',
        ]),
        (0.70, '#DAA520', '#FFFBEB', 'GOLD', [
            'month: 2024-01',
            'total_revenue: 150 000€',
            'unique_customers: 1 200',
            'avg_order_value: 125€',
        ]),
    ]

    for x, border, bg, title, items in boxes:
        ax.add_patch(FancyBboxPatch((x, 0.15), 0.27, 0.7, boxstyle="round,pad=0.02",
                                     facecolor=bg, edgecolor=border, linewidth=3))
        ax.text(x + 0.135, 0.78, title, ha='center', fontsize=16, fontweight='bold', color=border)
        for i, item in enumerate(items):
            ax.text(x + 0.04, 0.62 - i * 0.12, item, fontsize=9, color='#374151',
                    family='monospace')

    # Arrows between boxes
    ax.annotate('Nettoyage\nCast, Validation', xy=(0.36, 0.5), xytext=(0.29, 0.5),
                fontsize=9, ha='center', va='center', color='#6B7280', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#6B7280', lw=2))
    ax.annotate('Agrégation\nMétriques', xy=(0.70, 0.5), xytext=(0.63, 0.5),
                fontsize=9, ha='center', va='center', color='#6B7280', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#6B7280', lw=2))

    fig.suptitle('Transformations entre couches Medallion', fontsize=18, fontweight='bold', y=0.98)
    fig.savefig(os.path.join(out, 'medallion-transformations.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print("  ✓ medallion-transformations.png")


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
if __name__ == '__main__':
    print("=== Génération des diagrammes ===\n")
    gen_01()
    gen_02()
    gen_03()
    gen_04()
    gen_05()
    gen_06()
    gen_07()
    gen_08()
    print("\n=== Terminé ! ===")
