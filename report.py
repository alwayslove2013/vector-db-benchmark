import streamlit as st
import plotly.express as px
import json
from pathlib import Path
import os
from loguru import logger

dir_path = Path("./results")
data = []
for file_name in os.listdir(dir_path):
    # logger.info(f"file: {file_name}")
    if "upload" in file_name:
        continue
    file_path = dir_path / file_name
    with open(file_path, "r") as f:
        d = json.load(f)
        if d["params"]["engine"] == "redis":
            item = {**d["params"], **d["results"]}
            item["experiment"] += f"""-ef-{item["config"]["EF"]}"""
        else:
            item = {**d["params"], **d["results"]}
        # item["parallel"] = f"""conc-{item["parallel"]}"""
        data.append(item)

logger.info(f"data - length: {len(data)}; data[0]: {data[0]}")

def draw_chart(st, data, x:str, y:str):
    data.sort(key=lambda a: a["parallel"])
    # data.sort(key=lambda a: a[x])
    
    fig = px.line(
        data,
        x=x,
        y=y,
        color="experiment",
        text="parallel",
        markers=True,
        height=600
    )
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(
    page_title="Qdrant-benchmark Perf",
    layout="wide",
)
container = st.container()
draw_chart(container, data, "p95_time", "rps")