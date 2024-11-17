import streamlit as st
import pandas as pd
import numpy as np
import math

def erlang_b(traffic_intensity, servers):
    """
    Calculate the Erlang B loss probability.

    Parameters:
    traffic_intensity (float): The offered traffic in Erlangs (A).
    servers (int): The number of servers (S).

    Returns:
    float: The Erlang B loss probability.
    """
    numerator = (traffic_intensity ** servers) / math.factorial(servers)
    denominator = sum((traffic_intensity ** i) / math.factorial(i) for i in range(servers + 1))
    return numerator / denominator

def erlang_loss_table(max_servers, max_traffic, min_traffic=1):
    """
    Generate an Erlang Loss table.

    Parameters:
    max_servers (int): The maximum number of servers to consider.
    max_traffic (int): The maximum traffic intensity to consider.

    Returns:
    pd.DataFrame: A table with Erlang Loss probabilities.
    """
    data = []
    for servers in range(1, max_servers + 1):
        row = []
        for traffic in np.arange(min_traffic, max_traffic + 0.1, 0.1):
            loss_probability = erlang_b(traffic, servers)
            row.append(loss_probability)
        data.append(row)

    # Create a DataFrame to display the results
    df = pd.DataFrame(data, index=[f"Servers {i}" for i in range(1, max_servers + 1)],
                      columns=[f"Traffic {i:.1f} Erlangs" for i in np.arange(min_traffic, max_traffic + 0.1, 0.1)])
    return df.T

# Streamlit UI
st.title("Erlang B Loss Probability Calculator")

# Session 1: Generate Erlang B Loss Probability
st.header("Calculate Erlang B Loss Probability")
traffic_intensity = st.number_input("Enter the offered traffic in Erlangs (r):", min_value=0.0, value=1.33, step=0.01)
servers = st.number_input("Enter the number of servers (M):", min_value=1.0, value=5.0, step=1.0)

if st.button("Calculate Loss Probability"):
    loss_probability = erlang_b(traffic_intensity, servers)
    st.write(f"The Erlang B Loss Probability is: {loss_probability:.4f}")
    
    # Sample
    st.write("### Sample Calculation")
    st.write("For example, if the offered traffic is 10 Erlangs and there are 5 servers, the loss probability is calculated as follows:")
    sample_loss_probability = erlang_b(10, 5)
    st.write(f"Loss Probability for 10 Erlangs and 5 servers: {sample_loss_probability:.4f}")

# Session 2: Generate Erlang Loss Table
st.header("Generate Erlang Loss Table")
max_servers = st.number_input("Enter the maximum number of servers (M) to consider:", min_value=1, value=10, step=1)
min_traffic = st.number_input("Enter the minimum traffic intensity (r) to consider:", min_value=0.01, value=0.0, step=0.01)
max_traffic = st.number_input("Enter the maximum traffic intensity (r) to consider:", min_value=0.01, value=20.0, step=0.01)

if st.button("Generate Loss Table"):
    loss_table = erlang_loss_table(max_servers, max_traffic, min_traffic)
    st.write("### Erlang Loss Table")
    st.dataframe(loss_table)
    st.download_button(
        label="Download Loss Table as CSV",
        data=loss_table.to_csv().encode('utf-8'),
        file_name='erlang_loss_table.csv',
        mime='text/csv'
    )

