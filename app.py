
import streamlit as st
import base64
import pandas as pd
import io

st.set_page_config(page_title="Custo de Funcionário - ContFlow", layout="centered")

def calcular_custos(salario_base, beneficios, regime):
    ferias = salario_base / 12
    um_terco_ferias = ferias / 3
    decimo_terceiro = salario_base / 12
    fgts = salario_base * 0.08
    custo_beneficios = beneficios

    if regime == "Simples Nacional / MEI":
        inss_patronal = 0
        terceiros = 0
    else:
        inss_patronal = salario_base * 0.20
        terceiros = salario_base * 0.08

    custo_total = (
        salario_base +
        ferias + um_terco_ferias +
        decimo_terceiro +
        fgts +
        inss_patronal +
        terceiros +
        custo_beneficios
    )

    return {
        "Salário base": salario_base,
        "Férias (1/12 avos)": ferias,
        "1/3 Férias": um_terco_ferias,
        "13º Salário": decimo_terceiro,
        "FGTS (8%)": fgts,
        "INSS Patronal (20%)": inss_patronal,
        "Terceiros (8%)": terceiros,
        "Benefícios": custo_beneficios,
        "Custo Total Mensal": custo_total
    }

def contflow_style():
    st.markdown("""
        <style>
        body {
            background-color: #f3f6fa;
        }
        .main {
            background-color: #ffffff;
            color: #1A237E;
        }
        .stButton>button {
            background-color: #1A237E;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stRadio > div {
            background-color: #E3F2FD;
            padding: 10px;
            border-radius: 10px;
        }
        .stCheckbox > div {
            background-color: #E8EAF6;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

contflow_style()

# Logotipo
st.image("https://contflow.com.br/wp-content/uploads/2023/02/logo-contflow-h-azul.png", width=250)

st.title("💼 Calculadora de Custo de Funcionário")

st.markdown("""
Esta ferramenta calcula o **custo mensal total de um funcionário** para a empresa, considerando:

- Regime tributário (**Simples Nacional/MEI** ou **Regime Normal**);
- Férias e 13º proporcionais;
- Encargos trabalhistas (FGTS, INSS patronal, Terceiros);
- Benefícios variáveis (vale-refeição, transporte, etc).

Desenvolvido com carinho pela **ContFlow Contabilidade** 💙.
""")

with st.form("form"):
    regime = st.radio("Regime da empresa:", ["Simples Nacional / MEI", "Regime Normal (Lucro Real/Presumido)"])
    salario = st.number_input("Salário base (R$):", min_value=0.0, step=100.0, value=2000.0)
    beneficios = st.number_input("Total de benefícios mensais por funcionário (R$):", min_value=0.0, step=50.0, value=400.0)
    ver_detalhes = st.checkbox("Exibir detalhamento do cálculo")
    submitted = st.form_submit_button("Calcular")

if submitted:
    resultado = calcular_custos(salario, beneficios, regime)

    st.success(f"Custo total mensal do funcionário: R$ {resultado['Custo Total Mensal']:.2f}")

    if ver_detalhes:
        st.markdown("### 🔍 Detalhamento do Cálculo")
        df = pd.DataFrame(resultado.items(), columns=["Item", "Valor (R$)"])
        df["Valor (R$)"] = df["Valor (R$)"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(df, use_container_width=True)

        # Exporta para Excel
        output = io.BytesIO()
        df_excel = pd.DataFrame(resultado.items(), columns=["Item", "Valor (R$)"])
        df_excel.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="custo_funcionario_contflow.xlsx">📥 Baixar Excel</a>'
        st.markdown(href, unsafe_allow_html=True)
