import csv
import pandas as pd
import streamlit as st


ONGOING_CHARGE_CHOICE = 0
ETHICAL_CHOICE = 1
MAX_RISK_APPETITE = 2
AMOUNT_TO_INVEST = 3

data = pd.read_csv("content\20_Funds.csv")
first_row = list(data.head(1))

MIN_INVEST_COL = first_row.index("Minimum Investment in £")
TRANSACTION_FEE_COL = first_row.index("Transaction Fees")
ONGOING_CHARGE_COL = first_row.index("Ongoing Charge")
ETHICAL_COL = first_row.index("Ethical")
RISK_COL = first_row.index("Risk Rating")

COLS_TO_DISPLAY = ["Name", "Fund Owner", "ISA Provider", "Product Type", "Sector", "Average Yearly Return",
                   "Minimum Investment in £", "Minimum Monthly in £", "Transaction Fees as %", "Ongoing Charge as %", "Ethical", "Risk Rating"]

input_array = [0, 0, 0, 0]

initial_questions = {
    "Are you over 18?": "info age",
    "Are you paying interest on any loans?": "info interest",
    "Can your savings cover 3-6 months of living expenses?": "info savings",
    "Are you willing to invest for 5 years?": "info invest time",
    "Are you investing for a child?": "info child",
    "Do you have a stocks and shares ISA? - who with?": "info stocks"
}
filter_questions = [
    "Are you ok with an ongoing charge?",
    "Are you only looking for ethical funds?",
    "What is your risk appetite?",
    "How much are you willing to initially invest?"
]


def check_row(row: list, inputs: list[str]) -> bool:
    row_copy = row[:]
    for i, el in enumerate(row_copy):
        if el == 'N':
            row_copy[i] = "No"
        if el == 'Y':
            row_copy[i] = "Yes"

    if int(row_copy[MIN_INVEST_COL]) <= inputs[AMOUNT_TO_INVEST] and \
            int(row_copy[RISK_COL]) <= inputs[MAX_RISK_APPETITE] and \
            not (row_copy[ETHICAL_COL] == 'No' and inputs[ETHICAL_CHOICE] == 'Yes') and \
            not (row_copy[ONGOING_CHARGE_COL] == 'Yes' and inputs[ONGOING_CHARGE_CHOICE] == 'No'):
        return True
    return False


def return_results(input_array: list[str]) -> list[list]:

    with open("content\20_funds.csv", "r") as file:

        csv_reader = csv.reader(file)
        next(csv_reader)
        results_temp = []

        for row in csv_reader:
            if check_row(row, input_array):
                results_temp.append(row)
    df = pd.DataFrame(results_temp, columns=first_row)
    return df


st.set_page_config(
    page_title="EAZEVEST",
    layout="wide"
)


_, col2, _ = st.columns([1, 2, 1])
with col2:
    st.title("_EAZEVEST_ :sunglasses:")
    st.write("_Welcome message_")
    for question, answer in initial_questions.items():
        with st.expander(f"# {question}"):
            st.write(f"_{answer}_")

st.write("## Search funds")

input_array[ONGOING_CHARGE_CHOICE] = (
    st.selectbox(filter_questions[ONGOING_CHARGE_CHOICE], ["Yes", "No"], placeholder="Choose option"))
input_array[ETHICAL_CHOICE] = (
    st.selectbox(filter_questions[ETHICAL_CHOICE], ["Yes", "No"], placeholder="Choose option"))
input_array[MAX_RISK_APPETITE] = (
    st.select_slider(filter_questions[MAX_RISK_APPETITE], range(8)))
input_array[AMOUNT_TO_INVEST] = (
    st.slider(filter_questions[AMOUNT_TO_INVEST], 0, 1000, format=f"£%d", step=10))

search = st.button("Search funds")

if search:
    results = return_results(input_array)
    st.session_state.results_df = results

if 'results_df' in st.session_state:
    if len(st.session_state.results_df) == 0:
        st.write("No results")
    else:
        length = len(st.session_state.results_df)
        with st.container():
            st.dataframe(st.session_state.results_df[COLS_TO_DISPLAY],
                         hide_index=False, height=738, use_container_width=False)
